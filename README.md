# Universal-cli: command line for Solidity Smart Contracts

[![Discord](https://img.shields.io/discord/534485763354787851.svg)](https://discord.gg/vvUtWJB)

Universal-cli is a universal command line to instantly execute any Smart Contract call or transaction from contract sets supported by [skale-contracts](https://github.com/skalenetwork/skale-contracts) library.

## What it is

Universal-cli could be used to execute (almost) any call/transaction on Solidity contracts.
CLI groups and commands are generated automatically from provided project and alias/address.

All calls and transactions from the contracts are already here, just use `--help` to see the details.

## Python version

You need to have python version 3.11 or later installed.

## Binary installation

Download the latest binary:

```bash
VERSION_NUM={put the version number here} && sudo -E bash -c "curl -L https://github.com/skalenetwork/universal-cli/releases/download/$VERSION_NUM/uni-$VERSION_NUM-`uname -s`-`uname -m` >  /usr/local/bin/uni"
```

Apply executable permissions to the downloaded binary:

```bash
sudo chmod +x /usr/local/bin/uni
```

Test the installation:

```bash
uni --help
```

Check out the list of available projects:

```bash
uni projects
```

## Environment variables

You need to set the following environment variables:

```bash
PROJECT=""
ENDPOINT=""
ALIAS_OR_ADDRESS=""

# to use with plain private key
ETH_PRIVATE_KEY=""

# to use with SGX
SGX_URL=""
SGX_KEY_NAME=""
```

## Usage

This example shows how to send a simple call to the skale-manager contracts:

Environment variables:

```bash
PROJECT=skale-manager
ENDPOINT=https://ethereum-rpc.publicnode.com
ALIAS_OR_ADDRESS=production
```

Command:

```bash
uni Nodes getNodeDomainName --nodeIndex 60

# Output
{
  "domainName": "skale-jupiter-2.skale.figment.io"
}
```

## Setup

### Dev setup

```bash
pip install -e .[dev]
```

## Current limitations

* Complex data types are not supported
* No retries, dry runs and balance checks for transactions

## License

[![License](https://img.shields.io/github/license/skalenetwork/universal-cli.svg)](LICENSE)

Copyright (C) 2020-Present SKALE Labs
