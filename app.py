import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="US Disaster Analysis", layout="wide")

st.title("US Billion-Dollar Disasters (1980–2024)")

# Load data
df = pd.read_csv("events-US-1980-2024.csv", skiprows=2)

df.columns = df.columns.str.strip()

if st.checkbox("Show Raw Data"):
    st.dataframe(df)

st.write("Dataset loaded successfully.")

df['Begin Date'] = pd.to_datetime(df['Begin Date'], format='%Y%m%d')
df['End Date'] = pd.to_datetime(df['End Date'], format='%Y%m%d')

df['Year'] = df['Begin Date'].dt.year

df['Duration'] = (df['End Date'] - df['Begin Date']).dt.days
df["CPI-Adjusted Cost"] = pd.to_numeric(df["CPI-Adjusted Cost"], errors="coerce")
