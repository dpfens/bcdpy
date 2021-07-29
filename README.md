# bcdpy
A Python wrapper for the [better-call.dev](https://better-call.dev) API

## Install
```bash
git clone git@github.com:dpfens/bcdpy.git && cd bcdpy
python setup.py install
```

## Scripts
`bcd` comes with a few executable scripts for simple/common tasks:

*  `account` - Fetches the balances of the given account addresses
*  `contract` - Fetches the endpoints of a given contract
*  `domain` - Fetches/resolves domains on the Tezos blockchain
*  `head` - Fetches the current head of the blockchain
*  `search` - Executes a search with the specified query and configuration
*  `statistics` - Fetch statistics on the given network
*  `token` - Fetch information on tokens on the Tezos blockchain
