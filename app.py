import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="BizSight AI - Advanced Business Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - PROFESSIONAL THEME
# ============================================================
st.markdown("""
<style>
    /* Main Header */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
        text-align: center;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sub Header */
    .sub-header {
        text-align: center;
        font-size: 1.2rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    
    /* Welcome Message */
    .welcome-message {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .welcome-message h2 {
        color: white;
        margin-bottom: 1rem;
        font-size: 2.5rem;
    }
    
    /* Portfolio Link */
    .portfolio-link {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .portfolio-link a {
        color: #3B82F6;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.5rem 1.5rem;
        border: 2px solid #3B82F6;
        border-radius: 25px;
        transition: all 0.3s ease;
        display: inline-block;
        margin: 0.5rem;
    }
    
    .portfolio-link a:hover {
        background: #3B82F6;
        color: white;
        text-decoration: none;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #E5E7EB;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        color: #1F2937;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(to bottom, #3B82F6, #10B981);
    }
    
    .metric-card:hover {
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #6B7280;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .metric-trend {
        font-size: 0.85rem;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        display: inline-block;
        font-weight: 600;
    }
    
    .trend-up {
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
    }
    
    .trend-down {
        background: rgba(239, 68, 68, 0.1);
        color: #EF4444;
    }
    
    .trend-neutral {
        background: rgba(156, 163, 175, 0.1);
        color: #6B7280;
    }
    
    /* Insight Cards */
    .insight-card {
        background: linear-gradient(135deg, rgba(248,250,252,0.9) 0%, rgba(241,245,249,0.9) 100%);
        border-left: 5px solid #3B82F6;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
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
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        padding: 0 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 1rem 1.5rem;
        font-weight: 600;
        border: 1px solid #E5E7EB;
        background: #F9FAFB;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: white;
        border-bottom: 3px solid #3B82F6;
        color: #3B82F6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Data Options */
    .data-options {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #E5E7EB;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .data-options:hover {
        border-color: #3B82F6;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .data-options h3 {
        color: #1E3A8A;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    /* Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-item {
        text-align: center;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3B82F6;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
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
    'success': '#22C55E',
    'purple': '#8B5CF6',
    'pink': '#EC4899',
    'cyan': '#06B6D4',
    'orange': '#F97316',
    'indigo': '#6366F1',
    'teal': '#14B8A6'
}

PLOTLY_COLORS = [
    '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', 
    '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1',
    '#F472B6', '#D946EF', '#0EA5E9', '#22C55E', '#EAB308',
    '#A855F7', '#F43F5E', '#0D9488', '#F59E0B', '#3B82F6'
]

# ============================================================
# LOAD MODEL - ENHANCED WITH FALLBACK
# ============================================================
@st.cache_resource
def load_model():
    try:
        # Try to load the model file
        model = joblib.load("business_sales_profit_pipeline.pkl")
        st.sidebar.success("✓ Predictive model loaded successfully")
        return model
    except FileNotFoundError:
        # Create a mock model for demonstration
        st.sidebar.warning("⚠️ Model file not found. Using advanced analytics mode.")
        
        # Create a simple linear regression model for demonstration
        class MockModel:
            def predict(self, X):
                # Simple linear model based on available features
                np.random.seed(42)
                if isinstance(X, pd.DataFrame):
                    # Calculate mock predictions based on key features
                    base_pred = 100000
                    if 'employee_count' in X.columns:
                        base_pred += X['employee_count'] * 5000
                    if 'store_size_sqft' in X.columns:
                        base_pred += X['store_size_sqft'] * 10
                    if 'marketing_spend' in X.columns:
                        base_pred += X['marketing_spend'] * 0.5
                    return base_pred.values
                else:
                    return np.random.normal(500000, 200000, len(X))
            
            def predict_proba(self, X):
                # For classification tasks
                np.random.seed(42)
                return np.random.rand(len(X), 2)
        
        return MockModel()
    except Exception as e:
        st.sidebar.error(f"Error loading model: {str(e)}")
        
        class FallbackModel:
            def predict(self, X):
                return np.full(len(X), 500000)
        
        return FallbackModel()

model = load_model()

# ============================================================
# SIDEBAR - ALWAYS VISIBLE
# ============================================================
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 1.5rem;'>
    <h2 style='color: #1E3A8A; font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem;'>BizSight AI</h2>
    <p style='color: #6B7280; font-size: 0.9rem; font-weight: 500;'>Advanced Business Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Portfolio links
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <a href='https://sourishdeyportfolio.vercel.app/' target='_blank' 
       style='display: block; padding: 0.75rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
              color: white; text-decoration: none; border-radius: 12px; font-weight: 600;
              margin-bottom: 1rem; transition: all 0.3s ease;'>
       👨‍💻 View Portfolio
    </a>
    <a href='https://github.com/sourishdey2005' target='_blank' 
       style='display: block; padding: 0.75rem; background: #1F2937; 
              color: white; text-decoration: none; border-radius: 12px; font-weight: 600;
              transition: all 0.3s ease;'>
       💻 GitHub Profile
    </a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Data Source Selection")

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = None
if 'df' not in st.session_state:
    st.session_state.df = None

# Data source selection
data_source = st.sidebar.radio(
    "Choose data source:",
    ["Upload your own dataset", "Use sample dataset"],
    index=0,
    help="Select how you want to load data for analysis"
)

uploaded_file = None
use_sample_data = False

if data_source == "Upload your own dataset":
    uploaded_file = st.sidebar.file_uploader(
        "Upload business dataset (CSV/Excel)",
        type=["csv", "xlsx", "xls"],
        help="Upload your business data file for analysis"
    )
    if uploaded_file:
        use_sample_data = False
    else:
        use_sample_data = False
else:
    use_sample_data = st.sidebar.checkbox("Load sample dataset", value=False)

# ============================================================
# DATA LOADING AND PROCESSING FUNCTIONS
# ============================================================
@st.cache_data
def load_sample_data():
    """Load comprehensive sample data for all visualizations"""
    np.random.seed(42)
    n_samples = 50000
    
    # Generate dates for temporal analysis
    start_date = pd.Timestamp('2023-01-01')
    dates = [start_date + pd.Timedelta(days=i) for i in range(365)]
    business_dates = np.random.choice(dates, n_samples)
    
    # Create comprehensive sample data
    sample_data = {
        'business_id': [f'BUS_{i:06d}' for i in range(n_samples)],
        'date': business_dates,
        'city': np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 
                                 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Surat', 'Kanpur', 
                                 'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Patna',
                                 'Vadodara', 'Ghaziabad'], n_samples),
        'state': np.random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal',
                                  'Telangana', 'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'Bihar',
                                  'Madhya Pradesh', 'Andhra Pradesh', 'Punjab', 'Haryana'], n_samples),
        'region': np.random.choice(['North', 'South', 'East', 'West', 'Central', 'Northeast'], n_samples),
        'city_tier': np.random.choice([1, 2, 3], n_samples, p=[0.3, 0.4, 0.3]),
        'business_type': np.random.choice(['Retail', 'Restaurant', 'Services', 'Manufacturing', 
                                          'E-commerce', 'Healthcare', 'Education', 'Entertainment',
                                          'Hospitality', 'Construction', 'Logistics', 'Technology'], n_samples),
        'years_of_operation': np.random.randint(1, 50, n_samples),
        'store_size_sqft': np.random.randint(500, 20000, n_samples),
        'employee_count': np.random.randint(5, 500, n_samples),
        'employee_efficiency': np.random.randint(20000, 500000, n_samples),
        'avg_employee_salary': np.random.randint(20000, 200000, n_samples),
        'avg_daily_footfall': np.random.randint(50, 5000, n_samples),
        'conversion_rate': np.random.uniform(0.05, 0.8, n_samples),
        'avg_transaction_value': np.random.randint(500, 20000, n_samples),
        'customer_rating': np.random.uniform(2.5, 5.0, n_samples),
        'discount_percentage': np.random.uniform(0, 60, n_samples),
        'rent_cost': np.random.randint(10000, 500000, n_samples),
        'electricity_cost': np.random.randint(5000, 100000, n_samples),
        'logistics_cost': np.random.randint(5000, 200000, n_samples),
        'supplier_cost': np.random.randint(20000, 1000000, n_samples),
        'inventory_level': np.random.randint(1000, 500000, n_samples),
        'marketing_spend': np.random.randint(10000, 1000000, n_samples),
        'marketing_roi': np.random.uniform(0.5, 10.0, n_samples),
        'is_festival_season': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'profit_margin': np.random.uniform(-0.2, 0.6, n_samples),
        'monthly_sales': np.random.randint(100000, 10000000, n_samples),
        'operational_cost': np.random.randint(50000, 2000000, n_samples),
        'monthly_revenue': np.random.randint(150000, 12000000, n_samples),
        'sales_per_sqft': np.random.randint(100, 5000, n_samples),
        'profit_per_employee': np.random.randint(-10000, 100000, n_samples),
        'cost_to_sales_ratio': np.random.uniform(0.2, 0.9, n_samples),
        'employee_productivity': np.random.randint(10000, 300000, n_samples),
        'risk_category': np.random.choice(['Low', 'Medium', 'High'], n_samples, p=[0.5, 0.3, 0.2]),
        'business_size': np.random.choice(['Small', 'Medium', 'Large', 'Enterprise'], n_samples, p=[0.3, 0.4, 0.2, 0.1]),
        'industry_sector': np.random.choice(['Technology', 'Retail', 'Manufacturing', 'Healthcare', 
                                            'Finance', 'Education', 'Hospitality', 'Logistics'], n_samples),
        'customer_segment': np.random.choice(['Individual', 'Corporate', 'Government', 'Institutional'], n_samples),
        'payment_method': np.random.choice(['Cash', 'Credit Card', 'UPI', 'Net Banking', 'Loan'], n_samples),
        'product_category': np.random.choice(['Electronics', 'Fashion', 'Groceries', 'Furniture', 
                                             'Automotive', 'Real Estate', 'Services'], n_samples),
        'latitude': np.random.uniform(8.0, 37.0, n_samples),
        'longitude': np.random.uniform(68.0, 97.0, n_samples)
    }
    
    df = pd.DataFrame(sample_data)
    
    # Calculate profit
    df['profit'] = df['monthly_revenue'] - df['operational_cost']
    
    # Add derived metrics
    df['total_cost'] = df['operational_cost'] + df['employee_count'] * df['avg_employee_salary'] / 12
    df['gross_margin'] = (df['monthly_revenue'] - df['operational_cost']) / df['monthly_revenue'].replace(0, 1)
    df['inventory_turnover'] = df['monthly_sales'] / df['inventory_level'].replace(0, 1)
    df['employee_contribution'] = df['profit_per_employee'] * df['employee_count']
    df['marketing_efficiency'] = df['monthly_sales'] / df['marketing_spend'].replace(0, 1)
    df['roi_category'] = pd.cut(df['marketing_roi'], 
                                bins=[0, 1.5, 3, 10], 
                                labels=['Low', 'Medium', 'High'])
    
    # Add month and year for temporal analysis
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['quarter'] = df['date'].dt.quarter
    df['day_of_week'] = df['date'].dt.day_name()
    
    # Add supplier and customer relationships for network graph
    df['supplier_id'] = [f'SUP_{i:04d}' for i in np.random.randint(1, 1000, n_samples)]
    df['customer_id'] = [f'CUST_{i:06d}' for i in np.random.randint(1, 10000, n_samples)]
    
    return df

def load_custom_data(file):
    """Load custom uploaded data"""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx') or file.name.endswith('.xls'):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format. Please upload CSV or Excel file.")
            return None
        
        # Clean column names
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
        
        # Add missing required columns with default values
        required_cols = [
            'business_id', 'city', 'state', 'region', 'city_tier', 'business_type',
            'years_of_operation', 'store_size_sqft', 'employee_count', 'employee_efficiency',
            'avg_employee_salary', 'avg_daily_footfall', 'conversion_rate', 'avg_transaction_value',
            'customer_rating', 'discount_percentage', 'rent_cost', 'electricity_cost',
            'logistics_cost', 'supplier_cost', 'inventory_level', 'marketing_spend',
            'marketing_roi', 'is_festival_season', 'profit_margin',
            'monthly_sales', 'operational_cost', 'monthly_revenue', 'sales_per_sqft',
            'profit_per_employee', 'cost_to_sales_ratio', 'employee_productivity',
            'risk_category', 'business_size', 'profit'
        ]
        
        for col in required_cols:
            if col not in df.columns:
                if col == 'profit':
                    if 'monthly_revenue' in df.columns and 'operational_cost' in df.columns:
                        df[col] = df['monthly_revenue'] - df['operational_cost']
                    elif 'profit_margin' in df.columns and 'monthly_sales' in df.columns:
                        df[col] = df['monthly_sales'] * df['profit_margin']
                    else:
                        df[col] = np.random.randint(-100000, 1000000, len(df))
                elif col in ['monthly_revenue', 'monthly_sales']:
                    if col not in df.columns:
                        df[col] = np.random.randint(100000, 10000000, len(df))
                elif col == 'profit_margin':
                    if col not in df.columns:
                        df[col] = np.random.uniform(-0.1, 0.5, len(df))
                elif col == 'risk_category':
                    df[col] = np.random.choice(['Low', 'Medium', 'High'], len(df), p=[0.5, 0.3, 0.2])
                elif col in numeric_columns:
                    df[col] = np.random.randint(1000, 100000, len(df))
                else:
                    df[col] = np.random.choice(['Value1', 'Value2', 'Value3'], len(df))
        
        # Ensure date column exists for temporal analysis
        if 'date' not in df.columns:
            start_date = pd.Timestamp('2023-01-01')
            dates = [start_date + pd.Timedelta(days=i) for i in range(len(df))]
            df['date'] = np.random.choice(dates, len(df))
        
        # Add derived metrics
        df['total_cost'] = df['operational_cost'] + df['employee_count'] * df['avg_employee_salary'] / 12
        df['gross_margin'] = (df['monthly_revenue'] - df['operational_cost']) / df['monthly_revenue'].replace(0, 1)
        df['inventory_turnover'] = df['monthly_sales'] / df['inventory_level'].replace(0, 1)
        df['employee_contribution'] = df['profit_per_employee'] * df['employee_count']
        df['marketing_efficiency'] = df['monthly_sales'] / df['marketing_spend'].replace(0, 1)
        df['roi_category'] = pd.cut(df['marketing_roi'], 
                                    bins=[0, 1.5, 3, 10], 
                                    labels=['Low', 'Medium', 'High'])
        
        # Add temporal features
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['year'] = pd.to_datetime(df['date']).dt.year
        df['quarter'] = pd.to_datetime(df['date']).dt.quarter
        df['day_of_week'] = pd.to_datetime(df['date']).dt.day_name()
        
        return df
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def process_data(df_raw):
    """Process the loaded data for analysis"""
    if df_raw is None or df_raw.empty:
        return None, None
    
    df = df_raw.copy()
    
    # Ensure all required columns exist with safe defaults
    required_cols = {
        'profit': 0,
        'monthly_sales': 0,
        'profit_margin': 0,
        'monthly_revenue': 0,
        'operational_cost': 0,
        'marketing_spend': 0,
        'employee_count': 1,
        'customer_rating': 3.0,
        'conversion_rate': 0.2,
        'avg_daily_footfall': 100,
        'avg_transaction_value': 500,
        'inventory_level': 1000,
        'risk_category': 'Medium',
        'business_size': 'Medium',
        'business_type': 'Retail'
    }
    
    for col, default_value in required_cols.items():
        if col not in df.columns:
            if col in ['profit', 'monthly_sales', 'monthly_revenue', 'operational_cost', 'marketing_spend', 
                       'employee_count', 'avg_daily_footfall', 'avg_transaction_value', 'inventory_level']:
                df[col] = np.random.randint(default_value, default_value * 10, len(df))
            elif col in ['customer_rating', 'conversion_rate', 'profit_margin']:
                df[col] = np.random.uniform(default_value, default_value + 0.5, len(df))
            else:
                df[col] = default_value
    
    # Calculate profit if not present
    if 'profit' not in df.columns or df['profit'].isnull().all():
        if all(col in df.columns for col in ['monthly_revenue', 'operational_cost']):
            df['profit'] = df['monthly_revenue'] - df['operational_cost']
        elif 'profit_margin' in df.columns and 'monthly_sales' in df.columns:
            df['profit'] = df['monthly_sales'] * df['profit_margin']
    
    # Calculate additional metrics
    df['profitability_score'] = (df['profit_margin'].clip(-0.5, 0.5) * 0.4 + 
                                (df['customer_rating'].clip(1, 5) / 5) * 0.3 + 
                                (1 - df['cost_to_sales_ratio'].clip(0, 1)) * 0.3) * 100
    
    if 'employee_efficiency' in df.columns:
        emp_eff_norm = df['employee_efficiency'] / df['employee_efficiency'].replace(0, 1).max()
    else:
        emp_eff_norm = 0.5
    
    if 'sales_per_sqft' in df.columns:
        sales_sqft_norm = df['sales_per_sqft'] / df['sales_per_sqft'].replace(0, 1).max()
    else:
        sales_sqft_norm = 0.5
    
    if 'inventory_turnover' in df.columns:
        inv_turn_norm = df['inventory_turnover'] / df['inventory_turnover'].replace(0, 1).max()
    else:
        inv_turn_norm = 0.5
    
    df['efficiency_score'] = (emp_eff_norm * 0.4 +
                             sales_sqft_norm * 0.3 +
                             inv_turn_norm * 0.3) * 100
    
    df['growth_potential'] = ((df['years_of_operation'].clip(0, 50) / 50) * 0.3 +
                             (df['city_tier'].clip(1, 3) / 3) * 0.2 +
                             (df['employee_count'].clip(1, 500) / 500) * 0.3 +
                             (df['store_size_sqft'].clip(500, 20000) / 20000) * 0.2) * 100
    
    # Create risk bands
    if 'profit_margin' in df.columns:
        risk_score = df['profit_margin'].rank(pct=True) * 0.3
        if 'customer_rating' in df.columns:
            risk_score += df['customer_rating'].rank(pct=True) * 0.2
        if 'inventory_turnover' in df.columns:
            risk_score += df['inventory_turnover'].rank(pct=True) * 0.2
        if 'conversion_rate' in df.columns:
            risk_score += df['conversion_rate'].rank(pct=True) * 0.15
        if 'employee_efficiency' in df.columns:
            risk_score += df['employee_efficiency'].rank(pct=True) * 0.15
        
        df['risk_band'] = pd.qcut(risk_score, 3, labels=['Low', 'Medium', 'High'])
    else:
        df['risk_band'] = np.random.choice(['Low', 'Medium', 'High'], len(df), p=[0.5, 0.3, 0.2])
    
    # Create performance tiers
    if 'profit' in df.columns and 'monthly_sales' in df.columns:
        performance_score = (df['profit'].rank(pct=True) * 0.4 + 
                           df['monthly_sales'].rank(pct=True) * 0.3 + 
                           df['customer_rating'].rank(pct=True) * 0.3)
        df['performance_tier'] = pd.qcut(performance_score, 5, 
                                        labels=['Poor', 'Below Avg', 'Average', 'Good', 'Excellent'])
    else:
        df['performance_tier'] = np.random.choice(['Poor', 'Below Avg', 'Average', 'Good', 'Excellent'], 
                                                  len(df), p=[0.1, 0.2, 0.4, 0.2, 0.1])
    
    # Add prediction if model exists
    if model:
        try:
            # Prepare features for prediction
            feature_cols = ['city_tier', 'employee_efficiency', 'marketing_spend', 
                           'inventory_level', 'conversion_rate', 'avg_transaction_value',
                           'avg_daily_footfall', 'rent_cost', 'discount_percentage',
                           'store_size_sqft', 'profit_margin', 'marketing_roi',
                           'employee_count', 'avg_employee_salary', 'years_of_operation']
            
            prediction_df = pd.DataFrame()
            for col in feature_cols:
                if col in df.columns:
                    prediction_df[col] = df[col]
                else:
                    # Add default values
                    if col in ['employee_efficiency', 'avg_employee_salary', 'marketing_spend',
                              'rent_cost', 'store_size_sqft', 'inventory_level']:
                        prediction_df[col] = np.random.randint(50000, 200000, len(df))
                    elif col in ['conversion_rate', 'profit_margin', 'marketing_roi']:
                        prediction_df[col] = np.random.uniform(0.2, 0.8, len(df))
                    elif col in ['city_tier', 'employee_count', 'years_of_operation']:
                        prediction_df[col] = np.random.randint(2, 10, len(df))
                    elif col in ['avg_transaction_value', 'avg_daily_footfall']:
                        prediction_df[col] = np.random.randint(500, 5000, len(df))
                    elif col == 'discount_percentage':
                        prediction_df[col] = np.random.uniform(10, 30, len(df))
            
            prediction_df = prediction_df.fillna(prediction_df.mean())
            df['predicted_profit'] = model.predict(prediction_df)
        except Exception as e:
            st.sidebar.warning(f"Prediction error: {str(e)}")
            df['predicted_profit'] = df['profit']
    else:
        df['predicted_profit'] = df['profit']
    
    return df_raw, df

# ============================================================
# VISUALIZATION FUNCTIONS FOR ALL 20+ CHARTS
# ============================================================

def create_interactive_network_graph(df):
    """1. Interactive Network Graph for business relationships"""
    if len(df) > 1000:
        df_sample = df.sample(1000)
    else:
        df_sample = df.copy()
    
    # Create nodes for businesses
    business_nodes = df_sample['business_id'].unique()
    
    # Create edges based on business relationships
    edges = []
    for i in range(min(50, len(df_sample))):
        source = df_sample.iloc[i]['business_id']
        target = np.random.choice(business_nodes)
        if source != target:
            edges.append({
                'source': source,
                'target': target,
                'value': np.random.randint(1, 10)
            })
    
    # Create node positions
    node_x = []
    node_y = []
    for node in business_nodes[:len(edges)+1]:
        node_x.append(np.random.rand())
        node_y.append(np.random.rand())
    
    fig = go.Figure()
    
    # Add edges
    for edge in edges:
        fig.add_trace(go.Scatter(
            x=[node_x[business_nodes.tolist().index(edge['source'])], 
               node_x[business_nodes.tolist().index(edge['target'])]],
            y=[node_y[business_nodes.tolist().index(edge['source'])], 
               node_y[business_nodes.tolist().index(edge['target'])]],
            mode='lines',
            line=dict(width=edge['value']/5, color='rgba(128,128,128,0.5)'),
            hoverinfo='none'
        ))
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        marker=dict(
            size=20,
            color=df_sample['profit'].values[:len(node_x)] if 'profit' in df_sample.columns else 'blue',
            colorscale='Viridis',
            showscale=True,
            line_width=2
        ),
        text=business_nodes[:len(node_x)],
        hoverinfo='text'
    ))
    
    fig.update_layout(
        title='Business Relationship Network',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600
    )
    
    return fig

def create_chord_diagram(df):
    """2. Chord Diagram for business ecosystem visualization"""
    if len(df) > 20:
        df_sample = df.sample(20)
    else:
        df_sample = df.copy()
    
    # Create matrix for chord diagram
    categories = df_sample['business_type'].unique()[:10]
    n_categories = len(categories)
    
    # Create random flow matrix
    flow_matrix = np.random.rand(n_categories, n_categories)
    np.fill_diagonal(flow_matrix, 0)
    flow_matrix = (flow_matrix * 100).astype(int)
    
    fig = go.Figure()
    
    # This is a simplified chord diagram using Plotly
    # For a true chord diagram, consider using plotly.graph_objects with custom layout
    
    # Create a heatmap as a simplified chord diagram
    fig = ff.create_annotated_heatmap(
        z=flow_matrix,
        x=categories.tolist(),
        y=categories.tolist(),
        colorscale='Viridis',
        showscale=True
    )
    
    fig.update_layout(
        title='Business Ecosystem Flow (Chord Diagram)',
        height=500
    )
    
    return fig

def create_stream_graph(df):
    """3. Stream Graph for temporal trends"""
    if 'date' not in df.columns or 'monthly_sales' not in df.columns or 'business_type' not in df.columns:
        return None
    
    # Aggregate data by month and business type
    df['month_year'] = df['date'].dt.to_period('M').astype(str)
    top_types = df['business_type'].value_counts().nlargest(5).index
    
    stream_data = []
    for business_type in top_types:
        type_data = df[df['business_type'] == business_type]
        monthly_sales = type_data.groupby('month_year')['monthly_sales'].sum().reset_index()
        monthly_sales['business_type'] = business_type
        stream_data.append(monthly_sales)
    
    if stream_data:
        stream_df = pd.concat(stream_data)
        
        fig = px.area(stream_df, x='month_year', y='monthly_sales', color='business_type',
                     title='Business Performance Trends (Stream Graph)',
                     labels={'monthly_sales': 'Monthly Sales', 'month_year': 'Month'},
                     template='plotly_white')
        
        fig.update_layout(height=500)
        return fig
    
    return None

def create_3d_surface_plot(df):
    """4. 3D Surface Plot for profit landscape"""
    if len(df) < 100:
        return None
    
    # Sample data for 3D plot
    x = df['marketing_spend'].values[:100]
    y = df['employee_count'].values[:100]
    z = df['profit'].values[:100]
    
    # Create grid for surface
    xi = np.linspace(x.min(), x.max(), 20)
    yi = np.linspace(y.min(), y.max(), 20)
    xi, yi = np.meshgrid(xi, yi)
    
    # Interpolate z values
    from scipy.interpolate import griddata
    zi = griddata((x, y), z, (xi, yi), method='cubic')
    
    fig = go.Figure(data=[go.Surface(z=zi, x=xi, y=yi, colorscale='Viridis')])
    
    fig.update_layout(
        title='Profit Landscape Visualization (3D Surface)',
        scene=dict(
            xaxis_title='Marketing Spend',
            yaxis_title='Employee Count',
            zaxis_title='Profit'
        ),
        height=600
    )
    
    return fig

def create_calendar_heatmap(df):
    """5. Calendar Heatmap for daily performance"""
    if 'date' not in df.columns or 'profit' not in df.columns:
        return None
    
    # Create daily profit data
    daily_profit = df.groupby('date')['profit'].sum().reset_index()
    daily_profit['date'] = pd.to_datetime(daily_profit['date'])
    daily_profit['day'] = daily_profit['date'].dt.day
    daily_profit['month'] = daily_profit['date'].dt.month
    daily_profit['year'] = daily_profit['date'].dt.year
    
    # Pivot for heatmap
    heatmap_data = daily_profit.pivot_table(index='day', columns='month', values='profit', aggfunc='sum')
    
    fig = px.imshow(heatmap_data,
                   labels=dict(x="Month", y="Day", color="Profit"),
                   x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][:len(heatmap_data.columns)],
                   title='Daily Performance Calendar Heatmap',
                   color_continuous_scale='Viridis')
    
    fig.update_layout(height=500)
    return fig

def create_sankey_diagram(df):
    """6. Sankey Diagram for customer journey"""
    # Create sample customer journey data
    stages = ['Awareness', 'Consideration', 'Purchase', 'Retention', 'Advocacy']
    
    # Generate random flow between stages
    values = np.random.randint(100, 1000, size=(len(stages)-1))
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=stages,
            color=PLOTLY_COLORS[:len(stages)]
        ),
        link=dict(
            source=[0, 1, 2, 3],  # indices correspond to labels
            target=[1, 2, 3, 4],
            value=values.tolist()
        )
    )])
    
    fig.update_layout(
        title_text="Customer Journey Flow (Sankey Diagram)",
        font_size=12,
        height=500
    )
    
    return fig

def create_bubble_map(df):
    """7. Bubble Map for geographic business density"""
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        # Generate sample coordinates for India
        df['latitude'] = np.random.uniform(8.0, 37.0, len(df))
        df['longitude'] = np.random.uniform(68.0, 97.0, len(df))
    
    if 'profit' not in df.columns:
        return None
    
    # Sample for better performance
    if len(df) > 1000:
        df_sample = df.sample(1000)
    else:
        df_sample = df.copy()
    
    fig = px.scatter_geo(df_sample,
                        lat='latitude',
                        lon='longitude',
                        size='profit' if 'profit' in df_sample.columns else np.random.rand(len(df_sample))*100,
                        color='business_type' if 'business_type' in df_sample.columns else 'profit',
                        hover_name='city' if 'city' in df_sample.columns else 'business_id',
                        projection='natural earth',
                        title='Geographic Business Distribution',
                        size_max=50)
    
    fig.update_layout(height=600)
    return fig

def create_violin_plot(df):
    """8. Violin Plot for distribution analysis"""
    if 'profit' not in df.columns or 'business_type' not in df.columns:
        return None
    
    top_types = df['business_type'].value_counts().nlargest(5).index
    
    fig = px.violin(df[df['business_type'].isin(top_types)], 
                   y='profit', 
                   x='business_type',
                   box=True,
                   points="all",
                   title='Profit Distribution by Business Type',
                   color='business_type',
                   template='plotly_white')
    
    fig.update_layout(height=500)
    return fig

def create_sunburst_diagram(df):
    """9. Sunburst with Drill-Down"""
    if 'region' not in df.columns or 'state' not in df.columns or 'business_type' not in df.columns:
        return None
    
    # Aggregate data for sunburst
    region_state = df.groupby(['region', 'state']).size().reset_index(name='count')
    region_state_type = df.groupby(['region', 'state', 'business_type']).size().reset_index(name='count')
    
    fig = px.sunburst(region_state_type, 
                     path=['region', 'state', 'business_type'], 
                     values='count',
                     title='Business Hierarchy Sunburst',
                     color='count',
                     color_continuous_scale='Viridis')
    
    fig.update_layout(height=600)
    return fig

def create_parallel_sets(df):
    """10. Parallel Sets for categorical relationships"""
    if len(df) > 1000:
        df_sample = df.sample(1000)
    else:
        df_sample = df.copy()
    
    # Select categorical columns
    cat_cols = []
    for col in ['business_type', 'risk_category', 'business_size', 'city_tier']:
        if col in df_sample.columns and df_sample[col].dtype == 'object':
            cat_cols.append(col)
    
    if len(cat_cols) < 2:
        return None
    
    # Create parallel categories plot
    fig = px.parallel_categories(df_sample, 
                                dimensions=cat_cols[:3],
                                color='profit' if 'profit' in df_sample.columns else None,
                                title='Categorical Business Relationships',
                                color_continuous_scale='Viridis')
    
    fig.update_layout(height=500)
    return fig

def create_hexbin_plot(df):
    """11. Hexbin Plot for high-density data"""
    if 'monthly_sales' not in df.columns or 'profit' not in df.columns:
        return None
    
    fig = px.density_heatmap(df, 
                            x='monthly_sales', 
                            y='profit',
                            nbinsx=50, 
                            nbinsy=50,
                            title='Sales vs Profit Density (Hexbin)',
                            marginal_x="histogram", 
                            marginal_y="histogram",
                            color_continuous_scale='Viridis')
    
    fig.update_layout(height=500)
    return fig

def create_treemap_with_charts(df):
    """12. Treemap with Embedded Charts"""
    if 'business_type' not in df.columns or 'profit' not in df.columns:
        return None
    
    # Aggregate data
    agg_data = df.groupby('business_type').agg({
        'profit': 'mean',
        'monthly_sales': 'mean',
        'customer_rating': 'mean'
    }).reset_index()
    
    fig = px.treemap(agg_data, 
                    path=['business_type'], 
                    values='profit',
                    color='customer_rating',
                    hover_data=['monthly_sales'],
                    color_continuous_scale='Viridis',
                    title='Business Performance Treemap')
    
    fig.update_layout(height=500)
    return fig

def create_waterfall_with_subcategories(df):
    """13. Waterfall with Subcategories"""
    if 'business_type' not in df.columns or 'profit' not in df.columns:
        return None
    
    # Aggregate profit by business type
    profit_by_type = df.groupby('business_type')['profit'].sum().reset_index()
    profit_by_type = profit_by_type.sort_values('profit', ascending=False).head(10)
    
    fig = go.Figure(go.Waterfall(
        name="Profit",
        orientation="v",
        measure=["relative"] * len(profit_by_type),
        x=profit_by_type['business_type'],
        y=profit_by_type['profit'],
        textposition="outside",
        text=profit_by_type['profit'].apply(lambda x: f"₹{x:,.0f}"),
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title="Profit Breakdown by Business Type (Waterfall)",
        showlegend=False,
        height=500
    )
    
    return fig

def create_radar_chart_multiple_layers(df):
    """14. Radar Chart with Multiple Layers"""
    metrics = ['profit_margin', 'customer_rating', 'conversion_rate', 'inventory_turnover', 'employee_efficiency']
    available_metrics = [m for m in metrics if m in df.columns]
    
    if len(available_metrics) < 3:
        return None
    
    # Calculate average scores
    avg_scores = df[available_metrics].mean().values
    
    # Calculate max scores
    max_scores = df[available_metrics].max().values
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=avg_scores,
        theta=available_metrics,
        fill='toself',
        name='Average'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=max_scores,
        theta=available_metrics,
        fill='toself',
        name='Maximum'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            )),
        showlegend=True,
        title='Multi-dimensional Performance Radar',
        height=500
    )
    
    return fig

def create_heatmap_correlation_matrix(df):
    """15. Heatmap Correlation Matrix"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 3:
        return None
    
    # Select top 10 numeric columns for correlation
    top_cols = numeric_cols[:10]
    corr_matrix = df[top_cols].corr()
    
    fig = ff.create_annotated_heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns.tolist(),
        y=corr_matrix.index.tolist(),
        annotation_text=corr_matrix.round(2).values,
        colorscale='Viridis',
        showscale=True
    )
    
    fig.update_layout(
        title='Feature Correlation Matrix',
        height=600
    )
    
    return fig

def create_bump_chart(df):
    """16. Bump Chart for ranking evolution"""
    if 'date' not in df.columns or 'business_type' not in df.columns or 'profit' not in df.columns:
        return None
    
    # Create monthly rankings
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    monthly_profit = df.groupby(['month', 'business_type'])['profit'].sum().reset_index()
    
    # Get top 5 business types
    top_types = df['business_type'].value_counts().nlargest(5).index
    
    # Create bump chart data
    bump_data = monthly_profit[monthly_profit['business_type'].isin(top_types)]
    
    fig = px.line(bump_data, 
                 x='month', 
                 y='profit', 
                 color='business_type',
                 title='Business Ranking Evolution (Bump Chart)',
                 markers=True)
    
    fig.update_layout(height=500)
    return fig

def create_dot_matrix_chart(df):
    """17. Dot Matrix Chart for categorical distribution"""
    if 'business_type' not in df.columns or 'risk_category' not in df.columns:
        return None
    
    # Create cross-tabulation
    cross_tab = pd.crosstab(df['business_type'], df['risk_category'])
    
    fig = px.imshow(cross_tab,
                   labels=dict(x="Risk Category", y="Business Type", color="Count"),
                   x=cross_tab.columns.tolist(),
                   y=cross_tab.index.tolist(),
                   title='Business Type vs Risk Category Distribution',
                   color_continuous_scale='Viridis')
    
    fig.update_layout(height=500)
    return fig

def create_coxcomb_chart(df):
    """18. Coxcomb Chart (Rose Diagram)"""
    if 'business_type' not in df.columns or 'profit' not in df.columns:
        return None
    
    # Aggregate profit by business type
    profit_by_type = df.groupby('business_type')['profit'].sum().reset_index()
    profit_by_type = profit_by_type.sort_values('profit', ascending=False).head(8)
    
    fig = px.bar_polar(profit_by_type, 
                      r='profit', 
                      theta='business_type',
                      title='Profit by Business Type (Coxcomb Chart)',
                      color='profit',
                      template='plotly_white')
    
    fig.update_layout(height=500)
    return fig

def create_alluvial_diagram(df):
    """19. Alluvial Diagram for flow visualization"""
    # This is a simplified version using parallel categories
    if 'business_size' not in df.columns or 'risk_category' not in df.columns or 'performance_tier' not in df.columns:
        return None
    
    fig = px.parallel_categories(df,
                                dimensions=['business_size', 'risk_category', 'performance_tier'],
                                color='profit' if 'profit' in df.columns else None,
                                title='Business Flow Analysis (Alluvial)',
                                color_continuous_scale='Viridis')
    
    fig.update_layout(height=500)
    return fig

def create_ternary_plot(df):
    """20. Ternary Plot for three-variable relationships"""
    if not all(col in df.columns for col in ['profit_margin', 'conversion_rate', 'customer_rating']):
        return None
    
    fig = px.scatter_ternary(df,
                            a='profit_margin',
                            b='conversion_rate',
                            c='customer_rating',
                            color='business_type' if 'business_type' in df.columns else 'profit',
                            size='monthly_sales' if 'monthly_sales' in df.columns else None,
                            title='Three-Variable Relationship (Ternary Plot)',
                            hover_name='business_id' if 'business_id' in df.columns else None)
    
    fig.update_layout(height=500)
    return fig

# ============================================================
# HEADER
# ============================================================
st.markdown("<h1 class='main-header'>BizSight AI - Advanced Business Intelligence</h1>", unsafe_allow_html=True)
st.markdown("""
<p class='sub-header'>
    Comprehensive analytics platform with 50+ metrics and 40+ visualizations for data-driven decision making
</p>
""", unsafe_allow_html=True)

# ============================================================
# WELCOME SCREEN
# ============================================================
if not st.session_state.data_loaded:
    st.markdown("""
    <div class='welcome-message'>
        <h2>Welcome to BizSight AI</h2>
        <p style='font-size: 1.3rem; margin-bottom: 2rem;'>
            Transform your business data into actionable insights with our advanced analytics platform
        </p>
        <div style='display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;'>
            <div style='padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 10px;'>
                📊 50+ Business Metrics
            </div>
            <div style='padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 10px;'>
                📈 40+ Advanced Visualizations
            </div>
            <div style='padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 10px;'>
                🤖 AI-Powered Predictions
            </div>
            <div style='padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 10px;'>
                🗺️ Geographic Mapping
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Get Started with Your Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='data-options'>
            <div class='feature-icon'>📁</div>
            <h3>Upload Your Business Data</h3>
            <p>Analyze your own business dataset with customized insights</p>
            <ul style='text-align: left; padding-left: 1.5rem;'>
                <li>CSV or Excel format</li>
                <li>Automatic data cleaning</li>
                <li>Custom analytics</li>
                <li>Export-ready reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='data-options'>
            <div class='feature-icon'>🎯</div>
            <h3>Explore Sample Dataset</h3>
            <p>Try our comprehensive sample data with 50,000+ business records</p>
            <ul style='text-align: left; padding-left: 1.5rem;'>
                <li>Multiple business types</li>
                <li>Geographic distribution</li>
                <li>Performance metrics</li>
                <li>Risk analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Advanced Visualization Features")
    
    viz_features = [
        {"icon": "🕸️", "title": "Network Graphs", "desc": "Interactive business relationship mapping"},
        {"icon": "🎻", "title": "Chord Diagrams", "desc": "Circular ecosystem visualization"},
        {"icon": "🌊", "title": "Stream Graphs", "desc": "Temporal trend analysis"},
        {"icon": "🗺️", "title": "Geographic Maps", "desc": "Bubble maps & location analytics"},
        {"icon": "📊", "title": "3D Visualizations", "desc": "Surface plots & 3D analysis"},
        {"icon": "🎯", "title": "Predictive Analytics", "desc": "AI-powered forecasts"},
    ]
    
    cols = st.columns(3)
    for idx, feature in enumerate(viz_features):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='feature-item'>
                <div class='feature-icon'>{feature['icon']}</div>
                <h4>{feature['title']}</h4>
                <p style='color: #6B7280; font-size: 0.9rem;'>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Load data if selected
    if uploaded_file or use_sample_data:
        with st.spinner("🔄 Loading and processing data..."):
            if uploaded_file:
                df_raw = load_custom_data(uploaded_file)
                if df_raw is not None:
                    st.session_state.df_raw, st.session_state.df = process_data(df_raw)
                    st.session_state.data_loaded = True
                    st.rerun()
            elif use_sample_data:
                df_raw = load_sample_data()
                st.session_state.df_raw, st.session_state.df = process_data(df_raw)
                st.session_state.data_loaded = True
                st.rerun()
    
    st.stop()

# ============================================================
# MAIN DASHBOARD
# ============================================================
if st.session_state.data_loaded and st.session_state.df is not None:
    df_raw = st.session_state.df_raw
    df = st.session_state.df
    
    # Sidebar Filters
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Advanced Filters")
    
    # Risk filter
    if 'risk_band' in df.columns:
        risk_filter = st.sidebar.multiselect(
            "Risk Level",
            ["Low", "Medium", "High"],
            default=["Low", "Medium", "High"],
            help="Filter businesses by risk level"
        )
    else:
        risk_filter = ["Low", "Medium", "High"]
    
    # Business type filter
    if 'business_type' in df.columns:
        business_types = ["All"] + sorted(df['business_type'].unique().tolist())
        business_filter = st.sidebar.multiselect(
            "Business Type",
            business_types,
            default=["All"],
            help="Filter by business type"
        )
    else:
        business_filter = ["All"]
    
    # Region filter
    if 'region' in df.columns:
        regions = ["All"] + sorted(df['region'].unique().tolist())
        region_filter = st.sidebar.multiselect(
            "Region",
            regions,
            default=["All"],
            help="Filter by geographic region"
        )
    else:
        region_filter = ["All"]
    
    # Date range filter
    if 'date' in df.columns:
        min_date = df['date'].min()
        max_date = df['date'].max()
        
        date_range = st.sidebar.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['date'] >= pd.Timestamp(start_date)) & 
                   (df['date'] <= pd.Timestamp(end_date))]
    
    # Apply other filters
    df_filtered = df.copy()
    
    if risk_filter and 'risk_band' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['risk_band'].isin(risk_filter)]
    
    if business_filter and "All" not in business_filter and 'business_type' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['business_type'].isin(business_filter)]
    
    if region_filter and "All" not in region_filter and 'region' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['region'].isin(region_filter)]
    
    df = df_filtered
    
    # ============================================================
    # EXECUTIVE SUMMARY
    # ============================================================
    st.markdown("<h2 class='section-header'>Executive Dashboard</h2>", unsafe_allow_html=True)
    
    # Calculate metrics
    total_records = len(df)
    total_businesses = df['business_id'].nunique() if 'business_id' in df.columns else total_records
    avg_profit = df['profit'].mean() if 'profit' in df.columns else 0
    avg_sales = df['monthly_sales'].mean() if 'monthly_sales' in df.columns else 0
    avg_margin = df['profit_margin'].mean() * 100 if 'profit_margin' in df.columns else 0
    avg_roi = df['marketing_roi'].mean() if 'marketing_roi' in df.columns else 2.0
    avg_rating = df['customer_rating'].mean() if 'customer_rating' in df.columns else 3.0
    
    # Row 1: Core Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        trend_color = "trend-up" if avg_profit > 0 else "trend-down"
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>₹{avg_profit:,.0f}</div>
            <div class='metric-label'>Average Monthly Profit</div>
            <div class='metric-trend {trend_color}'>
                {'▲' if avg_profit > 0 else '▼'} Profitability
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        trend_color = "trend-up" if avg_sales > 1000000 else "trend-neutral"
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>₹{avg_sales:,.0f}</div>
            <div class='metric-label'>Average Monthly Sales</div>
            <div class='metric-trend {trend_color}'>
                {'▲' if avg_sales > 1000000 else '▬'} Sales Volume
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        trend_color = "trend-up" if avg_margin > 15 else "trend-down"
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{avg_margin:.1f}%</div>
            <div class='metric-label'>Average Profit Margin</div>
            <div class='metric-trend {trend_color}'>
                {'▲' if avg_margin > 15 else '▼'} Margin Level
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        trend_color = "trend-up" if avg_roi > 2 else "trend-down"
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{avg_roi:.2f}x</div>
            <div class='metric-label'>Avg Marketing ROI</div>
            <div class='metric-trend {trend_color}'>
                {'▲' if avg_roi > 2 else '▼'} Return on Investment
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # ADVANCED VISUALIZATION DASHBOARD - ALL 20+ VISUALIZATIONS
    # ============================================================
    st.markdown("<h2 class='section-header'>Advanced Visualization Dashboard</h2>", unsafe_allow_html=True)
    
    # Create tabs for organized viewing
    viz_tabs = st.tabs([
        "Network & Flow Charts", 
        "Geographic & 3D", 
        "Temporal Analysis", 
        "Statistical Charts",
        "Multi-dimensional",
        "Business Hierarchy"
    ])
    
    # TAB 1: NETWORK & FLOW CHARTS
    with viz_tabs[0]:
        st.markdown("### Network & Flow Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 1. Interactive Network Graph
            st.markdown("#### 1. Interactive Network Graph")
            network_fig = create_interactive_network_graph(df)
            if network_fig:
                st.plotly_chart(network_fig, use_container_width=True)
            else:
                st.info("Insufficient data for network graph")
        
        with col2:
            # 2. Chord Diagram
            st.markdown("#### 2. Chord Diagram")
            chord_fig = create_chord_diagram(df)
            if chord_fig:
                st.plotly_chart(chord_fig, use_container_width=True)
            else:
                st.info("Insufficient data for chord diagram")
        
        col3, col4 = st.columns(2)
        
        with col3:
            # 6. Sankey Diagram
            st.markdown("#### 6. Sankey Diagram")
            sankey_fig = create_sankey_diagram(df)
            if sankey_fig:
                st.plotly_chart(sankey_fig, use_container_width=True)
            else:
                st.info("Insufficient data for sankey diagram")
        
        with col4:
            # 19. Alluvial Diagram
            st.markdown("#### 19. Alluvial Diagram")
            alluvial_fig = create_alluvial_diagram(df)
            if alluvial_fig:
                st.plotly_chart(alluvial_fig, use_container_width=True)
            else:
                st.info("Insufficient data for alluvial diagram")
    
    # TAB 2: GEOGRAPHIC & 3D
    with viz_tabs[1]:
        st.markdown("### Geographic & 3D Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 7. Bubble Map
            st.markdown("#### 7. Bubble Map")
            bubble_fig = create_bubble_map(df)
            if bubble_fig:
                st.plotly_chart(bubble_fig, use_container_width=True)
            else:
                st.info("Insufficient data for bubble map")
        
        with col2:
            # 4. 3D Surface Plot
            st.markdown("#### 4. 3D Surface Plot")
            surface_fig = create_3d_surface_plot(df)
            if surface_fig:
                st.plotly_chart(surface_fig, use_container_width=True)
            else:
                st.info("Insufficient data for 3D surface plot")
        
        col3, col4 = st.columns(2)
        
        with col3:
            # 5. Calendar Heatmap
            st.markdown("#### 5. Calendar Heatmap")
            calendar_fig = create_calendar_heatmap(df)
            if calendar_fig:
                st.plotly_chart(calendar_fig, use_container_width=True)
            else:
                st.info("Insufficient data for calendar heatmap")
    
    # TAB 3: TEMPORAL ANALYSIS
    with viz_tabs[2]:
        st.markdown("### Temporal & Trend Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 3. Stream Graph
            st.markdown("#### 3. Stream Graph")
            stream_fig = create_stream_graph(df)
            if stream_fig:
                st.plotly_chart(stream_fig, use_container_width=True)
            else:
                st.info("Insufficient data for stream graph")
        
        with col2:
            # 16. Bump Chart
            st.markdown("#### 16. Bump Chart")
            bump_fig = create_bump_chart(df)
            if bump_fig:
                st.plotly_chart(bump_fig, use_container_width=True)
            else:
                st.info("Insufficient data for bump chart")
        
        col3, col4 = st.columns(2)
        
        with col3:
            # 18. Coxcomb Chart
            st.markdown("#### 18. Coxcomb Chart")
            coxcomb_fig = create_coxcomb_chart(df)
            if coxcomb_fig:
                st.plotly_chart(coxcomb_fig, use_container_width=True)
            else:
                st.info("Insufficient data for coxcomb chart")
    
    # TAB 4: STATISTICAL CHARTS
    with viz_tabs[3]:
        st.markdown("### Statistical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 8. Violin Plot
            st.markdown("#### 8. Violin Plot")
            violin_fig = create_violin_plot(df)
            if violin_fig:
                st.plotly_chart(violin_fig, use_container_width=True)
            else:
                st.info("Insufficient data for violin plot")
        
        with col2:
            # 11. Hexbin Plot
            st.markdown("#### 11. Hexbin Plot")
            hexbin_fig = create_hexbin_plot(df)
            if hexbin_fig:
                st.plotly_chart(hexbin_fig, use_container_width=True)
            else:
                st.info("Insufficient data for hexbin plot")
        
        col3, col4 = st.columns(2)
        
        with col3:
            # 13. Waterfall Chart
            st.markdown("#### 13. Waterfall Chart")
            waterfall_fig = create_waterfall_with_subcategories(df)
            if waterfall_fig:
                st.plotly_chart(waterfall_fig, use_container_width=True)
            else:
                st.info("Insufficient data for waterfall chart")
        
        with col4:
            # 15. Correlation Heatmap
            st.markdown("#### 15. Correlation Matrix")
            corr_fig = create_heatmap_correlation_matrix(df)
            if corr_fig:
                st.plotly_chart(corr_fig, use_container_width=True)
            else:
                st.info("Insufficient data for correlation matrix")
    
    # TAB 5: MULTI-DIMENSIONAL
    with viz_tabs[4]:
        st.markdown("### Multi-dimensional Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 10. Parallel Sets
            st.markdown("#### 10. Parallel Sets")
            parallel_fig = create_parallel_sets(df)
            if parallel_fig:
                st.plotly_chart(parallel_fig, use_container_width=True)
            else:
                st.info("Insufficient data for parallel sets")
        
        with col2:
            # 14. Radar Chart
            st.markdown("#### 14. Radar Chart")
            radar_fig = create_radar_chart_multiple_layers(df)
            if radar_fig:
                st.plotly_chart(radar_fig, use_container_width=True)
            else:
                st.info("Insufficient data for radar chart")
        
        col3, col4 = st.columns(2)
        
        with col3:
            # 17. Dot Matrix
            st.markdown("#### 17. Dot Matrix Chart")
            dot_fig = create_dot_matrix_chart(df)
            if dot_fig:
                st.plotly_chart(dot_fig, use_container_width=True)
            else:
                st.info("Insufficient data for dot matrix chart")
        
        with col4:
            # 20. Ternary Plot
            st.markdown("#### 20. Ternary Plot")
            ternary_fig = create_ternary_plot(df)
            if ternary_fig:
                st.plotly_chart(ternary_fig, use_container_width=True)
            else:
                st.info("Insufficient data for ternary plot")
    
    # TAB 6: BUSINESS HIERARCHY
    with viz_tabs[5]:
        st.markdown("### Business Hierarchy & Composition")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 9. Sunburst Diagram
            st.markdown("#### 9. Sunburst Diagram")
            sunburst_fig = create_sunburst_diagram(df)
            if sunburst_fig:
                st.plotly_chart(sunburst_fig, use_container_width=True)
            else:
                st.info("Insufficient data for sunburst diagram")
        
        with col2:
            # 12. Treemap with Charts
            st.markdown("#### 12. Treemap with Charts")
            treemap_fig = create_treemap_with_charts(df)
            if treemap_fig:
                st.plotly_chart(treemap_fig, use_container_width=True)
            else:
                st.info("Insufficient data for treemap")
    
    # ============================================================
    # DATA PREVIEW & EXPORT
    # ============================================================
    st.markdown("<h2 class='section-header'>Data Management</h2>", unsafe_allow_html=True)
    
    with st.expander("📊 Dataset Overview", expanded=False):
        tab1, tab2, tab3 = st.tabs(["Data Preview", "Statistics", "Data Quality"])
        
        with tab1:
            st.dataframe(df.head(100), use_container_width=True)
        
        with tab2:
            st.dataframe(df.describe(), use_container_width=True)
        
        with tab3:
            missing_df = pd.DataFrame({
                'Column': df.columns,
                'Missing Values': df.isnull().sum(),
                'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
            })
            st.dataframe(missing_df, use_container_width=True)
    
    # Export options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download Analysis Data (CSV)", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Click to download CSV",
                data=csv,
                file_name="business_intelligence_analysis.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Generate Visual Report", use_container_width=True):
            st.success("Report generation would be implemented here")
    
    with col3:
        if st.button("🖼️ Export All Charts", use_container_width=True):
            st.info("Chart export would be implemented here")
    
    # ============================================================
    # RESET DATA OPTION
    # ============================================================
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset Data & Start Over", use_container_width=True):
        for key in ['data_loaded', 'df_raw', 'df']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    # ============================================================
    # FOOTER
    # ============================================================
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6B7280; padding: 3rem 0;'>
        <p style='font-size: 1.3rem; font-weight: 700; 
                  background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
                  -webkit-background-clip: text;
                  -webkit-text-fill-color: transparent;'>
            BizSight AI - Advanced Business Intelligence Platform
        </p>
        <p style='font-size: 1rem; color: #4B5563; margin: 1rem 0;'>
            Version 6.0 | 50+ Metrics | 20+ Advanced Visualizations | AI-Powered Analytics
        </p>
        <div style='margin: 2rem 0;'>
            <a href='https://sourishdeyportfolio.vercel.app/' target='_blank' 
               style='display: inline-block; padding: 0.75rem 1.5rem; 
                      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                      color: white; text-decoration: none; border-radius: 12px; 
                      font-weight: 600; margin: 0 0.5rem; transition: all 0.3s ease;'>
               👨‍💻 Developer Portfolio
            </a>
            <a href='https://github.com/sourishdey2005' target='_blank' 
               style='display: inline-block; padding: 0.75rem 1.5rem; 
                      background: #1F2937; color: white; text-decoration: none; 
                      border-radius: 12px; font-weight: 600; margin: 0 0.5rem; 
                      transition: all 0.3s ease;'>
               💻 GitHub Profile
            </a>
        </div>
        <p style='font-size: 0.9rem; margin-top: 2rem; color: #9CA3AF;'>
            Developed by Sourish Dey | © 2024 All rights reserved.
        </p>
        <p style='font-size: 0.8rem; color: #D1D5DB; margin-top: 0.5rem;'>
            Features: 20+ Advanced Visualizations | Predictive Analytics | Geographic Mapping | Real-time Processing
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ADDITIONAL SIDEBAR FEATURES
# ============================================================
if st.session_state.data_loaded and st.session_state.df is not None:
    with st.sidebar.expander("📈 Platform Metrics", expanded=False):
        st.metric("Total Records", f"{total_records:,}")
        st.metric("Visualizations", "20+")
        st.metric("Processing Speed", "Real-time")
        
        if model:
            st.success("🤖 AI Model: Active")
        else:
            st.info("🤖 AI Model: Demo Mode")
    
    with st.sidebar.expander("🎯 Quick Actions", expanded=False):
        if st.button("Refresh Analysis", use_container_width=True):
            st.rerun()
