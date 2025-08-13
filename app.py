# sales_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ===== Page Config =====
st.set_page_config(page_title="📊 Sales Dashboard", page_icon="📈", layout="wide")

# ===== Generate Sample Data =====
@st.cache_data
def load_data():
    dates = pd.date_range("2024-01-01", periods=180, freq="D")
    categories = ["Electronics", "Clothing", "Groceries", "Books"]
    data = {
        "Date": np.random.choice(dates, 500),
        "Category": np.random.choice(categories, 500),
        "Sales": np.random.randint(100, 2000, 500),
        "Profit": np.random.randint(20, 500, 500),
    }
    return pd.DataFrame(data)

df = load_data()

# ===== Sidebar Filters =====
st.sidebar.header("🔍 Filters")
start_date = st.sidebar.date_input("Start Date", df["Date"].min())
end_date = st.sidebar.date_input("End Date", df["Date"].max())
category_filter = st.sidebar.multiselect("Select Category", df["Category"].unique(), default=df["Category"].unique())

# ===== Filter Data =====
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date)) &
    (df["Category"].isin(category_filter))
]

# ===== Dashboard =====
st.title("📊 Sales Dashboard")
st.markdown(f"Showing data from **{start_date}** to **{end_date}** for categories: **{', '.join(category_filter)}**")

# KPIs
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
avg_profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("📊 Profit Margin", f"{avg_profit_margin:.2f}%")

# ===== Charts =====
col1, col2 = st.columns(2)

with col1:
    fig_sales = px.line(filtered_df.groupby("Date")["Sales"].sum().reset_index(),
                        x="Date", y="Sales", title="Daily Sales Over Time")
    st.plotly_chart(fig_sales, use_container_width=True)

with col2:
    fig_profit = px.bar(filtered_df.groupby("Category")["Profit"].sum().reset_index(),
                        x="Category", y="Profit", title="Profit by Category")
    st.plotly_chart(fig_profit, use_container_width=True)

# Pie chart
fig_pie = px.pie(filtered_df, names="Category", values="Sales", title="Sales Distribution by Category")
st.plotly_chart(fig_pie, use_container_width=True)

# ===== Data Table =====
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered_df)
