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
file_path = r'c:\Users\admin\Downloads\Magic Coupon Retaile (1).xlsx'  # Replace with your file path
data = pd.read_excel(file_path)

# Encrypt and save each row
# encrypted_rows = []
encoded_encrypted_rows=[]

for index, row in data.iterrows():
    row_data = (str(row.iloc[3]) + "-" + row.iloc[4]+ "-" + row.iloc[0] + "-" + row.iloc[1]).encode("utf-8") #(str(row.iloc[0]) + "-" + row.iloc[1]).encode("utf-8") ,,,,(str(row.iloc[0]) + "-" + row.iloc[1]+ "-" + row.iloc[2]).encode("utf-8")
    padded_row_data = pad_message(row_data)
    encrypted_row = encrypt_message(padded_row_data, key, iv)

#http://push.sms.com/api/?apikey=asjdosadjsdja&text=%E0%A4%A7%E0%A4%A8%E0%A5%8D%E0%A4%AF%E0%A4%B5%E0%A4%BE%E0%A4%A6%20%21%20%E0%A4%86%E0%A4%AA%E0%A4%A3%20%E0%A4%95%E0%A5%87%E0%A4%B2%E0%A5%87%E0%A4%B2%E0%A5%8D%E0%A4%AF%E0%A4%BE%20Winter%20Offer%20%E0%A4%AE%E0%A4%A7%E0%A5%80%E0%A4%B2%20%E0%A4%B8%E0%A4%B9%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%9A%E0%A5%80%20%E0%A4%86%E0%A4%AE%E0%A5%8D%E0%A4%B9%E0%A5%80%20%E0%A4%B5%E0%A4%BF%E0%A4%B6%E0%A5%87%E0%A4%B7%20%E0%A4%A8%E0%A5%8B%E0%A4%82%E0%A4%A6%20%E0%A4%95%E0%A5%87%E0%A4%B2%E0%A5%80%20%E0%A4%86%E0%A4%B9%E0%A5%87.%20http%3A%2F%2Fcoupon.sapatchai.com%2F%3Fu%3DmNr%252B4ZKS%252Bkm2u8KGzLtW5EGmlRMlPRR%252BS4rkwfAuVZ7nda2PeEd5qROC4EnU%252FGoE%E0%A4%AF%E0%A4%BE%20%E0%A4%B2%E0%A4%BF%E0%A4%82%E0%A4%95%20%E0%A4%B5%E0%A4%B0%20%E0%A4%9C%E0%A4%BE%E0%A4%8A%E0%A4%A8%20%E0%A4%86%E0%A4%AA%E0%A4%A3%20%E0%A4%86%E0%A4%AA%E0%A4%B2%E0%A5%87%20%28Scratch%20%26%20win%20%E0%A4%AA%E0%A4%A6%E0%A5%8D%E0%A4%A7%E0%A4%A4%E0%A5%80%E0%A4%A8%E0%A5%87%20%29%20%E0%A4%AE%E0%A5%85%E0%A4%9C%E0%A4%BF%E0%A4%95%20%E0%A4%95%E0%A5%81%E0%A4%AA%E0%A4%A8%20%E0%A4%AE%E0%A4%BF%E0%A4%B3%E0%A4%B5%E0%A5%82%20%E0%A4%B6%E0%A4%95%E0%A4%A4%E0%A4%BE.%20%E0%A4%B9%E0%A4%BE%20%E0%A4%AE%E0%A5%87%E0%A4%B8%E0%A5%87%E0%A4%9C%20%E0%A4%95%E0%A5%8B%E0%A4%A3%E0%A4%BE%E0%A4%B8%E0%A4%B9%E0%A5%80%20share%20%E0%A4%95%E0%A4%B0%E0%A5%82%20%E0%A4%A8%E0%A4%95%E0%A4%BE.%20-%E0%A4%B8%E0%A4%AA%E0%A4%9F

    encrypted_data = base64.b64encode(encrypted_row).decode('utf-8')
    # encrypted_data = base64.b64encode("http://coupon.sapatchai.com/"+encrypted_row).dncode('utf-8')
    # print("encrypted_datammmmmmm",encrypted_data)
    
    # Encode the encrypted data
    encoded_encrypted_data = quote(encrypted_data, safe='')
    # encoded_encrypted_data2 = quote("http://coupon.sapatchai.com/?u=" + encoded_encrypted_data , safe='')
    # print("encoded_encrypted_datadddddddddd333333333",encoded_encrypted_data)
    encoded_encrypted_rows.append("http://coupon.sapatchai.com/?u="+encoded_encrypted_data)
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
data.to_excel('Magic Coupon Retaile.xlsx', index=False)

# Save encrypted rows to a new Excel file
# encrypted_df = pd.DataFrame({'EncryptedData': encrypted_rows})
# encrypted_df.to_excel('encrypted_data.xlsx', index=False)
