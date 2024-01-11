import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import pandas as pd
from urllib.parse import quote



def pad_message(message):
    block_size = algorithms.AES.block_size // 8  # Block size in bytes (AES uses 128 bits)
    padding_length = block_size - (len(message) % block_size)
    padding = bytes([padding_length]) * padding_length
    return message + padding

def encrypt_message(message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(message) + encryptor.finalize()
    return ct

# Convert the key and IV to bytes
key = b"35b49627ee3ef324580b5c2248ac31d3"
iv = "RRF5D8C71B39E4C0".encode('utf-8')  

# Read data from Excel file
file_path = r'c:\Users\admin\Downloads\Untitled spreadsheet (5).xlsx'  # Replace with your file path
data = pd.read_excel(file_path)

# Encrypt and save each row
# encrypted_rows = []
encoded_encrypted_rows=[]

for index, row in data.iterrows():
    row_data = (str(row.iloc[0]) + "-" + row.iloc[1]+ "-" + row.iloc[2]).encode("utf-8") #(str(row.iloc[0]) + "-" + row.iloc[1]).encode("utf-8") ,,,,(str(row.iloc[0]) + "-" + row.iloc[1]+ "-" + row.iloc[2]).encode("utf-8")
    padded_row_data = pad_message(row_data)
    encrypted_row = encrypt_message(padded_row_data, key, iv)



    encrypted_data = base64.b64encode(encrypted_row).decode('utf-8')
    # print("encrypted_datammmmmmm",encrypted_data)
    
    # Encode the encrypted data
    encoded_encrypted_data = quote(encrypted_data)
    # print("encoded_encrypted_datadddddddddd",encoded_encrypted_data)
    encoded_encrypted_rows.append(encoded_encrypted_data)
    # print("encoded_encrypted_rowsssssssssssss",encoded_encrypted_rows)




data['EncryptedData'] = encoded_encrypted_rows
    


######### this only encrytp data regarding     
#     encrypted_rows.append(base64.b64encode(encrypted_row).decode('utf-8'))
#     print("encrypted_row",encrypted_rows)

# data['EncryptedData'] = encrypted_rows
    
############### end this encrytp

######### this funcation get in encode code regarding 
# def encode_row(row):
#     return quote('-'.join(str(cell) for cell in row))

# # Encode all rows in the DataFrame and store in a new column 'Encode'
# data['Encode'] = data.apply(encode_row, axis=1)




# Save the modified DataFrame back to the Excel file
data.to_excel('encryptedexcel_data222.xlsx', index=False)

# Save encrypted rows to a new Excel file
# encrypted_df = pd.DataFrame({'EncryptedData': encrypted_rows})
# encrypted_df.to_excel('encrypted_data.xlsx', index=False)
