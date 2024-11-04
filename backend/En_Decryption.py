import os
import base64
from datetime import datetime
import algo


# Encrypt a file using AES, 3DES, and RC2
def EncryptFile(FilePath):
    with open(FilePath, 'rb') as F:
        FileData = F.read()

    # Split the file into 3 parts
    PartSize = len(FileData) // 3
    Part1, Part2, Part3 = FileData[:PartSize], FileData[PartSize:PartSize*2], FileData[PartSize*2:]
    
    CurrentTime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Generate keys and encrypt the parts
    Key1 = os.urandom(16) # AES 128-bit
    EncryptedPart1 = algo.AES_Encrypt(Part1, Key1)
    Key2 = os.urandom(24) # 3DES 192-bit
    EncryptedPart2 = algo.TripleDES_Encrypt(Part2, Key2)
    Key3 = os.urandom(16) # RC2 128-bit
    EncryptedPart3 = algo.RC2_Encrypt(Part3, Key3)
    
    FileName, FileExtension = os.path.splitext(os.path.basename(FilePath))
    
    def GetEncryptedFileName(Part, AlgorithmName):
        RawName = f"{FileExtension[1:]}_{CurrentTime}_{AlgorithmName}_Part{Part}"
        EncodedName = base64.urlsafe_b64encode(RawName.encode()).decode()
        return EncodedName
    
    Part1Name = GetEncryptedFileName(1, "AES")
    Part2Name = GetEncryptedFileName(2, "3DES")
    Part3Name = GetEncryptedFileName(3, "RC2")
    
    # store encrypted files
    with open(os.path.join('backend/storage', Part1Name), 'wb') as F:
        F.write(EncryptedPart1)
    
    with open(os.path.join('backend/storage', Part2Name), 'wb') as F:
        F.write(EncryptedPart2)
    
    with open(os.path.join('backend/storage', Part3Name), 'wb') as F:
        F.write(EncryptedPart3)

    # Encode keys to base64 for safe output
    EncodedKey1 = base64.urlsafe_b64encode(Key1).decode('utf-8')
    EncodedKey2 = base64.urlsafe_b64encode(Key2).decode('utf-8')
    EncodedKey3 = base64.urlsafe_b64encode(Key3).decode('utf-8')
    
    # Return filenames and encoded keys as a single string
    return f"{Part1Name},{EncodedKey1},{Part2Name},{EncodedKey2},{Part3Name},{EncodedKey3}"

# Decrypt those files, combine them
def DecryptFile(EncryptedFileString):
    Parts = EncryptedFileString.split(',')
    if len(Parts) != 6:
        raise ValueError("Invalid input format.")
    
    # decode the keys
    Part1Name, EncodedKey1, Part2Name, EncodedKey2, Part3Name, EncodedKey3 = Parts
    Key1 = base64.urlsafe_b64decode(EncodedKey1)
    Key2 = base64.urlsafe_b64decode(EncodedKey2)
    Key3 = base64.urlsafe_b64decode(EncodedKey3)

    # 从文件名中提取原始文件扩展名
    DecodedFileName = base64.urlsafe_b64decode(Part1Name).decode()
    OriginalExtension = DecodedFileName.split('_')[0]

    with open(os.path.join('backend/storage', Part1Name), 'rb') as F:
        EncryptedPart1 = F.read()
    with open(os.path.join('backend/storage', Part2Name), 'rb') as F:
        EncryptedPart2 = F.read()
    with open(os.path.join('backend/storage', Part3Name), 'rb') as F:
        EncryptedPart3 = F.read()

    # Decrypt the parts
    DecryptedPart1 = algo.AES_Decrypt(EncryptedPart1, Key1)
    DecryptedPart2 = algo.TripleDES_Decrypt(EncryptedPart2, Key2)
    DecryptedPart3 = algo.RC2_Decrypt(EncryptedPart3, Key3)

    # Check if decryption failed
    if DecryptedPart1 is None or DecryptedPart2 is None or DecryptedPart3 is None:
        raise ValueError("Decryption failed for one or more parts, received None as decrypted output.")
    
    DecryptedData = DecryptedPart1 + DecryptedPart2 + DecryptedPart3
    
    return DecryptedData, OriginalExtension

if __name__ == "__main__":
    TestFilePath = "backend/transit/test.txt"
    
    Result = EncryptFile(TestFilePath)

    print(Result)

    DecryptedData, OriginalExtension = DecryptFile(Result)

    with open(f"backend/transit/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.{OriginalExtension}", 'wb') as F:
        F.write(DecryptedData)