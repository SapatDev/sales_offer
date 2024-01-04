from sqlalchemy import text
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


@app.route('/GetSalesDataPerYearPerMonthUsingParameter')
def hello():
    result = db.session.execute(text('CALL GetSalesDataPerYearPerMonthUsingParameter(12, 2023);'))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
  
    return render_template('index.html',dict_list=dict_list)
    


###################################### Sales data 
@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == 'POST':
        selected_month = request.form['month']
        selected_year = request.form['year']

        # Check if both month and year are not empty strings
        if selected_month and selected_year:
            result = db.session.execute(text('CALL GetSalesDataPerYearPerMonthUsingParameter(:month, :year);'), {'month': selected_month, 'year': selected_year})
        else:
            
            return "Please select both month and year"

    else:
        # Default query for initial page load
        result = db.session.execute(text('CALL GetSalesDataPerYearPerMonthUsingParameter(12, 2023);'))
   
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        return render_template('sales.html', dict_list=dict_list)

# @app.route('/sales')
# def sales():
#     result = db.session.execute(text('CALL GetSalesDataPerYearPerMonthUsingParameter(12, 2023);'))
#     datakey = result.keys()
#     data = result.fetchall()
#     result.close()
#     dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

#     return render_template('sales.html',dict_list=dict_list)



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

@app.route('/')
def OfferDetailsdisplay():
    result = db.session.execute(text('CALL OfferDetails();'))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

    return render_template('offerdetails.html',dict_list=dict_list)
    


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
    


######################  Totalsales
@app.route('/totalsales')
def totalsales():
        result = db.session.execute(text('CALL GetTotalSalesData();'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        return render_template('totalsales.html',dict_list=dict_list)




@app.route('/api/TotalSales', methods=['GET'])
def GetTotalSalesData():
    try:
        # result = db.session.execute(text(f'CALL GetSKUList();'))    
        result = db.session.execute(text('CALL GetTotalSalesData();'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
        # return render_template({"code": 200, "status": True, "result": dict_list}), 200
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400
    
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
        df = pd.DataFrame(dict_list)
        df2=pd.DataFrame(dict_list_type)
        salesgroups = df['salesgroup'].unique()
        unique_type_ids = df2['type_Id'].unique()
        
        # print("unique_type_ids",unique_type_ids)

        # Create an empty DataFrame with salesgroups as index and type_Ids as columns
        result_df = pd.DataFrame(index=salesgroups, columns=df['type_Id'])

        # Fill the result_df with scheme_count values
        for index, row in df.iterrows():
            result_df.loc[row['salesgroup'], row['type_Id']] = row['scheme_count']

        # Convert the DataFrame to HTML table
        html_table = result_df.to_html()


        counts = []

        # Fetch counts for different offers and append to the counts list
        if offerID == 'SSC2':
            result_ssc_count = db.session.execute(text('CALL GetSweetSummerOfferDistinctOutletCount();'))
            count = result_ssc_count.fetchone()[0]  
            result_ssc_count.close()
            counts.append(count)
        elif offerID == 'SPD1':
            result_wso_count = db.session.execute(text('CALL GetSpdOfferDetails()'))
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
            result_wso_count = db.session.execute(text('CALL GetEkSeBadhkarEkOfferSeason1()'))
            count = result_wso_count.fetchone()[0]
            result_wso_count.close()
            counts.append(count)
        elif offerID == 'NYD':
            result_wso_count = db.session.execute(text('CALL GetEkSeBadhkarEkOffer()'))
            count = result_wso_count.fetchone()[0]
            result_wso_count.close()
            counts.append(count)
        else:
            result_monsoon_count = db.session.execute(text('CALL GetMonsoonOfferDistinctOutletCount(); ;'))
            count = result_monsoon_count.fetchone()[0]
            result_monsoon_count.close()
            counts.append(count)
            print("ncountsnnnnnn",counts)

        sales_group_data = {}

        # Populate sales_group_data with sales groups and their Type ID counts
        for salesgroup in salesgroups:
            sales_data = result_df.loc[salesgroup].dropna()
            sales_group_data[salesgroup] = sales_data.sum()

        # Convert the sales_group_data dictionary to a DataFrame
        sales_group_df = pd.DataFrame.from_dict(sales_group_data, orient='index', columns=['Total_Type_ID_Count'])

        # Plotting a bar chart for Type ID counts across all sales groups
        plt.figure(figsize=(10, 6))
        plt.bar(sales_group_df.index, sales_group_df['Total_Type_ID_Count'])
        plt.xlabel('Sales Groups')
        plt.ylabel('Total Type ID Count')
        plt.title('Total Type ID Count Across Sales Groups')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot as an image
        plt.savefig('static/sales_groups_comparison_chart.png')



        return render_template('sweetsummer.html',counts=counts,dict_list_type=dict_list_type,dict_list=dict_list,html_table=html_table,unique_type_ids=unique_type_ids,salesgroups=salesgroups,offer_id=offer_id)

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
            # print("Type IDs:", type_ids)
        


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
       

        # Create an empty DataFrame with salesgroups as index and type_Ids as columns
        result_df = pd.DataFrame(index=payerId, columns=df['type_Id'])

        # Fill the result_df with scheme_count values
        for index, row in df.iterrows():
            result_df.loc[row['payerId'], row['type_Id']] = row['scheme_count']

        # print("----", result_df.to_dict())

        # Convert the DataFrame to HTML table
        html_table = result_df.to_html()
        
        
       
        return render_template('newsweetsummer.html',dict_list_type=dict_list_type,stokist_name_Id=stokist_name_Id,payerId=payerId,salesgroups=salesgroups,dict_list=dict_list,unique_type_ids=unique_type_ids,html_table=html_table,scheme_counts=scheme_count,offer_id=offer_id)

############################# same anthore payer funcation
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
            # payerId = df['payerId'].unique()
            scheme_count=df['scheme_count']
            unique_type = df2['type_Id'].unique()
            unique_beatname=df['beatname']
            unique_outlet_type_ids = df['outlet_type']
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
            
        
            return render_template('payerdata.html',unique_outletName=unique_outletName,unique_outlet_type_ids=unique_outlet_type_ids,unique_coupon_type=unique_coupon_type,outletId=outletId,dict_list_type=dict_list_type,unique_beatname=unique_beatname,dict_list=dict_list,unique_type=unique_type,html_table=html_table,scheme_counts=scheme_count,offer_id=offer_id)
        except KeyError as e:
                        error_message = f"KeyError: {str(e)} occurred."
                        return render_template('payerdata.html', error_message=error_message)

########################################## click on payerID releted data
@app.route('/offer_payer2/<payer2>/<int:pkey>') #@app.route('/offer/<payer>')
def PayerId1(payer,pkey):
        try:
        # print("offer/<payer_id>", request.args.get('offer_id', type=int))
            
            offer_id = request.args.get('offer_id', type=int)
            

            resultType=db.session.execute(text('CALL GetOfferCouponType('+str(pkey)+');'))
            datakey=resultType.keys()
            data=resultType.fetchall()
            resultType.close()
            dict_list_type=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]

            
            if offer_id == 1:
                result = db.session.execute(text(f"CALL GetNewSweetSummerOfferBypayerId('{payer}');"))

            elif offer_id == 2:
                result = db.session.execute(text(f"CALL GetSpdOfferDetailsBypayerId('{payer}');"))
            
            elif offer_id == 3:
                result = db.session.execute(text(f"CALL GetNewMonsoonOfferByPayerId('{payer}');"))

            elif offer_id == 4:
                result = db.session.execute(text(f"CALL GetNewWinterOfferBypayerId('{payer}');"))

            elif offer_id == 5:
                result = db.session.execute(text(f"CALL GetNewWinterOfferBypayerId('{payer}');"))

            elif offer_id== 6:
                 result = db.session.execute(text(f"CALL GetNewWinterOfferBypayerId('{payer}');"))
            else:
                 result = db.session.execute(text(f"CALL GetNewSweetSummerOfferBypayerId('{payer}');"))


        
            datakey = result.keys()
            data = result.fetchall()
            
            result.close()
            dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
            # dict_length=len(dict_list)

            df = pd.DataFrame(dict_list)
            df2=pd.DataFrame(dict_list_type)
            # print("df2",df)
           
            if 'outletId' in df.columns:
                outletId = df['outletId'].unique()
            else:
                outletId = []
            print("outletIdcccccccccccccccc",outletId)

            # outletId = df['outletId'].unique()
            scheme_count=df['scheme_count']
            unique_outlet_type_ids = df['outlet_type']
            unique_beatname=df['beatname']
            unique_outletName=df['outletName']
            unique_coupon_type = df['coupon_type'].unique()

            unique_typeId = df2['type_Id'].unique()
            print("unique_typessss",unique_typeId)
        

            # Create an empty DataFrame with salesgroups as index and type_Ids as columns
            result_df = pd.DataFrame(index=outletId, columns=df2['type_Id'])
            # result_df = pd.DataFrame(index=outletId, columns=df['coupon_type'])
            # print("Dddddsss",result_df)

            # Fill the result_df with scheme_count values
            for index, row in df.iterrows():
                result_df.loc[row['outletId'], row['type_Id']] = row['scheme_count']
                # result_df.loc[row['outletId'], row['coupon_type']] = row['scheme_count']

             # Convert the DataFrame to HTML table
            html_table = result_df.to_html()
           
          #unique_coupon_type=unique_coupon_type,
            # return render_template('payerIdshow.html',unique_typeId=unique_typeId,unique_coupon_type=unique_coupon_type,unique_outletName=unique_outletName,unique_beatname=unique_beatname,outletId=outletId,unique_outlet_type_ids=unique_outlet_type_ids,dict_list_type=dict_list_type,dict_list=dict_list,html_table=html_table,scheme_counts=scheme_count,offer_id=offer_id)
            return render_template('payerdata.html',unique_typeId=unique_typeId,unique_coupon_type=unique_coupon_type,unique_outletName=unique_outletName,unique_beatname=unique_beatname,outletId=outletId,scheme_counts=scheme_count,unique_outlet_type_ids=unique_outlet_type_ids,offer_id=offer_id,html_table=html_table,dict_list=dict_list)
        except KeyError as e:
                error_message = f"KeyError: {str(e)} occurred."
                return render_template('payerdata.html', error_message=error_message)
                # return render_template('payerIdshow.html', error_message=error_message)
        
        
# @app.route('/offer/EKS2')
# def EKS2():
#         result = db.session.execute(text('CALL SweetSummerOffer();'))
#         datakey = result.keys()
#         data = result.fetchall()
#         result.close()
#         dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

#         return render_template('monsoonoffer.html',dict_list=dict_list)




####################### Saledata per year month
@app.route('/saledata/<int:page>')
def saledata(page=1):
        # result = db.session.execute(text('CALL GetSalesDataPerYearPerMonth();'))
        # datakey = result.keys()
        # data = result.fetchall()
        # result.close()
        # dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
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

########### monsoonoffer 
@app.route('/offer/monsoonoffer')
def monsoonofferdata():
        result = db.session.execute(text('CALL MonsoonOffer();'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        return render_template('monsoonoffer.html',dict_list=dict_list)


@app.route('/api/monsoonoffer',methods=['GET'])
def monsoonoffer():
            try:
                result = db.session.execute(text('CALL MonsoonOffer();'))
                datakey = result.keys()
                data = result.fetchall()
                result.close()
                dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
                return jsonify({"code": 200, "status": True, "result": dict_list}), 200
            except Exception as e:
                return jsonify({"code": 400, "status": False, "error": str(e)}), 400





######################### menulist
@app.route('/api/GetWinterOfferByPayerId', methods=['GET'])
def menulist():
    try:
        result = db.session.execute(text(f"CALL GetEkSeBadhkarEkOfferSeason1ByPayerId('NIM001')"))   #GetMonsoonOfferByPayerId('SHR097')  GetEkSeBadhkarEkOfferSeason1
        # result = db.session.execute(text("CALL GetEkSeBadhkarEkOfferSeason1();"))
        # result =db.session.execute(text(f"CALL GetEkSeBadhkarEkOfferSeason1BySalesgroup('KHANDESH - 1');"))
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