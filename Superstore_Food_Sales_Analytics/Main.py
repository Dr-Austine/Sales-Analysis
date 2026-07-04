import os
import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_option_menu import option_menu  # Fixed missing import

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Superstore Food Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# ============================================
# LOAD DATA
# ============================================

@st.cache_data
def load_data():
    # 1. Finds the folder where Main.py is currently running
    current_dir = os.path.dirname(__file__)
    
    # 2. Builds a dynamic path to the data folder
    path = os.path.join(current_dir, "data", "data.csv")
    
    # 3. Read and process the data
    df = pd.read_csv(path)
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    return df
# ============================================
# FUNCTION TO EXPORT TO EXCEL
# ============================================
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Load the dataset
df = load_data()

# ============================================
# COMBINED SIDEBAR (Navigation & Filters)
# ============================================
with st.sidebar:
    # Brand logo at the top - Fixed broken closing quote syntax
    st.image(
        r"C:\Users\HomePC\Documents\Sch\Programming\Prog\Visual Studio\Projects\Streamlit\Superstore Food Sales Analytics\data\Logo.jpg",
        caption="Superstore Analytics"
    )
    
    # Navigation menu
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dashboard", "Exploratory Analysis", "Data Viewer"],
        icons=["house", "graph-up-arrow", "table"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )
    
    st.divider()
    st.title("Filters")

    start_date = st.date_input(
        "Start Date",
        value=df["OrderDate"].min().date()
    )

    end_date = st.date_input(
        "End Date",
        value=df["OrderDate"].max().date()
    )

# ============================================
# FILTER DATA
# ============================================
df2 = df[
    (df["OrderDate"] >= pd.to_datetime(start_date)) &
    (df["OrderDate"] <= pd.to_datetime(end_date))
]

# Check if filtered data is empty
if df2.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

# ============================================
# DASHBOARD PAGE
# ============================================
if selected == "Dashboard":  # Fixed variable from 'page' to 'selected'

    st.title("🛒 Superstore Food Sales Analytics Dashboard")
    st.info(f"Showing analytics from **{start_date}** to **{end_date}**")

    # ==================================================
    # KPI SECTION
    # ==================================================
    st.subheader("📈 Key Performance Indicators")
    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        with st.container(border=True):
            st.metric("💰 Sales", f"${df2['TotalPrice'].sum():,.2f}")

    with k2:
        with st.container(border=True):
            st.metric("📦 Quantity Sold", f"{df2['Quantity'].sum():,}")

    with k3:
        with st.container(border=True):
            st.metric("💵 Average Sale", f"${df2['TotalPrice'].mean():,.2f}")

    with k4:
        with st.container(border=True):
            st.metric("🍪 Products", df2["Product"].nunique())

    with k5:
        with st.container(border=True):
            st.metric("🏙️ Cities", df2["City"].nunique())

    # ==================================================
    # SUMMARY SECTION
    # ==================================================
    st.subheader("📝 Executive Summary")

    total_sales = df2["TotalPrice"].sum()
    total_quantity = df2["Quantity"].sum()
    top_product = df2.groupby("Product")["TotalPrice"].sum().idxmax()
    top_city = df2.groupby("City")["TotalPrice"].sum().idxmax()
    top_category = df2.groupby("Category")["TotalPrice"].sum().idxmax()

    st.success(
        f"""
        • Total Sales Generated: ${total_sales:,.2f}
        • Total Units Sold: {total_quantity:,}
        • Top Performing Product: {top_product}
        • Highest Revenue City: {top_city}
        • Best Performing Category: {top_category}
        """
    )

    st.divider()
    a1, a2 = st.columns(2)

    # ==================================================
    # PRODUCT QUANTITY CHART
    # ==================================================
    with a1:
        st.subheader("📦 Product Quantities")
        product_sales = (
            df2.groupby("Product", as_index=False)["Quantity"]
            .sum()
            .sort_values("Quantity", ascending=False)
        )

        bar_chart = (
            alt.Chart(product_sales)
            .mark_bar()
            .encode(
                x=alt.X("Quantity:Q", title="Total Quantity"),
                y=alt.Y("Product:N", sort="-x"),
                tooltip=["Product", "Quantity"]
            )
            .properties(height=450)
        )
        st.altair_chart(bar_chart, use_container_width=True)

    # ==================================================
    # SALES BY CATEGORY
    # ==================================================
    with a2:
        st.subheader("🥧 Sales by Category")
        category_sales = df2.groupby("Category", as_index=False)["TotalPrice"].sum()

        pie_chart = (
            alt.Chart(category_sales)
            .mark_arc()
            .encode(
                theta="TotalPrice:Q",
                color="Category:N",
                tooltip=["Category", "TotalPrice"]
            )
            .properties(height=450)
        )
        st.altair_chart(pie_chart, use_container_width=True)

    # ==================================================
    # SALES TREND
    # ==================================================
    st.subheader("📈 Monthly Sales Trend")
    monthly_sales = (
        df2.groupby(pd.Grouper(key="OrderDate", freq="ME"))["TotalPrice"]
        .sum()
        .reset_index()
    )

    trend_chart = (
        alt.Chart(monthly_sales)
        .mark_line(point=True)
        .encode(
            x="OrderDate:T",
            y="TotalPrice:Q",
            tooltip=["OrderDate", "TotalPrice"]
        )
        .properties(height=450)
    )
    st.altair_chart(trend_chart, use_container_width=True)

# ============================================
# EXPLORATORY ANALYSIS PAGE
# ============================================
elif selected == "Exploratory Analysis":

    st.header("🔍 Exploratory Analysis")

    # ==================================================
    # EXPORT SECTION
    # ==================================================
    st.subheader("📥 Export Data")
    col_export1, col_export2 = st.columns(2)

    with col_export1:
        csv = df2.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download CSV",
            csv,
            "filtered_sales_data.csv",
            "text/csv",
            use_container_width=True
        )

    with col_export2:
        excel_file = to_excel(df2)
        st.download_button(
            "📊 Download Excel",
            excel_file,
            "filtered_sales_data.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.divider()

    # ==================================================
    # RAW DATA
    # ==================================================
    with st.expander("👀 View Raw Data"):
        st.dataframe(df2, use_container_width=True)

    # ==================================================
    # DATA EXPLORER
    # ==================================================
    with st.expander("🔎 Interactive Data Explorer"):
        filtered_df = dataframe_explorer(df2, case=False)
        st.dataframe(filtered_df, use_container_width=True)

    st.divider()
    b1, b2 = st.columns(2)

    # ==================================================
    # SCATTER CHART
    # ==================================================
    with b1:
        st.subheader("Product & Total Price", divider="rainbow")
        scatter_chart = (
            alt.Chart(df2)
            .mark_circle(size=80)
            .encode(
                x="Product:N",
                y="TotalPrice:Q",
                color="Category:N",
                tooltip=["Product", "Category", "TotalPrice"]
            )
            .interactive()
        )
        st.altair_chart(scatter_chart, use_container_width=True)

    # ==================================================
    # UNIT PRICE ANALYSIS
    # ==================================================
    with b2:
        st.subheader("Unit Price Analysis", divider="rainbow")
        source = df2.copy()
        source["Month"] = source["OrderDate"].dt.strftime("%b")
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        unit_price_chart = (
            alt.Chart(source)
            .mark_bar()
            .encode(
                x=alt.X("Month:N", sort=month_order, title="Month"),
                y=alt.Y("mean(UnitPrice):Q", title="Average Unit Price ($)"),
                color="Product:N",
                tooltip=["Month", "Product", "mean(UnitPrice)"]
            )
            .properties(height=450)
        )
        st.altair_chart(unit_price_chart, use_container_width=True)

    st.divider()
    c1, c2 = st.columns(2)

    # ==================================================
    # INTERACTIVE SCATTER
    # ==================================================
    with c1:
        st.subheader("Interactive Scatter Plot", divider="rainbow")
        numeric_cols = list(df2.select_dtypes(include="number").columns)

        feature_x = st.selectbox("Select X Axis", numeric_cols, key="x")
        feature_y = st.selectbox("Select Y Axis", numeric_cols, key="y")

        fig, ax = plt.subplots(figsize=(8, 5))
        
        if len(df2["Product"].unique()) > 1:
            sns.scatterplot(
                data=df2, x=feature_x, y=feature_y, hue="Product", ax=ax, palette="viridis"
            )
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            sns.scatterplot(data=df2, x=feature_x, y=feature_y, ax=ax, color="blue")
        
        ax.set_title(f"{feature_x} vs {feature_y}")
        ax.set_xlabel(feature_x)
        ax.set_ylabel(feature_y)
        st.pyplot(fig)

    # ==================================================
    # FREQUENCY ANALYSIS
    # ==================================================
    with c2:
        st.subheader("Feature Frequency", divider="rainbow")
        feature = st.selectbox(
            "Select Qualitative Feature",
            df2.select_dtypes(include="object").columns,
            key="feature"
        )

        fig, ax = plt.subplots(figsize=(8, 5))
        value_counts = df2[feature].value_counts()
        
        sns.countplot(
            data=df2, x=feature, order=value_counts.index, palette="viridis", ax=ax
        )
        plt.xticks(rotation=45, ha='right')
        ax.set_title(f"Frequency of {feature}")
        ax.set_xlabel(feature)
        ax.set_ylabel("Count")
        
        for p in ax.patches:
            ax.annotate(
                f'{int(p.get_height())}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points'
            )
        st.pyplot(fig)

# ============================================
# DATA VIEWER PAGE
# ============================================
elif selected == "Data Viewer":
    st.header("🗂️ Data Viewer")
    st.dataframe(df2, use_container_width=True)

st.divider()
st.caption("📊 Superstore Food Sales Analytics Dashboard | Powered by Streamlit")
