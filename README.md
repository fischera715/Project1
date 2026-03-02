# U.S. Billion-Dollar Weather and Climate Disasters (1980-2024)

## Project Overview
This project explores patterns, trends, and financial impacts of U.S. weather and climate disasters from 1980 to 2024 that caused at least $1 billion in damages (CPI-adjusted). The analysis is presented in an **interactive Streamlit dashboard** with multiple visualizations, highlighting disaster frequency, costs, duration, and trends over time.

### Analytical Questions
1. Has the frequency of billion-dollar disasters changed over time?
2. Have total inflation-adjusted costs increased over time?
3. What disaster types account for the largest share of total economic losses in the US?
4. Are certain disaster types becoming more financially dominant over time?

---

## Dataset
- **Source:** NOAA National Centers for Environmental Information (NCEI)  
- **Citation:** Smith, Adam B. (2020). *U.S. Billion-dollar Weather and Climate Disasters, 1980 - present* (NCEI Accession 0209268). Subset used: 1980–2024, all events ≥ $1 billion in damages. [DOI: 10.25921/stkw-7w73](https://doi.org/10.25921/stkw-7w73)  
- **Accessed:** March 02, 2026  
- **Description:** Event-level data including disaster type, start and end dates, duration, deaths, unadjusted and CPI-adjusted costs.  
- **License:** Publicly available for research, education, and policy analysis.  
- **Updating:** Dataset is archived; no future updates will be available.

---

## Streamlit Dashboard
The dashboard includes four main tabs:

1. **Overview Trends**  
   - Number of disasters per year  
   - Scatter plot: CPI-adjusted vs unadjusted costs  
   - Total CPI-adjusted costs per year

2. **By Disaster Type**  
   - Deaths vs. CPI-adjusted cost by disaster type (scatter plot)
   - CPI-adjusted cost of each disaster type (bar chart) 
   - Cost trends over time (line chart, interactive filter by disaster type)  
   - Duration trends over time (line chart with same filter)

3. **Duration Analysis**  
   - Box plot of disaster durations by type  
   - Scatter plot: Disaster duration vs CPI-adjusted cost (log scale)

4. **Data Source & Sustainability**  
   - Original source, dataset description, licensing, and updating process  

**Interactive Elements:**  
- Checkbox to view or hide full dataset
- Selectbox to filter by disaster type for trend analyses  
- Hover data on scatter plots to explore individual events

**Visualization Highlights:**  
- Financial losses are heavily skewed, with a few extreme events dominating totals  
- Duration and cost are weakly correlated (R ≈ 0.08)  
- Tropical Cyclones dominate average costs, while other disasters are less costly but frequent  

**Dashboard URL:** (https://project1-hvdapnzuyz4gu8q7jeshh6.streamlit.app/#disaster-duration-by-type)
