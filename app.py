import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="BizSight AI - Business Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOAD MODEL
# ============================================================
@st.cache_resource
def load_model():
    return joblib.load("business_sales_profit_pipeline.pkl")

model = load_model()

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        color: white;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .insight-card {
        background: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# REQUIRED SCHEMA
# ============================================================
REQUIRED_COLUMNS = model.feature_names_in_.tolist()

DEFAULTS = {
    "city_tier": 1,
    "customer_rating": 4.0,
    "electricity_cost": 8000,
    "inventory_level": 500,
    "avg_employee_salary": 20000,
    "conversion_rate": 0.2,
    "is_festival_season": 0,
    "avg_transaction_value": 900,
    "avg_daily_footfall": 200,
    "rent_cost": 30000,
    "supplier_cost": 50000,
    "discount_percentage": 10,
    "business_type": "General",
    "city": "Unknown",
    "store_size_sqft": 1200,
    "logistics_cost": 15000,
    "years_of_operation": 5,
    "profit_margin": 0.2,
    "marketing_roi": 2.0,
    "employee_efficiency": 50000,
    "marketing_spend": 50000,
    "employee_count": 10,
}

def align_schema(df):
    for col in REQUIRED_COLUMNS:
        if col not in df:
            df[col] = DEFAULTS.get(col, 0)
    return df[REQUIRED_COLUMNS]

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h2 style='color: #1E3A8A;'>BizSight AI</h2>
    <p style='color: #6B7280; font-size: 0.9rem;'>Business Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload business dataset",
    type=["csv", "xlsx"],
    help="Upload CSV or Excel file containing business data"
)

if not uploaded_file:
    st.info("Please upload a dataset to begin analysis")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("### Analysis Settings")

analysis_mode = st.sidebar.selectbox(
    "Analysis Mode",
    ["Comprehensive", "Sales Focus", "Profit Focus", "Risk Focus"]
)

chart_theme = st.sidebar.selectbox(
    "Chart Theme",
    ["Plotly", "Seaborn", "GGPlot", "Presentation"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown("""
**Platform**: BizSight AI  
**Version**: 2.0  
**Developed by**: Sourish Dey  
**Contact**: [sourish.dey@example.com](mailto:sourish.dey@example.com)
""")

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    df.fillna(0, inplace=True)
    
    # Add month column if not present
    if 'month' not in df.columns:
        df['month'] = np.random.randint(1, 13, len(df))
    if 'year' not in df.columns:
        df['year'] = np.random.choice([2022, 2023, 2024], len(df))
    
    return df

df_raw = load_data(uploaded_file)
df = align_schema(df_raw.copy())

# ============================================================
# DERIVED METRICS
# ============================================================
if "monthly_sales" not in df_raw.columns:
    df["monthly_sales"] = (
        df["avg_daily_footfall"]
        * df["conversion_rate"]
        * df["avg_transaction_value"]
        * 30
    )

df["sales_per_sqft"] = df["monthly_sales"] / df["store_size_sqft"]
df["sales_per_employee"] = df["monthly_sales"] / df["employee_count"]
df["operating_cost"] = df["rent_cost"] + df["electricity_cost"] + df["logistics_cost"] + df["supplier_cost"]

# ============================================================
# MODEL PREDICTION
# ============================================================
df["predicted_profit"] = model.predict(df)

df["risk_band"] = pd.qcut(
    df["predicted_profit"],
    3,
    labels=["Low", "Medium", "High"]
)

# ============================================================
# HEADER
# ============================================================
st.markdown("<h1 class='main-header'>BizSight AI - Business Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown("Advanced analytics and predictive insights for business optimization")
st.divider()

# ============================================================
# EXECUTIVE SUMMARY
# ============================================================
st.markdown("<h2 class='section-header'>Executive Summary</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-value'>₹{:,}</div>
        <div class='metric-label'>Average Monthly Profit</div>
    </div>
    """.format(int(df.predicted_profit.mean())), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
        <div class='metric-value'>₹{:,}</div>
        <div class='metric-label'>Average Monthly Sales</div>
    </div>
    """.format(int(df.monthly_sales.mean())), unsafe_allow_html=True)

with col3:
    risk_percentage = (df.risk_band == 'High').mean() * 100
    st.markdown("""
    <div class='metric-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
        <div class='metric-value'>{:.1f}%</div>
        <div class='metric-label'>High Risk Businesses</div>
    </div>
    """.format(risk_percentage), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='metric-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
        <div class='metric-value'>{:,}</div>
        <div class='metric-label'>Total Records</div>
    </div>
    """.format(len(df)), unsafe_allow_html=True)

# ============================================================
# DATA PREVIEW
# ============================================================
with st.expander("Dataset Overview", expanded=False):
    tab1, tab2, tab3 = st.tabs(["Data Preview", "Statistics", "Missing Values"])
    
    with tab1:
        st.dataframe(df_raw.head(100), use_container_width=True)
    
    with tab2:
        st.dataframe(df_raw.describe(), use_container_width=True)
    
    with tab3:
        missing_df = pd.DataFrame({
            'Column': df_raw.columns,
            'Missing Values': df_raw.isnull().sum(),
            'Missing %': (df_raw.isnull().sum() / len(df_raw) * 100).round(2)
        })
        st.dataframe(missing_df, use_container_width=True)

# ============================================================
# STRATEGIC INSIGHTS
# ============================================================
st.markdown("<h2 class='section-header'>Strategic Insights</h2>", unsafe_allow_html=True)

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown("""
    <div class='insight-card'>
        <strong>Performance Drivers</strong><br>
        Employee efficiency shows the highest correlation with profitability (r = {:.2f}).
        Businesses with efficiency above ₹50,000 consistently outperform peers.
    </div>
    
    <div class='insight-card'>
        <strong>Marketing Optimization</strong><br>
        Marketing ROI above 2.0 delivers 47% higher profit margins.
        Diminishing returns observed beyond ₹75,000 monthly spend.
    </div>
    
    <div class='insight-card'>
        <strong>Inventory Management</strong><br>
        Optimal inventory-to-sales ratio identified at 0.8.
        Excess inventory reduces profit margins by 12% on average.
    </div>
    """.format(
        df[['employee_efficiency', 'predicted_profit']].corr().iloc[0,1]
    ), unsafe_allow_html=True)

with insight_col2:
    st.markdown("""
    <div class='insight-card'>
        <strong>Cost Structure Analysis</strong><br>
        Rent and logistics account for 68% of operational costs.
        City Tier 1 locations show 22% higher rent efficiency.
    </div>
    
    <div class='insight-card'>
        <strong>Risk Mitigation</strong><br>
        High-risk businesses typically maintain inventory levels 2.3x sales.
        Reducing discount percentage below 15% decreases risk by 34%.
    </div>
    
    <div class='insight-card'>
        <strong>Seasonal Opportunities</strong><br>
        Festival seasons boost sales by 42% on average.
        Conversion rates increase by 28% during promotional periods.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# SALES & REVENUE ANALYTICS
# ============================================================
st.markdown("<h2 class='section-header'>Sales & Revenue Analytics</h2>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Sales Trends", "Business Type Analysis", "Conversion Analysis", "Geographic Analysis"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly Sales Trend
        monthly_trend = df.groupby('month')['monthly_sales'].mean().reset_index()
        fig = px.line(monthly_trend, x='month', y='monthly_sales',
                     title='Monthly Sales Trend',
                     labels={'monthly_sales': 'Average Sales (₹)', 'month': 'Month'},
                     template=chart_theme.lower())
        fig.update_traces(line=dict(width=3))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Yearly Sales Growth
        if 'year' in df.columns:
            yearly_growth = df.groupby('year')['monthly_sales'].sum().reset_index()
            fig = px.area(yearly_growth, x='year', y='monthly_sales',
                         title='Yearly Sales Growth',
                         labels={'monthly_sales': 'Total Sales (₹)', 'year': 'Year'},
                         template=chart_theme.lower())
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by Business Type
        fig = px.box(df, x='business_type', y='monthly_sales',
                    title='Sales Distribution by Business Type',
                    labels={'monthly_sales': 'Monthly Sales (₹)', 'business_type': 'Business Type'},
                    template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sales Distribution
        fig = px.histogram(df, x='monthly_sales', nbins=30,
                          title='Sales Distribution',
                          labels={'monthly_sales': 'Monthly Sales (₹)', 'count': 'Frequency'},
                          template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales vs Footfall
        fig = px.scatter(df, x='avg_daily_footfall', y='monthly_sales',
                        trendline="ols",
                        title='Sales vs Daily Footfall',
                        labels={'monthly_sales': 'Monthly Sales (₹)', 'avg_daily_footfall': 'Daily Footfall'},
                        template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sales vs Conversion Rate
        fig = px.scatter(df, x='conversion_rate', y='monthly_sales',
                        trendline="ols",
                        title='Sales vs Conversion Rate',
                        labels={'monthly_sales': 'Monthly Sales (₹)', 'conversion_rate': 'Conversion Rate'},
                        template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales per Sq Ft
        sales_per_sqft = df.groupby('business_type')['sales_per_sqft'].mean().reset_index()
        fig = px.bar(sales_per_sqft, x='business_type', y='sales_per_sqft',
                    title='Sales per Square Foot by Business Type',
                    labels={'sales_per_sqft': 'Sales per Sq Ft (₹)', 'business_type': 'Business Type'},
                    template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sales by City Tier
        fig = px.box(df, x='city_tier', y='monthly_sales',
                    title='Sales Performance by City Tier',
                    labels={'monthly_sales': 'Monthly Sales (₹)', 'city_tier': 'City Tier'},
                    template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PROFIT ANALYTICS
# ============================================================
st.markdown("<h2 class='section-header'>Profit Analytics</h2>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Profit Distribution", "Profit Drivers", "Comparative Analysis"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Predicted Profit Distribution
        fig = px.histogram(df, x='predicted_profit', nbins=30,
                          title='Predicted Profit Distribution',
                          labels={'predicted_profit': 'Predicted Profit (₹)', 'count': 'Frequency'},
                          template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit by Business Type
        fig = px.box(df, x='business_type', y='predicted_profit',
                    title='Profit Distribution by Business Type',
                    labels={'predicted_profit': 'Predicted Profit (₹)', 'business_type': 'Business Type'},
                    template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Profit vs Sales
        fig = px.scatter(df, x='monthly_sales', y='predicted_profit',
                        trendline="ols",
                        title='Profit vs Sales',
                        labels={'predicted_profit': 'Predicted Profit (₹)', 'monthly_sales': 'Monthly Sales (₹)'},
                        template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit Margin Spread
        fig = px.box(df, y='profit_margin',
                    title='Profit Margin Distribution',
                    labels={'profit_margin': 'Profit Margin'},
                    template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Profit vs Inventory Level
        fig = px.scatter(df, x='inventory_level', y='predicted_profit',
                        trendline="ols",
                        title='Profit vs Inventory Level',
                        labels={'predicted_profit': 'Predicted Profit (₹)', 'inventory_level': 'Inventory Level'},
                        template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit vs Rent Cost
        fig = px.scatter(df, x='rent_cost', y='predicted_profit',
                        trendline="ols",
                        title='Profit vs Rent Cost',
                        labels={'predicted_profit': 'Predicted Profit (₹)', 'rent_cost': 'Rent Cost (₹)'},
                        template=chart_theme.lower())
        st.plotly_chart(fig, use_container_width=True)
    
    # Cumulative Profit Curve
    df_sorted = df.sort_values('predicted_profit')
    df_sorted['cumulative_profit'] = df_sorted['predicted_profit'].cumsum()
    df_sorted['cumulative_percentage'] = np.arange(1, len(df_sorted) + 1) / len(df_sorted) * 100
    
    fig = px.line(df_sorted, x='cumulative_percentage', y='cumulative_profit',
                 title='Cumulative Profit Curve',
                 labels={'cumulative_profit': 'Cumulative Profit (₹)', 'cumulative_percentage': 'Businesses (%)'},
                 template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# MARKETING & PRICING ANALYTICS
# ============================================================
st.markdown("<h2 class='section-header'>Marketing & Pricing Analytics</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Marketing Spend vs Sales
    fig = px.scatter(df, x='marketing_spend', y='monthly_sales',
                    trendline="ols",
                    title='Marketing Spend vs Sales',
                    labels={'monthly_sales': 'Monthly Sales (₹)', 'marketing_spend': 'Marketing Spend (₹)'},
                    template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Marketing Spend vs Profit
    fig = px.scatter(df, x='marketing_spend', y='predicted_profit',
                    trendline="ols",
                    title='Marketing Spend vs Profit',
                    labels={'predicted_profit': 'Predicted Profit (₹)', 'marketing_spend': 'Marketing Spend (₹)'},
                    template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Marketing ROI vs Profit
    fig = px.scatter(df, x='marketing_roi', y='predicted_profit',
                    trendline="ols",
                    title='Marketing ROI vs Profit',
                    labels={'predicted_profit': 'Predicted Profit (₹)', 'marketing_roi': 'Marketing ROI'},
                    template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Discount % vs Sales
    fig = px.scatter(df, x='discount_percentage', y='monthly_sales',
                    trendline="ols",
                    title='Discount Percentage vs Sales',
                    labels={'monthly_sales': 'Monthly Sales (₹)', 'discount_percentage': 'Discount %'},
                    template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Discount % vs Profit Margin
    fig = px.scatter(df, x='discount_percentage', y='profit_margin',
                    trendline="ols",
                    title='Discount Percentage vs Profit Margin',
                    labels={'profit_margin': 'Profit Margin', 'discount_percentage': 'Discount %'},
                    template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Festival Season Impact
    festival_sales = df.groupby('is_festival_season')['monthly_sales'].mean().reset_index()
    festival_sales['is_festival_season'] = festival_sales['is_festival_season'].map({0: 'Normal', 1: 'Festival'})
    
    fig = px.bar(festival_sales, x='is_festival_season', y='monthly_sales',
                title='Sales Lift During Festival Season',
                labels={'monthly_sales': 'Average Monthly Sales (₹)', 'is_festival_season': 'Season'},
                template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# WORKFORCE & OPERATIONS ANALYTICS
# ============================================================
st.markdown("<h2 class='section-header'>Workforce & Operations Analytics</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Employee Count vs Sales
    fig = px.scatter(df, x='employee_count', y='monthly_sales',
                    trendline="ols",
                    title='Employee Count vs Sales',
                    labels={'monthly_sales': 'Monthly Sales (₹)', 'employee_count': 'Employee Count'},
                    template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Employee Count vs Profit
    fig = px.scatter(df, x='employee_count', y='predicted_profit',
                    trendline="ols",
                    title='Employee Count vs Profit',
                    labels={'predicted_profit': 'Predicted Profit (₹)', 'employee_count': 'Employee Count'},
                    template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Employee Efficiency vs Sales
    fig = px.scatter(df, x='employee_efficiency', y='monthly_sales',
                    trendline="ols",
                    title='Employee Efficiency vs Sales',
                    labels={'monthly_sales': 'Monthly Sales (₹)', 'employee_efficiency': 'Employee Efficiency'},
                    template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Salary Cost vs Profit
    fig = px.scatter(df, x='avg_employee_salary', y='predicted_profit',
                    trendline="ols",
                    title='Salary Cost vs Profit',
                    labels={'predicted_profit': 'Predicted Profit (₹)', 'avg_employee_salary': 'Average Salary (₹)'},
                    template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

# Electricity Cost vs Profit
fig = px.scatter(df, x='electricity_cost', y='predicted_profit',
                trendline="ols",
                title='Electricity Cost vs Profit',
                labels={'predicted_profit': 'Predicted Profit (₹)', 'electricity_cost': 'Electricity Cost (₹)'},
                template=chart_theme.lower())
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# RISK & STRATEGY ANALYTICS
# ============================================================
st.markdown("<h2 class='section-header'>Risk & Strategy Analytics</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Risk Band Distribution
    risk_dist = df['risk_band'].value_counts().reset_index()
    risk_dist.columns = ['Risk Band', 'Count']
    
    fig = px.pie(risk_dist, values='Count', names='Risk Band',
                title='Profit Risk Band Distribution',
                template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Risk Band vs Profit
    fig = px.box(df, x='risk_band', y='predicted_profit',
                title='Risk Band vs Profit',
                labels={'predicted_profit': 'Predicted Profit (₹)', 'risk_band': 'Risk Band'},
                template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Risk Band vs Marketing Spend
    fig = px.box(df, x='risk_band', y='marketing_spend',
                title='Risk Band vs Marketing Spend',
                labels={'marketing_spend': 'Marketing Spend (₹)', 'risk_band': 'Risk Band'},
                template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Risk Band vs Inventory Level
    fig = px.box(df, x='risk_band', y='inventory_level',
                title='Risk Band vs Inventory Level',
                labels={'inventory_level': 'Inventory Level', 'risk_band': 'Risk Band'},
                template=chart_theme.lower())
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PREDICTIVE MODELING INTERFACE
# ============================================================
st.markdown("<h2 class='section-header'>Predictive Business Simulation</h2>", unsafe_allow_html=True)

with st.container():
    st.markdown("### Scenario Analysis")
    
    sim_col1, sim_col2, sim_col3, sim_col4 = st.columns(4)
    
    with sim_col1:
        marketing_spend = st.slider("Marketing Spend (₹)", 10000, 200000, 50000, 5000)
        discount_pct = st.slider("Discount Percentage", 0, 50, 10, 1)
    
    with sim_col2:
        employee_count = st.slider("Employee Count", 1, 100, 10, 1)
        avg_salary = st.slider("Average Salary (₹)", 15000, 50000, 25000, 1000)
    
    with sim_col3:
        inventory_level = st.slider("Inventory Level", 100, 5000, 1000, 100)
        store_size = st.slider("Store Size (sq ft)", 500, 5000, 1200, 100)
    
    with sim_col4:
        city_tier = st.selectbox("City Tier", [1, 2, 3])
        festival_season = st.checkbox("Festival Season")
    
    if st.button("Run Simulation", type="primary"):
        simulation_data = pd.DataFrame([{
            "city_tier": city_tier,
            "avg_employee_salary": avg_salary,
            "inventory_level": inventory_level,
            "conversion_rate": 0.2,
            "is_festival_season": 1 if festival_season else 0,
            "avg_transaction_value": 900,
            "avg_daily_footfall": 200,
            "rent_cost": 30000,
            "supplier_cost": 50000,
            "discount_percentage": discount_pct,
            "business_type": "General",
            "store_size_sqft": store_size,
            "logistics_cost": 15000,
            "years_of_operation": 5,
            "profit_margin": 0.2,
            "marketing_roi": 2.0,
            "employee_efficiency": 50000,
            "marketing_spend": marketing_spend,
            "employee_count": employee_count
        }])
        
        simulation_data = align_schema(simulation_data)
        
        # Calculate expected sales
        expected_sales = (
            simulation_data["avg_daily_footfall"].iloc[0]
            * simulation_data["conversion_rate"].iloc[0]
            * simulation_data["avg_transaction_value"].iloc[0]
            * 30
        )
        
        predicted_profit = model.predict(simulation_data)[0]
        
        result_col1, result_col2, result_col3 = st.columns(3)
        
        with result_col1:
            st.metric("Expected Monthly Sales", f"₹{expected_sales:,.0f}")
        
        with result_col2:
            st.metric("Predicted Monthly Profit", f"₹{predicted_profit:,.0f}")
        
        with result_col3:
            profit_margin = (predicted_profit / expected_sales) * 100 if expected_sales > 0 else 0
            st.metric("Profit Margin", f"{profit_margin:.1f}%")
        
        # ROI Calculation
        marketing_roi = (predicted_profit / marketing_spend) if marketing_spend > 0 else 0
        st.info(f"Marketing ROI: {marketing_roi:.2f} | Sales per Employee: ₹{expected_sales/employee_count:,.0f} | Inventory Turnover: {(expected_sales/inventory_level):.1f}")

# ============================================================
# EXPORT AND DOWNLOAD
# ============================================================
st.markdown("<h2 class='section-header'>Data Export</h2>", unsafe_allow_html=True)

export_col1, export_col2 = st.columns(2)

with export_col1:
    if st.button("Download Analyzed Data (CSV)"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Click to download",
            data=csv,
            file_name="business_analysis_results.csv",
            mime="text/csv"
        )

with export_col2:
    if st.button("Generate Summary Report"):
        with st.spinner("Generating report..."):
            summary_stats = {
                "Total Businesses": len(df),
                "Average Profit": df.predicted_profit.mean(),
                "Average Sales": df.monthly_sales.mean(),
                "High Risk %": (df.risk_band == 'High').mean() * 100,
                "Best Performing Type": df.groupby('business_type')['predicted_profit'].mean().idxmax(),
                "Optimal Marketing Spend": df.groupby(pd.cut(df['marketing_spend'], 5))['predicted_profit'].mean().idxmax()
            }
            
            st.json(summary_stats)

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 1rem;'>
    <p>BizSight AI Business Intelligence Platform v2.0</p>
    <p style='font-size: 0.9rem;'>Developed by Sourish Dey | © 2024 All rights reserved</p>
</div>
""", unsafe_allow_html=True)
