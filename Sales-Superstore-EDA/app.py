import streamlit as st
import plotly.express as px
import pandas as pd 
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:", layout="wide")

# HEADER
st.title("📊 SuperStore EDA")

# FILE UPLOAD
fl = st.file_uploader("📂 Upload a file", type=["csv", "txt", "xlsx", "xls"])

if fl is not None:
    df = pd.read_csv(fl)
    st.success("File uploaded successfully!")
else:
    df = pd.read_csv("Superstore.csv")
    st.info("Using default dataset")


# DISPLAY DATA in expander
with st.expander("🔍 Click to view dataset preview"):
    st.dataframe(df.head())

# COLUMNS
col1, col2 = st.columns(2)

# DATE CONVERSION
df["Order Date"] = pd.to_datetime(df["Order Date"])

# MIN / MAX DATE
startDate = df["Order Date"].min()
endDate = df["Order Date"].max()

# DATE INPUTS
with col1:
    date1 = st.date_input("Start Date", startDate)

with col2:
    date2 = st.date_input("End Date", endDate)

# CONVERT TO DATETIME
date1 = pd.to_datetime(date1)
date2 = pd.to_datetime(date2)

# FILTER BY DATE
df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

# SIDEBAR
st.sidebar.header("Choose your filter:")

# Create a working copy
filtered_df = df.copy()

# REGION FILTER
region = st.sidebar.multiselect(
    "Pick your Region",
    df["Region"].unique()
)

if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]

# STATE FILTER (depends on region selection)
state = st.sidebar.multiselect(
    "Pick the State",
    filtered_df["State"].unique()
)

if state:
    filtered_df = filtered_df[filtered_df["State"].isin(state)]

# CITY FILTER
city = st.sidebar.multiselect(
    "Pick your City",
    filtered_df["City"].unique()
)

if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]

# GROUP DATA
category_df = filtered_df.groupby(
    by="Category", as_index=False
)["Sales"].sum()

# COLUMNS
col1, col2 = st.columns(2)

# BAR CHART
with col1:
    st.subheader("Category wise Sales")

    fig = px.bar(
        category_df,
        x="Category",
        y="Sales",
        text=category_df["Sales"].apply(lambda x: f"${x:,.2f}"),
        template="seaborn"
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

# PIE CHART
with col2:
    st.subheader("Region wise Sales")

    fig = px.pie(
        filtered_df,
        values="Sales",
        names="Region",
        hole=0.4
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    st.plotly_chart(fig, use_container_width=True)


cl1, cl2 = st.columns(2)

with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Data",
            data=csv,
            file_name="Category.csv",
            mime="text/csv",
            help="Click here to download the data as a CSV file"
        )

with cl2:
    with st.expander("Region_ViewData"):
        region = filtered_df.groupby(by="Region", as_index=False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Data",
            data=csv,
            file_name="Region.csv",
            mime="text/csv",
            help="Click here to download the data as a CSV file"
        )

# Create the period column
filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")

st.subheader("Time Series Analysis")

# Group by formatted date
linechart = pd.DataFrame(
    filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y-%b"))["Sales"].sum()
).reset_index()

# Rename columns for clarity
linechart.columns = ["month_year", "Sales"]

# Create line chart
fig2 = px.line(
    linechart,
    x="month_year",
    y="Sales",
    labels={"Sales": "Amount ($)", "month_year": "Month"},
    height=500,
    width=1000,
    template="gridon"
)

st.plotly_chart(fig2, use_container_width=True)


with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap= "Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data = csv, file_name = "TimeSeries.csv", mime = 'text/csv')

# Create a treem based on Region, Category, Sub-Category
st.subheader("Hierarchical View of Sales Using Treemap")

fig3 = px.treemap(
    filtered_df,
    path=["Region", "Category", "Sub-Category"],
    values="Sales",
    color="Sales",  # Color by sales amount instead of Sub-Category
    hover_data={"Sales": ": $", "Profit": ": $"},  # Add profit info
    color_continuous_scale="Viridis",  # Clean, modern color scheme
)

fig3.update_layout(
    margin=dict(t=30, l=10, r=10, b=10),  # Minimal padding
    font=dict(size=12, family="Arial"),   # Clean font
    paper_bgcolor="rgba(0,0,0,0)",        # Transparent background
    plot_bgcolor="rgba(0,0,0,0)",         # Transparent plot area
)

chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Segment wise Sales")
    fig = px.pie(
        filtered_df,
        values="Sales",
        names="Segment",
        template="simple_white",
        color_discrete_sequence=["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont_size=14,
        marker=dict(line=dict(color="white", width=3))
    )
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader("Category wise Sales")
    fig = px.pie(
        filtered_df,
        values="Sales",
        names="Category",
        template="simple_white",
        color_discrete_sequence=["#f781bf", "#a65628", "#999999", "#e6ab02", "#66c2a5"]
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont_size=14,
        marker=dict(line=dict(color="white", width=3))
    )
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)


st.subheader("👉 Monthly wise sub-category sales Summary")

with st.expander("Summary Table"):
    # Basic data table
    st.dataframe(
        df[["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]].head(10),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Month wise Sub-Category Table")
    
    # Extract month name
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    
    # Create pivot table
    sub_category_year = pd.pivot_table(
        data=filtered_df,
        values="Sales",
        index=["Sub-Category"],
        columns="month",
        aggfunc="sum",
        fill_value=0
    ).round(3)
    # Optional: Sort months chronologically
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    sub_category_year = sub_category_year.reindex(columns=month_order, fill_value=0)
    
    # Display with gradient
st.write(
    sub_category_year.style
    .background_gradient(cmap="Blues")
    .format("{:.3f}")
)

# Create a scatter plot
st.subheader("📈 Sales vs Profit Analysis")

fig = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    size="Quantity",
    color="Segment",
    hover_data=["Category", "Sub-Category"],
    opacity=0.6
)

fig.update_layout(
    title="Relationship between Sales and Profits",
    title_font=dict(size=20),
    xaxis_title="Sales ($)",
    yaxis_title="Profit ($)",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("view Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

    
# Download Original Dataset
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name="Data.csv", mime = "text/csv")
