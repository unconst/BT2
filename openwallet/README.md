# BTWallet - v0.0.0

BTWallet is a library for managing wallet keypairs, keyfiles, etc. for the [Bittensor Python API](https://github.com/opentensor/bittensor).  

The purpose of this repo is to separate the concern of keyfile management from the https://github.com/opentensor/bittensor repo, to decrease the attack surface of Bittensor related to local keys and wallet functionality.  

# Installation
This package can be installed from [PyPi.org](https://pypi.org/project/bt-wallet/):
```bash
pip install bt-wallet==0.0.0
```
or via this repo (using [gh-cli](https://cli.github.com/)):  
```bash
gh repo clone opentensor/bt-wallet
cd bt-wallet
pip install -e .
```


