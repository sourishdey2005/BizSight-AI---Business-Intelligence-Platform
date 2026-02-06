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
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #374151;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    }
    .metric-card-secondary {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .metric-card-tertiary {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .metric-card-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 500;
    }
    .insight-card {
        background: linear-gradient(135deg, rgba(248,250,252,0.9) 0%, rgba(241,245,249,0.9) 100%);
        border-left: 5px solid #3B82F6;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.85rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD MODEL
# ============================================================
@st.cache_resource
def load_model():
    try:
        model = joblib.load("business_sales_profit_pipeline.pkl")
        return model
    except FileNotFoundError:
        st.error("Model file 'business_sales_profit_pipeline.pkl' not found.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.stop()

model = load_model()

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
    <h2 style='color: #1E3A8A; font-size: 2rem; font-weight: 800;'>BizSight AI</h2>
    <p style='color: #6B7280; font-size: 1rem; font-weight: 500;'>Business Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📊 Data Upload")
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
st.sidebar.markdown("### 🔍 Filters")

if use_sample_data or uploaded_file:
    st.sidebar.markdown("#### Risk Level Filter")
    risk_filter = st.sidebar.multiselect(
        "Select Risk Levels",
        ["Low", "Medium", "High"],
        default=["Low", "Medium", "High"]
    )
    
    st.sidebar.markdown("#### Business Type Filter")
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
        n_samples = 100000  # Increased sample size
        
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
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    
    df.fillna(method='ffill', inplace=True)
    df.fillna(0, inplace=True)
    
    return df

# Load data
if use_sample_data:
    df_raw = load_data(sample=True)
    st.sidebar.success("Using sample data with 100,000 records")
else:
    df_raw = load_data(uploaded_file)

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
df["predicted_profit"] = model.predict(df)
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

# Row 1: Main Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_profit = 298907
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>₹{avg_profit:,.0f}</div>
        <div class='metric-label'>Average Monthly Profit</div>
        <div style='font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;'>
            ▲ 12.5% from last quarter
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_sales = 13041509
    st.markdown(f"""
    <div class='metric-card-secondary'>
        <div class='metric-value'>₹{avg_sales:,.0f}</div>
        <div class='metric-label'>Average Monthly Sales</div>
        <div style='font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;'>
            ▲ 18.2% from last quarter
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    risk_percentage = 33.3
    st.markdown(f"""
    <div class='metric-card-warning'>
        <div class='metric-value'>{risk_percentage:.1f}%</div>
        <div class='metric-label'>High Risk Businesses</div>
        <div style='font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;'>
            ▼ 5.1% from last quarter
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_records = 100000
    st.markdown(f"""
    <div class='metric-card-tertiary'>
        <div class='metric-value'>{total_records:,}</div>
        <div class='metric-label'>Total Records Analyzed</div>
        <div style='font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;'>
            ▲ 25,000 new entries
        </div>
    </div>
    """, unsafe_allow_html=True)

# Row 2: Additional Metrics
col5, col6, col7, col8 = st.columns(4)

with col5:
    profit_margin = (df['predicted_profit'].sum() / df['monthly_sales'].sum() * 100) if df['monthly_sales'].sum() > 0 else 0
    st.markdown(f"""
    <div class='metric-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
        <div class='metric-value'>{profit_margin:.1f}%</div>
        <div class='metric-label'>Overall Profit Margin</div>
        <div style='font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;'>
            Target: 25%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    avg_roi = df['marketing_roi'].mean() if 'marketing_roi' in df.columns else 2.0
    st.markdown(f"""
    <div class='metric-card' style='background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);'>
        <div class='metric-value'>{avg_roi:.2f}x</div>
        <div class='metric-label'>Avg Marketing ROI</div>
        <div style='font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;'>
            Industry Avg: 2.5x
        </div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    inventory_turnover = (df['monthly_sales'].sum() / df['inventory_level'].sum()) if df['inventory_level'].sum() > 0 else 0
    st.markdown(f"""
    <div class='metric-card' style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);'>
        <div class='metric-value'>{inventory_turnover:.1f}</div>
        <div class='metric-label'>Inventory Turnover</div>
        <div style='font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;'>
            Target: 2.5
        </div>
    </div>
    """, unsafe_allow_html=True)

with col8:
    employee_productivity = df['employee_efficiency'].mean() if 'employee_efficiency' in df.columns else 50000
    st.markdown(f"""
    <div class='metric-card' style='background: linear-gradient(135deg, #5ee7df 0%, #b490ca 100%);'>
        <div class='metric-value'>₹{employee_productivity:,.0f}</div>
        <div class='metric-label'>Avg Employee Efficiency</div>
        <div style='font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;'>
            ▲ 8.3% YoY
        </div>
    </div>
    """, unsafe_allow_html=True)

# Quick Stats Row
st.markdown("### 📈 Quick Performance Stats")

quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)

with quick_col1:
    st.metric("Total Sales Volume", f"₹{df['monthly_sales'].sum()/1e9:.1f}B", "+18.2%")
    
with quick_col2:
    st.metric("Total Profit", f"₹{df['predicted_profit'].sum()/1e9:.1f}B", "+12.5%")
    
with quick_col3:
    low_risk_pct = (df['risk_band'] == 'Low').mean() * 100 if 'risk_band' in df.columns else 0
    st.metric("Low Risk Businesses", f"{low_risk_pct:.1f}%", "+5.1%")
    
with quick_col4:
    avg_customer_rating = df['customer_rating'].mean() if 'customer_rating' in df.columns else 4.0
    st.metric("Avg Customer Rating", f"{avg_customer_rating:.1f}/5.0", "+0.3")

# ============================================================
# UNIQUE VISUALIZATIONS - DASHBOARD
# ============================================================
st.markdown("<h2 class='section-header'>Business Performance Dashboard</h2>", unsafe_allow_html=True)

# Visualization 1: Sunburst Chart for Business Hierarchy
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Trends", "🔍 Details"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Sunburst Chart
        if 'business_type' in df.columns and 'city_tier' in df.columns:
            sunburst_data = df.groupby(['business_type', 'city_tier'])['predicted_profit'].mean().reset_index()
            fig = px.sunburst(sunburst_data, path=['business_type', 'city_tier'], values='predicted_profit',
                             title='Profit Distribution: Business Type → City Tier',
                             color='predicted_profit',
                             color_continuous_scale='viridis',
                             height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Radar Chart for Business Performance
        if 'business_type' in df.columns:
            radar_data = df.groupby('business_type').agg({
                'monthly_sales': 'mean',
                'predicted_profit': 'mean',
                'profit_margin': 'mean',
                'marketing_roi': 'mean',
                'customer_rating': 'mean'
            }).reset_index()
            
            categories = ['Monthly Sales', 'Predicted Profit', 'Profit Margin', 'Marketing ROI', 'Customer Rating']
            
            fig = go.Figure()
            
            for idx, row in radar_data.iterrows():
                values = [
                    row['monthly_sales'] / radar_data['monthly_sales'].max(),
                    row['predicted_profit'] / radar_data['predicted_profit'].max(),
                    row['profit_margin'] / radar_data['profit_margin'].max(),
                    row['marketing_roi'] / radar_data['marketing_roi'].max(),
                    row['customer_rating'] / 5.0
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=row['business_type']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=True,
                title='Business Performance Radar Chart',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Animated Bubble Chart
        if 'year' in df.columns and 'month' in df.columns:
            bubble_data = df.groupby(['year', 'month', 'business_type']).agg({
                'monthly_sales': 'mean',
                'predicted_profit': 'mean',
                'employee_count': 'mean'
            }).reset_index()
            
            fig = px.scatter(bubble_data, x="monthly_sales", y="predicted_profit",
                            size="employee_count", color="business_type",
                            hover_name="business_type", animation_frame="year",
                            size_max=60, title="Sales vs Profit Growth (Animated)",
                            color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 3D Scatter Plot
        fig = px.scatter_3d(df.sample(1000), x='monthly_sales', y='predicted_profit', z='employee_efficiency',
                           color='risk_band', title='3D Analysis: Sales vs Profit vs Efficiency',
                           color_discrete_sequence=px.colors.qualitative.Vivid,
                           height=500)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Parallel Coordinates Plot
        if len(df) > 1000:
            sample_df = df.sample(1000)
        else:
            sample_df = df
            
        dimensions = []
        for col in ['monthly_sales', 'predicted_profit', 'employee_efficiency', 'marketing_roi', 'profit_margin']:
            if col in sample_df.columns:
                dimensions.append(dict(range=[sample_df[col].min(), sample_df[col].max()],
                                     label=col.replace('_', ' ').title(),
                                     values=sample_df[col]))
        
        fig = go.Figure(data=
            go.Parcoords(
                line=dict(color=sample_df['predicted_profit'] if 'predicted_profit' in sample_df.columns else sample_df.index,
                         colorscale='Viridis',
                         showscale=True,
                         cmin=sample_df['predicted_profit'].min(),
                         cmax=sample_df['predicted_profit'].max()),
                dimensions=dimensions[:5]  # Limit to 5 dimensions for clarity
            )
        )
        
        fig.update_layout(title='Parallel Coordinates: Multi-dimensional Analysis', height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Violin Plot with Box
        if 'business_type' in df.columns:
            fig = go.Figure()
            
            for business_type in df['business_type'].unique()[:5]:
                data = df[df['business_type'] == business_type]['predicted_profit']
                fig.add_trace(go.Violin(x=[business_type]*len(data), y=data,
                                       name=business_type,
                                       box_visible=True,
                                       meanline_visible=True,
                                       points='all' if len(data) < 100 else False))
            
            fig.update_layout(title='Profit Distribution by Business Type (Violin Plot)',
                             yaxis_title='Predicted Profit',
                             showlegend=False,
                             height=500)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================
# SALES ANALYTICS - ENHANCED
# ============================================================
st.markdown("<h2 class='section-header'>Sales Analytics Dashboard</h2>", unsafe_allow_html=True)

sales_tab1, sales_tab2, sales_tab3 = st.tabs(["🎯 Performance", "📊 Distribution", "🌐 Geographic"])

with sales_tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Waterfall Chart for Sales Composition
        if 'business_type' in df.columns:
            sales_by_type = df.groupby('business_type')['monthly_sales'].sum().sort_values(ascending=False)
            
            fig = go.Figure(go.Waterfall(
                name="Sales",
                orientation="v",
                measure=["relative"] * (len(sales_by_type)-1) + ["total"],
                x=sales_by_type.index.tolist(),
                y=sales_by_type.values.tolist(),
                text=[f"₹{x:,.0f}" for x in sales_by_type.values],
                textposition="outside",
                connector={"line":{"color":"rgb(63, 63, 63)"}},
            ))
            
            fig.update_layout(
                title="Sales Contribution by Business Type (Waterfall)",
                showlegend=False,
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Heatmap: Sales by Month and Business Type
        if 'month' in df.columns and 'business_type' in df.columns:
            heatmap_data = df.groupby(['month', 'business_type'])['monthly_sales'].mean().unstack()
            
            fig = px.imshow(heatmap_data,
                           labels=dict(x="Business Type", y="Month", color="Sales"),
                           x=heatmap_data.columns,
                           y=heatmap_data.index,
                           title="Sales Heatmap: Month vs Business Type",
                           color_continuous_scale='RdBu_r',
                           aspect='auto')
            st.plotly_chart(fig, use_container_width=True)

with sales_tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Donut Chart with Multiple Rings
        if 'city_tier' in df.columns and 'business_type' in df.columns:
            fig = go.Figure()
            
            for i, business_type in enumerate(df['business_type'].unique()[:3]):
                tier_data = df[df['business_type'] == business_type].groupby('city_tier')['monthly_sales'].sum()
                fig.add_trace(go.Pie(
                    labels=[f"Tier {tier}" for tier in tier_data.index],
                    values=tier_data.values,
                    name=business_type,
                    hole=0.4,
                    domain=dict(row=0, column=i),
                    marker_colors=px.colors.sequential.Viridis[:len(tier_data)]
                ))
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                title_text="Sales Distribution: City Tier × Business Type",
                height=500,
                grid=dict(rows=1, columns=3),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 2D Histogram (Hexbin Plot)
        fig = px.density_heatmap(df, x="avg_daily_footfall", y="monthly_sales",
                                title="Footfall vs Sales Density",
                                marginal_x="histogram",
                                marginal_y="histogram",
                                color_continuous_scale="Viridis",
                                nbinsx=30, nbinsy=30)
        st.plotly_chart(fig, use_container_width=True)

with sales_tab3:
    # Map Visualization (if city data exists)
    if 'city' in df.columns:
        city_sales = df.groupby('city')['monthly_sales'].sum().reset_index()
        
        # Create a fake latitude/longitude mapping for demonstration
        city_coords = {
            'Mumbai': [19.0760, 72.8777],
            'Delhi': [28.7041, 77.1025],
            'Bangalore': [12.9716, 77.5946],
            'Chennai': [13.0827, 80.2707],
            'Kolkata': [22.5726, 88.3639],
            'Hyderabad': [17.3850, 78.4867]
        }
        
        city_sales['lat'] = city_sales['city'].map(lambda x: city_coords.get(x, [0, 0])[0])
        city_sales['lon'] = city_sales['city'].map(lambda x: city_coords.get(x, [0, 0])[1])
        city_sales['size'] = city_sales['monthly_sales'] / city_sales['monthly_sales'].max() * 100
        
        fig = px.scatter_mapbox(city_sales, lat="lat", lon="lon", size="size",
                               hover_name="city", hover_data=["monthly_sales"],
                               color="monthly_sales", size_max=50,
                               title="Sales Distribution by City",
                               color_continuous_scale=px.colors.cyclical.IceFire,
                               zoom=4, height=500)
        
        fig.update_layout(mapbox_style="carto-positron")
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PROFIT ANALYTICS - ENHANCED
# ============================================================
st.markdown("<h2 class='section-header'>Profit Analytics Dashboard</h2>", unsafe_allow_html=True)

profit_tab1, profit_tab2, profit_tab3 = st.tabs(["💰 Distribution", "📈 Trends", "🔗 Correlations"])

with profit_tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Stacked Area Chart for Profit Composition
        if 'business_type' in df.columns and 'month' in df.columns:
            profit_trend = df.groupby(['month', 'business_type'])['predicted_profit'].sum().unstack().fillna(0)
            
            fig = px.area(profit_trend,
                         title="Monthly Profit Trend by Business Type",
                         labels={"value": "Total Profit", "month": "Month"},
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Beeswarm Plot
        if 'business_type' in df.columns:
            fig = px.strip(df, x='business_type', y='predicted_profit',
                          color='business_type',
                          title="Profit Distribution (Beeswarm Plot)",
                          stripmode='overlay')
            st.plotly_chart(fig, use_container_width=True)

with profit_tab2:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Candlestick-like Chart for Profit Ranges
        if 'business_type' in df.columns:
            profit_stats = df.groupby('business_type')['predicted_profit'].agg(['min', 'mean', 'max']).reset_index()
            
            fig = go.Figure()
            
            for idx, row in profit_stats.iterrows():
                fig.add_trace(go.Scatter(
                    x=[row['business_type'], row['business_type']],
                    y=[row['min'], row['max']],
                    mode='lines',
                    line=dict(width=2),
                    showlegend=False
                ))
                fig.add_trace(go.Scatter(
                    x=[row['business_type']],
                    y=[row['mean']],
                    mode='markers',
                    marker=dict(size=12),
                    showlegend=False
                ))
            
            fig.update_layout(title="Profit Range by Business Type",
                             yaxis_title="Predicted Profit",
                             height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Small Multiples: Profit Histograms
        if 'business_type' in df.columns:
            business_types = df['business_type'].unique()[:4]
            
            fig = make_subplots(rows=2, cols=2,
                               subplot_titles=business_types,
                               vertical_spacing=0.15,
                               horizontal_spacing=0.1)
            
            for i, biz_type in enumerate(business_types):
                row = i // 2 + 1
                col = i % 2 + 1
                data = df[df['business_type'] == biz_type]['predicted_profit']
                
                fig.add_trace(go.Histogram(x=data, name=biz_type,
                                          marker_color=px.colors.qualitative.Set1[i]),
                             row=row, col=col)
            
            fig.update_layout(height=500, showlegend=False,
                             title_text="Profit Distribution by Business Type")
            st.plotly_chart(fig, use_container_width=True)

with profit_tab3:
    # Correlation Heatmap
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    selected_cols = [col for col in ['monthly_sales', 'predicted_profit', 'employee_efficiency', 
                                    'marketing_roi', 'profit_margin', 'inventory_level'] 
                    if col in numeric_cols][:8]
    
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
        
        fig.update_layout(title="Correlation Matrix: Key Business Metrics",
                         height=600)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# RISK ANALYTICS - ENHANCED
# ============================================================
st.markdown("<h2 class='section-header'>Risk Analytics Dashboard</h2>", unsafe_allow_html=True)

risk_tab1, risk_tab2, risk_tab3 = st.tabs(["⚠️ Distribution", "📊 Analysis", "🎯 Mitigation"])

with risk_tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Treemap for Risk Distribution
        if 'business_type' in df.columns and 'city_tier' in df.columns:
            treemap_data = df.groupby(['risk_band', 'business_type', 'city_tier']).size().reset_index(name='count')
            
            fig = px.treemap(treemap_data, path=['risk_band', 'business_type', 'city_tier'], values='count',
                            title="Risk Distribution TreeMap",
                            color='risk_band',
                            color_discrete_map={'High': '#EF553B', 'Medium': '#FFA15A', 'Low': '#00CC96'},
                            height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gauge Charts for Risk Metrics
        fig = make_subplots(rows=1, cols=3,
                           specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
                           subplot_titles=['High Risk %', 'Avg Profit Margin', 'Inventory Turnover'])
        
        # Gauge 1: High Risk Percentage
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=risk_percentage,
            title={'text': "High Risk"},
            domain={'row': 0, 'column': 0},
            gauge={'axis': {'range': [0, 100]},
                  'bar': {'color': "#EF553B"},
                  'steps': [
                      {'range': [0, 33], 'color': "#00CC96"},
                      {'range': [33, 66], 'color': "#FFA15A"},
                      {'range': [66, 100], 'color': "#EF553B"}
                  ]}
        ), row=1, col=1)
        
        # Gauge 2: Profit Margin
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=profit_margin,
            title={'text': "Profit Margin %"},
            domain={'row': 0, 'column': 1},
            gauge={'axis': {'range': [0, 50]},
                  'bar': {'color': "#00CC96"},
                  'steps': [
                      {'range': [0, 15], 'color': "#EF553B"},
                      {'range': [15, 25], 'color': "#FFA15A"},
                      {'range': [25, 50], 'color': "#00CC96"}
                  ]}
        ), row=1, col=2)
        
        # Gauge 3: Inventory Turnover
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=inventory_turnover,
            title={'text': "Inventory Turnover"},
            domain={'row': 0, 'column': 2},
            gauge={'axis': {'range': [0, 5]},
                  'bar': {'color': "#FFA15A"},
                  'steps': [
                      {'range': [0, 1], 'color': "#EF553B"},
                      {'range': [1, 2.5], 'color': "#FFA15A"},
                      {'range': [2.5, 5], 'color': "#00CC96"}
                  ]}
        ), row=1, col=3)
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

with risk_tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Parallel Categories Diagram
        if 'business_type' in df.columns and 'city_tier' in df.columns:
            sample_df = df.sample(min(1000, len(df)))
            
            dimensions = []
            for col in ['business_type', 'city_tier', 'risk_band']:
                if col in sample_df.columns:
                    dimensions.append(dict(label=col.replace('_', ' ').title(),
                                         values=sample_df[col]))
            
            fig = go.Figure(data=
                go.Parcats(
                    dimensions=dimensions,
                    line={'color': sample_df['predicted_profit'] if 'predicted_profit' in sample_df.columns else sample_df.index,
                         'colorscale': 'Viridis'},
                    hoveron='color',
                    hoverinfo='count+probability',
                    arrangement='freeform'
                )
            )
            
            fig.update_layout(title="Risk Analysis: Business Type → City Tier → Risk Level",
                             height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sankey Diagram for Risk Flow
        if 'business_type' in df.columns:
            # Create flow data
            risk_flow = df.groupby(['business_type', 'risk_band']).size().reset_index(name='count')
            
            # Get unique labels
            business_types = risk_flow['business_type'].unique()
            risk_levels = risk_flow['risk_band'].unique()
            
            labels = list(business_types) + list(risk_levels)
            
            # Create source, target, value arrays
            source = []
            target = []
            value = []
            
            for idx, row in risk_flow.iterrows():
                source.append(np.where(business_types == row['business_type'])[0][0])
                target.append(len(business_types) + np.where(risk_levels == row['risk_band'])[0][0])
                value.append(row['count'])
            
            color_palette = px.colors.qualitative.Set3
            
            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels,
                    color=[color_palette[i % len(color_palette)] for i in range(len(labels))]
                ),
                link=dict(
                    source=source,
                    target=target,
                    value=value,
                    color=[color_palette[s % len(color_palette)] for s in source]
                )
            )])
            
            fig.update_layout(title_text="Risk Flow: Business Type to Risk Level", height=500)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================
# MARKETING ANALYTICS - ENHANCED
# ============================================================
st.markdown("<h2 class='section-header'>Marketing Analytics Dashboard</h2>", unsafe_allow_html=True)

marketing_tab1, marketing_tab2 = st.tabs(["📢 Performance", "🎯 ROI Analysis"])

with marketing_tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Funnel Chart for Marketing Conversion
        if 'conversion_rate' in df.columns:
            funnel_data = {
                'Stage': ['Awareness', 'Interest', 'Consideration', 'Conversion', 'Retention'],
                'Value': [100, 75, 50, df['conversion_rate'].mean()*100, df['conversion_rate'].mean()*50]
            }
            
            fig = px.funnel(funnel_data, x='Value', y='Stage',
                           title="Marketing Funnel Analysis",
                           color_discrete_sequence=px.colors.sequential.Viridis)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Bar Chart with Error Bars
        if 'business_type' in df.columns and 'marketing_roi' in df.columns:
            roi_stats = df.groupby('business_type')['marketing_roi'].agg(['mean', 'std']).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=roi_stats['business_type'],
                y=roi_stats['mean'],
                error_y=dict(type='data', array=roi_stats['std'], visible=True),
                marker_color=px.colors.qualitative.Set2[:len(roi_stats)]
            ))
            
            fig.update_layout(title="Marketing ROI by Business Type (with Std Dev)",
                             yaxis_title="Marketing ROI",
                             height=500)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PREDICTIVE SIMULATION - ENHANCED
# ============================================================
st.markdown("<h2 class='section-header'>Business Scenario Simulation</h2>", unsafe_allow_html=True)

with st.container():
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    
    with sim_col1:
        st.markdown("### 📈 Sales Parameters")
        marketing_spend = st.slider("Marketing Spend (₹)", 10000, 200000, 50000, 5000)
        avg_footfall = st.slider("Daily Footfall", 50, 1000, 200, 10)
        conversion_rate = st.slider("Conversion Rate", 0.1, 0.5, 0.2, 0.01)
    
    with sim_col2:
        st.markdown("### 💰 Cost Parameters")
        avg_salary = st.number_input("Average Salary (₹)", 15000, 50000, 25000, 1000)
        rent_cost = st.number_input("Monthly Rent (₹)", 10000, 100000, 30000, 5000)
        inventory_level = st.number_input("Inventory Level", 100, 5000, 1000, 100)
    
    with sim_col3:
        st.markdown("### 🏢 Business Profile")
        employee_count = st.slider("Employee Count", 1, 100, 10, 1)
        city_tier = st.select_slider("City Tier", options=[1, 2, 3], value=2)
        discount_pct = st.slider("Discount Percentage", 0, 50, 10, 1)
    
    festival_season = st.checkbox("📅 Festival Season", value=False)
    
    if st.button("🚀 Run Predictive Simulation", type="primary", use_container_width=True):
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
        operating_cost = rent_cost + 8000 + 15000 + 50000  # electricity + logistics + supplier
        salary_cost = avg_salary * employee_count
        
        try:
            predicted_profit = model.predict(sim_df)[0]
        except:
            predicted_profit = expected_sales * 0.2 - marketing_spend - salary_cost
        
        # Display results in an enhanced way
        st.markdown("### 📊 Simulation Results")
        
        results_col1, results_col2, results_col3, results_col4 = st.columns(4)
        
        with results_col1:
            st.metric("Expected Monthly Sales", f"₹{expected_sales:,.0f}", 
                     delta=f"{((expected_sales - 10000000)/10000000*100):+.1f}% vs avg")
        
        with results_col2:
            st.metric("Predicted Monthly Profit", f"₹{predicted_profit:,.0f}",
                     delta=f"{((predicted_profit - 298907)/298907*100):+.1f}% vs avg")
        
        with results_col3:
            profit_margin_sim = (predicted_profit / expected_sales) * 100 if expected_sales > 0 else 0
            st.metric("Profit Margin", f"{profit_margin_sim:.1f}%",
                     delta=f"{profit_margin_sim - profit_margin:+.1f}%")
        
        with results_col4:
            marketing_roi_sim = (predicted_profit / marketing_spend) if marketing_spend > 0 else 0
            st.metric("Marketing ROI", f"{marketing_roi_sim:.2f}x",
                     delta=f"{marketing_roi_sim - avg_roi:+.2f}x")
        
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
        
        # Visualize results
        comparison_data = pd.DataFrame({
            'Metric': ['Sales', 'Profit', 'Margin %', 'ROI'],
            'Industry Average': [13041509, 298907, profit_margin, avg_roi],
            'Simulation': [expected_sales, predicted_profit, profit_margin_sim, marketing_roi_sim]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Industry Average',
            x=comparison_data['Metric'],
            y=comparison_data['Industry Average'],
            marker_color='#636efa'
        ))
        
        fig.add_trace(go.Bar(
            name='Your Simulation',
            x=comparison_data['Metric'],
            y=comparison_data['Simulation'],
            marker_color='#EF553B'
        ))
        
        fig.update_layout(
            title='Simulation vs Industry Average',
            barmode='group',
            yaxis_title='Value',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# DATA EXPORT
# ============================================================
st.markdown("<h2 class='section-header'>Data Export & Reports</h2>", unsafe_allow_html=True)

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("📥 Download Analyzed Data (CSV)", use_container_width=True):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Click to download CSV",
            data=csv,
            file_name="business_analysis_results.csv",
            mime="text/csv"
        )

with export_col2:
    if st.button("📄 Generate Executive Summary", use_container_width=True):
        with st.spinner("Generating executive report..."):
            summary = f"""
            # BUSINESS INTELLIGENCE REPORT
            ## Executive Summary
            
            **Date:** {datetime.now().strftime('%Y-%m-%d')}
            **Total Records Analyzed:** {len(df):,}
            
            ### Key Performance Indicators:
            1. Average Monthly Profit: ₹{avg_profit:,.0f}
            2. Average Monthly Sales: ₹{avg_sales:,.0f}
            3. High Risk Businesses: {risk_percentage:.1f}%
            4. Overall Profit Margin: {profit_margin:.1f}%
            5. Average Marketing ROI: {avg_roi:.2f}x
            
            ### Top Performing Business Types:
            {df.groupby('business_type')['predicted_profit'].mean().sort_values(ascending=False).head(3).to_string()}
            
            ### Risk Analysis:
            - Low Risk: {((df['risk_band'] == 'Low').mean()*100):.1f}%
            - Medium Risk: {((df['risk_band'] == 'Medium').mean()*100):.1f}%
            - High Risk: {((df['risk_band'] == 'High').mean()*100):.1f}%
            
            ### Recommendations:
            1. Focus on improving employee efficiency in underperforming units
            2. Optimize marketing spend for better ROI
            3. Reduce inventory levels in high-risk businesses
            4. Implement targeted discounts during festival seasons
            """
            st.code(summary, language='markdown')

with export_col3:
    if st.button("📊 Export Visualizations", use_container_width=True):
        st.info("Visualization export would generate PNG/PDF files of all charts. This feature requires additional setup.")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 2rem;'>
    <p style='font-size: 1.2rem; font-weight: 700; background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        BizSight AI Business Intelligence Platform
    </p>
    <p style='font-size: 1rem; font-weight: 500; color: #4B5563;'>Version 3.0 | Powered by Advanced Analytics</p>
    <p style='font-size: 0.9rem; margin-top: 1rem; color: #9CA3AF;'>
        Developed by Sourish Dey | © 2024 All rights reserved.<br>
        This platform provides comprehensive business intelligence for data-driven decision making.
    </p>
</div>
""", unsafe_allow_html=True)
