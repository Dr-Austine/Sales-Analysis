import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import os  # <-- Make sure OS is imported at the top!

# Call connection file
from mysql_con import *

# ==============================================================================
# PLACE THE CORRECTED FUNCTION HERE (Right after your imports)
# ==============================================================================
def local_css(style.css):
    """
    Dynamically builds the path to the CSS file based on Main.py's location
    and injects its styles into the Streamlit DOM.
    """
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, style.css)
    
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Initialize master application page state parameters
st.set_page_config("Business Analytics Dashboard", page_icon="", layout="wide")

# Call the function to load your styles
local_css("style.css")

st.subheader("Business Analytics Dashboard")

# ... rest of your code continues below ...


# ==============================================================================
# 2. INGESTION LAYER: RETRIEVE AND STRUCTURE SOURCE MATRIX
# ==============================================================================

# Fetch rows directly from the connected backend data layer
result = view_all_data()

# Construct structured pandas DataFrame with schema attributes
df = pd.DataFrame(
    result,
    columns=[
        "EEID",          # Employee ID
        "FullName",      # Full Name
        "JobTitle",      # Current Job Position Title
        "Department",    # Division / Functional Department
        "BusinessUnit",  # Higher-level Corporate Entity Division
        "Gender",        # Gender Demographics
        "Ethnicity",     # Racial / Ethnic Group Data
        "Age",           # Age Profile (Numerical)
        "HireDate",      # Historical Onboarding Date
        "AnnualSalary",  # Base Cash Compensation ($)
        "Bonus",         # Bonus Allocation Percentage / Value
        "Country",       # Geographic Location (Country Layer)
        "City",          # Geographic Location (City Layer)
        "id",            # Unique Serial Record Key
    ],
)


# ==============================================================================
# 3. INTERACTIVE CONTROL INTERFACE: SIDEBAR NAVIGATION & FILTER SETS
# ==============================================================================

# Sidebar Navigation Router Block
with st.sidebar:
    # Add your brand logo at the very top of the sidebar panel
    st.image("data/Logo.jpg", caption="Online Analytics")
    
    # Navigation menu controller sits immediately underneath the logo
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Demographics", "Table"],
        icons=["house", "people", "book"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )

# Sidebar Filter Section Layout Configuration
st.sidebar.header("Filter Options")

# 3.1 Department Filter (With collapsed label parameters for clean visual styling)
st.sidebar.subheader("Department")
department = st.sidebar.multiselect(
    label="Department", 
    options=df["Department"].unique(), 
    default=[], 
    placeholder="All Departments",
    label_visibility="collapsed",  # Shuts off label visibility and completely reclaims empty spaces
    key="dept_filter"
)

# 3.2 Country Filter (With collapsed label parameters for clean visual styling)
st.sidebar.subheader("Country")
country = st.sidebar.multiselect(
    label="Country", 
    options=df["Country"].unique(), 
    default=[], 
    placeholder="All Countries", 
    label_visibility="collapsed",  # Shuts off label visibility and completely reclaims empty spaces
    key="country_filter"
)

# 3.3 City Filter (Cascading Design Pattern - Choices Dependent on Country Selections)
# If countries are specified, subset options dynamically; otherwise fallback to full dataset values
if country:
    df_countries_filtered = df.query("Country in @country")
else:
    df_countries_filtered = df

st.sidebar.subheader("City")
city = st.sidebar.multiselect(
    label="City", 
    options=df_countries_filtered["City"].unique(), 
    default=[], 
    placeholder="All Cities",
    label_visibility="collapsed",  # Shuts off label visibility and completely reclaims empty spaces
    key="city_filter"
)

# 3.4 Business Unit Filter (With collapsed label parameters for clean visual styling)
st.sidebar.subheader("Business Unit")
BusinessUnit = st.sidebar.multiselect(
    label="Business Unit",
    options=df["BusinessUnit"].unique(),
    default=[],
    placeholder="All Business Units",
    label_visibility="collapsed",  # Shuts off label visibility and completely reclaims empty spaces
    key="bu_filter"
)


# ==============================================================================
# 4. FLEXIBLE MATRIX QUERY ENGINE (DYNAMIC FILTER CONSTRUCTOR)
# ==============================================================================

# Initialize an array to store conditional query fragment strings
query_parts = []

# Populate vector arrays based on user interactions
if department:   query_parts.append("Department in @department")
if country:      query_parts.append("Country in @country")
if city:         query_parts.append("City in @city")
if BusinessUnit: query_parts.append("BusinessUnit in @BusinessUnit")

# If criteria are active, compute the selection slice; otherwise, clone the reference vector
if query_parts:
    query_string = " and ".join(query_parts)
    df_selection = df.query(query_string)
else:
    df_selection = df.copy()


# ==============================================================================
# 5. MODULAR VIEW RENDER PAGES
# ==============================================================================

def metrics():
    """
    Renders core operational cash metrics across a balanced 4-column panel grid.
    Applies custom styling to cards and forces text visibility color definitions.
    """
    from streamlit_extras.metric_cards import style_metric_cards

    col1, col2, col3, col4 = st.columns(4)

    # Calculate and assign operational summary statistics
    col1.metric(
        label="Total Customers",
        value=f"{df_selection['id'].count():,}",
        delta="All Customers",
    )

    col2.metric(
        label="Average Salary",
        value=f"${df_selection['AnnualSalary'].mean():,.0f}",
        delta="Per Employee",
    )

    col3.metric(
        label="Total Annual Salary",
        value=f"${df_selection['AnnualSalary'].sum():,.0f}",
        delta="Combined Payroll",
    )

    col4.metric(
        label="Maximum Salary",
        value=f"${df_selection['AnnualSalary'].max():,.0f}",
        delta="Highest Earner",
    )

    # Inject specific background colors and layout boundaries for cards
    style_metric_cards(
        background_color="#071021",
        border_size_px=1,
        border_color="#1f66bd",
        border_radius_px=5,
        border_left_color="#1f66bd",
    )

    # Force internal metric labels to render white to prevent dark-theme text dropouts
    st.markdown(
        """
        <style>
        div[data-testid="stMetricValue"], 
        div[data-testid="stMetricLabel"], 
        div[data-testid="stMetricLabel"] * {
            color: #FFFFFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def charts():
    """
    Renders financial overview visual breakdowns (Pie chart and Bar graph) 
    split evenly across a 2-column container.
    """
    div1, div2 = st.columns(2)

    # Render financial share distribution pie chart
    with div1:
        fig_pie = px.pie(
            df_selection,
            values="AnnualSalary",
            names="Department",
            title="Customer by Department",
        )
        fig_pie.update_layout(legend_title="Department", legend_y=0.9)
        fig_pie.update_traces(textinfo="none", textposition="inside")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Render departmental operational cash payroll bar graph
    with div2:
        fig_bar = px.bar(
            df_selection,
            y="AnnualSalary",
            x="Department",
            text_auto=".2s",  # Formats short scales automatically (e.g., $1.2M)
            title="Simple Bar Graph",
        )
        fig_bar.update_traces(
            textfont_size=18,
            textangle=0,
            textposition="outside",
            cliponaxis=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True)


def demographics():
    """
    Renders detailed workforce distribution analytics focusing on metrics 
    including gender, age distribution profile, and diversity tracking arrays.
    """
    from streamlit_extras.metric_cards import style_metric_cards

    col1, col2, col3 = st.columns(3)

    # Demographic Metric 1: Track average workforce age index
    with col1:
        st.metric(
            label="Average Employee Age",
            value=f"{df_selection['Age'].mean():.1f} Years",
            delta="Workforce Maturity",
        )

    # Demographic Metric 2: Quantify female employee breakdown ratio
    with col2:
        total_count = len(df_selection)
        female_pct = (
            (len(df_selection[df_selection["Gender"] == "Female"]) / total_count) * 100
            if total_count > 0
            else 0
        )
        st.metric(
            label="Female Workforce Ratio",
            value=f"{female_pct:.1f}%",
            delta="Gender Balance",
        )

    # Demographic Metric 3: Generate comparative breakdown between genders
    with col3:
        gender_salaries = df_selection.groupby("Gender")["AnnualSalary"].mean()
        female_avg = gender_salaries.get("Female", 0)
        male_avg = gender_salaries.get("Male", 0)
        
        if female_avg > 0 and male_avg > 0:
            value_display = f"${female_avg:,.0f} / ${male_avg:,.0f}"
            delta_display = "Female vs Male Avg"
        elif female_avg > 0:
            value_display = f"${female_avg:,.0f}"
            delta_display = "Female Avg Only"
        elif male_avg > 0:
            value_display = f"${male_avg:,.0f}"
            delta_display = "Male Avg Only"
        else:
            value_display = "$0"
            delta_display = "No Salary Data"

        st.metric(
            label="Gender Salary Breakdown",
            value=value_display,
            delta=delta_display,
        )

    # Standardize metric cards layout presentation properties
    style_metric_cards(
        background_color="#071021",
        border_size_px=1,
        border_color="#1f66bd",
        border_radius_px=5,
        border_left_color="#1f66bd",
    )

    div1, div2 = st.columns(2)

    # Plot 1: Visualizes ethnic representation distribution inside a donut chart
    with div1:
        fig_donut = px.pie(
            df_selection,
            names="Ethnicity",
            title="Workforce Diversity (Ethnicity)",
            hole=0.4,
        )
        fig_donut.update_traces(textinfo="percent")
        st.plotly_chart(fig_donut, use_container_width=True)

    # Plot 2: Splitting sub-views via internal sub-tabs
    with div2:
        chart_tab1, chart_tab2 = st.tabs(["Age Profile", "Salary Visual Comparison"])
        
        # Sub-tab A: Visualizes general workforce profile distribution
        with chart_tab1:
            fig_hist = px.histogram(
                df_selection,
                x="Age",
                nbins=15,
                title="Age Distribution Profile",
                color_discrete_sequence=["#1f66bd"],
            )
            fig_hist.update_layout(
                bargap=0.1, yaxis_title="Employee Count", xaxis_title="Age Groups"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
        # Sub-tab B: Renders direct horizontal bar wage variance breakdown across values
        with chart_tab2:
            df_gender_sal = df_selection.groupby("Gender")["AnnualSalary"].mean().reset_index()
            fig_gender_sal = px.bar(
                df_gender_sal,
                x="AnnualSalary",
                y="Gender",
                orientation="h",
                title="Average Salary Comparison ($)",
                text_auto=".2s",
                color="Gender",
                color_discrete_map={"Female": "#ff6b6b", "Male": "#1f66bd"}
            )
            fig_gender_sal.update_layout(
                xaxis_title="Average Annual Salary ($)",
                yaxis_title="",
                showlegend=False
            )
            st.plotly_chart(fig_gender_sal, use_container_width=True)


def table():
    """
    Renders raw transactional rows within an interactive, expandable data component grid view.
    Includes columns selector toggles for granular inspection arrays.
    """
    with st.expander("My Database Table", expanded=True):
        shwdata = st.multiselect(
            "Filter Dataset Columns",
            df_selection.columns,
            default=[
                "EEID", "FullName", "JobTitle", "Department", "BusinessUnit",
                "Gender", "Ethnicity", "Age", "HireDate", "AnnualSalary",
                "Bonus", "Country", "City", "id",
            ],
            label_visibility="collapsed",  # Collapses internal layout structure spacing here too
            key="table_cols_filter"
        )
        st.dataframe(df_selection[shwdata], use_container_width=True)


# ==============================================================================
# 6. ROUTER ROUTINE APPLICATION ENTRY CONTROL
# ==============================================================================

# Match active side-menu state targets to compute active layouts dynamically
if selected == "Home":
    metrics()
    charts()
elif selected == "Demographics":
    demographics()
elif selected == "Table":
    table()
    # Generates transactional transposed statistical matrix details summary (count, mean, std)
    st.dataframe(df_selection.describe().T, use_container_width=True)
