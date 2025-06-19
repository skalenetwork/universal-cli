#   -*- coding: utf-8 -*-
#
#   This file is part of universal-cli
#
#   Copyright (C) 2019-Present SKALE Labs
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

from skale.utils.helper import init_default_logger
from skale.utils.web3_utils import init_web3
from skale_contracts import skale_contracts
from skale_contracts.instance import Instance
from skale_contracts.project_factory import SkaleProject

from web3_utils import init_wallet
from config import ENDPOINT, ALIAS_OR_ADDRESS, PROJECT, DEBUG
from helper import (
    get_enum_by_value,
    is_func_call,
    format_outputs,
    abi_type_to_python,
    kwargs_to_args,
)


if DEBUG:
    init_default_logger()
logger = logging.getLogger(__name__)


def generate_cmd(contract_name_key, instance: Instance, fn: dict) -> click.Command:
    function_name = fn['name']
    params: list[click.Option] = []

    for input_variable in fn['inputs']:
        if not input_variable.get('components'):
            if input_variable['name'] != '':
                opt_name = f'--{input_variable["name"]}'
                name = input_variable['name']
            else:
                opt_name = '--option'
                name = 'Enter option value'
            sol_type = input_variable['type']
            py_type = abi_type_to_python(sol_type)
            opt = click.Option((opt_name,), type=py_type, prompt=f'{name} ({sol_type})')
            params.append(opt)

    @click.pass_context
    def callback(*args, **kwargs):
        contract = instance.get_contract(contract_name_key)
        func = contract.functions[fn['name']]
        func_args = kwargs_to_args(**kwargs)
        is_call = is_func_call(fn)

        if is_call:
            res = func(*func_args).call()
            format_outputs(fn['outputs'], res)
        else:
            wallet = init_wallet(instance.web3)
            if not click.confirm(
                f'transaction: {function_name}, arguments: {func_args}, sender: {wallet.address}, proceed?'
            ):
                click.echo('Aborted.')
                return

            # print(func_args)
            # print(func(*func_args))

            tx = func(*func_args).build_transaction()
            tx_hash = wallet.sign_and_send(tx)
            print(f'⏳ Transaction sent: {tx_hash}, waiting for receipt...')
            wallet.wait(tx_hash=tx_hash)
            print(f'✅ Transaction confirmed: {tx_hash}')

    return click.Command(function_name, params=params, callback=callback)


def get_contract_names(contract_names: set) -> list:
    return sorted([contract.value for contract in contract_names])


def init_groups(instance: Instance | None):
    if not instance:
        return []
    logger.info(f'Initializing groups for instance of {instance._project.name()}')
    groups = []
    contract_names_set = instance.contract_names
    contract_names = get_contract_names(contract_names_set)
    for contract_name in contract_names:
        group = click.Group(name=f'{contract_name}_cli')
        group_internal = click.Group(name=f'{contract_name}')
        try:
            contract_name_key = get_enum_by_value(contract_names_set, contract_name)
            contract_abi = instance.abi[contract_name_key]
            for fn in contract_abi:
                if fn.get('name'):
                    cmd = generate_cmd(contract_name_key, instance, fn)
                    group_internal.add_command(cmd)
        except Exception:
            # logger.exception(f'Could not load contract {contract_name}: {e}')
            continue

        group.add_command(group_internal)
        groups.append(group)
    return groups


def init_instance() -> Instance | None:
    if not PROJECT or not ENDPOINT or not ALIAS_OR_ADDRESS:
        return None
    logger.info(f'Initializing project {PROJECT} at {ENDPOINT} with alias {ALIAS_OR_ADDRESS}')
    web3 = init_web3(ENDPOINT)
    network = skale_contracts.get_network_by_provider(web3.provider)
    project = network.get_project(PROJECT)
    return project.get_instance(ALIAS_OR_ADDRESS)


@click.group()
def cli():
    pass


@cli.command('projects', help='Show supported projects')
def projects():
    print('Supported projects: \n')
    for project in SkaleProject:
        print(project.value)
    print('\nSet PROJECT variable in env: PROJECT=project-name')


if __name__ == '__main__':
    instance = init_instance()
    groups = init_groups(instance)
    cmd_collection = click.CommandCollection(sources=[cli, *groups])
    cmd_collection()
