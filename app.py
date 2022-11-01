import streamlit as st
import pandas as pd
import numpy as np

st.title('Inventory Parser')

uploaded_file = st.file_uploader("Select CSV file to upload")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    event_name_array = df['event_name'].drop_duplicates().to_numpy()
    dfs = {}
    for event in event_name_array:
        dfs[event] = pd.pivot_table(df[(df.event_name == event)], values=['contracted','left_to_sell','sold','sold_in_default'], index=['event_name','hotel_name','room_type'], columns=['room_date'], aggfunc=np.sum, fill_value=0)
    st.write(len(dfs), ' events processed')
    with open('export_csv.csv','w') as f:
        f.write("Inventory Report\n")
    with open('export_csv.csv','a') as f:
        for event in event_name_array:
            dfs[event].to_csv(f)
            f.write("\n")
    with open('export_csv.csv') as f:
        st.download_button(
            label='Download Processed File', 
            data=f, 
            file_name='inventory_summary.csv',
            mime='text/csv'
        )