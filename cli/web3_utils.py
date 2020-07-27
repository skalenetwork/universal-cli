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


from skale.wallets import LedgerWallet, RPCWallet, Web3Wallet
from skale.utils.web3_utils import init_web3
from skale.utils.exceptions import InvalidWalletError, EmptyWalletError, IncompatibleAbiError

from cli.config import TM_URL, ETH_PRIVATE_KEY, LEDGER, USE_CALLS


def init_wallet(endpoint):
    if TM_URL:
        return RPCWallet(TM_URL)
    web3 = init_web3(endpoint)
    if LEDGER:
        return LedgerWallet(web3, debug=True)
    if ETH_PRIVATE_KEY:
        return Web3Wallet(ETH_PRIVATE_KEY, web3)

        raise Exception(
            'You should provide TM_URL or ETH_PRIVATE_KEY or '
            'set LEDGER=1 to init wallet'
        )
    return Web3Wallet(ETH_PRIVATE_KEY, web3)
