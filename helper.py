#   -*- coding: utf-8 -*-
#
#   This file is part of universal-cli
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

import re
import json
import logging
from typing import Union

from web3 import Web3

logger = logging.getLogger(__name__)


def is_func_call(fn):
    return fn.get('stateMutability') == 'view'


def get_enum_by_value(enum_class, value):
    for item in enum_class:
        if item.value == value:
            return item
    return None


def kwargs_to_args(**kwargs):
    return list(kwargs.values())


def hex_to_bytes_python(hex_string: str) -> bytes:
    if hex_string.startswith('0x') or hex_string.startswith('0X'):
        hex_string = hex_string[2:]
    if len(hex_string) % 2:
        hex_string = '0' + hex_string
    return bytes.fromhex(hex_string)


def format_func_args(args):
    formatted_args = []
    for arg in args:
        if isinstance(arg, str) and arg.startswith('0x'):
            formatted_args.append(Web3.to_bytes(hexstr=arg))
        else:
            formatted_args.append(arg)
    return formatted_args


def abi_type_to_python(abi_type: str) -> Union[type, str]:
    array_match = re.match(r'(.+)(\[\d*\])', abi_type)
    if array_match:
        return str
    if re.fullmatch(r'u?int\d*', abi_type):
        return int
    elif abi_type == 'address':
        return str
    elif abi_type == 'bool':
        return bool
    elif abi_type == 'string':
        return str
    elif abi_type == 'bytes':
        return str
    elif re.fullmatch(r'bytes\d+', abi_type):
        return str
    else:
        return str


def format_outputs(outputs_abi: list, call_result) -> None:
    if not outputs_abi:
        print(json.dumps({'result': 'No outputs defined'}, indent=2))
        return

    if len(outputs_abi) == 1:
        output = outputs_abi[0]
        name = output.get('name', 'result')
        formatted_value = convert_value_for_json(call_result, output['type'])
        result = {name: formatted_value}
    else:
        if not isinstance(call_result, (list, tuple)):
            call_result = [call_result]

        result = {}
        for i, output in enumerate(outputs_abi):
            name = output.get('name', f'output_{i}')
            if i < len(call_result):
                value = call_result[i]
                formatted_value = convert_value_for_json(value, output['type'])
                result[name] = formatted_value
            else:
                result[name] = None

    print(json.dumps(result, indent=2))


def convert_value_for_json(value, abi_type: str):
    try:
        if '[' in abi_type and ']' in abi_type:
            if isinstance(value, (list, tuple)):
                base_type = abi_type.split('[')[0]
                return [convert_value_for_json(item, base_type) for item in value]
            else:
                return str(value)
        if re.match(r'u?int\d*', abi_type):
            return int(value)
        elif abi_type == 'address':
            return str(value)
        elif abi_type == 'bool':
            return bool(value)
        elif abi_type == 'string':
            return str(value)
        elif abi_type == 'bytes' or re.match(r'bytes\d+', abi_type):
            if isinstance(value, bytes):
                return f'0x{value.hex()}'
            else:
                return str(value)
        else:
            return str(value)

    except Exception as e:
        logger.warning(f'Error converting value {value} of type {abi_type}: {e}')
        return str(value)
