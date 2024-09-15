# Image Encryption with DES

The script converts an image into bytes, encrypts it using DES in both ECB mode and OFB mode, and then saves and displays the encrypted images.

## Concepts

### DES (Data Encryption Standard)
DES is a symmetric-key block cipher that encrypts data in 64-bit blocks using a 56-bit key. DES operates in various modes to enhance its security and functionality, where each mode has its unique characteristics and use cases.

### ECB (Electronic Codebook) Mode
ECB is one of the simplest encryption modes where each block of plaintext is encrypted independently using the same key. While easy to implement, ECB is less secure because identical plaintext blocks produce identical ciphertext blocks, revealing patterns in the plaintext.

### OFB (Output Feedback) Mode
OFB mode converts a block cipher into a stream cipher. It generates a keystream by encrypting an initialization vector (IV) and XORs this keystream with the plaintext. This mode helps obscure plaintext patterns and is generally more secure against pattern analysis compared to ECB.

### scrypt Key Derivation Function
scrypt is a key derivation function designed to convert a password into a cryptographic key. It provides resistance against hardware attacks by using parameters to control the computational and memory costs of the key derivation process.


## Installation

1. **Install the dependencies** using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place an image file named `sample_input.png` in the same directory as the script. The image should be in RGB format.

2. Execute the script with Python. The script will:
   - Derive a DES key from a password.
   - Load and convert the image to bytes.
   - Encrypt the image bytes using DES in both ECB and OFB modes.
   - Save and display the encrypted images.


    ```bash
    python main.py
    ```


## Code Explanation

### `derive_key(password: str)`

```python
def derive_key(password: str):
    salt = get_random_bytes(16)
    print(f"Salt: {salt} Length: {len(salt)}")

    encoded_password = password.encode()
    print(f"Encoded Password: {encoded_password} Length: {len(encoded_password)}")

    key = scrypt(password=encoded_password, salt=salt, key_len=8, N=2**14, r=8,  p=1)
    print(f"Key: {key} Length: {len(key)}")
    return key
```

This function derives a DES key from a user-provided password using the scrypt key derivation function. 

- **Parameters**:
  - `password`: The user-provided password used to generate the cryptographic key.
- **Process**:
  - A 16-byte salt is generated using `get_random_bytes(16)`. The salt ensures that the same password produces different keys each time it is used.
  - The password is encoded to bytes.
  - `scrypt` is used to derive an 8-byte key from the encoded password and salt. The parameters for scrypt are:
    - `key_len=8`: Specifies the length of the derived key in bytes (DES key is 8 bytes).
    - `N=2**14`: Determines the CPU/memory cost. Higher values increase security but require more computation.
    - `r=8`: The block size for the internal hash function.
    - `p=1`: The parallelization factor.
- **Outputs**:
  - The function prints the salt, encoded password, and derived key for verification and returns the DES key.

### `image_to_bytes(image: Image.Image)`

```python
def image_to_bytes(image: Image.Image):
    img_data = np.array(image)
    print(f"Image Shape: {img_data.shape}")
    plain_text = img_data.tobytes()
    return plain_text
```

This function converts an image into a byte representation suitable for encryption.

- **Parameters**:
  - `image`: A PIL Image object that is to be converted to bytes.
- **Process**:
  - The image is converted to a NumPy array, which allows easy manipulation of image data.
  - The shape of the array is printed, showing the image dimensions and color channels.
  - The array is flattened into a bytes object using `tobytes()`.
- **Outputs**:
  - Returns the byte representation of the image.

### `bytes_to_image(data: bytes, original_image: Image.Image)`

```python
def bytes_to_image(data: bytes, original_image: Image.Image):
    arr = np.frombuffer(data, dtype=np.uint8).reshape(original_image.size[1], original_image.size[0], 3)
    return Image.fromarray(arr)
```

This function converts bytes back into an image.

- **Parameters**:
  - `data`: The byte data that needs to be converted into an image.
  - `original_image`: The original PIL Image object, used to retrieve the image dimensions.
- **Process**:
  - Converts the byte data into a NumPy array using `frombuffer()`.
  - Reshapes the array to match the dimensions of the original image (width, height, color channels).
  - Creates a new PIL Image from the reshaped array.
- **Outputs**:
  - Returns a PIL Image object created from the byte data.

### `des_encryption_ecb(plain_text: bytes, key: bytes)`

```python
def des_encryption_ecb(plain_text: bytes, key: bytes):
    des = DES.new(key, mode=DES.MODE_ECB)
    padding_len = (8 - len(plain_text) % 8) % 8
    data = plain_text + b'\x00' * padding_len
    encrypted_data = des.encrypt(data)
    return encrypted_data
```

This function performs DES encryption in ECB mode.

- **Parameters**:
  - `plain_text`: The byte data of the image to be encrypted.
  - `key`: The 8-byte DES key used for encryption.
- **Process**:
  - Creates a DES cipher object with ECB mode.
  - Calculates padding length to ensure that the plaintext length is a multiple of 8 bytes (DES block size).
  - Adds padding to the plaintext.
  - Encrypts the padded plaintext using DES in ECB mode.
- **Outputs**:
  - Returns the encrypted ciphertext.

### `des_encryption_ofb(plain_text: bytes, key: bytes)`

```python
def des_encryption_ofb(plain_text: bytes, key: bytes):
    iv = get_random_bytes(8)
    des = DES.new(key, mode=DES.MODE_OFB, iv=iv)
    encrypted_data = des.encrypt(plain_text)
    return encrypted_data
```

This function performs DES encryption in OFB mode.

- **Parameters**:
  - `plain_text`: The byte data of the image to be encrypted.
  - `key`: The 8-byte DES key used for encryption.
- **Process**:
  - Generates a random 8-byte initialization vector (IV).
  - Creates a DES cipher object with OFB mode and the generated IV.
  - Encrypts the plaintext using DES in OFB mode.
- **Outputs**:
  - Returns the encrypted ciphertext.

### `main()`

```python
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
```
