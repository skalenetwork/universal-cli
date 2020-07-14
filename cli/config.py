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

import os
from dotenv import load_dotenv


load_dotenv()

ENDPOINT = os.environ['ENDPOINT']
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ABI_FILEPATH = os.path.join(DIR_PATH, os.pardir, 'manager.json')
TM_URL = os.environ.get('TM_URL')
ETH_PRIVATE_KEY = os.environ.get('ETH_PRIVATE_KEY')
LEDGER = os.environ.get('LEDGER')
