import streamlit as st
import time
import numpy as np
import pandas as pd
import requests

st.title("Орон сууцны 1 метр талбайн дундаж үнэ, Улаанбаатар хотын 6 дүүргээр")

# Define the API endpoint URL
api_url = "https://opendata.1212.mn/api/Data"

# Define the input values as a dictionary
input_data = {
    "tbl_id": "DT_NSO_0300_00V2",
}

# Send a POST request to the API with the input data as JSON
response = requests.post(api_url, json=input_data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Now 'data' contains the API response as a Python dictionary
    #print(data)
    #We need only data so we selecting Data from response data
    df = pd.json_normalize(data['DataList'])
    # remove some redundant columns that we do not use
    df.drop(columns=['TBL_ID','SCR_ENG','SCR_ENG1','CODE2', 'SCR_MN2','SCR_ENG2'],inplace=True)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

