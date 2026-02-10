import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Retail Store Inventory Analysis",
    layout="wide"
)

st.title("🏬 Retail Store Inventory Dashboard")
st.markdown("Analysis and insights from retail inventory data")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("retail_store_inventory.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Region"].isin(region))
]

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(20))

# -----------------------------
# KPI Metrics
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Products", filtered_df["Product ID"].nunique())
col2.metric("Total Units Sold", int(filtered_df["Units Sold"].sum()))
col3.metric("Avg Inventory Level", round(filtered_df["Inventory Level"].mean(), 2))
col4.metric("Avg Demand Forecast", round(filtered_df["Demand Forecast"].mean(), 2))

# -----------------------------
# EDA Visuals
# -----------------------------
st.subheader("📈 Exploratory Data Analysis")

col1, col2 = st.columns(2)

# Inventory by Category
with col1:
    st.markdown("### Inventory Level by Category")
    inv_cat = filtered_df.groupby("Category")["Inventory Level"].mean()
    fig, ax = plt.subplots()
    inv_cat.plot(kind="bar", ax=ax)
    ax.set_ylabel("Average Inventory Level")
    st.pyplot(fig)

# Units Sold by Region
with col2:
    st.markdown("### Units Sold by Region")
    sold_region = filtered_df.groupby("Region")["Units Sold"].sum()
    fig, ax = plt.subplots()
    sold_region.plot(kind="bar", ax=ax)
    ax.set_ylabel("Total Units Sold")
    st.pyplot(fig)

# -----------------------------
# Trend Analysis
# -----------------------------
st.subheader("📅 Sales Trend Over Time")

daily_sales = filtered_df.groupby("Date")["Units Sold"].sum()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(daily_sales)
ax.set_xlabel("Date")
ax.set_ylabel("Units Sold")
st.pyplot(fig)

# -----------------------------
# Simple Prediction Insight
# -----------------------------
st.subheader("🤖 Demand Insight")

st.markdown("""
This is a **basic analytical prediction** based on historical averages  
(not a trained ML model).
""")

product_id = st.selectbox(
    "Select Product ID",
    filtered_df["Product ID"].unique()
)

product_df = filtered_df[filtered_df["Product ID"] == product_id]

avg_demand = product_df["Demand Forecast"].mean()
avg_sales = product_df["Units Sold"].mean()

st.success(
    f"📦 **Expected Demand:** {avg_demand:.2f} units  \n"
    f"🛒 **Average Units Sold:** {avg_sales:.2f} units"
)

# -----------------------------
# Conclusion
# -----------------------------
st.subheader("✅ Conclusion")

st.markdown("""
- Inventory and sales vary significantly by **category and region**
- Some products show **higher demand forecasts than actual sales**
- This dashboard helps identify:
  - Over-stocked items
  - High-demand products
  - Regional sales patterns
""")

st.markdown("🚀 *Built using Streamlit*")
