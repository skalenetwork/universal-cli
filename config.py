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

import os
from dotenv import load_dotenv


load_dotenv()

ENDPOINT = os.environ.get('ENDPOINT')
PROJECT = os.environ.get('PROJECT')
ALIAS_OR_ADDRESS = os.environ.get('ALIAS_OR_ADDRESS')

ETH_PRIVATE_KEY = os.environ.get('ETH_PRIVATE_KEY')
SGX_URL = os.environ.get('SGX_URL')
SGX_KEY_NAME = os.environ.get('SGX_KEY_NAME')

DRY_RUN = os.getenv('DRY_RUN') == 'True'
CALL_SENDER = os.environ.get('CALL_SENDER')
GAS_LIMIT = os.environ.get('GAS_LIMIT')
GAS_PRICE = os.environ.get('GAS_PRICE')

LEDGER = os.getenv('LEDGER') == 'True'
DEBUG = os.getenv('DEBUG') == 'True'
