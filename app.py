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

# Cleaning data
df['Begin Date'] = pd.to_datetime(df['Begin Date'], format='%Y%m%d')
df['End Date'] = pd.to_datetime(df['End Date'], format='%Y%m%d')

df['Year'] = df['Begin Date'].dt.year

df['Duration'] = (df['End Date'] - df['Begin Date']).dt.days
df["CPI-Adjusted Cost"] = pd.to_numeric(df["CPI-Adjusted Cost"], errors="coerce")

# Begin overview of trends
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
        "Notice there is an increase in events in more recent years."
    )
    
    st.header("CPI-Adjusted Cost vs. Unadjusted Cost")

    st.write(
        "This plot shows the correlation between CPI-adjusted cost and regular cost "
        "to prove that they are proportional and the analyses using CPI adjusted cost is accurate."
    )

    fig = px.scatter(
        df,
        x="Unadjusted Cost",
        y="CPI-Adjusted Cost",
        color="Disaster",
        trendline="ols",
        trendline_scope="overall",
        hover_data=["Name", "Year", "Disaster"],
        title="CPI-Adjusted Cost vs Unadjusted Cost",
        labels={"Unadjusted Cost": "Unadjusted Cost (Millions USD)",
                    "CPI-Adjusted Cost": "CPI-Adjusted Cost (Millions USD)"}
        )
    
    fig.update_yaxes(type="log")
    fig.update_xaxes(type="log")
    st.plotly_chart(fig, use_container_width=True)

    st.write(
        "The scatter plot comparing CPI-adjusted and unadjusted costs shows a very high coefficient of determination "
        "(R² ≈ 0.95), indicating that adjusting for inflation preserves the relative scale of disaster costs over time. "
        "All financial values in this dashboard are shown as CPI-adjusted to make them comparable across years."
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
    "While disaster frequency has increased over time, total costs exhibit extreme spikes "
    "in certain years, driven by catastrophic events such as major hurricanes. "
    "This suggests that the number of disasters does not necessarily correlate with the total cost."
    )

# Disaster Type Analysis
with tab2:
    # Scatter plot: Deaths vs CPI-Adjusted Cost
    fig_deaths = px.scatter(
        df,
        x="CPI-Adjusted Cost",
        y="Deaths",
        color="Disaster",
        hover_data=["Name", "Year", "Disaster", "CPI-Adjusted Cost"],
        title="Deaths vs CPI-Adjusted Cost by Disaster Type",
        labels={"CPI-Adjusted Cost": "CPI-Adjusted Cost (Millions USD)", "Deaths": "Number of Deaths"},
        trendline="ols",
        trendline_scope="overall"
    )
    
    fig_deaths.update_xaxes(type="log")
    fig_deaths.update_yaxes(type="log")
    
    st.plotly_chart(fig_deaths, use_container_width=True)

    st.write(
        "This scatter plot shows how financial impact relates to human impact. "
        "While not all costly disasters are deadly, there is a moderate positive "
        "correlation (R² ≈ 0.35) indicating that higher-cost events often result "
        "in more fatalities."
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

    st.header("Cost Trends by Disaster Type")

    # Interactive filter
    disaster_list = sorted(df["Disaster"].unique())
    selected_disaster = st.selectbox(
        "Select a Disaster Type:",
        disaster_list
    )

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

# Duration Analysis
with tab3:
    st.header("Duration of Disasters by Type")

    st.write(
        "This box plot shows the durations of each specific disaster, "
         "highlighting how long different kinds of events typically last and the variability across events."
    )
    
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
    )

    st.header("Disaster Duration vs Financial Impact")

    st.write(
        "This scatter plot explores whether longer disasters lead to higher costs. "
        "A log scale is used to better visualize extreme outliers."
    )

    duration_df = df[df["Duration"] >= 0]

    fig5 = px.scatter(
        duration_df,
        x="Duration",
        y="CPI-Adjusted Cost",
        hover_data=["Year"],
        title="Duration vs CPI-Adjusted Cost",
        trendline="ols"
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





