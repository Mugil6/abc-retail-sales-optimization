import pandas as pd
import streamlit as st
import plotly.express as px
import calendar

# Load Data
df = pd.read_csv("train.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M')
df['DayOfWeek'] = df['Date'].dt.day_name()

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
st.title(" Retail Sales Dashboard")

# Sidebar filters
store_filter = st.sidebar.multiselect("Select Store(s)", options=df['Store'].unique(), default=df['Store'].unique())
df = df[df['Store'].isin(store_filter)]

# KPIs
total_sales = df['Sales'].sum()
avg_sales = df['Sales'].mean()
st.metric("Total Sales", f"{total_sales:,.0f}")
st.metric("Average Daily Sales", f"{avg_sales:,.0f}")

# Sales trend line
st.subheader("Sales Trend Over Time")
sales_trend = df.groupby('Date')['Sales'].sum().reset_index()
fig1 = px.line(sales_trend, x='Date', y='Sales', title="Daily Sales")
st.plotly_chart(fig1, use_container_width=True)

# Monthly Bar Plot
st.subheader(" Monthly Sales Summary")
monthly_sales = df.groupby('Month')['Sales'].sum().reset_index()
monthly_sales['Month'] = monthly_sales['Month'].astype(str)
fig2 = px.bar(monthly_sales, x='Month', y='Sales', title="Monthly Sales Total")
st.plotly_chart(fig2, use_container_width=True)

# Heatmap of sales per store and weekday
st.subheader("Sales Heatmap (Store vs Day of Week)")
heatmap_data = df.groupby(['Store', 'DayOfWeek'])['Sales'].mean().reset_index()
heatmap_pivot = heatmap_data.pivot(index='Store', columns='DayOfWeek', values='Sales').fillna(0)
heatmap_pivot = heatmap_pivot[["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
st.dataframe(heatmap_pivot.style.background_gradient(cmap='YlOrRd'), height=500)


# Forecast Section
st.header("Sales Forecast for Next Month")

try:
    forecast_df = pd.read_csv("next_month_forecast_all_stores.csv")

    st.subheader("Forecast Summary Table")
    st.dataframe(forecast_df)

    st.subheader("Predicted Sales per Store")
    if "Store" in forecast_df.columns and "Predicted_Total_Sales" in forecast_df.columns:
        chart_df = forecast_df[["Store", "Predicted_Total_Sales"]].set_index("Store")
        st.bar_chart(chart_df)
    else:
        st.warning("Columns 'Store' or 'Predicted_Total_Sales' not found in forecast file.")

    st.markdown(f"**Forecast Month:** {forecast_df['Forecast_Month'].iloc[0]}")

except FileNotFoundError:
    st.error("Forecast file not found. Please ensure 'next_month_forecast_all_stores.csv' is in the same folder as this app.")
except Exception as e:
    st.error(f"An error occurred: {e}")


