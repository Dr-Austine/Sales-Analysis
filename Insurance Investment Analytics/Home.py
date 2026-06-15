import streamlit as st
import pandas as pd
import plotly.express as px 
import time 
from streamlit_option_menu import option_menu
from numerize.numerize import numerize 
from Query import *

# 1. INITIAL APP PAGE CONFIGURATION
st.set_page_config(page_title="Insurance Analytics Dashboard", page_icon="🌍", layout="wide")

# 2. FETCH AND CONSTRUCT BASE DATA MATRIX
result = view_all_data()

# Match the exact column order coming from your database (id added FIRST via SQL)
df = pd.DataFrame(result, columns=[
    "Policy", "Expiry", "Location", "State", "Region", 
    "Investment", "Construction", "BusinessType", "Earthquake", "Flood", "Rating","id"
])


# 3. NAVIGATION APP MENU CONTROLLER (MOVED TO THE TOP OF THE SIDEBAR)
with st.sidebar:
    st.sidebar.image("data/Logo.jpg", caption="Online Analytics")
    
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Progress"],
        icons=["house", "eye"],
        menu_icon="cast",
        default_index=0
    )


# 4. INTERACTIVE SIDEBAR FILTER GENERATION (RENDERS BELOW NAVIGATION MENU)
st.sidebar.header("Please Filter Data")

# Multi-select controls for data filters
Region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

Location = st.sidebar.multiselect(
    "Select Location",
    options=df["Location"].unique(),
    default=df["Location"].unique()
)

Construction = st.sidebar.multiselect(
    "Select Construction",
    options=df["Construction"].unique(),
    default=df["Construction"].unique()
)

# Apply interactive selections dynamically to the dataframe rows
df_selection = df.query(
    "Region == @Region & Location == @Location & Construction == @Construction"
)


# 5. VIEW PAGE FUNCTIONS
def Home_Page(df_selection):
    st.subheader("🔔 Insurance Descriptive Analytics")
    st.markdown("##")
    
    # --- Compute Top Analytics ---
    if not df_selection.empty:
        total_investment = df_selection["Investment"].astype(float).sum()
        investment_mean = df_selection["Investment"].astype(float).mean()
        investment_median = df_selection["Investment"].astype(float).median()
        rating = df_selection["Rating"].astype(float).sum()

        mode_series = df_selection["Investment"].astype(float).mode()
        investment_mode = mode_series.iloc[0] if not mode_series.empty else 0.0
    else:
        total_investment = investment_mean = investment_median = rating = investment_mode = 0.0

    # --- Create the 5 KPI Display Cards ---
    total1, total2, total3, total4, total5 = st.columns(5, gap='large')

    with total1:
        st.info("Total Investment", icon="📊")
        st.metric(label="Sum USD", value=f"${total_investment:,.0f}")

    with total2:
        st.info("Most Frequent", icon="📊")
        st.metric(label="Mode USD", value=f"${investment_mode:,.0f}")

    with total3:
        st.info("Average Investment", icon="📊")
        st.metric(label="Average USD", value=f"${investment_mean:,.0f}")

    with total4:
        st.info("Central Earnings", icon="📊")
        st.metric(label="Median USD", value=f"${investment_median:,.0f}")

    with total5:
        st.info("Ratings Summary", icon="📊")
        st.metric(label="Rating Total", value=numerize(rating), help=f"Total Cumulative Rating: {rating:,.1f}")

    st.markdown("---")

    # --- Expandable Data Viewer Section ---
    with st.expander("Tabular View"):
        showData = st.multiselect('Filter Columns to Display: ', options=df_selection.columns, default=list(df_selection.columns))
        if showData:
            st.dataframe(df_selection[showData], use_container_width=True)
        else:
            st.warning("Please select at least one column to display data.")


def Progress_Page(df_selection):
    st.subheader("📈 Performance Metrics & Projections")
    st.markdown("##")
    
    # Run the structural components
    Progressbar(df_selection)
    graphs(df_selection)


def Progressbar(df_selection):
    st.markdown("### 🎯 Investment Target Progress")
    
    # Custom CSS styling to make the progress bar look sleek and modern
    st.markdown(
        """
        <style>
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #0083b8, #00b4db);
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    target = 5000000000 
    current = df_selection["Investment"].astype(float).sum()
    
    if target > 0:
        percent = int(round((current / target) * 100))
    else:
        percent = 0

    if percent >= 100:
        st.subheader("🎉 Target Achieved! Excellent Portfolio Growth!")
        visual_percent = 100  
    else:
        st.write(f"You have achieved **{percent}%** of your **${target:,.0f} USD** benchmark target.")
        visual_percent = percent

    if visual_percent > 0:
        mybar = st.progress(0)
        for percent_complete in range(visual_percent):
            time.sleep(0.005)  # Fast smooth loader tick rate
            mybar.progress(percent_complete + 1, text=f"Processing KPI Vector: {percent_complete + 1}%")
    else:
        st.progress(0, text="Waiting for metric visibility...")

    st.markdown("---")


def graphs(df_selection):
    if df_selection.empty:
        st.warning("No data available to display graphs. Please adjust your sidebar filters.")
        return

    # --- CHART 1: HORIZONTAL BAR (Investment by Business Type) ---
    investment_by_business_type = (
        df_selection.groupby(by=["BusinessType"])[["Investment"]]
        .sum()
        .sort_values(by="Investment", ascending=True)
        .reset_index()
    )

    fig_investment = px.bar(
        investment_by_business_type,   
        x="Investment",               
        y="BusinessType",             
        orientation="h",
        title="<b>Investment by Business Type</b>",
        color_discrete_sequence=["#0083b8"],
        template="plotly_white",
    )
    fig_investment.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))


    # --- CHART 2: LINE CHART (Investment by State) ---
    investment_by_state = (
        df_selection.groupby(by=["State"])[["Investment"]]
        .sum()
        .sort_values(by="State")
        .reset_index()
    )

    fig_state = px.line(
        investment_by_state,          
        x="State",                     
        y="Investment",                
        title="<b>Investment Trends by State</b>",
        color_discrete_sequence=["#00b4db"],
        template="plotly_white",
    )
    fig_state.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(showgrid=False))


    # --- CHART 3: TREEMAP (Concentration by Region & State) ---
    fig_treemap = px.treemap(
        df_selection,
        path=["Region", "State"],  
        values="Investment",       
        title="<b>Investment Concentration Hierarchy</b>",
        template="plotly_white",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )


    # --- CHART 4: DONUT CHART (Market Share by Construction Type) ---
    construction_share = df_selection.groupby("Construction")["Investment"].sum().reset_index()

    fig_donut = px.pie(
        construction_share,
        values="Investment",
        names="Construction",
        hole=0.5,  
        title="<b>Market Share by Construction Type</b>",
        template="plotly_white",
       color_discrete_sequence=px.colors.sequential.Blues_r
    )


    # --- GRID SYSTEM LAYOUT GENERATION ($2 \times 2$ Grid Display) ---
    # Row 1: Line Chart & Horizontal Bar Chart
    row1_left, row1_right = st.columns(2)
    row1_left.plotly_chart(fig_state, use_container_width=True)
    row1_right.plotly_chart(fig_investment, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True) # Spacing break row

    # Row 2: Treemap Hierarchical Block & Donut Share Chart
    row2_left, row2_right = st.columns(2)
    row2_left.plotly_chart(fig_treemap, use_container_width=True)
    row2_right.plotly_chart(fig_donut, use_container_width=True)


# --- ROUTER ROUTINE APPLICATION ENTRY CONTROL ---
if selected == "Home":
    Home_Page(df_selection)
elif selected == "Progress":
    Progress_Page(df_selection)


