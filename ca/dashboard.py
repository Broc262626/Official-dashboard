import streamlit as st
import pandas as pd

def show_dashboard():
    st.title('Device Repair Dashboard')
    df = pd.read_csv('data/repairs.csv')
    st.dataframe(df)

    uploaded_file = st.file_uploader('Import Excel', type=['csv','xlsx'])
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            new_df = pd.read_csv(uploaded_file)
        else:
            new_df = pd.read_excel(uploaded_file)
        st.dataframe(new_df)
