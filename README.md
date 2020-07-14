# SKALE Universal CLI

Universal Python wrapper for SKALE Manager contracts.  

## What it is

This CLI/Python module could be used to execute (almost) any call/transaction on SKALE Manager contracts.  
CLI groups and commands are generated automatically from provided ABI file so there is no need to update CLI after SM changes.  
Also there is no such thing as 'call implemented only on SKALE Manager side' - all calls and transactions from ABI file are already here, just add `--help` to see the details.

#### Current limitations

- Complex data types are not supported
- No retries, dry runs and balance checks for transactions
- No data formatting - only raw data from smart contracts
- No gas estimation (8m for all transactions)

## Usage

ManagerClient could be used as CLI tool or directly from Python scripts.

Supported wallets:

- SGX wallet
- Web3 wallet
- Ledger wallet

### CLI usage

#### List avaliable contacts

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
res = mc.run_func(
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
