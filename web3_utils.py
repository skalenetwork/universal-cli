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

from web3 import Web3
from skale.wallets import LedgerWallet, Web3Wallet, SgxWallet, BaseWallet

from config import ETH_PRIVATE_KEY, LEDGER, SGX_URL, SGX_KEY_NAME


def init_wallet(w3: Web3) -> BaseWallet:
    if LEDGER:
        return LedgerWallet(w3, debug=True)
    if ETH_PRIVATE_KEY:
        return Web3Wallet(ETH_PRIVATE_KEY, w3)
    if SGX_URL:
        return SgxWallet(SGX_URL, w3, key_name=SGX_KEY_NAME)
