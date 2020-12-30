#   -*- coding: utf-8 -*-
#
#   This file is part of universal-cli
#
#   Copyright (C) 2020 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return ''.join(x.title() for x in components)


def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def check_bool(s):
    if isinstance(s, int):
        return False
    return s.lower() in ['true', 'false']


def str_to_bool(s):
    return s.lower() in ['true']


def is_func_call(fn):
    return fn['stateMutability'] == 'view'


def get_contract_names(abi):
    contract_names = []
    for contract_name in abi:
        if '_address' in str(contract_name):
            contract_names.append(contract_name.replace('_address', ''))
    return contract_names
