# import base64
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# import pandas as pd
# import string
# import random


# file_path = r'c:\Users\admin\Downloads\Magic Coupon Retaile (1).xlsx'  
# data = pd.read_excel(file_path)

# encoded_encrypted_rows=[]

# for index, row in data.iterrows():
#     row_data = int(row.iloc[3])
#     result =random.choice(string.ascii_letters)+str(row_data*745)+random.choice(string.ascii_letters)
#     encoded_encrypted_rows.append("http://coupon.sapatchai.com/?u="+result)
#     # print("Ddddddddd","http://coupon.sapatchai.com/?u="+result)

# data['ShortData'] = encoded_encrypted_rows

# data.to_excel('excelletter.xlsx', index=False)

    




