import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="Bank Churn Dashboard", layout="wide")

# --- 2. SIDEBAR: PROFILE & FILTERS ---
st.sidebar.header("About Me")

# A. Profile Image
# Make sure you have a file named 'profile.jpg' or 'dp.png' in your folder!
try:
    # Change 'profile.jpg' to your actual file name
    profile_image = Image.open('profile.jpg') 
    st.sidebar.image(profile_image, caption="Data Analyst", use_container_width=True)
except FileNotFoundError:
    st.sidebar.warning("⚠️ Upload an image named 'profile.jpg' to see it here.")

# B. Profile Description
st.sidebar.markdown("""
**Name:** [Your Name]  
**Role:** Data Science Student  
**Goal:** Helping businesses reduce customer churn through data-driven insights.
""")

st.sidebar.divider()

# --- 3. PROJECT EXPLANATION ---
st.title("📊 Bank Customer Churn Analysis")

with st.expander("ℹ️ About this Project (Click to Expand)", expanded=True):
    st.markdown("""
    ### **Project Overview**
    This dashboard analyzes a dataset of bank customers to identify the key reasons why they leave (churn). 
    By understanding these patterns, the bank can take proactive steps to retain valuable customers.
    
    **Key Objectives:**
    * **Visualize** the distribution of churn across demographics (Age, Gender, Income).
    * **Identify** high-risk segments (e.g., specific credit card types or inactivity periods).
    * **Provide** actionable insights for the marketing team.
    
    **Data Source:** Bank Churners Dataset (Kaggle).
    """)

# --- 4. LOAD DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('bank_churn_data.csv')
        if 'Attrition_Flag' not in df.columns:
            df['is_churn'] = df['attrition_flag'].apply(lambda x: 1 if x == 'Attrited Customer' else 0)
        else:
             # Ensure we have a numeric column for calculation
             df['is_churn'] = df['attrition_flag'].apply(lambda x: 1 if x == 'Attrited Customer' else 0)
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("⚠️ File 'bank_churn_data.csv' not found. Please upload it to your project folder.")
    st.stop()

# --- 5. SIDEBAR FILTERS ---
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

# --- 6. KEY METRICS ---
st.subheader("Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)

total_customers = len(df_filtered)
churn_count = df_filtered['is_churn'].sum()
churn_rate = (churn_count / total_customers) * 100 if total_customers > 0 else 0

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churn_count:,}")
col3.metric("Churn Rate", f"{churn_rate:.2f}%")

st.divider()

# --- 7. INTERACTIVE CHARTS ---
st.subheader("🔍 Deep Dive Analysis")

chart_choice = st.selectbox(
    "Choose a variable to visualize against Churn:",
    ["education_level", "income_category", "marital_status", "contacts_count_12_mon"]
)

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown(f"**Churn Distribution by {chart_choice}**")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    if pd.api.types.is_numeric_dtype(df_filtered[chart_choice]):
        sns.histplot(data=df_filtered, x=chart_choice, hue="attrition_flag", kde=True, ax=ax, palette="coolwarm")
    else:
        sns.countplot(data=df_filtered, x=chart_choice, hue="attrition_flag", ax=ax, palette="coolwarm")
        plt.xticks(rotation=45)
    
    st.pyplot(fig)

with row1_col2:
    st.markdown("**Income vs Credit Limit (Scatter)**")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    # Using total_trans_amt and total_trans_ct as proxies for 'Income vs Credit Limit' based on typical dataset fields
    # You can change these x and y values to 'Credit_Limit' or 'Income_Category' if you convert income to numeric
    sns.scatterplot(data=df_filtered, x='total_trans_amt', y='total_trans_ct', hue='attrition_flag', alpha=0.6, ax=ax2)
    plt.title("Transaction Amount vs Count")
    st.pyplot(fig2)

# --- 8. RAW DATA VIEW ---
st.subheader("📂 Raw Data Explorer")
with st.expander("Click to view raw data"):
    st.dataframe(df_filtered)

st.markdown("---")
st.caption("Dashboard created with Streamlit by [Your Name]")
