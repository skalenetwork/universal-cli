# Universal-cli: command line for Solidity Smart Contracts

[![Discord](https://img.shields.io/discord/534485763354787851.svg)](https://discord.gg/vvUtWJB)

Universal-cli is a universal command line to instantly execute any Solidity smart contract.

Super simple and useful for scripts and automation! All you need is ABI file!

Used and maintained heavily by SKALE


## What it is

Universal-cli could be used to execute (almost) any call/transaction on Solidity contracts.  

CLI groups and commands are generated automatically from provided ABI file so there is no need to update CLI after SM changes.  

All calls and transactions from ABI file are already here, just use `--help` to see the details.


## Python version

You need to have python version 3.6 or later installed.

## Installation

Clone this repo and then do 

```
pip install .
```

Copy your ABI file to abi.json in the project root dir.

If you want to use another file name, use ABI_FILEPATH option as described below.


## Usage

Could be used as CLI tool or directly from Python scripts.

Supported wallets:

- Web3.py wallet
- Ledger wallet
- SKALE SGX wallet

### Environment options

#### Required

- `ENDPOINT` - Ethereum JSON-RPC endpoint.

For transactions you should set one of those:

- `ETH_PRIVATE_KEY` - ETH private key
- `LEDGER` - use Ledger (true or false)
- `TM_URL` - use SKALE trasaction manager

#### Optional

- `DRY_RUN` - Run the transaction method as a call (`True/False`). Default: `False`.
- `SKIP_ESTIMATE` - skip gas estimation before running (`True/False`). Default: `False`.
- `CALL_SENDER` - Ethereum address that will be used in the call. Default: `None`.
- `GAS_LIMIT` - gas limit for the transaction/call. Default: result of the `estimateGas` function.
- `GAS_PRICE` - gas price for the transaction. Default: calculated by `web3py`.
- `ABI_FILEPATH` - path to the ABI. Default: `[PROJECT_ROOT]/manager.json`

### CLI usage

#### List avaliable contracts

```bash
python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  bounty
  constants_holder
  contract_manager
  decryption
  delegation_controller
  delegation_period_manager
  distributor
  ...
```

#### List avaliable methods on contracts

```bash
python main.py nodes --help

Usage: main.py nodes [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  DEFAULT_ADMIN_ROLE
  ExitCompleted
  ExitInited
  NodeCreated
  RoleGranted
  RoleRevoked
  addSpaceToNode
  ...
```

#### Run cmd

```bash
python main.py validator_service validators --option 1
```

#### Show required options for the command

```bash
python main.py validator_service registerValidator --help

Usage: main.py validator_service registerValidator [OPTIONS]

Options:
  --name TEXT
  --description TEXT
  --feeRate TEXT
  --minimumDelegationAmount TEXT
  --help                          Show this message and exit.
```

### Python usage

```python
wallet = Web3Wallet(ETH_PRIVATE_KEY, web3)
mc = ManagerClient(ENDPOINT, ABI, wallet)

kwargs = {
    'name': 'test',
    'description': 'test',
    'feeRate': '10',
    'minimumDelegationAmount': '100',
}
res = mc.exec(
    contract_name='validator_serivce',
    function_name='registerValidator',
    transaction=True,
    kwargs=kwargs
)
print(res)
```

## Setup

### Dev setup

```bash
pip install -e .[dev]
```



## Current limitations

- Complex data types are not supported
- No data formatting - only raw data from smart contracts
- No retries, dry runs and balance checks for transactions
- No pre-built binary and no pip package (yet)



## License

[![License](https://img.shields.io/github/license/skalenetwork/sgx.py.svg)](LICENSE)

Copyright (C) 2020-present SKALE Labs
