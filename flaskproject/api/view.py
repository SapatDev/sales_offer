from sqlalchemy import text
from decode import encrypt_message
# from encryt import encrypt_data
from config import *
from flask import Flask, render_template
import pandas
from flask import Flask, render_template, request
import pandas as pd
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from flask import send_file
from flask import render_template, request
import io
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets
import string
import os
from datetime import datetime
from werkzeug.exceptions import BadRequestKeyError




###################################### Sales data 

@app.route('/sales', methods=['GET', 'POST'])
def sales():
    global selected_date
    if request.method == 'GET':
        try:
            selected_date = request.args.get('selectedDate')
            print(selected_date)
        except BadRequestKeyError:
            selected_date = "2023-12"

        if not selected_date:
            selected_date = "2023-12"

        # Parse the selected date string into a datetime object
        selected_datetime = datetime.strptime(selected_date, '%Y-%m')

        # Extract month and year
        selected_month = selected_datetime.month
        selected_year = selected_datetime.year

        # Check if both month and year are not empty strings
        if selected_month and selected_year:
            query = text('CALL GetSalesDataPerYearPerMonthUsingParameter(:month, :year);')
            result = db.session.execute(query, {'month': selected_month, 'year': selected_year})
        else:
            return "Please select both month and year"

    else:
        # Default query for initial page load
        query = text('CALL GetSalesDataPerYearPerMonthUsingParameter(12, 2023);')
        result = db.session.execute(query)

    datakey = result.keys()
    dict_list = []

    # Use a server-side cursor to fetch data in chunks
    while True:
        chunk = result.fetchmany(500)  # Adjust the chunk size as needed

        if not chunk:
            break
        dict_list.extend([{item: tup[i] for i, item in enumerate(datakey)} for tup in chunk])

    result.close()

    return render_template('sales.html', dict_list=dict_list)



@app.route('/api/GetSalesDataPerYearPerMonthUsingParameter', methods=['GET'])
def GetSalesDataPerYearPerMonthUsingParameter():
    try:
        result=db.session.execute(text('CALL GetSalesDataPerYearPerMonthUsingParameter(11, 2023);'))
        datakey=result.keys()
        data=result.fetchall()
        result.close()
        dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("ddtat",dict_list)
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400
    

###################################### GetOfferCouponType
@app.route('/getOfferCouponType')
def getOfferCouponTypedata():
    result = db.session.execute(text('CALL GetOfferCouponType(5);'))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
  
    return render_template('getOfferCouponType.html',dict_list=dict_list)
    


@app.route('/api/getOfferCouponType', methods=['GET'])
def getOfferCouponType():
    try:
        result=db.session.execute(text('CALL GetOfferCouponType(1);'))
        datakey=result.keys()
        data=result.fetchall()
        result.close()
        dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("ddtat",dict_list)
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400 

#################################### OfferDetails 
def get_offer_count(offer_id):
    if offer_id == 'SSC2':
        result = db.session.execute(text('CALL GetSweetSummerOfferDistinctOutletCount();'))
    elif offer_id == 'SPD1':
        result = db.session.execute(text('CALL GetSpdOfferDistinctOutletCount()'))
    elif offer_id == 'MO':
        result = db.session.execute(text('CALL GetMonsoonOfferDistinctOutletCount()'))
    elif offer_id == 'WSO':
        result = db.session.execute(text('CALL GetWinterOfferDistinctOutletCount()'))
    elif offer_id == 'EKS2':
        result = db.session.execute(text('CALL GetEkSeBadhkarEkDistinctOutletCount()'))  #GetWinterOfferDistinctOutletCount()  same function used because not count get table not proper
    elif offer_id == 'NYD':
        result = db.session.execute(text('CALL GetSpdOfferDetails()')) #same function used because not count get table not proper
    
        
    # Add similar blocks for other offer IDs
    else:
        # Provide a default action or raise an exception for unknown offer IDs
        raise ValueError(f"Unknown offer ID: {offer_id}")

    count = result.fetchone()[0]
    result.close()
    return count

@app.route('/')
def OfferDetailsdisplay():

    offer_id = request.args.get('offer_id', type=str)

    result = db.session.execute(text('CALL OfferDetails();'))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
 
    dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

    
    counts = []
    offer_ids = ['SSC2', 'SPD1', 'MO', 'WSO', 'EKS2', 'NYD']
    counts = [get_offer_count(offer_id) for offer_id in offer_ids]
    print("Sscounts",counts)

    # # Fetch counts for different offers and append to the counts list
    # if offer_id == 'SSC2':
    #     result_ssc_count = db.session.execute(text('CALL GetSweetSummerOfferDistinctOutletCount();'))
    #     count = result_ssc_count.fetchone()[0]  
    #     result_ssc_count.close()
    #     counts.append(count)
    # elif offer_id == 'SPD1':
    #     result_wso_count = db.session.execute(text('CALL GetSpdOfferDetails()'))
    #     count = result_wso_count.fetchone()[0]
    #     result_wso_count.close()
    #     counts.append(count)
    # elif offer_id == 'MO':
    #     result_wso_count = db.session.execute(text('CALL GetMonsoonOfferDistinctOutletCount()'))
    #     count = result_wso_count.fetchone()[0]
    #     result_wso_count.close()
    #     counts.append(count)
    # elif offer_id == 'WSO':
    #     result_wso_count = db.session.execute(text('CALL GetWinterOfferDistinctOutletCount()'))
    #     count = result_wso_count.fetchone()[0]
    #     result_wso_count.close()
    #     counts.append(count)
    # elif offer_id == 'EKS2':
    #     result_wso_count = db.session.execute(text('CALL GetEkSeBadhkarEkOfferSeason1()'))
    #     count = result_wso_count.fetchone()[0]
    #     result_wso_count.close()
    #     counts.append(count)
    #     print("ncountsnnnnnn",counts)
    # elif offer_id == 'NYD':
    #     result_wso_count = db.session.execute(text('CALL GetMonsoonOfferDistinctOutletCount()'))
    #     count = result_wso_count.fetchone()[0]
    #     result_wso_count.close()
    #     counts.append(count)
    #     print("ncountsnnnnnn",counts)
    # else:
    #     result_monsoon_count = db.session.execute(text('CALL GetMonsoonOfferDistinctOutletCount(); ;'))
    #     count = result_monsoon_count.fetchone()[0]
    #     result_monsoon_count.close()
    #     counts.append(count)
    #     print("ncountsnnnnnn",counts)

    return render_template('offerdetails.html',dict_list=dict_list,counts=counts,offer_ids=offer_ids)

    

@app.route('/api/offerdetails', methods=['GET'])
def OfferDetails():
    try:
        result=db.session.execute(text('CALL OfferDetails();'))
        datakey=result.keys()
        data=result.fetchall()
        result.close()
        dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("ddtat",dict_list)
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400 



#############################  NewOffer 

@app.route('/newoffer')
def newoffer():
    result = db.session.execute(text('CALL NewOffer;'))
     
    datakey = result.keys()
    data = result.fetchall()
 
    result.close()
    dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
    df2=pd.DataFrame(dict_list)
        
    unique_type_ids = df2['type_Id'].unique()
    print("unique_type_ids",unique_type_ids)
    # print("unique_type_ids",data)

    return render_template('newoffer.html',dict_list=dict_list)

@app.route('/api/newoffer', methods=['GET'])
def NewOffer():
    try:
        result=db.session.execute(text('CALL NewOffer();'))
        datakey=result.keys()
        data=result.fetchall()
        result.close()
        dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("ddtat",dict_list)
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400



##################### salesmonth 

@app.route('/api/salesmonth', methods=['GET'])
def salesmonth():
    try:
        result=db.session.execute(text('CALL GetSalesDataPerYearPerMonth();'))
        datakey=result.keys()
        data=result.fetchall()
        result.close()
        dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("ddtat",dict_list)
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400
    
########################################### Employee Name Display #############
@app.route('/employee')
def employeename():
        result = db.session.execute(text('CALL GetEmployeeData();'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        return render_template('employee_name.html',dict_list=dict_list)


@app.route('/employee_info')
def employee_info():
    employee_id = request.args.get('empId')
    result = db.session.execute(text(f"CALL GetEmployeeInfo('{employee_id}');"))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list  = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
    
    return jsonify({"dict":dict_list})
   
    # return render_template('employee_Id.html', dict_list=dict_list)



@app.route('/employee_payerId')
def employee_payerId():
    payer_id = request.args.get('payerId')
    result = db.session.execute(text(f"CALL GetEmployeeInfoBypayerId('{payer_id}');"))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list  = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
    # print("PayerIdDatannnnnnnnnnnn",dict_list)
    
    # return jsonify(dict_data)
    return render_template('employeepayerId.html', dict_list=dict_list)


@app.route('/api/emp', methods=['GET'])
def employeelist():
    try:
        # result=db.session.execute(text(f"CALL GetEmployeeData()"))
        result=db.session.execute(text(f"CALL GetEmployeeInfoBypayerId('GAU006')"))      #text("CALL GetEmployeePayerInfo('S2284');"))
        datakey=result.keys()
        data=result.fetchall()
        result.close()
        dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("ddtat",dict_list)
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400
    


#######################################

######################  Totalsales
@app.route('/totalsales')
def totalsales():
        result = db.session.execute(text('CALL GetTotalSalesData();'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        return render_template('totalsales.html',dict_list=dict_list)

    

########### SweetSummerOffer  html template create only 
@app.route('/offer/<offerID>/<int:pkey>')
def SSC2(offerID,pkey):
    
    # print("/offer/<offerID>/<int:pkey>", request.args.get('offer_name', type=int))
        offer_id = request.args.get('offer_name', type=int)
     
        resultType=db.session.execute(text('CALL GetOfferCouponType('+str(pkey)+');'))
        datakey=resultType.keys()
        data=resultType.fetchall()
        resultType.close()
        dict_list_type=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]


        if offerID == "EKS2":
            resultType = db.session.execute(text('CALL GetOldOfferCoupenType();'))
            datakey = resultType.keys()
            data = resultType.fetchall()
            resultType.close()
            dict_list_type = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
            type_ids = [item['type_Id'] for item in dict_list_type]
    
            # print("Type IDs:", type_ids)
        
        if (offerID=='SSC2'):
            result = db.session.execute(text('CALL SweetSummerOffer();'))
        elif(offerID=="SPD1"):
            result = db.session.execute(text('CALL GetSpdOfferDetails();'))          
        elif(offerID=='MO'):
            result = db.session.execute(text('CALL MonsoonOffer();'))
        elif(offerID=='WSO'):
            result = db.session.execute(text('CALL NewOffer();')) 
        elif(offerID=="EKS2"):
            result = db.session.execute(text('CALL GetEkSeBadhkarEkOfferSeason1();'))
        elif(offerID=="NYD"):
            result = db.session.execute(text('CALL MonsoonOffer();'))
        else:
            result = db.session.execute(text('CALL MonsoonOffer();'))

        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        # Extract year and month from created_at
        for entry in dict_list:
            entry['year'] = entry['created_at'].year
            entry['month'] = entry['created_at'].month
            


        df = pd.DataFrame(dict_list)
        df2=pd.DataFrame(dict_list_type)
        salesgroups = df['salesgroup'].unique()
        unique_type_ids = df2['type_Id'].unique()
        df_year = df['year'].unique()
        df_month =df['month'].unique()
        print("df_month",df_month)

        print("df_year",df_year)

        
        # Create an empty DataFrame with salesgroups as index and type_Ids as columns
        result_df = pd.DataFrame(index=salesgroups, columns=df['type_Id'])
    

        # Fill the result_df with scheme_count values
        for index, row in df.iterrows():
            result_df.loc[row['salesgroup'], row['type_Id']] = row['scheme_count']
            

        # Convert the DataFrame to HTML table
        html_table = result_df.to_html()
        # print("html_table",html_table)


        counts = []

        # Fetch counts for different offers and append to the counts list
        if offerID == 'SSC2':
            result_ssc_count = db.session.execute(text('CALL GetSweetSummerOfferDistinctOutletCount();'))
            count = result_ssc_count.fetchone()[0]  
            result_ssc_count.close()
            counts.append(count)
        elif offerID == 'SPD1':
            result_wso_count = db.session.execute(text('CALL GetSpdOfferDistinctOutletCount()'))
            count = result_wso_count.fetchone()[0]
            result_wso_count.close()
            counts.append(count)
        elif offerID == 'MO':
            result_wso_count = db.session.execute(text('CALL GetMonsoonOfferDistinctOutletCount()'))
            count = result_wso_count.fetchone()[0]
            result_wso_count.close()
            counts.append(count)
        elif offerID == 'WSO':
            result_wso_count = db.session.execute(text('CALL GetWinterOfferDistinctOutletCount()'))
            count = result_wso_count.fetchone()[0]
            result_wso_count.close()
            counts.append(count)
        elif offerID == 'EKS2':
            result_wso_count = db.session.execute(text('CALL GetMonsoonOfferDistinctOutletCount()'))
            count = result_wso_count.fetchone()[0]
            result_wso_count.close()
            counts.append(count)
        elif offerID == 'NYD':
            result_wso_count = db.session.execute(text('CALL GetSpdOfferDistinctOutletCount()'))
            count = result_wso_count.fetchone()[0]
            result_wso_count.close()
            counts.append(count)
        else:
            result_monsoon_count = db.session.execute(text('CALL GetMonsoonOfferDistinctOutletCount(); ;'))
            count = result_monsoon_count.fetchone()[0]
            result_monsoon_count.close()
            counts.append(count)
            # print("ncountsnnnnnn",counts)

        sales_group_data = {}

        # Populate sales_group_data with sales groups and their Type ID counts
        for salesgroup in salesgroups:
            sales_data = result_df.loc[salesgroup].dropna()
            sales_group_data[salesgroup] = sales_data.unique().sum() 
           
    
        return render_template('sweetsummer.html',df_year=df_year,df_month=df_month,sales_group_data=sales_group_data,counts=counts,dict_list_type=dict_list_type,dict_list=dict_list,html_table=html_table,unique_type_ids=unique_type_ids,salesgroups=salesgroups,offer_id=offer_id)

######################################### click on salesgroup regarding 
@app.route('/offer_details/<salesgroup>/<int:pkey>')
def salesgroup(salesgroup,pkey):
        # print("/offer/<offerID>/<string:pkey>", request.args.get('salesgroup', type=int))
        # print("/offer_details/<salesgroup>/<int:pkey>", request.args.get('offer_name', type=int))
        offer_id = request.args.get('offer_id', type=int)
        # print("ss",offer_id)

        resultType=db.session.execute(text('CALL GetOfferCouponType('+str(pkey)+');'))
        datakey=resultType.keys()
        data=resultType.fetchall()
        resultType.close()
        dict_list_type=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("Ss",dict_list_type)

        if offer_id == 5:
            resultType = db.session.execute(text('CALL GetOldOfferCoupenType();'))
            datakey = resultType.keys()
            data = resultType.fetchall()
            resultType.close()
            dict_list_type = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
            type_ids = [item['type_Id'] for item in dict_list_type]
            print("Type IDs:", type_ids)
        


        if offer_id == 1:
            result = db.session.execute(text(f"CALL GetSalesgroupDataSummerOffer('{salesgroup}');"))

        elif offer_id == 2:
            result = db.session.execute(text(f"CALL GetSpdOfferDetailsBySalesgroup('{salesgroup}');"))

        elif offer_id == 3:
            result = db.session.execute(text(f"CALL GetSalesgroupDataMonsoonOffer('{salesgroup}');"))

        elif offer_id == 4:
            result = db.session.execute(text(f"CALL GetSalesgroupData('{salesgroup}');"))

        elif offer_id == 5:
            result = db.session.execute(text(f"CALL GetEkSeBadhkarEkOfferSeason1BySalesgroup('{salesgroup}');"))

        elif offer_id == 6:
            result = db.session.execute(text(f"CALL GetSalesgroupData('{salesgroup}');"))
        else:
            result = db.session.execute(text(f"CALL GetSalesgroupData('{salesgroup}');"))



        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        df = pd.DataFrame(dict_list)
        df2=pd.DataFrame(dict_list_type)
        # idtype=df['id'].unique()
        # print("dfddddddddddddddddddddddddddddddd",df)

        salesgroups = df['salesgroup'].unique()
        payerId = df['payerId'].unique()
        scheme_count=df['scheme_count']
        unique_type_ids = df2['type_Id'].unique()
        stokist_name_Id=df['stokist_name'].unique()
        # unique_type_ids = df2['type_Id'].unique()
        # Get the selected month and year from the request parameters
        

        # Create an empty DataFrame with salesgroups as index and type_Ids as columns
        result_df = pd.DataFrame(index=payerId, columns=df['type_Id'])

        # Fill the result_df with scheme_count values
        for index, row in df.iterrows():
            result_df.loc[row['payerId'], row['type_Id']] = row['scheme_count']

        # print("----", result_df.to_dict())

        # Convert the DataFrame to HTML table
        html_table = result_df.to_html()
        
       
        return render_template('newsweetsummer.html',dict_list_type=dict_list_type,stokist_name_Id=stokist_name_Id,payerId=payerId,salesgroups=salesgroups,dict_list=dict_list,unique_type_ids=unique_type_ids,html_table=html_table,scheme_counts=scheme_count,offer_id=offer_id)

########################################## click on payerID releted data
@app.route('/offer_payer/<payer>/<int:pkey>')
def PayerId(payer,pkey):
        try:
            # print("/offer/<offerID>/<string:pkey>", request.args.get('salesgroup', type=int))
            # print("/offer_details/<salesgroup>/<int:pkey>", request.args.get('offer_name', type=int))
            offer_id = request.args.get('offer_id', type=int)
            # print("ss",offer_id)

            resultType=db.session.execute(text('CALL GetOfferCouponType('+str(pkey)+');'))
            datakey=resultType.keys()
            data=resultType.fetchall()
            resultType.close()
            dict_list_type=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
            # print("Ss",dict_list_type)

            if offer_id == 5:
                resultType = db.session.execute(text('CALL GetOldOfferCoupenType();'))
                datakey = resultType.keys()
                data = resultType.fetchall()
                resultType.close()
                dict_list_type = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
                type_ids = [item['type_Id'] for item in dict_list_type]
                # print("Type IDs:", type_ids)
            


            if offer_id == 1:
                result = db.session.execute(text(f"CALL GetNewSweetSummerOfferBypayerId('{payer}');"))

            elif offer_id == 2:
                result = db.session.execute(text(f"CALL GetSpdOfferDetailsBypayerId('{payer}');"))
            
            elif offer_id == 3:
                result = db.session.execute(text(f"CALL GetNewMonsoonOfferByPayerId('{payer}');"))

            elif offer_id == 4:
                result = db.session.execute(text(f"CALL GetNewWinterOfferBypayerId('{payer}');"))

            elif offer_id == 5:
                result = db.session.execute(text(f"CALL GetEkSeBadhkarEkOfferSeason1ByPayerId('{payer}');"))

            elif offer_id== 6:
                result = db.session.execute(text(f"CALL GetNewWinterOfferBypayerId('{payer}');"))
            else:
                result = db.session.execute(text(f"CALL GetNewSweetSummerOfferBypayerId('{payer}');"))



            datakey = result.keys()
            data = result.fetchall()
            result.close()
            dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

            df = pd.DataFrame(dict_list)
            df2=pd.DataFrame(dict_list_type)
            # idtype=df['id'].unique()
            # print("iddd",idtype)

            if 'outletId' in df.columns:
                outletId = df['outletId'].unique()
            else:
                outletId = []
            # print("outletIdssssss",outletId)
            # payerId = df['payerId'].unique()
            scheme_count=df['scheme_count']
            unique_type = df2['type_Id'].unique()
            unique_beatname=df['beatname']
            # unique_outlet_type_ids = df['outlet_type']
            unique_outletName=df['outletName']
            unique_coupon_type = df['coupon_type'].unique()
            
        

            # Create an empty DataFrame with salesgroups as index and type_Ids as columns
            result_df = pd.DataFrame(index=outletId, columns=df2['type_Id'])

            # Fill the result_df with scheme_count values
            for index, row in df.iterrows():
                result_df.loc[row['outletId'], row['coupon_type']] = row['scheme_count']

            # print("----", result_df.to_dict())

            # Convert the DataFrame to HTML table
            html_table = result_df.to_html()
            
        
            return render_template('payerdata.html',unique_outletName=unique_outletName,unique_coupon_type=unique_coupon_type,outletId=outletId,dict_list_type=dict_list_type,unique_beatname=unique_beatname,dict_list=dict_list,unique_type=unique_type,html_table=html_table,scheme_counts=scheme_count,offer_id=offer_id)
        except KeyError as e:
                        error_message = f"KeyError: {str(e)} occurred."
                        return render_template('payerdata.html', error_message=error_message)



####################### Saledata per year month
@app.route('/saledata/<int:page>')
def saledata(page=1):
       
        items_per_page = 20  # Define how many items to display per page
        result = db.session.execute(text('CALL GetSalesDataPerYearPerMonth();'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        
        total_items = len(data)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        
        offset = (page - 1) * items_per_page
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data[offset:offset+items_per_page]]
        
        return render_template('saledata.html', dict_list=dict_list, total_pages=total_pages)




######################### menulist
@app.route('/api/GetWinterOfferByPayerId', methods=['GET'])
def menulist():
    try:
        result = db.session.execute(text(f"CALL GetEkSeBadhkarEkDistinctOutletCount()"))
        # result = db.session.execute(text(f"CALL GetEmployeeInfo('S2358')"))   #GetMonsoonOfferByPayerId('SHR097')  GetEkSeBadhkarEkOfferSeason1
        # result = db.session.execute(text("CALL GetEmployeeData();"))
        # result =db.session.execute(text(f"CALL GetEmployeeInfoBypayerId('SSS71');"))
        # result.count()
        # print("result_data",result_data)
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
        # return render_template({"code": 200, "status": True, "result": dict_list}), 200
 
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400
    





