from flask import Flask, request
import urllib.parse
from urllib.parse import urlencode,quote
from config import *
import pandas as pd
from urllib.parse import quote



# @app.route('/encode', methods=['GET'])
# def encode_url():
#     if request.method == 'GET':
#         query = request.form.get('query')
#         if query:
#             encoded_query = urllib.parse.quote(query,safe="")
#             if encoded_query.startswith("%27") and encoded_query.endswith("%27"):
#                 encoded_query = encoded_query[3:-3]
#             print("sssssencoded_query",encoded_query)
#             return f"Encoded URL: {encoded_query}"
#         else:
#             return "Please provide a 'query' parameter."
#     else:
#         return "Only POST requests are allowed."
    

@app.route('/encode', methods=['GET'])
def encode_url():
    if request.method == 'GET':
        query = 'tiC4EIEf04xtHE7AwREYkt6bS8sG5qWmxJEWPPmX3ctKVwBWVicah9aDJKfy5RjUwpUL2ySWMhXVp3DmsgEJ7A==' #request.form.get('query') 'Hellö Wörld@Python'
        if query:
            encoded_query = quote(query)
            print("Encoded query:", encoded_query)
            return f"Encoded URL: {encoded_query}"
        else:
            return "Please provide a 'query' parameter."
    else:
        return "Only GET requests are allowed."
    
    


# @app.route('/encode1', methods=['GET'])
# def encode_excel():
#     file_path = r'c:\Users\admin\Downloads\Untitled spreadsheet (5).xlsx'
#     df = pd.read_excel(file_path)
#     # Encrypt and save each row
#     encoded_columns = []

#     for index, row in df.iterrows():
#         row_data = (str(row.iloc[0]) + "-" + row.iloc[1]+ "-" + row.iloc[2]) #(str(row.iloc[0]) + "-" + row.iloc[1]).encode("utf-8") ,,,,(str(row.iloc[0]) + "-" + row.iloc[1]+ "-" + row.iloc[2]).encode("utf-8")
#         padded_row_data = quote(row_data)
#         encoded_columns.append(padded_row_data)
#         # encrypted_row = encrypt_message(padded_row_data, key, iv)
#         # encrypted_rows.append(base64.b64encode(encrypted_row).decode('utf-8'))
#         print("encodedataexcel_row",encoded_columns)

#     df['EncryptedData'] = encoded_columns

#     # Save the modified DataFrame back to the Excel file
#     df.to_excel('encodeedexcel_data.xlsx', index=False)



@app.route('/encode1', methods=['GET'])
def encode_excel():
    file_path = r'c:\Users\admin\Downloads\table_data (11).xlsx'
    df = pd.read_excel(file_path)

    # Function to encode a string
    def encode_row(row):
        return quote('-'.join(str(cell) for cell in row))

    # Encode all rows in the DataFrame and store in a new column 'EncryptedData'
    df['Encode'] = df.apply(encode_row, axis=1)

    # Save the DataFrame with encoded data to a new Excel file
    df.to_excel('encoded_outpute2.xlsx', index=False)

    return df['Encode'].tolist()



    # def encode_row(row):
    #     return row.apply(lambda cell: quote(str(cell)))

    # encoded_columns = []
    # for index, row in df.iterrows():
    #     encoded_column_name = (str(row.iloc[0]) + "-" + row.iloc[1]+ "-" + row.iloc[2]) 
    #     df[encoded_column_name] = encode_row(row)
    #     encoded_columns.append(encoded_column_name)

    # output_file_name = 'encodeddata_output.xlsx'
    # print("output_file_name", output_file_name)
    # with pd.ExcelWriter(output_file_name, engine='openpyxl') as writer:
    #     df.to_excel(writer, index=False, sheet_name='Encoded Data', columns=encoded_columns)

    # return df.to_string()  