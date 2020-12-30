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

import os
from dotenv import load_dotenv


load_dotenv()

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

ENDPOINT = os.environ.get('ENDPOINT')

ABI_FILEPATH = os.environ.get("ABI_FILEPATH")
if not ABI_FILEPATH:
    ABI_FILEPATH = os.path.join(DIR_PATH, os.pardir, 'manager.json')

TM_URL = os.environ.get('TM_URL')
ETH_PRIVATE_KEY = os.environ.get('ETH_PRIVATE_KEY')
LEDGER = os.environ.get('LEDGER')

DRY_RUN = os.getenv('DRY_RUN') == 'True'
SKIP_ESTIMATE = os.getenv('SKIP_ESTIMATE') == 'True'
CALL_SENDER = os.environ.get("CALL_SENDER")
GAS_LIMIT = os.environ.get("GAS_LIMIT")
GAS_PRICE = os.environ.get("GAS_PRICE")
