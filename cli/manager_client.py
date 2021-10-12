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

from skale.utils.web3_utils import get_provider, wait_for_receipt_by_blocks
from skale.contracts.contract_manager import ContractManager
from skale.contracts.base_contract import BaseContract
from skale.utils.abi_utils import get_contract_address_by_name, get_contract_abi_by_name
from skale.transactions.tools import post_transaction

from cli.web3_utils import init_wallet
from cli.helper import to_camel_case, check_int, get_contract_names, check_bool, str_to_bool

logger = logging.getLogger(__name__)


class SkaleMock:
    def __init__(self, web3):
        self.web3 = web3


class ManagerClient:
    def __init__(self, endpoint, abi, wallet=None, provider_timeout=30):
        logger.info(f'Initializing ManagerClient, endpoint: {endpoint}')
        self.contract_names = get_contract_names(abi)
        self.abi = abi
        self.wallet = wallet if wallet else init_wallet(endpoint)
        self.web3 = Web3(get_provider(endpoint, timeout=provider_timeout))
        self.skale = SkaleMock(self.web3)
        # self.cm_contract = ContractManager(
        #     skale=self.skale,
        #     name='ContractManager',
        #     address=get_contract_address_by_name(abi, 'contract_manager'),
        #     abi=get_contract_abi_by_name(abi, 'contract_manager')
        # )

    # def get_contract_address(self, contract_name):
    #     return self.cm_contract.get_contract_address(
    #         name=to_camel_case(contract_name)
        # )

    def init_contract(self, contract_name):
        address = get_contract_address_by_name(self.abi, contract_name)
        contract_abi = get_contract_abi_by_name(self.abi, contract_name)
        return BaseContract(
            skale=self.skale,
            name=contract_name,
            address=address,
            abi=contract_abi
        )

    def transform_kwargs(self, kwargs):
        for name in kwargs:
            if check_int(kwargs[name]):
                kwargs[name] = int(kwargs[name])
            if check_bool(kwargs[name]):
                kwargs[name] = str_to_bool(kwargs[name])
        return list(kwargs.values())

    def exec(self, contract_name, function_name, is_call, call_sender=None, gas_limit=None,
             gas_price=None, skip_estimate=False, kwargs={}):
        logger.info(f'Executing function {function_name} on contract {contract_name}')
        contract = self.init_contract(contract_name)
        params = self.transform_kwargs(kwargs)
        func_to_run = getattr(contract.contract.functions, function_name)

        call_params = {'from':  call_sender} if call_sender else {}

        if skip_estimate and not gas_limit:
            logger.error('Remove SKIP_ESTIMATE or specify GAS_LIMIT')
            exit(1)

        if not skip_estimate:
            try:
                gas = func_to_run(*params).estimateGas(call_params)
                if not gas_limit:
                    gas_limit = gas
            except Exception as e:
                logger.error(f'estimateGas for {contract_name}.{function_name} failed, check the logs')
                raise(e)
            logger.info(f'Estimated gas for {contract_name}.{function_name}: {gas}')

        if is_call:
            res = func_to_run(*params).call(call_params)
        else:
            tx_hash = post_transaction(self.wallet, func_to_run(*params), gas_limit=int(gas_limit),
                                       gas_price=int(gas_price))
            res = wait_for_receipt_by_blocks(
                self.skale.web3,
                tx_hash
            )
        return res
