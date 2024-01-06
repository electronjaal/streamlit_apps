import streamlit as st
import time
import numpy as np
import pandas as pd
import requests

import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.title("Орон сууцны 1 метр талбайн дундаж үнэ, Улаанбаатар хотын 6 дүүргээр")

def load_data():

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
        df.drop(columns=['TBL_ID','CODE','SCR_ENG','SCR_ENG1','CODE2', 'SCR_MN2','SCR_ENG2'],inplace=True)
        df['Period'] = pd.to_datetime(df['Period'], format='%Y%m')
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    return df

def plot_data(data):
    # Creating separate plots for each unique value in SCR_MN1
    unique_scr_mn1 = data['SCR_MN1'].unique()

    # Set up the matplotlib figure
    n_plots = len(unique_scr_mn1)
    fig, axes = plt.subplots(n_plots, 1, figsize=(15, 5 * n_plots), sharex=True)

    # Plot each SCR_MN1 category in a separate subplot
    for i, category in enumerate(unique_scr_mn1):
        ax = axes[i]
        #ax.set_ylim(2, 4)
        subset_data = data[data['SCR_MN1'] == category]
        sns.lineplot(data=subset_data, x='Period', y='DTVAL_CO', hue='SCR_MN', ax=ax)
        ax.set_title(f'{category} үнийн харьцуулалт')
        ax.set_ylabel('Метр квадратын үнэ (сая төгрөгөөр)')
        ax.legend(title='Дүүрэг', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Improve y-axis readability
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=10))  # Adjust the number of y-axis labels
        #ax.yaxis.set_major_formatter(ticker.ScalarFormatter())   # Use scalar formatter for readability
        #ax.yaxis.set_tick_params(rotation=45)  

    plt.xlabel('Он сар')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Streamlit app
def main():

    # Load and display the data
    data = load_data()
    st.write(data)

    # Plotting
    st.subheader('Үнийн харьцуулсан график')
    fig = plot_data(data)
    st.pyplot(fig)

if __name__ == '__main__':
    main()