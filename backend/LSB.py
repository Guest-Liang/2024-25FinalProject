from PIL import Image
import base64, datetime


def LSB_Encode(image_path, output_path, secret_message):
    # Read image
    img = Image.open(image_path)
    if img is None:
        raise ValueError("Image could not be loaded.")
    encoded = img.copy()
    width, height = img.size
    pixels = encoded.load()
    if pixels is None:
        raise ValueError("Pixels could not be loaded.")

    binary_message = "".join([format(ord(char), "08b") for char in secret_message])
    binary_message += "".join([format(ord(c), "08b") for c in "~~"])  # Add end mark "~~"

    data_index = 0

    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for i in range(3):  # R, G, B channels
                if data_index < len(binary_message):
                    pixel[i] = int(format(pixel[i], "08b")[:-1] + binary_message[data_index], 2)
                    data_index += 1
            pixels[x, y] = tuple(pixel)

            if data_index >= len(binary_message):  # All data has been encoded
                break
        if data_index >= len(binary_message):
            break

    encoded.save(output_path)
    print(f"[{datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')}]Message encoded into {output_path}")


def LSB_Decode(image_path):
    # Read image
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()
    if pixels is None:
        raise ValueError("Pixels could not be loaded.")

    binary_message = ""
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            for i in range(3):  # Get R, G, B LSB
                binary_message += format(pixel[i], "08b")[-1]

    # Binary to bytes
    all_bytes = [binary_message[i : i + 8] for i in range(0, len(binary_message), 8)]
    decoded_message = ""
    for byte in all_bytes:
        decoded_message += chr(int(byte, 2))
        if decoded_message[-2:] == "~~":  # End mark, stop decode
            break

    return decoded_message[:-2]


if __name__ == "__main__":

    SecretMessage = "Hello, this is a test secret message!"
    Base64_Message = base64.b64encode(SecretMessage.encode()).decode()
    print("Base64 encoded message:", Base64_Message)
    LSB_Encode(r"backend\pic\4.png", "output_image.png", Base64_Message)

    DecodedMessage = LSB_Decode("output_image.png")
    print("Image Decoded message:", DecodedMessage)
    DebasedMessage = base64.b64decode(DecodedMessage)
    print("Base64 decoded message:", DebasedMessage)
