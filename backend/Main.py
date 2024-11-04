import algo
import os
"""
key length
AES: 16 bytes (128 bits)
TripleDES: 24 bytes (192 bits)
RC2: 16 bytes (128 bits)

padding
AES: 16 bytes
TripleDES: 8 bytes
RC2: 8 bytes
"""

if __name__ == "__main__":

    AES_Key = os.urandom(16)  # use 128-bit key
    TripleDES_Key = os.urandom(24)  # use 192-bit key
    RC2_Key = os.urandom(16)  # use 128-bit key

    Data = b"Hello, Wolrd!123"

    print(AES_Key)
    print(TripleDES_Key)
    print(RC2_Key)
    print(Data)

    EncryptedData = algo.AES_Encrypt(Data, AES_Key)
    print(EncryptedData)

    DecryptedData = algo.AES_Decrypt(EncryptedData, AES_Key)
    print(DecryptedData)

    EncryptedData = algo.TripleDES_Encrypt(Data, TripleDES_Key)
    print(EncryptedData)

    DecryptedData = algo.TripleDES_Decrypt(EncryptedData, TripleDES_Key)
    print(DecryptedData)

    EncryptedData = algo.RC2_Encrypt(Data, RC2_Key)
    print(EncryptedData)

    DecryptedData = algo.RC2_Decrypt(EncryptedData, RC2_Key)
    print(DecryptedData)

  
