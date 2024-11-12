# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from sklearn.model_selection import train_test_split

# Configure page
st.set_page_config(page_title="Milk Production Dashboard", layout="centered")

# Title and description
st.title("🥛 Milk Production Analysis Dashboard")
st.markdown("""
Analyze monthly milk production data with simple and exponential moving averages. 
Get insights into trends and generate forecasts!
""")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file with milk production data", type="csv")

# When a file is uploaded, load and process data
if uploaded_file:
    # Load data and display a preview
    data = pd.read_csv(uploaded_file, index_col='Month', parse_dates=True)
    data.rename(columns={"Monthly milk production (pounds per cow)": "Milk Production"}, inplace=True)
    st.write("Data Preview:")
    st.dataframe(data.head())

    # Calculate moving averages
    data['SMA_12'] = data['Milk Production'].rolling(window=12).mean()
    data['SMA_12_shifted'] = data['SMA_12'].shift(1)
    data['EMA_12'] = data['Milk Production'].ewm(span=12, adjust=False).mean()
    data['EMA_12_shifted'] = data['EMA_12'].shift(1)
    data['Custom_EMA_0.6'] = data['Milk Production'].ewm(alpha=0.6, adjust=False).mean()
    data['Custom_EMA_0.6_shifted'] = data['Custom_EMA_0.6'].shift(1)

    # Interactive line plot with Plotly
    st.subheader("Milk Production and Moving Averages")
    plot_cols = ['Milk Production', 'SMA_12', 'EMA_12', 'Custom_EMA_0.6']
    selected_cols = st.multiselect("Select metrics to plot:", plot_cols, default=plot_cols)
    fig = px.line(data, x=data.index, y=selected_cols, 
                  title="Milk Production with Various Moving Averages",
                  labels={'value': 'Milk Production (pounds)', 'index': 'Month'})
    st.plotly_chart(fig)

    # Histogram for milk production
    st.subheader("Milk Production Histogram")
    bins = st.slider("Select number of bins:", 10, 50, 20)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(data['Milk Production'], bins=bins, color='skyblue', edgecolor='black')
    ax.set_title("Distribution of Milk Production")
    ax.set_xlabel("Milk Production (pounds)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Bar chart for seasonal analysis
    st.subheader("Monthly Production Overview")
    monthly_avg = data['Milk Production'].groupby(data.index.month).mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(monthly_avg.index, monthly_avg, color='lightcoral')
    ax.set_title("Average Milk Production by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Production (pounds)")
    st.pyplot(fig)

    # Train-Test Split for Forecasting
    st.subheader("Forecasting with Simple Exponential Smoothing")
    data.index = pd.date_range(start=data.index[0], periods=len(data), freq='MS')
    train, test = train_test_split(data, test_size=0.2, shuffle=False)

    # Forecasting with Simple Exponential Smoothing
    model = SimpleExpSmoothing(train['Milk Production'])
    fitted_model = model.fit(smoothing_level=0.1, optimized=False)
    forecast = fitted_model.forecast(steps=len(test))

    # Display actual vs forecasted data
    forecast_df = pd.DataFrame({'Actual': test['Milk Production'], 'Forecast': forecast})
    st.line_chart(forecast_df)

    # Display data preview and forecast results
    st.write("Preview of Forecast Results")
    st.dataframe(forecast_df.head())
    
    st.markdown("### Download Forecast Data")
    st.download_button(label="Download Forecast", data=forecast_df.to_csv(), file_name="forecast.csv")

else:
    st.info("Please upload a CSV file to proceed with the analysis.")
