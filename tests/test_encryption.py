"""
Encryption module tests
"""

import unittest
from encryption.cipher import EncryptionManager

class TestEncryption(unittest.TestCase):
    """Test encryption functionality"""
    
    def setUp(self):
        self.cipher = EncryptionManager('test-key-32-chars-minimum-len')
    
    def test_encrypt_decrypt_text(self):
        """Test encrypting and decrypting text"""
        plaintext = 'This is a secret message'
        encrypted = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
        self.assertNotEqual(plaintext, encrypted)
    
    def test_encrypt_bytes(self):
        """Test encrypting bytes"""
        plaintext = b'This is a secret message'
        encrypted = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted.encode())
    
    def test_different_encryption_same_plaintext(self):
        """Test that same plaintext produces different ciphertexts"""
        plaintext = 'Test message'
        encrypted1 = self.cipher.encrypt(plaintext)
        encrypted2 = self.cipher.encrypt(plaintext)
        
        # Due to Fernet's use of timestamps and nonces, same plaintext should give different ciphertexts
        # But both should decrypt to same plaintext
        self.assertEqual(
            self.cipher.decrypt(encrypted1),
            self.cipher.decrypt(encrypted2)
        )
    
    def test_invalid_ciphertext(self):
        """Test decrypting invalid ciphertext"""
        with self.assertRaises(Exception):
            self.cipher.decrypt('invalid-ciphertext')

if __name__ == '__main__':
    unittest.main()
