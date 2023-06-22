# The MIT License (MIT)
# Copyright © 2021 Yuma Rao
# Copyright © 2022 Opentensor Foundation
# Copyright © 2023 Opentensor Technologies

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

__version__ = "0.0.0"

import argparse
import copy
import os

import openconfig
from .wallet_impl import Wallet
from .keyfile_impl import Keyfile
from.keypair_impl import Keypair

class keyfile (object):
    """ Factory for a bittensor on device keypair
    """
    def __new__( cls, path: str = None ) -> 'keyfile_impl.Keyfile':
        r""" Initialize a bittensor on device keypair interface.

            Args:
                path (required=False, default: ~/.bittensor/wallets/default/coldkey ):
                    Path where this keypair is stored.
        """
        path = '~/.bittensor/wallets/default/coldkey' if path == None else path
        return keyfile_impl.Keyfile( path = path )

class wallet:
    """ Create and init wallet that stores hot and coldkey
    """

    def __new__(
            cls,
            config: openconfig.Config = None,
            name: str = None,
            hotkey: str = None,
            path: str = None,
            _mock: bool = None
        ) -> 'wallet_impl.Wallet':
        r""" Init bittensor wallet object containing a hot and coldkey.

            Args:
                config (:obj:`bittensor.Config`, `optional`):
                    bittensor.wallet.config()
                name (required=False, default='default'):
                    The name of the wallet to unlock for running bittensor
                hotkey (required=False, default='default'):
                    The name of hotkey used to running the miner.
                path (required=False, default='~/.bittensor/wallets/'):
                    The path to your bittensor wallets
                _mock (required=False, default=False):
                    If true creates a mock wallet with random keys.
        """
        if config == None:
            config = wallet.config()
        config = copy.deepcopy( config )
        config.wallet.name = name if name != None else config.wallet.name
        config.wallet.hotkey = hotkey if hotkey != None else config.wallet.hotkey
        config.wallet.path = path if path != None else config.wallet.path
        config.wallet._mock = _mock if _mock != None else config.wallet._mock
        wallet.check_config( config )

        return wallet_impl.Wallet(
            name = config.wallet.get('name', bittensor.defaults.wallet.name),
            hotkey = config.wallet.get('hotkey', bittensor.defaults.wallet.hotkey),
            path = config.wallet.path,
            config = config
        )

    @classmethod
    def config(cls) -> 'openconfig.Config':
        """ Get config from the argument parser
        Return: bittensor.config object
        """
        parser = argparse.ArgumentParser()
        wallet.add_args( parser )
        return openconfig.config( parser )

    @classmethod
    def help(cls):
        """ Print help to stdout
        """
        parser = argparse.ArgumentParser()
        cls.add_args( parser )
        print (cls.__new__.__doc__)
        parser.print_help()

    @classmethod
    def add_args(cls, parser: argparse.ArgumentParser, prefix: str = None ):
        """ Accept specific arguments from parser
        """
        prefix_str = '' if prefix == None else prefix + '.'
        if prefix is not None:
            if not hasattr(bittensor.defaults, prefix):
                setattr(bittensor.defaults, prefix, openconfig.Config())
            getattr(bittensor.defaults, prefix).wallet = bittensor.defaults.wallet
        try:
            parser.add_argument('--' + prefix_str + 'wallet.name', required=False, default=argparse.SUPPRESS, help='''The name of the wallet to unlock for running bittensor (name mock is reserved for mocking this wallet)''')
            parser.add_argument('--' + prefix_str + 'wallet.hotkey', required=False, default=argparse.SUPPRESS, help='''The name of wallet's hotkey.''')
            parser.add_argument('--' + prefix_str + 'wallet.path', required=False, default=bittensor.defaults.wallet.path, help='''The path to your bittensor wallets''')
        
        except argparse.ArgumentError as e:
            pass

    @classmethod
    def add_defaults(cls, defaults):
        """ Adds parser defaults to object from enviroment variables.
        """
        defaults.wallet = openconfig.Config()
        defaults.wallet.name = os.getenv('BT_WALLET_NAME') if os.getenv('BT_WALLET_NAME') != None else 'default'
        defaults.wallet.hotkey = os.getenv('BT_WALLET_HOTKEY') if os.getenv('BT_WALLET_HOTKEY') != None else 'default'
        defaults.wallet.path = os.getenv('BT_WALLET_PATH') if os.getenv('BT_WALLET_PATH') != None else '~/.bittensor/wallets/'

    @classmethod
    def check_config(cls, config: 'openconfig.Config' ):
        """ Check config for wallet name/hotkey/path/hotkeys/sort_by
        """
        assert 'wallet' in config
        assert isinstance(config.wallet.get('name', bittensor.defaults.wallet.name), str)
        assert isinstance(config.wallet.get('hotkey', bittensor.defaults.wallet.hotkey), str ) or config.wallet.get('hotkey', bittensor.defaults.wallet.hotkey) == None
        assert isinstance(config.wallet.path, str)
