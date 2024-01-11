import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import pandas as pd

def pad_message(message):
    block_size = algorithms.AES.block_size // 8  # Block size in bytes (AES uses 128 bits)
    padding_length = block_size - (len(message) % block_size)
    padding = bytes([padding_length]) * padding_length
    return message + padding
# def pad_message(message):
#     block_size = algorithms.AES.block_size // 16  # 256 bits
#     padding_length = block_size - (len(message) % block_size)
#     padding = bytes([padding_length]) * padding_length
#     return message + padding


def encrypt_message(message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(message) + encryptor.finalize()
    return ct

# Convert the key and IV to bytes
key = b"35b49627ee3ef324580b5c2248ac31d3"
iv = "RRF5D8C71B39E4C0".encode('utf-8')  # Assuming IV is provided as hex

# Your message to encrypt
message = b'1111-Yash-Sapat-Worli'


########################### this funcation in excel file data

# # Read data from Excel file
# file_path = r'c:\Users\admin\Downloads\Untitled spreadsheet (4).xlsx'  # Replace with your file path
# data = pd.read_excel(file_path)

# # Encrypt and save each row
# encrypted_rows = []

# for index, row in data.iterrows():
#     # Convert the row to bytes and pad it if needed
#     row_data = row.to_csv(index=False, header=False).encode('utf-8')
#     padded_row_data = row_data.ljust(len(row_data) + (16 - len(row_data) % 16))  # Pad to match AES block size
    
#     # Encrypt the row
#     encrypted_row = encrypt_message(padded_row_data, key, iv)
#     encrypted_rows.append(base64.b64encode(encrypted_row).decode('utf-8'))
#     print("encrypted_rows",encrypted_rows)

# # Save encrypted rows to a new Excel file
# new_file_path = 'encrypted_data.xlsx'  # Replace with your desired output file path

# # Create a new DataFrame with the encrypted rows and save it to an Excel file
# encrypted_df = pd.DataFrame({'EncryptedData': encrypted_rows})
# print("encrypted_df",encrypted_df)
# encrypted_df.to_excel(new_file_path, index=False)

############################ end this excel file
        


# Pad the message if needed to match the block size
# block_size = algorithms.AES.block_size // 8
# if len(message) % block_size != 0:
    # message += b'\0' * (block_size - len(message) % block_size)
padded_message = pad_message(message)

# Perform encryption without padding
encrypted_message = encrypt_message(padded_message, key, iv)

# Encode the encrypted message (bytes) as base64 for storage or transmission
encrypted_base64 = base64.b64encode(encrypted_message).decode('utf-8')
# Perform encryption
# encrypted_message = encrypt_message(message, key, iv)

# # Encode the encrypted message (bytes) as base64 for storage or transmission
# encrypted_base64 = base64.b64encode(encrypted_message).decode('utf-8')

print("Encrypted Message (base64):", encrypted_base64)
