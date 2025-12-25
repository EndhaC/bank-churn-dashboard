import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="Bank Churn Dashboard", layout="wide")

# Title and Intro (Component 1: Text/Title)
st.title("📊 Bank Customer Churn Analysis")
st.markdown("""
This dashboard analyzes the **Bank Churn Dataset** to identify factors contributing to customer attrition.
Use the sidebar to filter data and explore different perspectives.
""")

# --- 2. LOAD DATA ---
@st.cache_data # Caching improves performance
def load_data():
    try:
        df = pd.read_csv('bank_churn_data.csv')
        # Create a numeric Churn column if it doesn't exist
        if 'Attrition_Flag' not in df.columns:
            df['is_churn'] = df['attrition_flag'].apply(lambda x: 1 if x == 'Attrited Customer' else 0)
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("⚠️ File 'bank_churn_data.csv' not found. Please upload it to your project folder.")
    st.stop()

# --- 3. SIDEBAR FILTERS (Component 2: Sidebar & Widgets) ---
st.sidebar.header("Filter Data")

# Filter by Gender
gender_filter = st.sidebar.multiselect(
    "Select Gender:",
    options=df['gender'].unique(),
    default=df['gender'].unique()
)

# Filter by Card Category
card_filter = st.sidebar.multiselect(
    "Select Card Type:",
    options=df['card_category'].unique(),
    default=df['card_category'].unique()
)

# Apply Filters
df_filtered = df.query("gender == @gender_filter & card_category == @card_filter")

# --- 4. KEY METRICS (Component 3: Metric) ---
st.subheader("Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)

total_customers = len(df_filtered)
churn_count = df_filtered['is_churn'].sum()
churn_rate = (churn_count / total_customers) * 100 if total_customers > 0 else 0

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churn_count:,}")
col3.metric("Churn Rate", f"{churn_rate:.2f}%")

st.divider()

# --- 5. INTERACTIVE CHARTS (Component 4: Pyplot/Charts) ---
st.subheader("🔍 Deep Dive Analysis")

# User chooses what to plot (Interactivity Requirement)
chart_choice = st.selectbox(
    "Choose a variable to visualize against Churn:",
    ["education_level", "income_category", "marital_status", "contacts_count_12_mon"]
)

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown(f"**Churn Distribution by {chart_choice}**")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Check if data is numeric or categorical for better plotting
    if pd.api.types.is_numeric_dtype(df_filtered[chart_choice]):
        sns.histplot(data=df_filtered, x=chart_choice, hue="attrition_flag", kde=True, ax=ax, palette="coolwarm")
    else:
        sns.countplot(data=df_filtered, x=chart_choice, hue="attrition_flag", ax=ax, palette="coolwarm")
        plt.xticks(rotation=45)
    
    st.pyplot(fig)

with row1_col2:
    st.markdown("**Income vs Credit Limit (Scatter)**")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df_filtered, x='total_trans_amt', y='total_trans_ct', hue='attrition_flag', alpha=0.6, ax=ax2)
    plt.title("Transaction Amount vs Count")
    st.pyplot(fig2)

# --- 6. RAW DATA VIEW (Component 5: Dataframe & Expander) ---
st.subheader("📂 Raw Data Explorer")
with st.expander("Click to view raw data"):
    st.dataframe(df_filtered)

# Footer
st.markdown("---")
st.caption("Dashboard created with Streamlit")