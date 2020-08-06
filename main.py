#   -*- coding: utf-8 -*-
#
#   This file is part of SKALE.py
#
#   Copyright (C) 2019 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import click

from skale.utils.helper import get_abi, init_default_logger
from skale.utils.abi_utils import get_contract_abi_by_name

from cli.manager_client import ManagerClient
from cli.config import (ENDPOINT, ABI_FILEPATH, ETH_PRIVATE_KEY, LEDGER, TM_URL, DRY_RUN,
                        CALL_SENDER, GAS_LIMIT, GAS_PRICE)
from cli.helper import is_func_call, get_contract_names


init_default_logger()
logger = logging.getLogger(__name__)

ABI = get_abi(ABI_FILEPATH)


def generate_cmd(contract_name, fn):
    function_name = fn['name']
    params = []

    for input_variable in fn['inputs']:
        if not input_variable.get('components'):

            if input_variable["name"] != "":
                opt_name = f'--{input_variable["name"]}'
                name = input_variable["name"]
            else:
                opt_name = '--option'
                name = 'no name'
            opt = click.Option((opt_name,), prompt=f'Name: {name}, type: {input_variable["type"]}')
            params.append(opt)

    @click.pass_context
    def callback(*args, **kwargs):
        if not ENDPOINT:
            logger.error('Set ENDPOINT option to the environment')
            exit(1)
        mc = ManagerClient(ENDPOINT, ABI)
        is_call = is_func_call(fn) or DRY_RUN
        if not is_call and not (ETH_PRIVATE_KEY or LEDGER or TM_URL):
            logger.error('To execute transactions you should set ETH_PRIVATE_KEY/LEDGER/TM_URL')
            exit(1)
        res = mc.exec(contract_name, function_name, is_call, CALL_SENDER, GAS_LIMIT, GAS_PRICE,
                      kwargs)
        logger.info(f'TRANSACTION_RESULT: {res}')
    return click.Command(function_name, params=params, callback=callback)


def init_groups():
    groups = []
    contract_names = get_contract_names(ABI)
    for contract_name in contract_names:
        group = click.Group(name=f'{contract_name}_cli')
        group_internal = click.Group(name=f'{contract_name}')

        contract_abi = get_contract_abi_by_name(ABI, contract_name)
        for fn in contract_abi:
            if fn.get('name'):
                cmd = generate_cmd(contract_name, fn)
                group_internal.add_command(cmd)
        group.add_command(group_internal)
        groups.append(group)
    return groups


if __name__ == "__main__":
    groups = init_groups()
    cmd_collection = click.CommandCollection(sources=groups)
    cmd_collection()
