import calendar
from sqlalchemy import text
# from decode import encrypt_message
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
from flask import render_template, request,session,make_response
import io
import base64
from flask_sqlalchemy import Pagination

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets
import string
import os
from datetime import datetime, timedelta
from werkzeug.exceptions import BadRequestKeyError
from functools import wraps




###################################### Sales data 

@app.route('/Newyear')
def Newyear():
    result = db.session.execute(text('CALL TotalNYDSalesGroupByoutletID();'))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
    
    return render_template('newyeardata.html', dict_list=dict_list)

   
# Define your static credentials
STATIC_USERNAME = "sapat"
STATIC_PASSWORD = "sapat@123"

# # Route to handle login requests
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Extract username and password from the form
#         username = request.form['username']
#         password = request.form['password']

#         # Check if the provided credentials match the static credentials
#         if username == STATIC_USERNAME and password == STATIC_PASSWORD:
#             # Authentication successful, redirect to a dashboard or home page
#             return redirect(url_for('Dashboard'))
#         else:
#             # Authentication failed, render login template with an error message
#             error = 'Invalid username or password. Please try again.'
#             return render_template('login.html', error=error)

#     # Render the login form template for GET requests
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Check if the provided credentials match the static credentials
        if username == STATIC_USERNAME and password == STATIC_PASSWORD:
            # Authentication successful, store username in session
            session['username'] = username
            
            return redirect(url_for('Dashboard'))
            # response = make_response(redirect(url_for('Dashboard')))
            # response.set_cookie('username', username)
            # response.set_cookie('password', password)
            # print("dddd",response.set_cookie('username', username))
            # print("dsssssdd",response)
            # return response
            
        else:
            # Authentication failed, render login template with an error message
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)

    # Render the login form template for GET requests
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
   
    # Redirect to the login page
    return redirect(url_for('login'))



def login_required(func):
    """
    Decorator function to restrict access to certain routes to logged-in users.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            # Redirect to the login page if user is not logged in
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/protected')
@login_required  # Apply the login decorator to this route
def protected_route():
    return 'This is a protected route, only accessible to logged-in users.'

@app.route('/employee_payerId1')
def employee_payerId1():
    result = db.session.execute(text('CALL GetEmployeeData();'))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

    return render_template('index.html', dict_list=dict_list)
# @app.route('/index')
# def newedmpoffer():

#         return render_template('index.html')

@app.route('/empdaa')
def newempoffer():
        result = db.session.execute(text('CALL GetEmployeeData();'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        return render_template('empmain.html',dict_list=dict_list) 




@app.route('/sales', methods=['GET', 'POST'])
def sales():
    global selected_date
    if request.method == 'GET':
        try:
            selected_date = request.args.get('selectedDate')

        except BadRequestKeyError:
            selected_date = "2023-12"
        if  selected_date is not None:
            

        # Parse the selected date string into a datetime object
            selected_datetime = datetime.strptime(selected_date, '%Y-%m')
    
            # Extract month and year
            selected_month = selected_datetime.month
            selected_year = selected_datetime.year

        else:
            # Default query for initial page load
            query = text('CALL GetSalesDataPerYearPerMonthUsingParameter(1, 2024);')
            result = db.session.execute(query)

        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
        # dict_list = []

        # # Use a server-side cursor to fetch data in chunks
        # while True:
        #     chunk = result.fetchmany(500)  # Adjust the chunk size as needed

        #     if not chunk:
        #         break
        #     dict_list.extend([{item: tup[i] for i, item in enumerate(datakey)} for tup in chunk])

        # result.close()

        return render_template('sales.html', dict_list=dict_list)



########### Closing stock #######################
# @app.route('/closingstockpayerid')
# def closingstockpayerid():
#     # payer_id = request.args.get('payerId')
#     result = db.session.execute(text(f"CALL GetDistinctPayersWithStokistName();"))
#     datakey = result.keys()
#     data = result.fetchall()
#     result.close()
#     dict_list  = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
#     return render_template('closingstockpayer.html',dict_list=dict_list)
    

@app.route('/closingsale')
def closingsale():
    date = request.args.get('date')

    if date:
        result = db.session.execute(text('CALL TotalClosingStockSummaryForEachSalesgroupUpdated(:date);').params(date=date))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
        

        result = db.session.execute(text('CALL TotalClosingStockSummaryAllSalesgroups(:date);').params(date=date))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list1 = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
        print("ddd",dict_list1)

        opening = [int(str(round(float(item['Opening'])))) for item in dict_list1]
        print("opening",opening)
        closing = [int(str(round(float(item['Closing'])))) for item in dict_list1]
        primary = [int(str(round(float(item['Primary_Stock'])))) for item in dict_list1]
        secondary = [int(str(round(float(item['Secondary'])))) for item in dict_list1]
    else:
        # If date is not provided, use today's date
        result = db.session.execute(text('CALL TotalClosingStockSummaryForEachSalesgroupUpdated("2024-01-31");'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        result = db.session.execute(text('CALL TotalClosingStockSummaryAllSalesgroups("2024-01-31");'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list1 = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        opening = dict_list1[0]['Opening'] if dict_list1 else None
        closing = dict_list1[0]['Closing'] if dict_list1 else None
        primary = dict_list1[0]['Primary_Stock'] if dict_list1 else None
        secondary = dict_list1[0]['Secondary'] if dict_list1 else None

        # opening = [int(str(round(float(item['Opening'])))) for item in dict_list1]
        # closing = [int(str(round(float(item['Closing'])))) for item in dict_list1]
        # primary = [int(str(round(float(item['Primary_Stock'])))) for item in dict_list1]
        # secondary = [int(str(round(float(item['Secondary'])))) for item in dict_list1]
   
    # result = db.session.execute(text('CALL TotalClosingStockSummaryForEachSalesgroup("2024-01-31");'))
    # datakey = result.keys()
    # data = result.fetchall()
    # result.close()
    # dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

    # # result = db.session.execute(text('CALL TotalClosingStockSummaryAllSalesgroups("2024-01-31");'))
    # datakey = result.keys()
    # data = result.fetchall()
    # result.close()
    # dict_list1 = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

    # opening = [int(str(round(float(item['Opening'])))) for item in dict_list1]
    # closing = [int(str(round(float(item['Closing'])))) for item in dict_list1]
    # primary = [int(str(round(float(item['Primary_Stock'])))) for item in dict_list1]
    # secondary = [int(str(round(float(item['Secondary'])))) for item in dict_list1]

    

    return render_template('salegruopcloging.html',date=date,secondary=secondary,primary=primary,closing=closing,opening=opening,dict_list=dict_list,dict_list1=dict_list1)

@app.route('/stocksales/<salesgroup>')
def stock_salesgroup(salesgroup):
        date = request.args.get('date')
        if date:
            result = db.session.execute(text('CALL GetPayerAndStokistBySalesgroupForClosingStockUpdated(:salesgroup, :date);').params(salesgroup=salesgroup, date=date))
        else:
            today = datetime.now()
            last_day_of_previous_month = today.replace(day=1) -timedelta(days=1)
            last_day_of_previous_month_str = last_day_of_previous_month.strftime("%Y-%m-%d")
            result = db.session.execute(text('CALL GetPayerAndStokistBySalesgroupForClosingStockUpdated(:salesgroup, :date);').params(salesgroup=salesgroup,date=last_day_of_previous_month_str))
        
        # Initialize dict_list outside of the if-else block with an empty list
        dict_list = []
        
        # Process the result data
        datakey=result.keys()
        data=result.fetchall()
        result.close()
        dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]

        salesgroups = dict_list[0]['salesgroup'] if dict_list else None

        return render_template('closingstockpayer.html',salesgroups=salesgroups,date=date,salesgroup=salesgroup,dict_list=dict_list)

# @app.route('/stocksales/<salesgroup>')
# def stock_salesgroup(salesgroup):
#     date = request.args.get('date')
#     if date:
#         result = db.session.execute(text('CALL GetPayerAndStokistBySalesgroupForClosingStockUpdated(:salesgroup, :date);').params(salesgroup=salesgroup, date=date))
#     else:
#         today = datetime.now()
#         last_day_of_previous_month = today.replace(day=1) -timedelta(days=1)
#         last_day_of_previous_month_str = last_day_of_previous_month.strftime("%Y-%m-%d")
#         result = db.session.execute(text('CALL GetPayerAndStokistBySalesgroupForClosingStockUpdated(:salesgroup, :date);').params(salesgroup=salesgroup,date=last_day_of_previous_month_str))
    
#     # Initialize dict_list outside of the if-else block with an empty list
#     dict_list = []
    
#     # Process the result data
#     datakey=result.keys()
#     data=result.fetchall()
#     result.close()
#     dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]

#     return render_template('closingstockpayer.html',salesgroup=salesgroup,dict_list=dict_list)

        
    


@app.route('/closingstockgrade/<payerId>')
def closingstockgrade(payerId):

    date = request.args.get('date') 
# this Skuid data
    if date:
        result = db.session.execute(text('CALL GetStockSummaryForPayerAndDateUpdated(:payerId, :date);').params(payerId=payerId, date=date))
    else:
        today = datetime.now()
        last_day_of_previous_month = today.replace(day=1) -timedelta(days=1)
        last_day_of_previous_month_str = last_day_of_previous_month.strftime("%Y-%m-%d")
        
        result = db.session.execute(text('CALL GetStockSummaryForPayerAndDateUpdated(:payerId, :date);').params(payerId=payerId, date=last_day_of_previous_month_str))
        # # today_date = "2024-01-31"
        # result = db.session.execute(text('CALL GetStockSummaryForPayerAndDateUpdated(:payerId, "2024-01-31");').params(payerId=payerId))
   
    datakey = result.keys()
    data = result.fetchall()
    result.close()

    dict_gradelist = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

   

    

# this grade code 
    if date:
        result = db.session.execute(text('CALL GetStockSummaryByGradeWithParamsUpdated(:payerId, :date);').params(payerId=payerId, date=date))
    else:
        today = datetime.now()
        last_day_of_previous_month = today.replace(day=1) -timedelta(days=1)
        last_day_of_previous_month_str = last_day_of_previous_month.strftime("%Y-%m-%d")
        
        result = db.session.execute(text('CALL GetStockSummaryByGradeWithParamsUpdated(:payerId, :date);').params(payerId=payerId, date=last_day_of_previous_month_str))
        # result = db.session.execute(text('CALL GetStockSummaryByGradeWithParamsUpdated(:payerId, "2024-01-31");').params(payerId=payerId))
   
    datakey = result.keys()
    data = result.fetchall()
    result.close()

    dict_list1 = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

#this sku id total related only
    if date:
        result = db.session.execute(text('CALL GetGrandTotalForStockSummaryForPayerAndDateUpdated(:payerId, :date);').params(payerId=payerId, date=date))
    else:
        today = datetime.now()
        last_day_of_previous_month = today.replace(day=1) -timedelta(days=1)
        last_day_of_previous_month_str = last_day_of_previous_month.strftime("%Y-%m-%d")
        
        result = db.session.execute(text('CALL GetGrandTotalForStockSummaryForPayerAndDateUpdated(:payerId, :date);').params(payerId=payerId, date=last_day_of_previous_month_str))
        # result = db.session.execute(text('CALL GetGrandTotalForStockSummaryForPayerAndDateUpdated(:payerId, "2024-01-31");').params(payerId=payerId))
    datakey = result.keys()
    data = result.fetchall()
    result.close()

    dict_total = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

    total_closingstock = dict_total[0]['Grand_Total_Closing'] if dict_total else None
    total_openingstock = dict_total[0]['Grand_Total_Opening'] if dict_total else None
    total_primarystock = dict_total[0]['Grand_Total_Primary_Stock'] if dict_total else None
    total_secondarystock= dict_total[0]['Grand_Total_Secondary'] if dict_total else None
    total_secondarytoatlsyock = dict_total[0]['Grand_Total_Secondary_Amount'] if dict_total else None

# grade total
    if date:
        result = db.session.execute(text('CALL GetGrandTotalForStockSummaryByGradeWithParamsUpdated(:payerId, :date);').params(payerId=payerId, date=date))
    else:
        today = datetime.now()
        last_day_of_previous_month = today.replace(day=1) -timedelta(days=1)
        last_day_of_previous_month_str = last_day_of_previous_month.strftime("%Y-%m-%d")
        
        result = db.session.execute(text('CALL GetGrandTotalForStockSummaryByGradeWithParamsUpdated(:payerId, :date);').params(payerId=payerId, date=last_day_of_previous_month_str))
        # result = db.session.execute(text('CALL GetStockSummaryByGradeWithParamsUpdated(:payerId, "2024-01-31");').params(payerId=payerId))
   
    datakey = result.keys()
    data = result.fetchall()
    result.close()

    dict_listgrade = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

    Grand_Total_Closing = dict_total[0]['Grand_Total_Closing'] if dict_total else None
    Grand_Total_Secondary = dict_total[0]['Grand_Total_Secondary'] if dict_total else None
    Grand_Total_Secondary_Amount = dict_total[0]['Grand_Total_Secondary_Amount'] if dict_total else None

    


    return render_template('closingstockgrade.html',data=date,Grand_Total_Secondary_Amount=Grand_Total_Secondary_Amount,Grand_Total_Secondary=Grand_Total_Secondary,Grand_Total_Closing=Grand_Total_Closing,dict_gradelist=dict_gradelist,total_secondarytoatlsyock=total_secondarytoatlsyock,total_secondarystock=total_secondarystock,total_primarystock=total_primarystock,total_openingstock=total_openingstock,total_closingstock=total_closingstock,dict_total=dict_total,date=date,payerId=payerId,dict_list1=dict_list1)




#################  Daily saledata
@app.route('/dailysalesgroup')
def dailysalesgroup():
    # payer_id = request.args.get('payerId')
    result = db.session.execute(text(f"CALL GetDistinctSalesgroup();"))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list  = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
    return render_template('dailysalesgroup.html',dict_list=dict_list)


@app.route('/dailysalesdata')
def dailysalesgroupdata():
  
    month = request.args.get('month')
    year = request.args.get('year')

    
    if month and year :
        result = db.session.execute(text('CALL GetSalesAndTargetDataBySalesgroup(:month, :year);').params(month=month,year=year))
    else:
        # result = db.session.execute(text('CALL GetTotalAchievementDataBySalesGroupUpdated(2, 24,:salesgroup);').params(salesgroup=salesgroup))
        result = db.session.execute(text('CALL GetSalesAndTargetDataBySalesgroup(:month, :year);').params( month=datetime.now().month, year=datetime.now().year))
  
    # if date:
    #     result = db.session.execute(text('CALL GetSalesAndTargetDataBySalesgroup(:date);').params(date=date))
    # else:
    #     # If date is not provided, use today's date
    #     today_date = "02-2024"
    #     result = db.session.execute(text('CALL GetSalesAndTargetDataBySalesgroup(:date);').params(date=today_date))
        
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list1  = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

    total_sale = sum(item['Sale'] for item in dict_list1)
    total_tgt_sale = sum(item['Target'] for item in dict_list1)
    



    result = db.session.execute(text(f"CALL GetDistinctSalesgroupWithPayerIdAndEmployeeCount();"))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list  = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

    total_tgt_emp = sum(item['employee_count'] for item in dict_list)
    Sum_of_payer = sum(item['payerId_count'] for item in dict_list)

    current_date = datetime.now()
    # Format the current date to get the month name
    current_month = current_date.strftime('%B')
    
    return render_template('dailysaledata.html',current_month=current_month,Sum_of_payer=Sum_of_payer,total_tgt_emp=total_tgt_emp,total_sale=total_sale,total_tgt_sale=total_tgt_sale,dict_list=dict_list,month=month,year=year,dict_list1=dict_list1)

    


@app.route('/dailysale/<salesgroup>')
def dailysales(salesgroup):
   
   


    from_month=request.args.get('from_month')
    from_year=request.args.get('from_year')
    end_month = request.args.get('end_month')
    end_year = request.args.get('end_year')

    if from_month and from_year and end_month and end_year:
       
        result = db.session.execute(text('CALL GetTotalAchievementDataBySalesGroupAsPerFinancialYearUpdated(:from_month,:from_year,:end_month, :end_year,:salesgroup);').params(salesgroup=salesgroup,from_month=from_month,from_year=from_year,end_year=end_year,end_month=end_month))
    else:
         result = db.session.execute(text('CALL GetTotalAchievementDataBySalesGroupAsPerFinancialYearUpdated(:from_month,:from_year,:end_month, :end_year,:salesgroup);').params(salesgroup=salesgroup, from_month=datetime.now().month, from_year=datetime.now().year,end_month=datetime.now().month,end_year=datetime.now().year))
       
# GetTotalAchievementDataBySalesGroupNewWithFromAndToMonthYear old 23-02-2024 
    
    # if month and year :
    #     result = db.session.execute(text('CALL GetTotalAchievementDataBySalesGroupUpdated(:month, :year,:salesgroup);').params(salesgroup=salesgroup,month=month,year=year))
    # else:
    #     # result = db.session.execute(text('CALL GetTotalAchievementDataBySalesGroupUpdated(2, 24,:salesgroup);').params(salesgroup=salesgroup))
    #     result = db.session.execute(text('CALL GetTotalAchievementDataBySalesGroupUpdated(:month, :year,:salesgroup);').params(salesgroup=salesgroup, month=datetime.now().month, year=datetime.now().year))
        
        
    
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

    total_tgt_sale = sum(item['Sum_of_Total_Target_Sale'] for item in dict_list)
    total_month_sale = sum(item['Sum_of_Total_Month_Sale'] for item in dict_list)
    total_tgt_gap = sum(item['Sum_of_Total_Target_Gap'] for item in dict_list)
    Sum_of_LY_Sales = sum(item['Sum_of_LY_Sales'] for item in dict_list)
    
    average_achievement_percentage = sum(item['Achievement_Percentage'] for item in dict_list) / len(dict_list) if dict_list else 0
    
    current_date = datetime.now()
    # Format the current date to get the month name
   
    # Pass the totals to the template
    # return render_template('dailysale.html', dict_list=dict_list, 
    #                     total_tgt_sale=total_tgt_sale, 
    #                     total_month_sale=total_month_sale,
    #                     total_tgt_gap=total_tgt_gap,salesgroup=salesgroup,Sum_of_LY_Sales=Sum_of_LY_Sales,month=month,year=year,
    #                     average_achievement_percentage=average_achievement_percentage)
    return render_template('dailypayerid.html', dict_list=dict_list,
                        total_tgt_sale=total_tgt_sale, 
                        total_month_sale=total_month_sale,
                        total_tgt_gap=total_tgt_gap,salesgroup=salesgroup,Sum_of_LY_Sales=Sum_of_LY_Sales,from_month=from_month,from_year=from_year,end_month=end_month,end_year=end_year,
                        average_achievement_percentage=average_achievement_percentage)          



@app.route('/targetsale/<payerId>')
def targetsales(payerId):

    from_month=request.args.get('from_month')
    from_year=request.args.get('from_year')
    end_month = request.args.get('end_month')
    end_year = request.args.get('end_year')

    if from_month and from_year and end_month and end_year:
        # GetAchievementDataByPayerIdNewWithFromAndToMonthYear
       
        result = db.session.execute(text('CALL GetAchievementDataByPayerIdNewWithFromAndToMonthYear(:from_month,:from_year,:end_month, :end_year,:payerId);').params(payerId=payerId,from_month=from_month,from_year=from_year,end_year=end_year,end_month=end_month))
    else:
         result = db.session.execute(text('CALL GetAchievementDataByPayerIdNewWithFromAndToMonthYear(:from_month,:from_year,:end_month, :end_year,:payerId);').params(payerId=payerId, from_month=datetime.now().month, from_year=datetime.now().year,end_month=datetime.now().month,end_year=datetime.now().year))



    # month = request.args.get('month')
    # year = request.args.get('year')
    
    # # print(month, year)
    # if month and year :
    #     result = db.session.execute(text('CALL GetAchievementDataByPayerIdNew(:month, :year,:payerId);').params(payerId=payerId,month=month,year=year))
    # else:
    #     # result = db.session.execute(text('CALL GetTotalAchievementDataBySalesGroupUpdated(2, 24,:salesgroup);').params(salesgroup=salesgroup))
    #     # result = db.session.execute(text('CALL GetAchievementDataByPayerIdNew(:month, :year,:payerId);').params(payerId=payerId, month=datetime.now().month, year=datetime.now().year))
  
    #     result = db.session.execute(text('CALL GetAchievementDataByPayerIdNew(2, 2024,:payerId);').params(payerId=payerId))
    # # result = db.session.execute(text('CALL GetAchievementDataByPayerIdNew(:month, :year,:payerId);').params(payerId=payerId,month=month,year=year))
    # # result = db.session.execute(text('CALL GetAchievementData(1, 2024);'))  
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
    # print("dict_list",dict_list)

   
    payer= [item['payerId'] for item in dict_list]
    # payerId = dict_list[0]['payerId']
    payerId = dict_list[0]['payerId'] if dict_list else None
    stokist_name = dict_list[0]['stokist_name'] if dict_list else None
   
    total_tgt_sale = sum(item['Total Target Sale'] for item in dict_list)
    total_month_sale = sum(item['Total Month Sale'] for item in dict_list)
    print("total_month_sale",total_month_sale)
    total_tgt_gap = sum(item['Target Gap'] for item in dict_list)
    LY_Sales = sum(item['LY_Sales'] for item in dict_list)
    print(LY_Sales)
    # average_achievement_percentage = sum(item['Achievement Percentage'] for item in dict_list) 
    average_achievement_percentage = sum(item['Achievement Percentage'] for item in dict_list) 


    # Pass the totals to the template
    # return render_template('targetsale.html', dict_list=dict_list, 
    #                     total_tgt_sale=total_tgt_sale, 
    #                     total_month_sale=total_month_sale,
    #                     total_tgt_gap=total_tgt_gap,LY_Sales=LY_Sales,month=month,year=year,
    #                     average_achievement_percentage=average_achievement_percentage)

    return render_template('dailyoutletid.html', dict_list=dict_list,payerId=payerId,stokist_name=stokist_name,
                            total_tgt_sale=total_tgt_sale, 
                            total_month_sale=total_month_sale,from_month=from_month,from_year=from_year,end_month=end_month,end_year=end_year,
                            total_tgt_gap=total_tgt_gap,LY_Sales=LY_Sales,
                            average_achievement_percentage=average_achievement_percentage)


@app.route('/api/GetSalesDataPerYearPerMonthUsingParameter', methods=['GET'])
def GetSalesDataPerYearPerMonthUsingParameter():
    try:
        result=db.session.execute(text('CALL GetSalesDataPerDateWithCreatedAtParameter("2024-01-01");'))
        datakey=result.keys()
        data=result.fetchall()
        result.close()
        dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("ddtat",dict_list)
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400

###################################### GetOfferCouponType
    
@app.route('/google')
def google():
    # result = db.session.execute(text('CALL GetLatestDailysalesUsingDate("20-01-2023");'))
    # datakey = result.keys()
    # data = result.fetchall()
    # result.close()
    # dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
  
    return render_template('googlemap.html')


@app.route('/getOfferCouponType')
def getOfferCouponTypedata():
    result = db.session.execute(text('CALL GetLatestDailysalesUsingDate("20-01-2023");'))
    datakey = result.keys()
    data = result.fetchall()
    result.close()
    dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
  
    return render_template('getOfferCouponType.html',dict_list=dict_list)
    


@app.route('/api/targetcoupn', methods=['GET'])  #GetTotalAchievementData(1, 2024)
def totaltarget():
    try:
        result=db.session.execute(text('CALL GetTotalAchievementDataBySalesGroupNewWithFromAndToMonthYearDemo(4, 2023, 2, 2024, "COASTAL");'))
        datakey=result.keys()
        data=result.fetchall()
        result.close()
        dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("ddtat",dict_list)
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400 



@app.route('/api/getOfferCouponType', methods=['GET'])
def getOfferCouponType():
    try:
        result=db.session.execute(text('CALL GetAchievementDataByPayerIdNew(12, 2023, "ABH003");'))
        datakey=result.keys()
        data=result.fetchall()
        result.close()
        dict_list=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("ddtat",dict_list)
        return jsonify({"code": 200, "status": True, "result": dict_list}), 200
    except Exception as e:
        return jsonify({"code": 400, "status": False, "error": str(e)}), 400 
    
################################ Dashboard 
@app.route('/dashboard')
def Dashboard():
    # Check if user is logged in
    if 'username' in session:


        result = db.session.execute(text('CALL GetStockSummaryForAllPayersAndLatestDateByGradeCode();'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]


        labels = [item['gradecode'] for item in dict_list]
        # closing_values = [int(item['Closing'] for item in dict_list)]
        # print("closing_values",closing_values)
        # opening_values = [item['Opening'] for item in dict_list]
        # primary_stock_values = [item['Primary_Stock'] for item in dict_list]
        closing_values = [int(item['Closing']) if item['Closing'] is not None else None for item in dict_list]
        Secondary_value =[int(item['Secondary']) if item['Secondary'] is not None else None for item in dict_list]
        # print("closing_values",closing_values)
        opening_values = [int(item['Opening']) if item['Opening'] is not None else None for item in dict_list]
        primary_stock_values = [int(item['Primary_Stock']) if item['Primary_Stock'] is not None else None for item in dict_list]



        Secondary = int(sum(value for value in Secondary_value if value is not None))

        # Calculate the total of Closing, Opening, and Primary_Stock values, handling None values and removing decimal points
        total_closing = int(sum(value for value in closing_values if value is not None))

        total_opening = int(sum(value for value in opening_values if value is not None))
        total_primary_stock = int(sum(value for value in primary_stock_values if value is not None))

        # closing  stock Report
        current_date = datetime.now()
        # Calculate the first day of the current month
        first_day_of_current_month = current_date.replace(day=1)
        # Calculate the last day of the previous month
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        # Extract year, month, and day for the last day of the previous month
        previous_year = last_day_of_previous_month.year
        previous_month = last_day_of_previous_month.month
        previous_day = last_day_of_previous_month.day

        # Construct the date string for the last day of the previous month
        previous_month_date = f"{previous_year}-{previous_month:02d}-{previous_day}"
        print("previous_month_date",previous_month_date)

        # Call the procedure with the dynamically obtained date for the last day of the previous month
        result = db.session.execute(text('CALL TotalClosingStockSummaryForEachSalesgroup(:previous_month_date)'), {'previous_month_date': previous_month_date})

        # result = db.session.execute(text('CALL TotalClosingStockSummaryForEachSalesgroup("2024-01-31");'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_stock = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        salesgroup_stock = [item['Salesgroup'] for item in dict_stock]
        closing_stock = [int(item['Closing']) if item['Closing'] is not None else None for item in dict_stock]
        Secondary_stock =[int(item['Secondary']) if item['Secondary'] is not None else None for item in dict_stock]
        opening_stock = [int(item['Opening']) if item['Opening'] is not None else None for item in dict_stock]
        primary_stock_stock = [int(item['Primary_Stock']) if item['Primary_Stock'] is not None else None for item in dict_stock]
        
        stock_closing = int(sum(value for value in closing_stock if value is not None))
        print("stock_closing",stock_closing)
        stock_secondary = int(sum(value for value in Secondary_stock if value is not None))
        stock_opening = int(sum(value for value in opening_stock if value is not None))
        print("stock_opening",stock_opening)
        stock_primary_stock = int(sum(value for value in primary_stock_stock if value is not None))
        print("stock_primary_stock",stock_primary_stock)







        result = db.session.execute(text('CALL OfferDetails();'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list1 = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        result_ssc = db.session.execute(text('CALL GetSweetSummerOfferDistinctOutletCount();'))
        result_spd = db.session.execute(text('CALL GetSpdOfferDistinctOutletCount();'))
        result_monsoon = db.session.execute(text('CALL GetMonsoonOfferDistinctOutletCount();'))
        result_winter = db.session.execute(text('CALL GetWinterOfferDistinctOutletCount();'))
        result_ek_se = db.session.execute(text('CALL GetEkSeBadhkarEkDistinctOutletCount();'))
        result_spd_details = db.session.execute(text('CALL GetSweetSummerOfferDistinctOutletCount();'))

        datakey = result_ssc.keys()
        datakey1 = result_spd.keys()
        datakey2 = result_monsoon.keys()
        datakey3 = result_winter.keys()
        datakey4 = result_ek_se.keys()
        datakey5 = result_spd_details.keys()
        # dict_list1 = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        # total_Opening = sum(item['Opening'] for item in dict_list)
        # total_Primary_Stock = sum(item['Primary_Stock'] for item in dict_list)
        # total_Closing = sum(item['Closing'] for item in dict_list)
        # total_Secondary = sum(item['Secondary'] for item in dict_list)

        # Fetch data keys and values for each result
        data_ssc = result_ssc.fetchall()
        data_spd = result_spd.fetchall()
        data_monsoon = result_monsoon.fetchall()
        data_winter = result_winter.fetchall()
        data_ek_se = result_ek_se.fetchall()
        data_spd_details = result_spd_details.fetchall()



        # Close the result sets
        result_ssc.close()
        result_spd.close()
        result_monsoon.close()
        result_winter.close()
        result_ek_se.close()
        result_spd_details.close()

        # Extract data count values for each offer, assuming 'count_value' is the column name
        ssc_count = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data_ssc]

        spd_count = [{item: tup[i] for i, item in enumerate(datakey1)} for tup in data_spd]
        monsoon_count = [{item: tup[i] for i, item in enumerate(datakey2)} for tup in data_monsoon]
        winter_count = [{item: tup[i] for i, item in enumerate(datakey3)} for tup in data_winter]
        ek_se_count = [{item: tup[i] for i, item in enumerate(datakey4)} for tup in data_ek_se]
        spd_details_count = [{item: tup[i] for i, item in enumerate(datakey5)} for tup in data_spd_details]

        ssc_count_data = ssc_count[0]['distinct_outlet_count'] if ssc_count else 0
        # print("ssc_count", ssc_count_data)
        spd_count_data = spd_count[0]['distinct_outlet_count'] if spd_count else 0
        monsoon_count_data = monsoon_count[0]['distinct_outlet_count'] if monsoon_count else 0
        winter_count_data = winter_count[0]['distinct_outlet_count'] if winter_count else 0
        ek_se_count_data = ek_se_count[0]['distinct_outlet_count'] if ek_se_count else 0
        spd_details_count_data = spd_details_count[0]['distinct_outlet_count'] if spd_details_count else 0

        total_count = (ssc_count_data +spd_count_data +monsoon_count_data +winter_count_data +ek_se_count_data +spd_details_count_data)
        # print("total_count",total_count)


        today_date = datetime.now().strftime("%Y-%m-%d")

        from_date = request.args.get('from_date') 
        to_date =request.args.get('to_date')

        if from_date and to_date:
            result = db.session.execute(text('CALL GetSalesAndTargetDataBySalesgroupUsingFromAndToDate( :from_date,:to_date);').params(from_date=from_date,to_date=to_date))
        else:
            # If date is not provided, use today's date
            # today_date = "2024-01-31"
            # result = db.session.execute(text('CALL GetStockSummaryForPayerAndDate(:payerId, :date);').params(date=today_date))
            result = db.session.execute(text('CALL GetSalesAndTargetDataBySalesgroupUsingFromAndToDate("2024-01-01","2024-02-01");'))
        # result = db.session.execute(text(f'CALL GetSalesAndTargetDataBySalesgroupUpdated("{today_date}");'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()

        saledate = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]


        salesgroup_daily = [item['salesgroup'] for item in saledate]
        sale_dailydata=[int(item['Sale']) for item in saledate]
        Target_data=[int(item['Target']) for item in saledate]




        # result=db.session.execute(text(f"CALL GetTotalMonthSaleAndTargetSaleForAllSalesgroup(2,2024)"))
        # # today_alldata = datetime.now().strftime("%Y-%m-%d")
        # # result = db.session.execute(text('CALL GetSalesAndTargetDataBySalesgroupUpdated("2024-02-01");'))
        # # result = db.session.execute(text(f'CALL GetTotalMonthSaleAndTargetSaleForAllSalesgroup("{today_alldata}");'))
        # datakey = result.keys()
        # data = result.fetchall()
        # result.close()
        # day_data = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        # month_saledata=[int(item['Month_Sale']) for item in day_data]
        # Target_Saledata=[int(item['Target_Sale']) for item in day_data]
        # print("s",month_saledata)
        # print("s",Target_Saledata)
        # Target_Saledata=Target_Saledata,month_saledata=month_saledata ,day_data=day_data,



        import dateutil.relativedelta as rl

        current_date = datetime.now()

        from_months = [current_date.replace(day=1).date()]
        to_months = [current_date.date()]
        for i in range(5):
            # Subtracting i months from the current date
            prev_month = current_date - timedelta(days=current_date.day)
            prev_month = prev_month.replace(day=1)  # Setting day to the 1st of the month
            from_months.append(prev_month.date())  # Format the date as month name and year
            to_months.append((prev_month.date() + rl.relativedelta(day=31)))  # Format the date as month name and year
            current_date = prev_month

        # print(from_months, to_months)

        links = []

        for i in range(0, len(from_months)):
            links.append(str(from_months[i]) + "*" + str(to_months[i]))


        # Annual data
        result = db.session.execute(text('CALL GetFinancialYearSalesReport();'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()

        final_result = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        Annual_Sales = int(final_result[0]['Annual_Sales'])
        Annual_Sales_LY = int(final_result[0]['Annual_Sales_LY']) 
        Annual_Target = int(final_result[0]['Annual_Target'])

            # Calculate the percentage achieved
        percentage_achieved = (Annual_Sales / Annual_Target) * 100
        percentage_achieved = round(percentage_achieved, 2)

        percentage_last_year = (Annual_Sales_LY / Annual_Sales) * 100

        percentage_last_year = round(percentage_last_year, 2)

        # e-Commerce month year 
        # result = db.session.execute(text('CALL GetTotalMonthSaleAndTargetSaleForAllSalesgroup(2,2024);'))
        # datakey = result.keys()
        # data = result.fetchall()
        # result.close()

        # month_result = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

        # Month_Sale = int(month_result[0]['Month_Sale']) 
        # Target_Sale = int(month_result[0]['Target_Sale'])

            
        #  current date
        current_date = datetime.now()
        # previous month
        previous_month = current_date - timedelta(days=current_date.day)
        #  month and year information
        current_month = current_date.strftime('%B')

        previous_month_name = previous_month.strftime('%B')

        year = current_date.year

        # Execute the procedure for the current month
        result_current_month = db.session.execute(text('CALL GetTotalMonthSaleAndTargetSaleForAllSalesgroup(:month, :year);'), {'month': current_date.month, 'year': year})
        datakey_current_month = result_current_month.keys()
        data_current_month = result_current_month.fetchall()
        result_current_month.close()

        # Execute the procedure for the previous month
        result_previous_month = db.session.execute(text('CALL GetTotalMonthSaleAndTargetSaleForAllSalesgroup(:month, :year);'), {'month': previous_month.month, 'year': year})
        datakey_previous_month = result_previous_month.keys()
        data_previous_month = result_previous_month.fetchall()
        result_previous_month.close()

        # Prepare data for current month
        month_result_current = [{item: tup[i] for i, item in enumerate(datakey_current_month)} for tup in data_current_month]
        Month_Sale_current = int(month_result_current[0]['Month_Sale'])
        Target_Sale_current = int(month_result_current[0]['Target_Sale'])

        # Prepare data for previous month
        month_result_previous = [{item: tup[i] for i, item in enumerate(datakey_previous_month)} for tup in data_previous_month]
        Month_Sale_previous = int(month_result_previous[0]['Month_Sale'])
        Target_Sale_previous = int(month_result_previous[0]['Target_Sale'])


        # target=[item['gradecode'] for item in saledate]
        # Pass all data to the template
        return render_template('dashboard.html',username=session['username'],Secondary=Secondary,percentage_achieved=percentage_achieved,percentage_last_year =percentage_last_year ,Target_Sale_previous=Target_Sale_previous,Month_Sale_previous=Month_Sale_previous,year=year,previous_month_name=previous_month_name,current_month=current_month,Target_Sale_current=Target_Sale_current,Month_Sale_current=Month_Sale_current,Annual_Target=Annual_Target,Annual_Sales_LY=Annual_Sales_LY,Annual_Sales=Annual_Sales,Target_data=Target_data,sale_dailydata=sale_dailydata,salesgroup_daily=salesgroup_daily,saledate=saledate,total_count=total_count,spd_details_count_data=spd_details_count_data,ek_se_count_data=ek_se_count_data,winter_count_data=winter_count_data,monsoon_count_data=monsoon_count_data,spd_count_data=spd_count_data,ssc_count_data=ssc_count_data,spd_details_count=spd_details_count,ek_se_count=ek_se_count,winter_count=winter_count,monsoon_count=monsoon_count,ssc_count=ssc_count,spd_count=spd_count,labels=labels, closing_values=closing_values,
                                opening_values=opening_values, primary_stock_values=primary_stock_values,
                                total_closing=total_closing, total_opening=total_opening,from_date=from_date,to_date=to_date,
                                total_primary_stock=total_primary_stock,dict_list1=dict_list1,ecommerce_analytics=links,selected_date=links[0],primary_stock_stock=primary_stock_stock,opening_stock=opening_stock,Secondary_stock=Secondary_stock,closing_stock=closing_stock,stock_closing=stock_closing,stock_secondary=stock_secondary,stock_opening=stock_opening,stock_primary_stock=stock_primary_stock,salesgroup_stock=salesgroup_stock)

    else:
        return redirect(url_for('login'))

   
    # Pass all data to the template
    # return render_template('dashboard.html',labels=labels, closing_values=closing_values,
    #                        opening_values=opening_values, primary_stock_values=primary_stock_values,
    #                        total_closing=total_closing, total_opening=total_opening,
    #                        total_primary_stock=total_primary_stock,dict_list1=dict_list1)
    

    # return render_template('dashboard.html', labels=labels, closing_values=closing_values,
    #                        opening_values=opening_values, primary_stock_values=primary_stock_values)
   
    # return render_template('dashboard.html',dict_list=dict_list)

@app.route('/get_Datedata', methods=['GET'])
def get_Datedata():
    try:
        from_date = request.args.get('from_date') 
        to_date =request.args.get('to_date')
    
        if from_date and to_date:
            result = db.session.execute(text('CALL GetSalesAndTargetDataBySalesgroupUsingFromAndToDate( :from_date,:to_date);').params(from_date=from_date,to_date=to_date))
        else:
            # If date is not provided, use today's date
            # today_date = "2024-01-31"
            # result = db.session.execute(text('CALL GetStockSummaryForPayerAndDate(:payerId, :date);').params(date=today_date))
            result = db.session.execute(text('CALL GetSalesAndTargetDataBySalesgroupUsingFromAndToDate("2024-01-01","2024-02-01");'))
        datakey = result.keys()
        data = result.fetchall()
        result.close()

        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

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

@app.route('/saleoffer')
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
    # print("Sscounts",counts)

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

    # return render_template('offerdetails.html',dict_list=dict_list,counts=counts,offer_ids=offer_ids)
    return render_template('offerscheme.html',offer_id=offer_id,dict_list=dict_list,counts=counts,offer_ids=offer_ids)

    

@app.route('/api/offerdetails', methods=['GET'])
def OfferDetails():
    try:
        result=db.session.execute(text('CALL GetSweetSummerOfferDistinctOutletCount();'))
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
        result=db.session.execute(text('CALL SweetSummerOffer();'))
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
        result=db.session.execute(text('CALL GetSalesDataPerYearPerMonthWithCreatedAt();'))
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

        # return render_template('employee_name.html',dict_list=dict_list)
        return render_template('empmain.html',dict_list=dict_list)


@app.route('/employee_info')
def employee_info():
    employee_id = request.args.get('empId')
    result = db.session.execute(text(f"CALL GetEmployeeInfoUpdated('{employee_id}');"))
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

    stokist_name = dict_list[0]['stokist_name'] if dict_list else None
    # return render_template('employeepayerId.html', dict_list=dict_list)
    return render_template('emp_payerid.html', dict_list=dict_list,stokist_name=stokist_name)


@app.route('/api/emp', methods=['GET'])
def employeelist():
    try:
        # result=db.session.execute(text(f"CALL GetEmployeeData()"))
        result=db.session.execute(text(f"CALL GetEmployeeInfoUpdated('S2284')"))      #text("CALL GetEmployeePayerInfo('S2284');"))
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

    

########### SweetSummerOffer  html template created only 
@app.route('/offer/<offerID>/<int:offer_id>')
def SSC2(offerID,offer_id):
    
    # print("/offer/<offerID>/<int:pkey>", request.args.get('offer_name', type=int))
        # offer_id = request.args.get('offer_name', type=int)
        # selected_date = request.args.get('selectedDate')
       

        resultType=db.session.execute(text('CALL GetOfferCouponType('+str(offer_id)+');'))
        datakey=resultType.keys()
        data=resultType.fetchall()
        resultType.close()
        dict_list_type=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("ddd",dict_list_type)


        # if offerID == "EKS2":
        #     resultType = db.session.execute(text('CALL GetOldOfferCoupenType();'))
        #     datakey = resultType.keys()
        #     data = resultType.fetchall()
        #     resultType.close()
        #     dict_list_type = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
        #     type_ids = [item['type_Id'] for item in dict_list_type]
    
            # print("Type IDs:", type_ids)SweetSummerOffer
        from_date = request.args.get('from_date') 
        to_date =request.args.get('to_date')
        current_date = datetime.now().date()
        print(current_date)
        if (offerID=='SSC2'):  
            
            # this Skuid data
            if from_date and to_date:
                result = db.session.execute(text('CALL SweetSummerOfferWithDateParams(:from_date,:to_date);').params(from_date=from_date,to_date=to_date))
            else:
                # result = db.session.execute(text('CALL SweetSummerOfferWithDateParams("2023-01-25",:current_date);').params(current_date=current_date,to_date=to_date))
                result = db.session.execute(text('CALL SweetSummerOffer();'))
        elif(offerID=="SPD1"):
            if from_date and to_date:
                result = db.session.execute(text('CALL GetSpdOfferDetailsWithDateParams(:from_date,:to_date);').params(from_date=from_date,to_date=to_date))
            else:
                result = db.session.execute(text('CALL GetSpdOfferDetails();'))          
        elif(offerID=='MO'):
            if from_date and to_date:
                result = db.session.execute(text('CALL MonsoonOfferWithDateParams(:from_date,:to_date);').params(from_date=from_date,to_date=to_date))
            else:
                result = db.session.execute(text('CALL MonsoonOffer();'))
        elif(offerID=='WSO'):
            if from_date and to_date:
                result = db.session.execute(text('CALL NewOfferWithDateParams(:from_date,:to_date);').params(from_date=from_date,to_date=to_date))
            else:
                result = db.session.execute(text('CALL NewOffer();')) 
        elif(offerID=="EKS2"):
            if from_date and to_date:
                result = db.session.execute(text('CALL GetEkSeBadhkarEkOfferSeason2WithDateParams(:from_date,:to_date);').params(from_date=from_date,to_date=to_date))
            else:
            # second GetEkSeBadhkarEkOfferSeason2 first is GetEkSeBadhkarEkOfferSeason1
                result = db.session.execute(text('CALL GetEkSeBadhkarEkOfferSeason2();'))
        elif(offerID=="NYD"):
            total_targetOffer=0
            total_total_multi_gift=0
            grouped_data=[]
            dict_NYDlist=[]


            if from_date and to_date:
                result = db.session.execute(text('CALL TotalNYDSalesGroupByoutletIDWithDateParams(:from_date,:to_date);').params(from_date=from_date,to_date=to_date))
            else:
                result = db.session.execute(text('CALL TotalNYDSalesGroupByoutletID();'))
                datakey = result.keys()
                data = result.fetchall()
                result.close()
                dict_NYDlist = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

                df = pd.DataFrame(dict_NYDlist)

                grouped_df = df.groupby('salesgroup').agg({'total_multi_gift': 'sum', 'targetOffer': 'sum'}).reset_index()

                grouped_data = grouped_df.to_dict(orient='records')

                # total_salesgroup = sum(item['salesgroup'] for item in grouped_data)
                total_total_multi_gift = sum(item['total_multi_gift'] for item in grouped_data)
                total_targetOffer = sum(item['targetOffer'] for item in grouped_data)
        

            return render_template('newyear.html',offerID=offerID,from_date=from_date,to_date=to_date,offer_id=offer_id,total_targetOffer=total_targetOffer,total_total_multi_gift=total_total_multi_gift,grouped_data=grouped_data,dict_NYDlist=dict_NYDlist)
        else:
            result = db.session.execute(text('CALL MonsoonOffer();'))

        datakey = result.keys()
        data = result.fetchall()
        result.close()
        dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
        # print("sss",dict_list)
        
        df = pd.DataFrame(dict_list)
        df2=pd.DataFrame(dict_list_type)
        print(df)

        sales_group_data = {}
        salesgroups=[]
        counts = []
        unique_type_ids = []
        df_day=None
        df_year=None
        df_month=None
        html_table=""
        # Extract year and month into new columns
        if len(df) > 0:
            if 'created_at' in df.columns and 'type_Id' in df.columns:
                df_year= df['created_at'].dt.year
                df_month= df['created_at'].dt.month
                df_day =df['created_at'].dt.day
                # print("df_day",df_day)

                # from_date = request.args.get('startDate')
                # selected_end_date = request.args.get('endDate')

                if from_date and to_date:
                    # Filter the DataFrame based on the selected date range
                    df = df[(df['created_at'].dt.date >= pd.to_datetime(from_date).date()) & 
                            (df['created_at'].dt.date <= pd.to_datetime(to_date).date())]
                
                
                salesgroups = df['salesgroup'].unique()
                unique_type_ids = df2['type_Id'].unique()
                # total_scheme_count= df['total_scheme_count'].unique()
                
                new_columns = list(unique_type_ids) + ['sum']

                
                # Create an empty DataFrame with salesgroups as index and type_Ids as columns df['type_Id']+["sum"]
                result_df = pd.DataFrame(index=salesgroups, columns=new_columns)


                # Fill the result_df with scheme_count values
                for index, row in df.iterrows():
                    result_df.loc[row['salesgroup'], row['type_Id']] = row['scheme_count']
                    result_df.loc[row['salesgroup'],"sum"]= result_df.loc[row['salesgroup'], "sum"] + row['scheme_count']
                    
                    result_df['sum'] = result_df['sum'].fillna(0)
                # print(result_df)

                # Convert the DataFrame to HTML table
                html_table = result_df.to_html()
                # print("html_table",html_table)


                # counts = []

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

                # sales_group_data = {}

                # Populate sales_group_data with sales groups and their Type ID counts
                for salesgroup in salesgroups:
                    sales_data = result_df.loc[salesgroup].dropna()
                    sales_group_data[salesgroup] = sales_data.unique().sum() 

                


                # return render_template('sweetsummer.html',selected_end_date=selected_end_date,selected_start_date=selected_start_date,df_day=df_day,offerID=offerID,df_month=df_month,df_year=df_year,sales_group_data=sales_group_data,counts=counts,dict_list_type=dict_list_type,dict_list=dict_list,html_table=html_table,unique_type_ids=unique_type_ids,salesgroups=salesgroups,offer_id=offer_id)
                # return render_template('salegroupdata.html',from_date=from_date,to_date=to_date,selected_end_date=selected_end_date,selected_start_date=selected_start_date,df_day=df_day,offerID=offerID,df_month=df_month,df_year=df_year,sales_group_data=sales_group_data,counts=counts,dict_list_type=dict_list_type,dict_list=dict_list,html_table=html_table,unique_type_ids=unique_type_ids,salesgroups=salesgroups,offer_id=offer_id)
            else:
                salesgroups = df['salesgroup'].unique()
                unique_type_ids = df2['type_Id'].unique()
                
                result_df = pd.DataFrame(index=salesgroups, columns=df['type_Id'])

                for index, row in df.iterrows():
                    result_df.loc[row['salesgroup'], row['type_Id']] = row['scheme_count']
                    
                html_table = result_df.to_html()
            
                

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

                

                for salesgroup in salesgroups:
                    sales_data = result_df.loc[salesgroup].dropna()
                    sales_group_data[salesgroup] = sales_data.unique().sum() 
                    # print(sales_group_data[salesgroup])
                    # print("SSwww",sales_group_data)


            

            # Render the template without the HTML table
            # return render_template('sweetsummer.html', sales_group_data=sales_group_data, counts=counts, dict_list_type=dict_list_type, dict_list=dict_list, unique_type_ids=unique_type_ids, salesgroups=salesgroups, offer_id=offer_id)
        # return render_template('salegroupdata.html',sales_group_data=sales_group_data, counts=counts, dict_list_type=dict_list_type, dict_list=dict_list, unique_type_ids=unique_type_ids, salesgroups=salesgroups, offer_id=offer_id)
        return render_template('salegroupdata.html',from_date=from_date,to_date=to_date,df_day=df_day,offerID=offerID,df_month=df_month,df_year=df_year,sales_group_data=sales_group_data,counts=counts,dict_list_type=dict_list_type,dict_list=dict_list,html_table=html_table,unique_type_ids=unique_type_ids,salesgroups=salesgroups,offer_id=offer_id)

######################################### click on salesgroup regarding 
@app.route('/offer_details/<salesgroup>/<int:offer_id>')
def salesgroup(salesgroup,offer_id):
        # print("/offer/<offerID>/<string:pkey>", request.args.get('salesgroup', type=int))
        # print("/offer_details/<salesgroup>/<int:pkey>", request.args.get('offer_name', type=int))
        # offer_id = request.args.get('offer_id', type=int)
        # print("ss",offer_id)

        resultType=db.session.execute(text('CALL GetOfferCouponType('+str(offer_id)+');'))
        datakey=resultType.keys()
        data=resultType.fetchall()
        resultType.close()
        dict_list_type=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
        # print("Ss",dict_list_type)

        # if offer_id == 5:
        #     resultType = db.session.execute(text('CALL GetOldOfferCoupenType();'))
        #     datakey = resultType.keys()
        #     data = resultType.fetchall()
        #     resultType.close()
        #     dict_list_type = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
        #     type_ids = [item['type_Id'] for item in dict_list_type]
        #     print("Type IDs:", type_ids)
    
        
       
        
        from_date = request.args.get('from_date') 
        to_date =request.args.get('to_date')
        
        if offer_id == 1:
            if from_date and to_date:
                result = db.session.execute(text('CALL GetSalesgroupDataSummerOfferWithDateParams(:salesgroup,:from_date,:to_date);').params(salesgroup=salesgroup,from_date=from_date,to_date=to_date))
            else:
                result = db.session.execute(text(f"CALL GetSalesgroupDataSummerOffer('{salesgroup}');"))

        elif offer_id == 2:
            if from_date and to_date:
                result = db.session.execute(text('CALL GetSpdOfferDetailsBySalesgroupWithDateParams(:salesgroup,:from_date,:to_date);').params(salesgroup=salesgroup,from_date=from_date,to_date=to_date))
            else:
                result = db.session.execute(text(f"CALL GetSpdOfferDetailsBySalesgroup('{salesgroup}');"))

        elif offer_id == 3:
            if from_date and to_date:
                result = db.session.execute(text('CALL GetSalesgroupDataMonsoonOfferWithDateParams(:salesgroup,:from_date,:to_date);').params(salesgroup=salesgroup,from_date=from_date,to_date=to_date))
            else:
                result = db.session.execute(text(f"CALL GetSalesgroupDataMonsoonOffer('{salesgroup}');"))

        elif offer_id == 4:
            if from_date and to_date:
                result = db.session.execute(text('CALL GetWinterSalesgroupDataWithDateParams(:salesgroup,:from_date,:to_date);').params(salesgroup=salesgroup,from_date=from_date,to_date=to_date))
            else:
                result = db.session.execute(text(f"CALL GetSalesgroupData('{salesgroup}');"))

        elif offer_id == 5:
            if from_date and to_date:
                result = db.session.execute(text('CALL GetEkSeBadhkarEkOfferSeason2BySalesgroupWithDateParams(:salesgroup,:from_date,:to_date);').params(salesgroup=salesgroup,from_date=from_date,to_date=to_date))
            else:
            # GetEkSeBadhkarEkOfferSeason1BySalesgroup first apply
                result = db.session.execute(text(f"CALL GetEkSeBadhkarEkOfferSeason2BySalesgroup('{salesgroup}');"))

        elif offer_id == 6:
            from_date = request.args.get('from_date') 
            to_date =request.args.get('to_date')        
            total_targetOffer=0
            total_total_multi_gift=0
            grouped_data=[]
            dict_NYDlist=[]
            if from_date and to_date:
                result = db.session.execute(text('CALL TotalNYDSalesGroupByoutletIDUsingSalesgroupParamAndDate(:salesgroup,:from_date,:to_date);').params(salesgroup=salesgroup,from_date=from_date,to_date=to_date))
                # print("dddsssssss",result)
                datakey = result.keys()
                data = result.fetchall()
                result.close()
                dict_NYDlist = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

                df = pd.DataFrame(dict_NYDlist)
                
                grouped_df = df.groupby(['payerId','salesgroup','beatname', 'stokist_name']).agg({'total_multi_gift': 'sum', 'targetOffer': 'sum'}).reset_index()
                unique_payer_df =df.groupby('payerId').first().reset_index()
                grouped_data = unique_payer_df.to_dict(orient='records')

                # grouped_df = df.groupby('payerId').agg({'total_multi_gift': 'sum', 'targetOffer': 'sum'}).reset_index()

                # grouped_data = grouped_df.to_dict(orient='records')

                total_total_multi_gift = unique_payer_df['total_multi_gift'].sum()
                total_targetOffer = unique_payer_df['targetOffer'].sum()
            else:
           
                result = db.session.execute(text(f"CALL TotalNYDSalesGroupByoutletIDUsingSalesgroupParamUpdated('{salesgroup}');"))
                print("ddd",result)
                datakey = result.keys()
                data = result.fetchall()
                result.close()
                dict_NYDlist = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]

                df = pd.DataFrame(dict_NYDlist)
                
                grouped_df = df.groupby(['payerId','salesgroup','beatname', 'stokist_name']).agg({'total_multi_gift': 'sum', 'targetOffer': 'sum'}).reset_index()
                unique_payer_df =df.groupby('payerId').first().reset_index()
                grouped_data = unique_payer_df.to_dict(orient='records')

                # grouped_df = df.groupby('payerId').agg({'total_multi_gift': 'sum', 'targetOffer': 'sum'}).reset_index()

                # grouped_data = grouped_df.to_dict(orient='records')

                total_total_multi_gift = unique_payer_df['total_multi_gift'].sum()
                total_targetOffer = unique_payer_df['targetOffer'].sum()
            # print(grouped_data)
            return render_template('newyearsalegruop.html',salesgroup=salesgroup,to_date=to_date,from_date=from_date,total_targetOffer=total_targetOffer,total_total_multi_gift=total_total_multi_gift,grouped_data=grouped_data,offer_id=offer_id,dict_NYDlist=dict_NYDlist)
        
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
        salesgroups=[]
        payerId=[]
        scheme_count=[]
        unique_type_ids=[]
        stokist_name_Id=[]
        payerid_data={}
        html_table=""


        if len(df) > 0:

            salesgroups = df['salesgroup'].unique()
            payerId = df['payerId'].unique()
            scheme_count=df['scheme_count']
            unique_type_ids = df2['type_Id'].unique()
            stokist_name_Id=df['stokist_name'].unique()

            # unique_type_ids = df2['type_Id'].unique()
            # Get the selected month and year from the request parameters

            new_columns = list(unique_type_ids) + ['sum']
            result_df = pd.DataFrame(index=payerId, columns=new_columns)
            for index, row in df.iterrows():
                result_df.loc[row['payerId'], row['type_Id']] = row['scheme_count']
                result_df.loc[row['payerId'],"sum"]= result_df.loc[row['payerId'], "sum"] + row['scheme_count']
                
                result_df['sum'] = result_df['sum'].fillna(0)    



            # Create an empty DataFrame with salesgroups as index and type_Ids as columns
                # first code 
            # result_df = pd.DataFrame(index=payerId, columns=df['type_Id'])

            # Fill the result_df with scheme_count values
            # for index, row in df.iterrows():
            #     result_df.loc[row['payerId'], row['type_Id']] = row['scheme_count']


            
        

            # Convert the DataFrame to HTML table
            html_table = result_df.to_html()
        
            payerid_data = {}

            for payer in payerId:
                sales_data = result_df.loc[payer].dropna()
                payerid_data[payer] = sales_data.unique().sum() 
                # print("payerid_data",payerid_data)
            
        
        # return render_template('newsweetsummer.html',dict_list_type=dict_list_type,stokist_name_Id=stokist_name_Id,payerId=payerId,salesgroups=salesgroups,dict_list=dict_list,unique_type_ids=unique_type_ids,html_table=html_table,scheme_counts=scheme_count,offer_id=offer_id)
        return render_template('salegrouppayerid.html',salesgroup=salesgroup,from_date=from_date,to_date=to_date,payerid_data=payerid_data,dict_list_type=dict_list_type,stokist_name_Id=stokist_name_Id,payerId=payerId,salesgroups=salesgroups,dict_list=dict_list,unique_type_ids=unique_type_ids,html_table=html_table,scheme_counts=scheme_count,offer_id=offer_id)

########################################## click on payerID releted data
@app.route('/offer_payer/<payer>/<int:offer_id>')
def PayerId(payer,offer_id):
        try:
            # print("/offer/<offerID>/<string:pkey>", request.args.get('salesgroup', type=int))
            # print("/offer_details/<salesgroup>/<int:pkey>", request.args.get('offer_name', type=int))
            # offer_id = request.args.get('offer_id', type=int)
            # print("ss",offer_id)

            resultType=db.session.execute(text('CALL GetOfferCouponType('+str(offer_id)+');'))
            datakey=resultType.keys()
            data=resultType.fetchall()
            resultType.close()
            dict_list_type=[{item:tup[i] for i,item in enumerate(datakey)}for tup in data]
            # print("Ss",dict_list_type)

            # if offer_id == 5:
            #     resultType = db.session.execute(text('CALL GetOldOfferCoupenType();'))
            #     datakey = resultType.keys()
            #     data = resultType.fetchall()
            #     resultType.close()
            #     dict_list_type = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
            #     type_ids = [item['type_Id'] for item in dict_list_type]
                # print("Type IDs:", type_ids)
            


            from_date = request.args.get('from_date') 
            to_date =request.args.get('to_date')
        
            if offer_id == 1:
                if from_date and to_date:
                    result = db.session.execute(text('CALL GetNewSweetSummerOfferBypayerIdWithDateParams(:payer,:from_date,:to_date);').params(payer=payer,from_date=from_date,to_date=to_date))
                else:
                    result = db.session.execute(text(f"CALL GetNewSweetSummerOfferBypayerId('{payer}');"))

            elif offer_id == 2:
                if from_date and to_date:
                    result = db.session.execute(text('CALL GetSpdOfferDetailsBypayerIdWithDateParams(:payer,:from_date,:to_date);').params(payer=payer,from_date=from_date,to_date=to_date))
                else:
                    result = db.session.execute(text(f"CALL GetSpdOfferDetailsBypayerId('{payer}');"))
            
            elif offer_id == 3:
                if from_date and to_date:
                    result = db.session.execute(text('CALL GetMonsoonOfferByPayerIdWithDateParams(:payer,:from_date,:to_date);').params(payer=payer,from_date=from_date,to_date=to_date))
                else:
                    result = db.session.execute(text(f"CALL GetNewMonsoonOfferByPayerId('{payer}');"))

            elif offer_id == 4:
                if from_date and to_date:
                    result = db.session.execute(text('CALL GetWinterOfferBypayerIdWithDateParams(:payer,:from_date,:to_date);').params(payer=payer,from_date=from_date,to_date=to_date))
                else:
                    result = db.session.execute(text(f"CALL GetNewWinterOfferBypayerId('{payer}');"))

            elif offer_id == 5:
                if from_date and to_date:
                    result = db.session.execute(text('CALL GetEkSeBadhkarEkOfferSeason2ByPayerIdWithDateParams(:payer,:from_date,:to_date);').params(payer=payer,from_date=from_date,to_date=to_date))
                else:
                #  GetEkSeBadhkarEkOfferSeason1ByPayerId first apply
                    result = db.session.execute(text(f"CALL GetEkSeBadhkarEkOfferSeason2ByPayerId('{payer}');"))

            elif offer_id== 6:
                from_date = request.args.get('from_date') 
                to_date =request.args.get('to_date')        
                total_target_offer=0
                total_total_multi_gift=0
                
                dict_NYDlist=[]
                if from_date and to_date:
                    result = db.session.execute(text('CALL TotalNYDSalesGroupByoutletIDUsingPayerAndDate(:payer,:from_date,:to_date);').params(payer=payer,from_date=from_date,to_date=to_date))
                    datakey = result.keys()
                    data = result.fetchall()
                    result.close()
                    dict_NYDlist = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
                    df = pd.DataFrame(dict_NYDlist)

                    # Calculate the sum of total_multi_gift and targetOffer
                    total_total_multi_gift = df['total_multi_gift'].sum()
                    total_target_offer = df['targetOffer'].sum()

                else:

                    result = db.session.execute(text(f"CALL TotalNYDSalesGroupByoutletIDUsingPayerId('{payer}');"))
                    # result = db.session.execute(text(f"CALL TotalNYDSalesGroupByoutletIDUsingSalesgroupParam('{salesgroup}');"))
                    datakey = result.keys()
                    data = result.fetchall()
                    result.close()
                    dict_NYDlist = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
                    df = pd.DataFrame(dict_NYDlist)

                    # Calculate the sum of total_multi_gift and targetOffer
                    total_total_multi_gift = df['total_multi_gift'].sum()
                    total_target_offer = df['targetOffer'].sum()

                    
                return render_template('newyearpayerid.html',payer=payer,total_target_offer=total_target_offer,total_total_multi_gift=total_total_multi_gift,offer_id=offer_id,dict_NYDlist=dict_NYDlist)

            else:
                result = db.session.execute(text(f"CALL GetNewSweetSummerOfferBypayerId('{payer}');"))



            datakey = result.keys()
            data = result.fetchall()
            result.close()
            dict_list = [{item: tup[i] for i, item in enumerate(datakey)} for tup in data]
            # print("dict_list",dict_list)

            df = pd.DataFrame(dict_list)
            df2=pd.DataFrame(dict_list_type)

            
            outletId = []
            unique_type=[]
            html_table=""
            unique_beatname=[]
            unique_outletName=[]
            unique_coupon_type=[]
            scheme_count=[]

            if len(df) > 0:

                if 'outletId' in df.columns:
                    outletId = df['outletId'].unique()
                else:
                    outletId = []
            
                scheme_count=df['scheme_count']
                unique_type = df2['type_Id'].unique()
                unique_beatname=df['beatname']
                # unique_outlet_type_ids = df['outlet_type']
                unique_outletName=df['outletName']
                unique_coupon_type = df['coupon_type'].unique()

                new_columns = list(unique_coupon_type) + ['sum']
                result_df = pd.DataFrame(index=outletId, columns=new_columns)
                for index, row in df.iterrows():
                    result_df.loc[row['outletId'], row['coupon_type']] = row['scheme_count']
                    result_df.loc[row['outletId'],"sum"]= result_df.loc[row['outletId'], "sum"] + row['scheme_count']
                    
                    result_df['sum'] = result_df['sum'].fillna(0)    
            
                
            

                # Create an empty DataFrame with salesgroups as index and type_Ids as columns
                    # first code 
                # result_df = pd.DataFrame(index=outletId, columns=df2['type_Id'])

                # # Fill the result_df with scheme_count values
                # for index, row in df.iterrows():
                #     result_df.loc[row['outletId'], row['coupon_type']] = row['scheme_count']

            
                # Convert the DataFrame to HTML table
                html_table = result_df.to_html()
                
            
            #     return render_template('payerdata.html',unique_outletName=unique_outletName,unique_coupon_type=unique_coupon_type,outletId=outletId,dict_list_type=dict_list_type,unique_beatname=unique_beatname,dict_list=dict_list,unique_type=unique_type,html_table=html_table,scheme_counts=scheme_count,offer_id=offer_id)
            # except KeyError as e:
            #                 error_message = f"KeyError: {str(e)} occurred."
            #                 return render_template('payerdata.html', error_message=error_message)
            return render_template('salegroupoutlet.html',payer=payer,unique_outletName=unique_outletName,unique_coupon_type=unique_coupon_type,outletId=outletId,dict_list_type=dict_list_type,unique_beatname=unique_beatname,dict_list=dict_list,unique_type=unique_type,html_table=html_table,scheme_counts=scheme_count,offer_id=offer_id)
        except KeyError as e:
                        error_message = f"KeyError: {str(e)} occurred."
                        return render_template('salegroupoutlet.html', error_message=error_message)



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
        # result=db.session.execute(text(f"CALL GetEkSeBadhkarEkOfferSeason2ByPayerId('NIM001')"))
        # result=db.session.execute(text(f"CALL GetGrandTotalForStockSummaryByGradeWithParamsUpdated('HAJ002','2024-01-31')"))
        result=db.session.execute(text(f"CALL TotalClosingStockSummaryAllSalesgroups('2023-11-30')"))
        # result = db.session.execute(text('CALL GetPayerAndStokistBySalesgroupForClosingStockUpdated("KHANDESH - 1","2024-01-31");'))
        # result=db.session.execute(text(f"CALL GetPayerAndStokistBySalesgroupForClosingStock('KHANDESH - 1')"))
        # result=db.session.execute(text(f"CALL GetTotalAchievementDataAsPerFinancialYearGradeCodeUpdated(2, 2024, 2, 2024, 'ABH003')"))
        # CALL GetTotalAchievementDataBySalesGroupAsPerFinancialYearUpdated(12, 2023, 2, 2024, 'KHANDESH - 1');
        # result=db.session.execute(text(f"CALL GetTotalMonthSaleAndTargetSaleForAllSalesgroup(1,2024)"))   
        # result=db.session.execute(text(f"CALL MonsoonOfferWithDateParams('2023-06-1','2024-1-30')"))
        # result=db.session.execute(text(f"CALL GetTotalMonthSaleAndTargetSaleForAllSalesgroup(1,2024)"))
        # result=db.session.execute(text(f"CALL GetTotalAchievementDataBySalesGroupNew(7, 2023, 8, 2023, 'COASTAL')"))
        # result = db.session.execute(text(f"CALL  GetTotalAchievementDataAsPerFinancialYearGradeCodeUpdated('2024-02-01')))
        # result=db.session.execute(text(f"CALL TotalNYDSalesGroupByoutletIDUsingSalesgroupParamAndDate('MARATHWADA - 1','2024-01-01','2024-02-10')"))
        # result = db.session.execute(text(f"CALL  GetStockSummaryByGradeWithParams('ABH003', '2024-01-31')"))
        # result = db.session.execute(text(f"CALL  GetSalesAndTargetDataBySalesgroup(2, 2024)"))
        # result = db.session.execute(text(f"CALL GetDistinctSalesgroupWithPayerIdAndEmployeeCount()"))
        # result = db.session.execute(text(f"CALL GetEmployeeInfo('S2358')"))   #GetMonsoonOfferByPayerId('SHR097')  GetEkSeBadhkarEkOfferSeason1
        # result = db.session.execute(text("CALL TotalNYDSalesGroupByoutletID();"))
        # result =db.session.execute(text(f"CALL GetEmployeeInfoBypayerId('HAN001');"))
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
    





