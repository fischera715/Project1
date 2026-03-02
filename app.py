import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="US Disaster Analysis", layout="wide")

st.title("US Billion-Dollar Disasters (1980–2024)")

# Load data
df = pd.read_csv("events-US-1980-2024.csv", skiprows=2)

df.columns = df.columns.str.strip()

if st.checkbox("Show Data"):
    st.dataframe(df)

df['Begin Date'] = pd.to_datetime(df['Begin Date'], format='%Y%m%d')
df['End Date'] = pd.to_datetime(df['End Date'], format='%Y%m%d')

df['Year'] = df['Begin Date'].dt.year

df['Duration'] = (df['End Date'] - df['Begin Date']).dt.days
df["CPI-Adjusted Cost"] = pd.to_numeric(df["CPI-Adjusted Cost"], errors="coerce")

st.header("Trend in Number of Billion-Dollar Disasters")

disasters_per_year = df.groupby("Year").size().reset_index(name="Count")

fig1 = px.bar(
    disasters_per_year,
    x="Year",
    y="Count",
    title="Number of Disasters per Year",
)

st.plotly_chart(fig1, use_container_width=True)

st.write(
    "This chart shows the annual frequency of billion-dollar disasters. "
    "Notice the increase in event counts in more recent decades."
)
