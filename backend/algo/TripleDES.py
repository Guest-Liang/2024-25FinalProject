from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.backends import default_backend
import os, logging
from .PKCS5 import *
logger = logging.getLogger(__name__)


def TripleDES_Encrypt(data, key):
    if len(key) != 24:
        raise ValueError("3DES key must be 24 bytes")

    iv = os.urandom(8)  # 8-byte initialization vector
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padded_data = PKCS5_Pad(data, 8)
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return iv + encrypted_data


def TripleDES_Decrypt(encrypted_data, key):
    try:
        if len(key) != 24:
            raise ValueError("3DES key must be 24 bytes")

        iv = encrypted_data[:8]  # Extract the initialization vector
        encrypted_data = encrypted_data[8:]  # Remove IV from encrypted data

        cipher = Cipher(
            algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend()
        )
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        return PKCS5_Unpad(decrypted_data)

    except ValueError as e:
        logger.error(f"ValueError: {e}")
    except Exception as e:
        logger.error(f"An error occurred during 3DES decryption: {e}")  # All other exceptions
        return None


if __name__ == "__main__":
    Key = os.urandom(24)
    Data = b"Hello, 3DES test!123"

    print("Key:", Key)
    print("Original Data:", Data)

    PaddedData = PKCS5_Pad(Data, 8)
    print("Padded Data:", PaddedData)
    print("Unpadded Data:", PKCS5_Unpad(PaddedData))

    EncryptedData = TripleDES_Encrypt(Data, Key)
    print("Encrypted Data:", EncryptedData)

    DecryptedData = TripleDES_Decrypt(EncryptedData, Key)
    print("Decrypted Data:", DecryptedData)
