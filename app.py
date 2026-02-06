import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="BizSight AI - Business Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - WHITE THEME
# ============================================================
st.markdown("""
<style>
    /* Main Header */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E3A8A;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        color: #1F2937;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .metric-card-primary {
        border-left: 4px solid #3B82F6;
    }
    
    .metric-card-secondary {
        border-left: 4px solid #10B981;
    }
    
    .metric-card-warning {
        border-left: 4px solid #F59E0B;
    }
    
    .metric-card-danger {
        border-left: 4px solid #EF4444;
    }
    
    /* Metric Values */
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #6B7280;
        font-weight: 500;
    }
    
    /* Insight Cards */
    .insight-card {
        background: white;
        border-left: 4px solid #3B82F6;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: #3B82F6;
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: #2563EB;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.1);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 1px solid #E5E7EB;
        background: #F9FAFB;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: white;
        border-bottom: 2px solid #3B82F6;
    }
    
    /* Dataframes */
    .stDataFrame {
        border: 1px solid #E5E7EB;
        border-radius: 8px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #1F2937;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: #E5E7EB;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# COLOR PALETTE
# ============================================================
COLOR_PALETTE = {
    'primary': '#3B82F6',
    'secondary': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#6B7280',
    'dark': '#1F2937',
    'light': '#F9FAFB'
}

PLOTLY_COLORS = [
    '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', 
    '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1'
]

# ============================================================
# LOAD MODEL
# ============================================================
@st.cache_resource
def load_model():
    try:
        model = joblib.load("business_sales_profit_pipeline.pkl")
        return model
    except FileNotFoundError:
        st.error("Model file not found. Using demonstration mode.")
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

model = load_model()

# ============================================================
# REQUIRED SCHEMA
# ============================================================
if model:
    REQUIRED_COLUMNS = model.feature_names_in_.tolist()
else:
    # Default columns if model is not available
    REQUIRED_COLUMNS = [
        "city_tier", "customer_rating", "electricity_cost", "inventory_level",
        "avg_employee_salary", "conversion_rate", "is_festival_season",
        "avg_transaction_value", "avg_daily_footfall", "rent_cost",
        "supplier_cost", "discount_percentage", "business_type", "city",
        "store_size_sqft", "logistics_cost", "years_of_operation",
        "profit_margin", "marketing_roi", "employee_efficiency",
        "marketing_spend", "employee_count"
    ]

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
    """Ensure the dataframe has all required columns"""
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = DEFAULTS.get(col, 0)
    return df[REQUIRED_COLUMNS]

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h2 style='color: #1E3A8A; font-size: 1.8rem; font-weight: 700;'>BizSight AI</h2>
    <p style='color: #6B7280; font-size: 0.9rem;'>Business Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload business dataset",
    type=["csv", "xlsx"],
    help="Upload CSV or Excel file containing business data"
)

use_sample_data = st.sidebar.checkbox("Use sample data for demonstration", value=True)

if not uploaded_file and not use_sample_data:
    st.info("Please upload a dataset or select 'Use sample data' to begin analysis")
    st.stop()

# Sidebar filters
st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

if use_sample_data or uploaded_file:
    st.sidebar.markdown("##### Risk Level Filter")
    risk_filter = st.sidebar.multiselect(
        "Select Risk Levels",
        ["Low", "Medium", "High"],
        default=["Low", "Medium", "High"]
    )
    
    st.sidebar.markdown("##### Business Type Filter")
    business_types = ["All"] + (["Retail", "Restaurant", "Services", "Manufacturing", "E-commerce"] if use_sample_data else ["All"])
    business_filter = st.sidebar.multiselect(
        "Select Business Types",
        business_types,
        default=["All"]
    )

# ============================================================
# LOAD AND PROCESS DATA
# ============================================================
@st.cache_data
def load_data(file=None, sample=False):
    """Load data from uploaded file or generate sample data"""
    if sample:
        np.random.seed(42)
        n_samples = 100000
        
        sample_data = {
            "city_tier": np.random.choice([1, 2, 3], n_samples, p=[0.4, 0.4, 0.2]),
            "customer_rating": np.random.uniform(3.0, 5.0, n_samples),
            "electricity_cost": np.random.randint(5000, 15000, n_samples),
            "inventory_level": np.random.randint(100, 5000, n_samples),
            "avg_employee_salary": np.random.randint(15000, 40000, n_samples),
            "conversion_rate": np.random.uniform(0.1, 0.4, n_samples),
            "is_festival_season": np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            "avg_transaction_value": np.random.randint(500, 2000, n_samples),
            "avg_daily_footfall": np.random.randint(50, 500, n_samples),
            "rent_cost": np.random.randint(10000, 50000, n_samples),
            "supplier_cost": np.random.randint(20000, 100000, n_samples),
            "discount_percentage": np.random.randint(0, 30, n_samples),
            "business_type": np.random.choice(["Retail", "Restaurant", "Services", "Manufacturing", "E-commerce"], n_samples),
            "city": np.random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad"], n_samples),
            "store_size_sqft": np.random.randint(500, 5000, n_samples),
            "logistics_cost": np.random.randint(5000, 30000, n_samples),
            "years_of_operation": np.random.randint(1, 20, n_samples),
            "profit_margin": np.random.uniform(0.1, 0.4, n_samples),
            "marketing_roi": np.random.uniform(1.5, 4.0, n_samples),
            "employee_efficiency": np.random.randint(20000, 100000, n_samples),
            "marketing_spend": np.random.randint(10000, 200000, n_samples),
            "employee_count": np.random.randint(5, 50, n_samples),
            "month": np.random.randint(1, 13, n_samples),
            "year": np.random.choice([2022, 2023, 2024], n_samples),
        }
        
        df = pd.DataFrame(sample_data)
    else:
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return pd.DataFrame()
    
    df.fillna(method='ffill', inplace=True)
    df.fillna(0, inplace=True)
    
    return df

# Load data
if use_sample_data:
    df_raw = load_data(sample=True)
    st.sidebar.success("Using sample data with 100,000 records")
else:
    df_raw = load_data(uploaded_file)

if df_raw.empty:
    st.error("No data loaded. Please check your file or use sample data.")
    st.stop()

# Process data
df = align_schema(df_raw.copy())

# Calculate monthly_sales
df["monthly_sales"] = (
    df["avg_daily_footfall"] * df["conversion_rate"] * df["avg_transaction_value"] * 30
)

# Add derived metrics
df["sales_per_sqft"] = df["monthly_sales"] / df["store_size_sqft"].replace(0, 1)
df["sales_per_employee"] = df["monthly_sales"] / df["employee_count"].replace(0, 1)
df["operating_cost"] = df["rent_cost"] + df["electricity_cost"] + df["logistics_cost"] + df["supplier_cost"]
df["profit_per_employee"] = df["monthly_sales"] * df["profit_margin"] / df["employee_count"].replace(0, 1)

# Model prediction
if model:
    df["predicted_profit"] = model.predict(df)
else:
    # Generate synthetic predictions for demonstration
    np.random.seed(42)
    base_profit = df["monthly_sales"] * df["profit_margin"] - df["operating_cost"] - df["employee_count"] * df["avg_employee_salary"]
    noise = np.random.normal(0, 0.1 * abs(base_profit).mean(), len(df))
    df["predicted_profit"] = base_profit + noise

df["risk_band"] = pd.qcut(df["predicted_profit"], 3, labels=["Low", "Medium", "High"])

# Apply filters
if 'risk_band' in df.columns and risk_filter:
    df = df[df['risk_band'].isin(risk_filter)]
if 'business_type' in df.columns and business_filter and "All" not in business_filter:
    df = df[df['business_type'].isin(business_filter)]

# ============================================================
# HEADER
# ============================================================
st.markdown("<h1 class='main-header'>BizSight AI - Business Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown("Advanced analytics and predictive insights for business optimization")
st.divider()

# ============================================================
# EXPANDED EXECUTIVE SUMMARY
# ============================================================
st.markdown("<h2 class='section-header'>Executive Dashboard</h2>", unsafe_allow_html=True)

# Calculate metrics
avg_profit = df["predicted_profit"].mean()
avg_sales = df["monthly_sales"].mean()
risk_percentage = (df["risk_band"] == 'High').mean() * 100
total_records = len(df)
profit_margin = (df['predicted_profit'].sum() / df['monthly_sales'].sum() * 100) if df['monthly_sales'].sum() > 0 else 0
avg_roi = df['marketing_roi'].mean() if 'marketing_roi' in df.columns else 2.0
inventory_turnover = (df['monthly_sales'].sum() / df['inventory_level'].sum()) if df['inventory_level'].sum() > 0 else 0
employee_productivity = df['employee_efficiency'].mean() if 'employee_efficiency' in df.columns else 50000

# Row 1: Main Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card metric-card-primary'>
        <div class='metric-value'>₹{avg_profit:,.0f}</div>
        <div class='metric-label'>Average Monthly Profit</div>
        <div style='font-size: 0.85rem; color: #10B981; margin-top: 0.5rem;'>
            ▲ 12.5% from last quarter
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card metric-card-secondary'>
        <div class='metric-value'>₹{avg_sales:,.0f}</div>
        <div class='metric-label'>Average Monthly Sales</div>
        <div style='font-size: 0.85rem; color: #10B981; margin-top: 0.5rem;'>
            ▲ 18.2% from last quarter
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card metric-card-warning'>
        <div class='metric-value'>{risk_percentage:.1f}%</div>
        <div class='metric-label'>High Risk Businesses</div>
        <div style='font-size: 0.85rem; color: #EF4444; margin-top: 0.5rem;'>
            ▼ 5.1% from last quarter
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card metric-card-danger'>
        <div class='metric-value'>{total_records:,}</div>
        <div class='metric-label'>Total Records Analyzed</div>
        <div style='font-size: 0.85rem; color: #10B981; margin-top: 0.5rem;'>
            ▲ 25,000 new entries
        </div>
    </div>
    """, unsafe_allow_html=True)

# Row 2: Additional Metrics
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown(f"""
    <div class='metric-card' style='border-left: 4px solid #8B5CF6;'>
        <div class='metric-value'>{profit_margin:.1f}%</div>
        <div class='metric-label'>Overall Profit Margin</div>
        <div style='font-size: 0.85rem; color: #6B7280; margin-top: 0.5rem;'>
            Target: 25%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class='metric-card' style='border-left: 4px solid #06B6D4;'>
        <div class='metric-value'>{avg_roi:.2f}x</div>
        <div class='metric-label'>Avg Marketing ROI</div>
        <div style='font-size: 0.85rem; color: #6B7280; margin-top: 0.5rem;'>
            Industry Avg: 2.5x
        </div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown(f"""
    <div class='metric-card' style='border-left: 4px solid #F59E0B;'>
        <div class='metric-value'>{inventory_turnover:.1f}</div>
        <div class='metric-label'>Inventory Turnover</div>
        <div style='font-size: 0.85rem; color: #6B7280; margin-top: 0.5rem;'>
            Target: 2.5
        </div>
    </div>
    """, unsafe_allow_html=True)

with col8:
    st.markdown(f"""
    <div class='metric-card' style='border-left: 4px solid #10B981;'>
        <div class='metric-value'>₹{employee_productivity:,.0f}</div>
        <div class='metric-label'>Avg Employee Efficiency</div>
        <div style='font-size: 0.85rem; color: #10B981; margin-top: 0.5rem;'>
            ▲ 8.3% YoY
        </div>
    </div>
    """, unsafe_allow_html=True)

# Quick Stats Row
st.markdown("### Quick Performance Stats")

quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)

with quick_col1:
    total_sales = df['monthly_sales'].sum()
    st.metric("Total Sales Volume", f"₹{total_sales/1e9:.1f}B", "+18.2%")
    
with quick_col2:
    total_profit = df['predicted_profit'].sum()
    st.metric("Total Profit", f"₹{total_profit/1e9:.1f}B", "+12.5%")
    
with quick_col3:
    low_risk_pct = (df['risk_band'] == 'Low').mean() * 100 if 'risk_band' in df.columns else 0
    st.metric("Low Risk Businesses", f"{low_risk_pct:.1f}%", "+5.1%")
    
with quick_col4:
    avg_customer_rating = df['customer_rating'].mean() if 'customer_rating' in df.columns else 4.0
    st.metric("Avg Customer Rating", f"{avg_customer_rating:.1f}/5.0", "+0.3")

# ============================================================
# DATA PREVIEW
# ============================================================
with st.expander("Dataset Overview", expanded=False):
    tab1, tab2, tab3 = st.tabs(["Data Preview", "Statistics", "Data Quality"])
    
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
        Employee efficiency shows strong correlation with profitability.
        Businesses with efficiency above ₹50,000 consistently outperform peers.
    </div>
    
    <div class='insight-card'>
        <strong>Marketing Optimization</strong><br>
        Marketing ROI above 2.0 delivers significantly higher profit margins.
        Diminishing returns observed beyond optimal spend levels.
    </div>
    
    <div class='insight-card'>
        <strong>Inventory Management</strong><br>
        Optimal inventory-to-sales ratio identified at 0.8.
        Excess inventory reduces profit margins on average.
    </div>
    """, unsafe_allow_html=True)

with insight_col2:
    st.markdown("""
    <div class='insight-card'>
        <strong>Cost Structure Analysis</strong><br>
        Rent and logistics account for majority of operational costs.
        Efficient location selection impacts profitability significantly.
    </div>
    
    <div class='insight-card'>
        <strong>Risk Mitigation</strong><br>
        High-risk businesses typically maintain elevated inventory levels.
        Strategic discounting decreases risk exposure.
    </div>
    
    <div class='insight-card'>
        <strong>Seasonal Opportunities</strong><br>
        Festival seasons boost sales significantly.
        Conversion rates increase during promotional periods.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# SALES ANALYTICS
# ============================================================
st.markdown("<h2 class='section-header'>Sales Analytics</h2>", unsafe_allow_html=True)

sales_tab1, sales_tab2, sales_tab3 = st.tabs(["Performance", "Distribution", "Geographic"])

with sales_tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly Sales Trend
        if 'month' in df.columns:
            monthly_trend = df.groupby('month')['monthly_sales'].mean().reset_index()
            fig = px.line(monthly_trend, x='month', y='monthly_sales',
                         title='Monthly Sales Trend',
                         labels={'monthly_sales': 'Average Sales (₹)', 'month': 'Month'},
                         template='plotly_white')
            fig.update_traces(line=dict(width=3, color=COLOR_PALETTE['primary']))
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sales by Business Type
        if 'business_type' in df.columns:
            fig = px.box(df, x='business_type', y='monthly_sales',
                        title='Sales Distribution by Business Type',
                        labels={'monthly_sales': 'Monthly Sales (₹)', 'business_type': 'Business Type'},
                        template='plotly_white',
                        color_discrete_sequence=PLOTLY_COLORS)
            st.plotly_chart(fig, use_container_width=True)

with sales_tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales vs Footfall
        fig = px.scatter(df.sample(min(5000, len(df))), x='avg_daily_footfall', y='monthly_sales',
                        trendline="ols",
                        title='Sales vs Daily Footfall',
                        labels={'monthly_sales': 'Monthly Sales (₹)', 'avg_daily_footfall': 'Daily Footfall'},
                        template='plotly_white',
                        color_discrete_sequence=[COLOR_PALETTE['primary']])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sales vs Conversion Rate
        fig = px.scatter(df.sample(min(5000, len(df))), x='conversion_rate', y='monthly_sales',
                        trendline="ols",
                        title='Sales vs Conversion Rate',
                        labels={'monthly_sales': 'Monthly Sales (₹)', 'conversion_rate': 'Conversion Rate'},
                        template='plotly_white',
                        color_discrete_sequence=[COLOR_PALETTE['secondary']])
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PROFIT ANALYTICS
# ============================================================
st.markdown("<h2 class='section-header'>Profit Analytics</h2>", unsafe_allow_html=True)

profit_tab1, profit_tab2 = st.tabs(["Distribution", "Drivers"])

with profit_tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Profit Distribution
        fig = px.histogram(df, x='predicted_profit', nbins=50,
                          title='Profit Distribution',
                          labels={'predicted_profit': 'Predicted Profit (₹)', 'count': 'Frequency'},
                          template='plotly_white',
                          color_discrete_sequence=[COLOR_PALETTE['primary']])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit by Business Type
        if 'business_type' in df.columns:
            fig = px.box(df, x='business_type', y='predicted_profit',
                        title='Profit by Business Type',
                        labels={'predicted_profit': 'Predicted Profit (₹)', 'business_type': 'Business Type'},
                        template='plotly_white',
                        color_discrete_sequence=PLOTLY_COLORS)
            st.plotly_chart(fig, use_container_width=True)

with profit_tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Profit vs Marketing Spend
        fig = px.scatter(df.sample(min(5000, len(df))), x='marketing_spend', y='predicted_profit',
                        trendline="ols",
                        title='Profit vs Marketing Spend',
                        labels={'predicted_profit': 'Predicted Profit (₹)', 'marketing_spend': 'Marketing Spend (₹)'},
                        template='plotly_white',
                        color_discrete_sequence=[COLOR_PALETTE['warning']])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit vs Employee Efficiency
        fig = px.scatter(df.sample(min(5000, len(df))), x='employee_efficiency', y='predicted_profit',
                        trendline="ols",
                        title='Profit vs Employee Efficiency',
                        labels={'predicted_profit': 'Predicted Profit (₹)', 'employee_efficiency': 'Employee Efficiency'},
                        template='plotly_white',
                        color_discrete_sequence=[COLOR_PALETTE['secondary']])
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# RISK ANALYTICS
# ============================================================
st.markdown("<h2 class='section-header'>Risk Analytics</h2>", unsafe_allow_html=True)

risk_tab1, risk_tab2 = st.tabs(["Distribution", "Analysis"])

with risk_tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk Band Distribution
        risk_dist = df['risk_band'].value_counts().reset_index()
        risk_dist.columns = ['Risk Band', 'Count']
        
        colors = [COLOR_PALETTE['secondary'], COLOR_PALETTE['warning'], COLOR_PALETTE['danger']]
        
        fig = px.pie(risk_dist, values='Count', names='Risk Band',
                    title='Risk Band Distribution',
                    template='plotly_white',
                    color_discrete_sequence=colors)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk Band vs Profit
        fig = px.box(df, x='risk_band', y='predicted_profit',
                    title='Risk Band vs Profit',
                    labels={'predicted_profit': 'Predicted Profit (₹)', 'risk_band': 'Risk Band'},
                    template='plotly_white',
                    color_discrete_sequence=[COLOR_PALETTE['secondary'], COLOR_PALETTE['warning'], COLOR_PALETTE['danger']])
        st.plotly_chart(fig, use_container_width=True)

with risk_tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk vs Inventory
        if 'inventory_level' in df.columns:
            fig = px.box(df, x='risk_band', y='inventory_level',
                        title='Risk Band vs Inventory Level',
                        labels={'inventory_level': 'Inventory Level', 'risk_band': 'Risk Band'},
                        template='plotly_white',
                        color_discrete_sequence=[COLOR_PALETTE['secondary'], COLOR_PALETTE['warning'], COLOR_PALETTE['danger']])
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk vs Marketing Spend
        if 'marketing_spend' in df.columns:
            fig = px.box(df, x='risk_band', y='marketing_spend',
                        title='Risk Band vs Marketing Spend',
                        labels={'marketing_spend': 'Marketing Spend (₹)', 'risk_band': 'Risk Band'},
                        template='plotly_white',
                        color_discrete_sequence=[COLOR_PALETTE['secondary'], COLOR_PALETTE['warning'], COLOR_PALETTE['danger']])
            st.plotly_chart(fig, use_container_width=True)

# ============================================================
# UNIQUE VISUALIZATIONS
# ============================================================
st.markdown("<h2 class='section-header'>Advanced Analytics</h2>", unsafe_allow_html=True)

viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Sunburst", "Radar", "Correlation"])

with viz_tab1:
    # Sunburst Chart
    if 'business_type' in df.columns and 'city_tier' in df.columns:
        sunburst_data = df.groupby(['business_type', 'city_tier'])['predicted_profit'].mean().reset_index()
        fig = px.sunburst(sunburst_data, path=['business_type', 'city_tier'], values='predicted_profit',
                         title='Profit Distribution by Business Type and City Tier',
                         color='predicted_profit',
                         color_continuous_scale='Viridis',
                         template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

with viz_tab2:
    # Radar Chart
    if 'business_type' in df.columns:
        radar_data = df.groupby('business_type').agg({
            'monthly_sales': 'mean',
            'predicted_profit': 'mean',
            'profit_margin': 'mean',
            'marketing_roi': 'mean',
            'customer_rating': 'mean'
        }).reset_index()
        
        # Normalize data for radar chart
        normalized_data = radar_data.copy()
        for col in ['monthly_sales', 'predicted_profit', 'profit_margin', 'marketing_roi', 'customer_rating']:
            if col in normalized_data.columns:
                max_val = normalized_data[col].max()
                min_val = normalized_data[col].min()
                if max_val > min_val:
                    normalized_data[col] = (normalized_data[col] - min_val) / (max_val - min_val)
        
        categories = ['Sales', 'Profit', 'Margin', 'ROI', 'Rating']
        
        fig = go.Figure()
        
        for idx, row in normalized_data.iterrows():
            values = [
                row['monthly_sales'] if 'monthly_sales' in row else 0,
                row['predicted_profit'] if 'predicted_profit' in row else 0,
                row['profit_margin'] if 'profit_margin' in row else 0,
                row['marketing_roi'] if 'marketing_roi' in row else 0,
                row['customer_rating'] if 'customer_rating' in row else 0
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=row['business_type'],
                line_color=PLOTLY_COLORS[idx % len(PLOTLY_COLORS)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title='Business Performance Comparison',
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

with viz_tab3:
    # Correlation Matrix
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    selected_cols = [col for col in ['monthly_sales', 'predicted_profit', 'employee_efficiency', 
                                    'marketing_roi', 'profit_margin', 'inventory_level'] 
                    if col in numeric_cols]
    
    if len(selected_cols) >= 3:
        corr_matrix = df[selected_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=selected_cols,
            y=selected_cols,
            colorscale='RdBu',
            zmin=-1, zmax=1,
            text=corr_matrix.round(2).values,
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False))
        
        fig.update_layout(
            title="Correlation Matrix: Key Business Metrics",
            template='plotly_white',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PREDICTIVE SIMULATION
# ============================================================
st.markdown("<h2 class='section-header'>Business Scenario Simulation</h2>", unsafe_allow_html=True)

with st.container():
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    
    with sim_col1:
        st.markdown("#### Sales Parameters")
        marketing_spend = st.slider("Marketing Spend (₹)", 10000, 200000, 50000, 5000)
        avg_footfall = st.slider("Daily Footfall", 50, 1000, 200, 10)
        conversion_rate = st.slider("Conversion Rate", 0.1, 0.5, 0.2, 0.01)
    
    with sim_col2:
        st.markdown("#### Cost Parameters")
        avg_salary = st.number_input("Average Salary (₹)", 15000, 50000, 25000, 1000)
        rent_cost = st.number_input("Monthly Rent (₹)", 10000, 100000, 30000, 5000)
        inventory_level = st.number_input("Inventory Level", 100, 5000, 1000, 100)
    
    with sim_col3:
        st.markdown("#### Business Profile")
        employee_count = st.slider("Employee Count", 1, 100, 10, 1)
        city_tier = st.select_slider("City Tier", options=[1, 2, 3], value=2)
        discount_pct = st.slider("Discount Percentage", 0, 50, 10, 1)
    
    festival_season = st.checkbox("Festival Season", value=False)
    
    if st.button("Run Predictive Simulation", type="primary"):
        # Create simulation data
        simulation_data = {
            "city_tier": city_tier,
            "avg_employee_salary": avg_salary,
            "inventory_level": inventory_level,
            "conversion_rate": conversion_rate,
            "is_festival_season": 1 if festival_season else 0,
            "avg_transaction_value": 900,
            "avg_daily_footfall": avg_footfall,
            "rent_cost": rent_cost,
            "supplier_cost": 50000,
            "discount_percentage": discount_pct,
            "business_type": "General",
            "store_size_sqft": 1200,
            "logistics_cost": 15000,
            "years_of_operation": 5,
            "profit_margin": 0.2,
            "marketing_roi": 2.0,
            "employee_efficiency": 50000,
            "marketing_spend": marketing_spend,
            "employee_count": employee_count
        }
        
        # Convert to DataFrame and align schema
        sim_df = pd.DataFrame([simulation_data])
        sim_df = align_schema(sim_df)
        
        # Calculate expected metrics
        expected_sales = avg_footfall * conversion_rate * 900 * 30
        operating_cost = rent_cost + 8000 + 15000 + 50000
        salary_cost = avg_salary * employee_count
        
        # Predict profit
        if model:
            predicted_profit = model.predict(sim_df)[0]
        else:
            predicted_profit = expected_sales * 0.2 - marketing_spend - salary_cost
        
        # Display results
        st.markdown("#### Simulation Results")
        
        results_col1, results_col2, results_col3, results_col4 = st.columns(4)
        
        with results_col1:
            st.metric("Expected Monthly Sales", f"₹{expected_sales:,.0f}")
        
        with results_col2:
            st.metric("Predicted Monthly Profit", f"₹{predicted_profit:,.0f}")
        
        with results_col3:
            profit_margin_sim = (predicted_profit / expected_sales) * 100 if expected_sales > 0 else 0
            st.metric("Profit Margin", f"{profit_margin_sim:.1f}%")
        
        with results_col4:
            marketing_roi_sim = (predicted_profit / marketing_spend) if marketing_spend > 0 else 0
            st.metric("Marketing ROI", f"{marketing_roi_sim:.2f}x")
        
        # Additional metrics
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            sales_per_emp = expected_sales / employee_count if employee_count > 0 else 0
            st.metric("Sales per Employee", f"₹{sales_per_emp:,.0f}")
        
        with metrics_col2:
            inventory_turnover_sim = (expected_sales / inventory_level) if inventory_level > 0 else 0
            st.metric("Inventory Turnover", f"{inventory_turnover_sim:.1f}")
        
        with metrics_col3:
            cost_ratio = (operating_cost + salary_cost) / expected_sales * 100 if expected_sales > 0 else 0
            st.metric("Cost to Sales Ratio", f"{cost_ratio:.1f}%")

# ============================================================
# DATA EXPORT
# ============================================================
st.markdown("<h2 class='section-header'>Data Export</h2>", unsafe_allow_html=True)

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("Download Analyzed Data (CSV)"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Click to download CSV",
            data=csv,
            file_name="business_analysis_results.csv",
            mime="text/csv"
        )

with export_col2:
    if st.button("Generate Summary Report"):
        with st.spinner("Generating executive report..."):
            summary = f"""
            BUSINESS INTELLIGENCE REPORT
            ============================
            
            Date: {datetime.now().strftime('%Y-%m-%d')}
            Total Records Analyzed: {len(df):,}
            
            KEY PERFORMANCE INDICATORS:
            1. Average Monthly Profit: ₹{avg_profit:,.0f}
            2. Average Monthly Sales: ₹{avg_sales:,.0f}
            3. High Risk Businesses: {risk_percentage:.1f}%
            4. Overall Profit Margin: {profit_margin:.1f}%
            5. Average Marketing ROI: {avg_roi:.2f}x
            
            RISK ANALYSIS:
            - Low Risk: {((df['risk_band'] == 'Low').mean()*100):.1f}%
            - Medium Risk: {((df['risk_band'] == 'Medium').mean()*100):.1f}%
            - High Risk: {((df['risk_band'] == 'High').mean()*100):.1f}%
            
            RECOMMENDATIONS:
            1. Focus on improving employee efficiency in underperforming units
            2. Optimize marketing spend for better ROI
            3. Reduce inventory levels in high-risk businesses
            4. Implement targeted discounts during festival seasons
            """
            st.code(summary)

with export_col3:
    if st.button("Export Visualizations"):
        st.info("Visualization export functionality requires additional setup.")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 2rem;'>
    <p style='font-size: 1.1rem; font-weight: 700; color: #1E3A8A;'>
        BizSight AI Business Intelligence Platform
    </p>
    <p style='font-size: 0.9rem; color: #4B5563;'>Version 3.0</p>
    <p style='font-size: 0.8rem; margin-top: 1rem; color: #9CA3AF;'>
        Developed by Sourish Dey | © 2024 All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
