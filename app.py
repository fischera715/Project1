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

with tab3:

    st.header("Disaster Duration vs Financial Impact")

    st.write(
        "This box plot shows the durations of each specific disaster."
        
    # Boxplot
    fig = px.box(
        df,
        x='Disaster',
        y='Duration',
        points="all",
        color='Disaster',
        title="Distribution of Disaster Duration by Type",
        labels={'Duration':'Duration (days)', 'Disaster':'Disaster Type'}
    )

    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.write(
        "The box plot shows that most disasters last less than 20 days, with the "
        "exception of Droughts, Wildfires, and Floods."
    
    st.write(
        "This scatter plot explores whether longer disasters lead to higher costs. "
        "A log scale is used to better visualize extreme outliers."
    )

    duration_df = df[df["Duration"] >= 0]

    fig5 = px.scatter(
        duration_df,
        x="Duration",
        y="CPI-Adjusted Cost",
        color="Disaster",
        hover_data=["Year"],
        title="Duration vs CPI-Adjusted Cost",
    )

    fig5.update_yaxes(type="log")

    st.plotly_chart(fig5, use_container_width=True)

    st.write(
        "The overall correlation between duration and cost is weak, suggesting that "
        "longer events do not automatically translate to higher financial losses."
    )


with tab4:

    st.header("Data Source & Sustainability")

    st.subheader("Original Data Source")

    st.write(
        """
        **Dataset:** U.S. Billion-Dollar Weather and Climate Disasters  
        **Source:** NOAA National Centers for Environmental Information (NCEI)  
        **Citation:** Smith, Adam B. (2020). U.S. Billion-dollar Weather and Climate Disasters, 1980 - present (NCEI Accession 0209268). 
        Subset used: 1980–2024, all events ≥ $1 billion in damages. NOAA National Centers for Environmental Information. 
        Dataset. https://doi.org/10.25921/stkw-7w73. Accessed March 02, 2026
        
        **Note:** NOAA has archived this dataset and will no longer be updating it.
        """
    )

    st.subheader("Dataset Description")

    st.write(
        """
        This dataset contains U.S. weather and climate disasters that caused 
        at least $1 billion in damages. The costs have been adjusted for inflation. Key variables 
        include disaster type, start and end dates, duration, and CPI-adjusted costs.
        """
    )

    st.subheader("Data Updating Process")
    st.write(
        """
        The dataset is archived; no additional updates will be provided. Future analyses would require re-downloading new data releases if available.
        """
    )

    st.subheader("License & Use")

    st.write(
        """
        The dataset is publicly available through NOAA and is intended for 
        research, educational, and public policy analysis.
        """
    )





