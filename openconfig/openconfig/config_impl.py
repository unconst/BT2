"""
Implementation of the config class, which manages the config of different bittensor modules.
"""
# The MIT License (MIT)
# Copyright © 2021 Yuma Rao
# Copyright © 2022 Opentensor Foundation

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

import yaml
import pandas
from munch import Munch
from pandas import json_normalize
from typing import Dict

class Config ( Munch ):
    """
    """
    __is_set: Dict[str, bool]

    def __init__(self, loaded_config = None ):
        super().__init__()
        if loaded_config:
            raise NotImplementedError('Function load_from_relative_path is not fully implemented.')

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "\n" + yaml.dump(self.toDict())

    def to_string(self, items) -> str:
        """ Get string from items
        """
        return "\n" + yaml.dump(items.toDict())

    def update_with_kwargs( self, kwargs ):
        """ Add config to self
        """
        for key,val in kwargs.items():
            self[key] = val

    @classmethod
    def _merge( cls, a, b ):
        """Merge two configurations recursively.
        If there is a conflict, the value from the second configuration will take precedence.
        """
        for key in b:
            if key in a:
                if isinstance( a[key], dict ) and isinstance( b[key], dict ):
                    a[key] = cls._merge( a[key], b[key] )
                else:
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a

    def merge(self, b):
        """ Merge two configs
        """
        self = self._merge( self, b )

    def is_set(self, param_name: str) -> bool:
        """
        Returns a boolean indicating whether the parameter has been set or is still the default.
        """
        if param_name not in self.get('__is_set'):
            return False
        else:
            return self.get('__is_set')[param_name]

    def __fill_with_defaults__(self, is_set_map: Dict[str, bool], defaults: 'Config') -> None:
        """
        Recursively fills the config with the default values using is_set_map
        """
        defaults_filtered = {}
        for key in self.keys():
            if key in defaults.keys():
                defaults_filtered[key] = getattr(defaults, key)
        # Avoid erroring out if defaults aren't set for a submodule
        if defaults_filtered == {}: return

        flat_defaults = json_normalize(defaults_filtered, sep='.').to_dict('records')[0]
        for key, val in flat_defaults.items():
            if key not in is_set_map:
                continue
            elif not is_set_map[key]:
                # If the key is not set, set it to the default value
                # Loop through flattened key to get leaf
                a = self
                keys = key.split('.')
                for key_ in keys[:-1]:
                    if key_ not in a:
                        a[key_] = {}
                    a = a[key_]
                # Set leaf to default value
                a[keys[-1]] = val
