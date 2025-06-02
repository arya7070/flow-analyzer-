# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 11:18:51 2025

@author: arya
"""
import os
import copy
import csv
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import datetime, timedelta
def Update_discount(flow):#['12/19 1:57 pm','TSLA','SWEEP','PUT','Bear','255.00','12/22','185k','500@3.70AA',10,'-22.0%']
    time.sleep(1)
    print((flow))
    print((flow[-5]))
    date_string =flow[-5]

# Convert to datetime object
    date_object = datetime.strptime(date_string, "%m/%d/%Y")

# Format the datetime object as a string with the desired format
    formatted_date = date_object.strftime("%Y-%m-%d")
    #flow[-5]=formatted_date 
    print((flow[-5]))
    print(flow[1])
    response = requests.get('https://api.tradier.com/v1/markets/options/chains',
        params={'symbol': flow[1], 'expiration': formatted_date , 'greeks': 'true'},
        headers={'Authorization': '', 'Accept': 'application/json'}
    )
    if response.status_code == 200:
        data = response.json()
        #print( data)
        if data['options'] is  None:
            return "?"
        betachain = data['options']['option']
        # Do something with the options chain data
    else:
        print(f'Error: {response.status_code} - {response.text}')
        print("fuck")
        return "?"

    # Specify the target strike price you're looking for
    target_strike_price = flow[-6][0:-1]  # Replace this with the desired strike price

    # Iterate through the options in betachain to find the one with the target strike price
    matching_option = "none"

    for option in betachain:
        if float(option['strike']) == float(target_strike_price) and option['option_type']==flow[3].lower():
            matching_option = option
            break  # Exit the loop once a match is found
    if (matching_option)=="none":
        return "?"
    # Split the string based on '@'
    parts = flow[-3].split('@')

    # Extract the number after '@' (assuming it's the second part)
    number_after_at = parts[1].strip()
    currentprice=str(((((((matching_option["bid"]+matching_option["ask"])/2)*100))/float(number_after_at))//1)-100)
    print((matching_option["bid"]+matching_option["ask"])/2)    
    print(number_after_at)
    print(currentprice)
    if float(currentprice)>0:
        return "+"+currentprice+"%"
def discount(flow): #takes insomething like ['12/19 9:37 am', 'SMCI', 'SWEEP', 'CALL', 'bull', '0.8', '280.00', '12/29/2023', '261100.0', '70 @ 37.30', 10, 'At Ask']
    time.sleep(1)
    #print((flow))
    #print((flow[-5]))
    date_string =flow[-5]

# Convert to datetime object
    date_object = datetime.strptime(date_string, "%m/%d/%Y")

# Format the datetime object as a string with the desired format
    formatted_date = date_object.strftime("%Y-%m-%d")
    #flow[-5]=formatted_date 
    #print((flow[-5]))
    #print(flow[1])
    response = requests.get('https://api.tradier.com/v1/markets/options/chains',
        params={'symbol': flow[1], 'expiration': formatted_date , 'greeks': 'true'},
        headers={'Authorization': '', 'Accept': 'application/json'}
    )
    if response.status_code == 200:
        data = response.json()
        #print( data)
        if data['options'] is  None:
            return "?"
        betachain = data['options']['option']
        # Do something with the options chain data
    else:
        print(f'Error: {response.status_code} - {response.text}')
        print("fuck")
        return "?"

    # Specify the target strike price you're looking for
    target_strike_price = flow[-6][0:-1]  # Replace this with the desired strike price

    # Iterate through the options in betachain to find the one with the target strike price
    matching_option = "none"

    for option in betachain:
        if float(option['strike']) == float(target_strike_price) and option['option_type']==flow[3].lower():
            matching_option = option
            break  # Exit the loop once a match is found
    if (matching_option)=="none":
        return "?"
    # Split the string based on '@'
    parts = flow[9].split('@')

    # Extract the number after '@' (assuming it's the second part)
    number_after_at = parts[1].strip()
    currentprice=str(((((((matching_option["bid"]+matching_option["ask"])/2)*100))/float(number_after_at))//1)-100)
    #print((matching_option["bid"]+matching_option["ask"])/2)    
    #print(number_after_at)
    #print(currentprice)
    if float(currentprice)>0:
        return "+"+currentprice+"%"
    return currentprice+"%"
def is_less_than_two_weeks(date_str):
    current_date = datetime.now()
    entry_date = datetime.strptime(date_str, '%m/%d/%Y')
    two_weeks_later = current_date + timedelta(days=14)
    return entry_date < two_weeks_later
def calculate_time_score(row):
    timestamp=row[0]

    market_open_time = datetime.strptime("09:30:00", "%H:%M:%S")
    market_close_time = datetime.strptime("16:01:00", "%H:%M:%S")
    timestamp=timestamp[0:-3]+":00 "+timestamp[-2:]
    entry_time = datetime.strptime(timestamp,"%m/%d %H:%M:%S %p")
    market_close_time=datetime.strptime(str(entry_time)[5:10]+" 16:01:00","%m-%d %H:%M:%S")
    market_open_time=datetime.strptime(str(entry_time)[5:10]+" 09:30:00","%m-%d %H:%M:%S")    
    # print("----------------------------")
    # print(timestamp)
    # print(entry_time)   
    # print(str(entry_time)[5:10])
    # print(market_close_time)
    # print(market_open_time)
    # print(entry_time-market_open_time)
    # print((entry_time-market_close_time).total_seconds())  
   
    # print("--------------------------------------")    
    # Calculate time difference to market open and close
    time_to_open = (entry_time - market_open_time).total_seconds() / 60
    time_to_close = (market_close_time- entry_time).total_seconds() / 60


    # Score calculation (you can adjust this based on your criteria)
    
    if time_to_open <15:
        return 10  # High score if close to market open
    elif time_to_open < 30:
        return 5  # Medium score if moderately close to market open
    elif time_to_open < 60:
        return 3  # Medium score if moderately close to market open
    elif time_to_close < 15:
        return 10  # High score if close to market close

    elif time_to_close < 30:
        return 4  # High score if close to market close

    elif time_to_close < 60:
        return 2  # Medium score if moderately close to market close
    else:
        return 1  # Low score if not close to open or close
# Specify the path to your downloaded files directory
def flowreader():
    downloaded_files_dir = 'C:\\Users\\arya\\Downloads'

    # Get a list of all files in the directory
    all_files = os.listdir(downloaded_files_dir)

    # Filter for CSV files
    csv_files = [file for file in all_files if file.endswith('.csv')]

    # Sort CSV files by modification time (most recent first)
    csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(downloaded_files_dir, x)), reverse=True)
    csv_file_path = "C:\\Users\\aryas\\Downloads\\data(2).csv"
    # Check if there are any CSV files
    if csv_files:
        # Choose the most recent CSV file
        most_recent_csv = csv_files[0]

        # Construct the full path to the most recent CSV file
        csv_file_path = os.path.join(downloaded_files_dir, most_recent_csv)
    else:
        print("No CSV files found in the directory.")
    print(csv_file_path)
    flows=[]
    flowsAsk=[]
    flowsbid=[]
    rowNumber=0
    with open(csv_file_path, 'r', newline='') as csvfile:
    # Create a CSV reader object
        csv_reader = csv.reader(csvfile)

        # Iterate through each row in the CSV file
        for row in csv_reader:
            if row[4] == "BEARISH":
                row[4]="Bear"
            if row[4] == "BULLISH":
                row[4]="bull"
            # Each row is a list of values
            if rowNumber==0:
                del row[6]
            #print(row)
            rowNumber=rowNumber+1
            if rowNumber>1 and is_less_than_two_weeks(row[8]) and row[2]=="SWEEP"and float(row[-2])>179000:
                del row[6]
                sweep_score = float(row[5])
                #time_score = calculate_time_score(row[0][6:])
                #time_score = calculate_time_score(row[0])
                time_score = calculate_time_score(row)
                row.append(time_score)
                if sweep_score > 0.97:
                    row.append('Above Ask')
                    flowsAsk.append(row)
                elif 0.75 <= sweep_score <= 0.97:
                        row.append('At Ask')
                        flowsAsk.append(row)
                elif 0.25 <= sweep_score < 0.75:
                        row.append('At Mid')
                elif 0.1 <= sweep_score < 0.25:
                        row.append('At Bid')
                        flowsbid.append(row)
                else:
                        row.append('Below Bid')
                        flowsbid.append(row)
                flows.append(row)
                #print(row)
    flows = sorted(flows, key=lambda x: float(x[5]), reverse=True)
    flowsAsk = sorted(flowsAsk, key=lambda x: float(x[5]), reverse=True)
    flowsbid = sorted(flowsbid, key=lambda x: float(x[5]), reverse=False)
    original_flowsAsk = copy.deepcopy(flowsAsk)

    edditedflowsAsk=[]
    for i in flowsAsk:
        #  print("ooooooooooooo")
        #  print(i)
        #  print('--------------')
        #  print(discount(i))
        #  print('--------------')
        i.append(discount(i))
        
        del i[5]
        #  print("555555555555555555")
        #  print(i)
        i[6]=i[6][0:5]
        i[7]=str(int(float(i[7])/1000))+"k"
        i[8]=i[8].replace(" @ ", "@")
        if i[10]=='Above Ask':
            i[8]=i[8]+"AA" 
        if i[10]=='At Ask':
            i[8]=i[8]+"A" 
        if i[10]=='Below Bid':
            i[8]=i[8]+"BB"
        if i[10]=='AT Bid':
            i[8]=i[8]+"B" 
        #  print("ssssssssssssssssss")
        #  print(i[10])
        del i[10]      #thi
        edditedflowsAsk.append(i)
    #flowsAsk=original_flowsAsk 
    midpoint = len(edditedflowsAsk) // 2
    if len(edditedflowsAsk)<30:
        list_part1 = edditedflowsAsk[:midpoint]
        list_part2 = edditedflowsAsk[midpoint:]
    else:   
        list_part1=edditedflowsAsk[0:15]
        list_part2=edditedflowsAsk[15:29]
    original_flowsbid = copy.deepcopy(flowsbid)

    edditedflowsbid = []

    for i in flowsbid:
        i.append(discount(i))
        del i[5]
        i[6] = i[6][0:5]
        i[7] = str(int(float(i[7]) / 1000)) + "k"
        i[8] = i[8].replace(" @ ", "@")
        if i[10] == 'Above Ask':
            i[8] = i[8] + "AA" 
        if i[10] == 'At Ask':
            i[8] = i[8] + "A" 
        if i[10] == 'Below Bid':
            i[8] = i[8] + "BB"
        if i[10] == 'At Bid':
            i[8] = i[8] + "B"     
        del i[10]
        edditedflowsbid.append(i)

    flowsbid = original_flowsbid

    midpoint_bid = len(edditedflowsbid) // 2

    if len(edditedflowsbid) < 30:
        list_part1_bid = edditedflowsbid[:midpoint_bid]
        list_part2_bid = edditedflowsbid[midpoint_bid:]
    else:
        list_part1_bid = edditedflowsbid[0:15]
        list_part2_bid = edditedflowsbid[15:29]
    flowscall=flowsAsk[0:5]
    flowssell=flowsbid[0:5]
    return(list_part1,list_part2,list_part1_bid,list_part2_bid )
def nicetable(data):
    """
    Displays the given trade data as a presentable table using pandas.
    
    Parameters:
    - data (list of lists): The table data where each sublist represents a row.
    
    Returns:
    - None: Prints the formatted table.
    """
    # Predefined column names
    columns = [
        'Time', 'Ticker', 'Type', 'Option Type', 'Sentiment', 
        'Strike Price', 'Expiration', 'Premium', 
        'Contract Details', 'Order Size', 'Percent Change'
    ]
    
    # Create a pandas DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    # Display the DataFrame in a presentable format
    print(df.to_string(index=False))
