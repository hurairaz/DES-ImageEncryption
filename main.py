import os
import sys
from PIL import Image
from Crypto.Cipher import DES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import numpy as np

def derive_key(password: str):
    salt = get_random_bytes(16)
    print(f"Salt: {salt} Length: {len(salt)}")

    encoded_password = password.encode()
    print(f"Encoded Password: {encoded_password} Length: {len(encoded_password)}")

    key = scrypt(password=encoded_password, salt=salt, key_len=8, N=2**14, r=8,  p=1)
    print(f"Key: {key} Length: {len(key)}")
    return key


def image_to_bytes(image: Image.Image):
    img_data = np.array(image)
    print(f"Image Shape: {img_data.shape}")
    plain_text = img_data.tobytes()
    return plain_text

def bytes_to_image(data: bytes, original_image: Image.Image):
    arr = np.frombuffer(data, dtype=np.uint8).reshape(original_image.size[1], original_image.size[0], 3)
    return Image.fromarray(arr)

def des_encryption_ecb(plain_text: bytes, key: bytes):
    des = DES.new(key, mode=DES.MODE_ECB)
    padding_len = (8 - len(plain_text) % 8) % 8
    data = plain_text + b'\x00' * padding_len
    encrypted_data = des.encrypt(data)
    return encrypted_data

def des_encryption_ofb(plain_text: bytes, key: bytes):
    iv = get_random_bytes(8)
    des = DES.new(key, mode=DES.MODE_OFB, iv=iv)
    encrypted_data = des.encrypt(plain_text)
    return encrypted_data

def main():
    password = "stormfiber"
    print("\nEncrypting Password...")
    key = derive_key(password=password)

    print("\nLoading Image...")
    try:
        image = Image.open("sample_input.png")
        image = image.convert("RGB")
    except Exception as e:
        print(f"Error loading image {e}")
        sys.exit(1)
    else:
        print("\nImage successfully loaded...")

    print("\nConverting image to bytes...")
    plain_text = image_to_bytes(image)

    print("\nGenerating Encrypted Image Using ECB...")
    ecb_cypher_text = des_encryption_ecb(plain_text, key)
    ecb_cypher_image = bytes_to_image(ecb_cypher_text, image)

    print("\nGenerating Encrypted Image Using OFB...")
    ofb_cypher_text = des_encryption_ofb(plain_text, key)
    ofb_cypher_image = bytes_to_image(ofb_cypher_text, image)

    ofb_cypher_image.save("ofb_cypher_image.png")
    ecb_cypher_image.save("ecb_cypher_image.png")

    ecb_cypher_image.show(title="ECB Encrypted Image")
    ofb_cypher_image.show(title="OFB Encrypted Image")

if __name__ == "__main__":
    main()