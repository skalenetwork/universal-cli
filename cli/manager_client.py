#   -*- coding: utf-8 -*-
#
#   This file is part of SKALE.py
#
#   Copyright (C) 2019-Present SKALE Labs
#
#   SKALE.py is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   SKALE.py is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with SKALE.py.  If not, see <https://www.gnu.org/licenses/>.

import logging

from web3 import Web3
from web3.middleware import geth_poa_middleware

from skale.utils.web3_utils import get_provider, wait_for_receipt_by_blocks
from cli.config import CALL_SENDER
from skale.contracts.contract_manager import ContractManager
from skale.contracts.base_contract import BaseContract
from skale.utils.abi_utils import get_contract_address_by_name, get_contract_abi_by_name
from skale.transactions.tools import post_transaction, make_dry_run_call

from cli.web3_utils import init_wallet
from cli.helper import to_camel_case, check_int

logger = logging.getLogger(__name__)


def init_contract_names(abi):
    contract_names = []
    for contract_name in abi:
        if '_address' in str(contract_name):
            contract_names.append(contract_name.replace('_address', ''))
    return contract_names


class Skale:
    def __init__(self, web3):
        self.web3 = web3


class ManagerClient:
    def __init__(self, endpoint, abi, wallet=None, provider_timeout=30):
        logger.info(f'Initializing ManagerClient, endpoint: {endpoint}')
        self.contract_names = init_contract_names(abi)
        self.abi = abi

        if wallet:
            self.wallet = wallet
        else:
            self.wallet = init_wallet(endpoint)

        provider = get_provider(endpoint, timeout=provider_timeout)
        self.web3 = Web3(provider)
        self.skale = Skale(self.web3)

        cm_address = get_contract_address_by_name(abi, 'contract_manager')
        cm_abi = get_contract_abi_by_name(abi, 'contract_manager')
        self.cm_contract = ContractManager(
            skale=self.skale,
            name='ContractManager',
            address=cm_address,
            abi=cm_abi
        )

    def run_func(self, contract_name, function_name, is_call, kwargs):
        cm_name = to_camel_case(contract_name)
        address = self.cm_contract.get_contract_address(cm_name)

        address = get_contract_address_by_name(self.abi, contract_name)
        abi = get_contract_abi_by_name(self.abi, contract_name)
        contract = BaseContract(
            skale=self.skale,
            name=contract_name,
            address=address,
            abi=abi
        )

        for name in kwargs:
            if check_int(kwargs[name]):
                kwargs[name] = int(kwargs[name])


        params = list(kwargs.values())



        print(f'Going to run {function_name} on {contract_name}')
        contract_funcs = contract.contract.functions
        func_to_run = getattr(contract_funcs, function_name)

        if is_call:
            if CALL_SENDER is not None:
                p = {'from':  CALL_SENDER}
            else:
                p = {}
            res = func_to_run(*params).call(p)
        else:
            tx_hash = post_transaction(self.wallet, func_to_run(*params), 8000000)
            res = wait_for_receipt_by_blocks(
                self.skale.web3,
                tx_hash
            )
        return res
