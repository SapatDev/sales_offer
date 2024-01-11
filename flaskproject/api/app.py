from config import *
from view import *
from decode import *
from encryt import *
from encodeurls import *
# from flask import Flask ,request, jsonify
# # from flask_mysqldb import MySQL
# # import mysql.connector

# app = Flask(__name__,static_folder='static')

# # app.config['MYSQL_HOST'] = '142.93.208.119'
# # app.config['MYSQL_USER'] = 'mandar'
# # app.config['MYSQL_PASSWORD'] = 'Nb7Np4!lURI0u'
# # app.config['MYSQL_DB'] = 'salesoffer'
 
# # mysql = MySQL(app)


# @app.route('/api/skulist', methods=['GET'])
# def get_sku_list():
#     conn = mysql.connection.cursor()
#     # cursor = conn.cursor()
#     sku=[]
#     try:
#         conn.callproc('GetSKUList')
#         crs_sku = conn.fetchall()
#         for row in crs_sku:
#             sku_list = {
#                 'sku_id': row[0],  
#                 'grade_code': row[1],
#                 'grammage': row[2],
#                 'stock_type': row[3] ,
#                 'category': row[4]              
#             }
#             sku.append(sku_list)
#             print("sku",sku)
#         # print("sku",sku[0].keys())
#     except Exception as e:
#         print(f"Error: {e}")

#     # cursor.close()
#     conn.close()

#     return jsonify({"skuList":sku,"code":200,"message":"All Sku list loadded"}),200


# @app.route('/')
# def hello_world():
#     return 'Hello World!'

# @app.route('/app/')
# def todo():
#     return jsonify({"msg":"hello world"})

if __name__ == '__main__':
    app.run(debug=True)
