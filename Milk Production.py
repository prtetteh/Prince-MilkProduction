# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Set up page configuration
st.set_page_config(page_title="Business Dashboard", page_icon="📊", layout="wide")

# 1.0 Title and Introduction
st.markdown("<h1 style='color: mediumvioletred;'>🌟 Business Dashboard 🌟</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color: darkblue; font-size: 20px;'>This dashboard provides insights into sales, customer demographics, and product performance. "
    "Upload your data to get started.</p>",
    unsafe_allow_html=True
)

# 2.0 Data Input
st.sidebar.header("Upload Business Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv", accept_multiple_files=False)

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.sidebar.success("Data loaded successfully!")
    
    # Show a preview of the data
    st.markdown("<h2 style='color: teal;'>📄 Data Preview</h2>", unsafe_allow_html=True)
    st.write(data.head())

    # Chart selection and customizations
    st.sidebar.header("Chart Customization")
    st.sidebar.markdown("<p style='color: darkorange;'><strong>Select the type of chart and columns to visualize:</strong></p>", unsafe_allow_html=True)

    chart_type = st.sidebar.selectbox("Choose a chart type:", ["Line Chart", "Bar Chart", "Histogram", "Pie Chart"])

    # X-axis and Y-axis selection for certain charts
    x_axis = st.sidebar.selectbox("Select X-axis column:", data.columns)
    y_axis = st.sidebar.selectbox("Select Y-axis column:", data.columns)

    # Dynamic visualization based on selected chart type
    st.markdown(f"<h2 style='color: darkorange;'>📊 {chart_type}</h2>", unsafe_allow_html=True)

    # Sales Line Chart
    if chart_type == "Line Chart":
        fig = px.line(
            data, x=x_axis, y=y_axis, 
            title=f"{y_axis} Over {x_axis}", 
            color_discrete_sequence=["#FF7F50"]
        )
        st.plotly_chart(fig, use_container_width=True)

    # Bar Chart for comparison
    elif chart_type == "Bar Chart":
        fig = px.bar(
            data, x=x_axis, y=y_axis, 
            color=x_axis, title=f"{y_axis} by {x_axis}", 
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig, use_container_width=True)

    # Histogram for data distribution
    elif chart_type == "Histogram":
        fig = px.histogram(
            data, x=x_axis, nbins=20,
            title=f"Distribution of {x_axis}", 
            color_discrete_sequence=["#1f77b4"]
        )
        st.plotly_chart(fig, use_container_width=True)

    # Pie Chart for segmentation
    elif chart_type == "Pie Chart":
        fig = px.pie(
            data, names=x_axis, values=y_axis, 
            title=f"{y_axis} by {x_axis} Segmentation",
            color_discrete_sequence=px.colors.sequential.Sunset
        )
        st.plotly_chart(fig, use_container_width=True)

    # Additional Pre-built Analyses
    st.markdown("<h2 style='color: darkgreen;'>📈 Pre-built Insights</h2>", unsafe_allow_html=True)

    # Sales over time if applicable
    if 'sales_date' in data.columns and 'sales_amount' in data.columns:
        fig_sales = px.line(
            data, x='sales_date', y='sales_amount', 
            title="Sales Over Time", color_discrete_sequence=["#FF6347"]
        )
        st.plotly_chart(fig_sales, use_container_width=True)

    # Customer Segmentation by Region
    if 'region' in data.columns and 'sales_amount' in data.columns:
        fig_region = px.pie(
            data, names='region', values='sales_amount', 
            title="Customer Segmentation by Region", color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_region, use_container_width=True)

    # Product Analysis
    if 'product' in data.columns and 'sales_amount' in data.columns:
        top_products_df = data.groupby('product').sum()['sales_amount'].nlargest(10)
        fig_products = px.bar(
            top_products_df, x=top_products_df.index, y='sales_amount', 
            title="Top 10 Products by Sales", color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_products, use_container_width=True)

    # Feedback Form
    st.markdown("<h2 style='color: purple;'>💬 Feedback</h2>", unsafe_allow_html=True)
    feedback = st.text_area("Please provide any feedback or suggestions.")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

# Footer
st.write("---")
st.write("This business dashboard template is flexible and customizable for your specific business needs.")
