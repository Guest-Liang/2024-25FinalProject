# PKCS#5 Padding, AES needs 16 bytes block size
def PKCS5_Pad(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding


# PKCS#5 Remove Padding
def PKCS5_Unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]
