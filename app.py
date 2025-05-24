import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load data
df = pd.read_excel("https://github.com/GayasuddinMohd/Matiks-Data-Analyst/blob/main/Matiks%20-%20Data%20Analyst%20Data.xlsx\\Matiks - Data Analyst Data.xlsx")

# Preprocess dates
df['Signup_Date'] = pd.to_datetime(df['Signup_Date'])
df['Last_Login'] = pd.to_datetime(df['Last_Login'])
df['Month'] = df['Last_Login'].dt.to_period('M').dt.to_timestamp()
df['Week'] = df['Last_Login'].dt.to_period('W').dt.start_time
df['Day'] = df['Last_Login'].dt.date

# Sidebar filters
st.sidebar.header("Filters")
selected_device = st.sidebar.multiselect("Device Type", options=df['Device_Type'].unique(), default=df['Device_Type'].unique())
selected_mode = st.sidebar.multiselect("Game Mode", options=df['Preferred_Game_Mode'].unique(), default=df['Preferred_Game_Mode'].unique())

filtered_df = df[df['Device_Type'].isin(selected_device) & df['Preferred_Game_Mode'].isin(selected_mode)]

st.title("🎮 Matiks User Analytics Dashboard")

# KPIs
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

dau = filtered_df['Day'].nunique()
wau = filtered_df['Week'].nunique()
mau = filtered_df['Month'].nunique()

col1.metric("DAU", dau)
col2.metric("WAU", wau)
col3.metric("MAU", mau)

# Revenue Trends
st.subheader("💰 Revenue Trends Over Time")
revenue_trend = filtered_df.groupby('Month')['Total_Revenue_USD'].sum().reset_index()
fig_revenue = px.line(revenue_trend, x='Month', y='Total_Revenue_USD', title="Monthly Revenue")
st.plotly_chart(fig_revenue)

# Breakdown by Device Type
st.subheader("📱 Revenue by Device Type")
device_revenue = filtered_df.groupby('Device_Type')['Total_Revenue_USD'].sum().reset_index()
fig_device = px.bar(device_revenue, x='Device_Type', y='Total_Revenue_USD', color='Device_Type', title="Revenue by Device")
st.plotly_chart(fig_device)

# Breakdown by Game Mode
st.subheader("🎮 Preferred Game Mode Analysis")
mode_revenue = filtered_df.groupby('Preferred_Game_Mode')['Total_Revenue_USD'].sum().reset_index()
fig_mode = px.pie(mode_revenue, names='Preferred_Game_Mode', values='Total_Revenue_USD', title="Revenue by Game Mode")
st.plotly_chart(fig_mode)

# User Activity Pattern
st.subheader("⏱️ Session Duration vs Play Sessions")
fig_sessions = px.scatter(filtered_df, x='Total_Play_Sessions', y='Avg_Session_Duration_Min',
                          size='Total_Revenue_USD', color='Device_Type',
                          hover_data=['Username', 'Game_Title'], title="Engagement Overview")
st.plotly_chart(fig_sessions)

# High Value Users
st.subheader("💎 Top 5 High-Value Users")
top_users = filtered_df.sort_values(by='Total_Revenue_USD', ascending=False).head(5)
st.dataframe(top_users[['Username', 'Total_Revenue_USD', 'Total_Play_Sessions', 'Preferred_Game_Mode', 'Subscription_Tier']])

# Churn Risk Users
st.subheader("⚠️ Potential Churn Risk Users (No login in last 14 days)")
today = datetime.today()
filtered_df['Days_Since_Last_Login'] = (today - filtered_df['Last_Login']).dt.days
churn_risk = filtered_df[filtered_df['Days_Since_Last_Login'] > 14].sort_values(by='Days_Since_Last_Login', ascending=False).head(10)
st.dataframe(churn_risk[['Username', 'Days_Since_Last_Login', 'Total_Play_Sessions', 'Total_Revenue_USD']])

# Recommendations
st.subheader("📌 Recommendations")
st.markdown("""
- Encourage **Mobile users** with low revenue to explore in-game purchases via promo offers.
- Target **Multiplayer and Co-op users** for seasonal events to boost session count.
- Re-engage users inactive for **14+ days** via email campaigns.
- Retain **top-tier spenders** with exclusive in-game rewards or loyalty programs.
""")
