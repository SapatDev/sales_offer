import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
# from encode import encrypt_message

def encrypt_message(message, key):
    # Pad the message to be a multiple of the block size (16 bytes for AES)
    block_size = algorithms.AES.block_size // 8
    padded_message = message.ljust(len(message) + (block_size - len(message) % block_size))

    # Generate a random Initialization Vector (IV)
    # iv = os.urandom(block_size)
    # print(iv)
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'RRF5D8C71B39E4C0'), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_message.encode('utf-8')) + encryptor.finalize()

    # Combine the IV and ciphertext and base64 encode the result
    encrypted_message = base64.b64encode(b'RRF5D8C71B39E4C0' + ciphertext)

    return encrypted_message

def decrypt_message(encrypted_message, key):
    # Extract IV from the first block
    iv = encrypted_message[:algorithms.AES.block_size // 8]
    ciphertext = encrypted_message[algorithms.AES.block_size // 8:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadded = decrypted.rstrip(b'\0')

    return unpadded


if __name__ == '__main__':
    key = b'35b49627ee3ef324580b5c2248ac31d3'
    message = "SAPAT INTERNATIONAL MUMBAI RISHABH"

    # Encrypt the message
    encrypted_message = encrypt_message(message, key)
    encode_message = encrypted_message.decode('utf-8')
    # print("Encrypted Message:", encrypted_message)
    print("Encrypted Message:", encode_message)

    # Decrypt the message
    decrypted_message = decrypt_message(base64.b64decode(b'UlJGNUQ4QzcxQjM5RTRDMFvfhrVpxMipPsR6b2sbayi+HE6/3vAs8EpIo8u/Iy89iN4lZ9xUfHcyKV1GnQ0X1WfUfYp+OGp9ZZOGQ4379EmSQCuuRr44WIvB5OjG0yyxltyTk8c5oe1mYgT8B+uDz4vIti1+7MRwDgqcwQ9JdQfhWIJdM27v3+47pAsGMBzA'), key)

    # Print the decrypted message as a raw byte sequence
    print("Decrypted Message:", decrypted_message.decode('utf-8'))
