# import pandas as pd
# import base64
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend

# # Function to encrypt the message using AES
# def encrypt_message(message, key):
#     block_size = algorithms.AES.block_size // 8
#     padded_message = message.ljust(len(message) + (block_size - len(message) % block_size))
#     cipher = Cipher(algorithms.AES(b''+key), modes.CBC(b'RRF5D8C71B39E4C0'), backend=default_backend())
#     encryptor = cipher.encryptor()
#     ciphertext = encryptor.update(padded_message.encode('utf-8')) 
#     encrypted_message = base64.b64encode(ciphertext)
#     print("encrypted_message",encrypted_message)
#     return encrypted_message

# # Read data from Excel file
# file_path = r'c:\Users\admin\Downloads\Untitled spreadsheet (4).xlsx'  # Replace with your file path
# data = pd.read_excel(file_path)

# # Encrypt and save each row
# key = b'35b49627ee3ef324580b5c2248ac31d3'  # AES key
# encrypted_rows = []

# for index, row in data.iterrows():
#     row_data = str(row.iloc[0]) + "-" + row.iloc[1]# Convert row to CSV string without headers
#     print("row_datakjjjjjjjjjjjjj",row_data )
#     encrypted_row = encrypt_message(row_data, key)
#     encrypted_rows.append(encrypted_row)
#     # print('ssssss,',encrypted_rows)

# # Save encrypted rows to a new Excel file
# new_file_path = 'encrypted_data.xlsx'  # Replace with your desired output file path

# with pd.ExcelWriter(new_file_path) as writer:
#     for i, encrypted_row in enumerate(encrypted_rows):
#         df = pd.DataFrame({'EncryptedData': [encrypted_row]})
#         df.to_excel(writer, sheet_name=f'Row_{i+1}', index=False)
