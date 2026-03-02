import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="US Disaster Analysis", layout="wide")

st.title("US Billion-Dollar Disasters (1980–2024)")

# Load data
df = pd.read_csv("events-US-1980-2024.csv")

df.columns = df.columns.str.strip()

if st.checkbox("Show Raw Data"):
    st.dataframe(df)

st.write("Dataset loaded successfully.")
