from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.backends import default_backend
import os
from .PKCS5 import *


def AES_Encrypt(data, key):
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes")

    iv = os.urandom(16)  # 16-byte initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padded_data = PKCS5_Pad(data, 16)
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return iv + encrypted_data


def AES_Decrypt(encrypted_data, key):
    try:
        if len(key) not in (16, 24, 32):
            raise ValueError("AES key must be 16, 24, or 32 bytes")

        iv = encrypted_data[:16]  # Extract the initialization vector
        encrypted_data = encrypted_data[16:]  # Remove iv from encrypted data

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        return PKCS5_Unpad(decrypted_data)

    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An error occurred during decryption: {e}")  # All other exceptions
        return None


if __name__ == "__main__":
    Key = os.urandom(16)  # 128-bit key
    Data = b"Hello, AES test!123"

    print("Key:", Key)
    print("Original Data:", Data)

    PaddedData = PKCS5_Pad(Data, 16)
    print("Padded Data:", PaddedData)

    for byte in PaddedData:
        print(f"{byte:02x}", end=" ")

    UnpaddedData = PKCS5_Unpad(PaddedData)
    print(repr(UnpaddedData))

    EncryptedData = AES_Encrypt(Data, Key)
    print(EncryptedData)

    DecryptedData = AES_Decrypt(EncryptedData, Key)
    print(DecryptedData)
