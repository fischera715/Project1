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

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview Trends",
    "By Disaster Type",
    "Duration Analysis",
    "Data Source"
])

df['Begin Date'] = pd.to_datetime(df['Begin Date'], format='%Y%m%d')
df['End Date'] = pd.to_datetime(df['End Date'], format='%Y%m%d')

df['Year'] = df['Begin Date'].dt.year

df['Duration'] = (df['End Date'] - df['Begin Date']).dt.days
df["CPI-Adjusted Cost"] = pd.to_numeric(df["CPI-Adjusted Cost"], errors="coerce")

with tab1:
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
        "Notice the increase in event counts in more recent years."
    )
    
    
    st.header("Total CPI-Adjusted Cost Per Year")

    total_cost_per_year = df.groupby("Year")["CPI-Adjusted Cost"].sum().reset_index()

    fig2 = px.line(
        total_cost_per_year,
        x="Year",
        y="CPI-Adjusted Cost",
        title="Total Inflation-Adjusted Disaster Cost per Year",
        markers=True
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.write(
        "While disaster frequency has increased, total costs show extreme spikes "
        "in certain years driven by catastrophic events such as major hurricanes."
    )

with tab2:

    st.header("Cost Trends by Disaster Type")

    # Interactive filter
    disaster_list = sorted(df["Disaster"].unique())
    selected_disaster = st.selectbox(
        "Select a Disaster Type:",
        disaster_list
    )

    # Filter data
    filtered_df = df[df["Disaster"] == selected_disaster]

    # Cost over time for selected disaster
    cost_by_year = (
        filtered_df.groupby("Year")["CPI-Adjusted Cost"]
        .sum()
        .reset_index()
    )

    fig3 = px.line(
        cost_by_year,
        x="Year",
        y="CPI-Adjusted Cost",
        markers=True,
        title=f"CPI-Adjusted Cost Over Time: {selected_disaster}"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.write(
        "This chart shows how the financial impact of a selected disaster type "
        "has evolved over time."
    )

    # Average cost bar chart
    st.subheader("Average Cost per Disaster Type")

    avg_cost = (
        df.groupby("Disaster")["CPI-Adjusted Cost"]
        .mean()
        .reset_index()
        .sort_values(by="CPI-Adjusted Cost", ascending=False)
    )

    fig4 = px.bar(
        avg_cost,
        x="Disaster",
        y="CPI-Adjusted Cost",
        title="Average CPI-Adjusted Cost per Disaster Type"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.write(
        "Tropical Cyclones dominate average losses, while other disaster "
        "types contribute smaller but more frequent costs."
    )










