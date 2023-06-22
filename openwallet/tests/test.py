import pytest
import unittest
from unittest.mock import patch

from openwallet import Keypair, Wallet

class TestWallet(unittest.TestCase):

    def test_regen_coldkeypub_from_ss58_addr(self):
        ss58_address = "5DD26kC2kxajmwfbbZmVmxhrY9VeeyR1Gpzy9i8wxLUg6zxm"
        mock_wallet = Wallet()
        with patch.object(mock_wallet, 'set_coldkeypub') as mock_set_coldkeypub:
            mock_wallet.regenerate_coldkeypub( ss58_address=ss58_address )

            mock_set_coldkeypub.assert_called_once()
            keypair: Keypair = mock_set_coldkeypub.call_args_list[0][0][0]
            self.assertEqual(keypair.ss58_address, ss58_address)

        ss58_address_bad = "5DD26kC2kxajmwfbbZmVmxhrY9VeeyR1Gpzy9i8wxLUg6zx" # 1 character short
        with pytest.raises(ValueError):
            self.mock_wallet.regenerate_coldkeypub(ss58_address=ss58_address_bad)

    def test_regen_coldkeypub_from_hex_pubkey_str(self):
        pubkey_str = "0x32939b6abc4d81f02dff04d2b8d1d01cc8e71c5e4c7492e4fa6a238cdca3512f"

        mock_wallet = Wallet()
        with patch.object(mock_wallet, 'set_coldkeypub') as mock_set_coldkeypub:
            mock_wallet.regenerate_coldkeypub(public_key=pubkey_str)

            mock_set_coldkeypub.assert_called_once()
            keypair: Keypair = mock_set_coldkeypub.call_args_list[0][0][0]
            self.assertEqual('0x' + keypair.public_key.hex(), pubkey_str)

        pubkey_str_bad = "0x32939b6abc4d81f02dff04d2b8d1d01cc8e71c5e4c7492e4fa6a238cdca3512" # 1 character short
        with pytest.raises(ValueError):
            self.mock_wallet.regenerate_coldkeypub(ss58_address=pubkey_str_bad)

    def test_regen_coldkeypub_from_hex_pubkey_bytes(self):
        pubkey_str = "0x32939b6abc4d81f02dff04d2b8d1d01cc8e71c5e4c7492e4fa6a238cdca3512f"
        pubkey_bytes = bytes.fromhex(pubkey_str[2:]) # Remove 0x from beginning

        mock_wallet = Wallet()
        with patch.object(mock_wallet, 'set_coldkeypub') as mock_set_coldkeypub:
            mock_wallet.regenerate_coldkeypub(public_key=pubkey_bytes)

            mock_set_coldkeypub.assert_called_once()
            keypair: Keypair = mock_set_coldkeypub.call_args_list[0][0][0]
            self.assertEqual(keypair.public_key, pubkey_bytes)

    def test_regen_coldkeypub_no_pubkey(self):
        mock_wallet = Wallet()

        with pytest.raises(ValueError):
            # Must provide either public_key or ss58_address
            mock_wallet.regenerate_coldkeypub(ss58_address=None, public_key=None)

    def test_regen_coldkey_from_hex_seed_str(self):
        ss58_addr = "5D5cwd8DX6ij7nouVcoxDuWtJfiR1BnzCkiBVTt7DU8ft5Ta"
        seed_str = "0x659c024d5be809000d0d93fe378cfde020846150b01c49a201fc2a02041f7636"

        mock_wallet = Wallet()
        with patch.object(mock_wallet, 'set_coldkey') as mock_set_coldkey:
            mock_wallet.regenerate_coldkey(seed=seed_str)

            mock_set_coldkey.assert_called_once()
            keypair: Keypair = mock_set_coldkey.call_args_list[0][0][0]
            self.assertRegex(keypair.seed_hex if isinstance(keypair.seed_hex, str) else keypair.seed_hex.hex(), rf'(0x|){seed_str[2:]}')
            self.assertEqual(keypair.ss58_address, ss58_addr) # Check that the ss58 address is correct

        seed_str_bad = "0x659c024d5be809000d0d93fe378cfde020846150b01c49a201fc2a02041f763" # 1 character short
        with pytest.raises(ValueError):
            mock_wallet.regenerate_coldkey(seed=seed_str_bad)

    def test_regen_hotkey_from_hex_seed_str(self):
        ss58_addr = "5D5cwd8DX6ij7nouVcoxDuWtJfiR1BnzCkiBVTt7DU8ft5Ta"
        seed_str = "0x659c024d5be809000d0d93fe378cfde020846150b01c49a201fc2a02041f7636"

        mock_wallet = Wallet()
        with patch.object(self.mock_wallet, 'set_hotkey') as mock_set_hotkey:
            mock_wallet.regenerate_hotkey(seed=seed_str)

            mock_set_hotkey.assert_called_once()
            keypair: Keypair = mock_set_hotkey.call_args_list[0][0][0]
            self.assertRegex(keypair.seed_hex if isinstance(keypair.seed_hex, str) else keypair.seed_hex.hex(), rf'(0x|){seed_str[2:]}')
            self.assertEqual(keypair.ss58_address, ss58_addr) # Check that the ss58 address is correct

        seed_str_bad = "0x659c024d5be809000d0d93fe378cfde020846150b01c49a201fc2a02041f763" # 1 character short
        with pytest.raises(ValueError):
            mock_wallet.regenerate_hotkey(seed=seed_str_bad)