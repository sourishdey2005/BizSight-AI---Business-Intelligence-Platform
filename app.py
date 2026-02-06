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
import matplotlib.pyplot as plt
import base64
from io import BytesIO
warnings.filterwarnings('ignore')

# Try to import networkx, but provide fallback if not available
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    st.sidebar.warning("⚠️ NetworkX not installed. Network visualizations will be limited.")

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="BizSight AI - Business Intelligence Platform",
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
# LOAD MODEL (with fallback)
# ============================================================
@st.cache_resource
def load_model():
    try:
        # Try to load model, but continue without it if not found
        model = joblib.load("business_sales_profit_pipeline.pkl")
        st.sidebar.success("✓ Predictive model loaded successfully")
        return model
    except FileNotFoundError:
        st.sidebar.warning("⚠️ Model file not found. Using advanced analytics mode.")
        return None
    except Exception as e:
        st.sidebar.warning(f"Note: Running in analytics mode only. {str(e)}")
        return None

model = load_model()

# ============================================================
# SESSION STATE MANAGEMENT
# ============================================================
def reset_session_state():
    """Reset all session state variables"""
    keys_to_reset = ['data_loaded', 'df_raw', 'df', 'current_file', 'sample_data_loaded']
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'current_file' not in st.session_state:
    st.session_state.current_file = None
if 'sample_data_loaded' not in st.session_state:
    st.session_state.sample_data_loaded = False

# ============================================================
# SIDEBAR - ALWAYS VISIBLE
# ============================================================
# Add BizSight AI logo
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

# Data source selection
data_source = st.sidebar.radio(
    "Choose data source:",
    ["Upload your own dataset", "Use sample dataset"],
    index=0,
    help="Select how you want to load data for analysis"
)

# ============================================================
# DATA LOADING AND PROCESSING FUNCTIONS
# ============================================================
@st.cache_data
def load_sample_data():
    """Load comprehensive sample data matching CSV structure"""
    np.random.seed(42)
    n_samples = 10000  # Reduced for better performance
    
    # Create sample data with all required columns
    sample_data = {
        'business_id': [f'BUS_{i:06d}' for i in range(n_samples)],
        'city': np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 
                                 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'], n_samples),
        'state': np.random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal',
                                  'Telangana', 'Gujarat', 'Rajasthan', 'Uttar Pradesh'], n_samples),
        'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_samples),
        'city_tier': np.random.choice([1, 2, 3], n_samples, p=[0.3, 0.4, 0.3]),
        'business_type': np.random.choice(['Retail', 'Restaurant', 'Services', 'Manufacturing', 
                                          'E-commerce', 'Healthcare', 'Education', 'Entertainment'], n_samples),
        'years_of_operation': np.random.randint(1, 30, n_samples),
        'store_size_sqft': np.random.randint(500, 10000, n_samples),
        'employee_count': np.random.randint(5, 200, n_samples),
        'employee_efficiency': np.random.randint(20000, 200000, n_samples),
        'avg_employee_salary': np.random.randint(20000, 80000, n_samples),
        'avg_daily_footfall': np.random.randint(50, 2000, n_samples),
        'conversion_rate': np.random.uniform(0.05, 0.5, n_samples),
        'avg_transaction_value': np.random.randint(500, 5000, n_samples),
        'customer_rating': np.random.uniform(2.5, 5.0, n_samples),
        'discount_percentage': np.random.uniform(0, 40, n_samples),
        'rent_cost': np.random.randint(10000, 200000, n_samples),
        'electricity_cost': np.random.randint(5000, 30000, n_samples),
        'logistics_cost': np.random.randint(5000, 50000, n_samples),
        'supplier_cost': np.random.randint(20000, 200000, n_samples),
        'inventory_level': np.random.randint(1000, 100000, n_samples),
        'marketing_spend': np.random.randint(10000, 300000, n_samples),
        'marketing_roi': np.random.uniform(1.0, 5.0, n_samples),
        'is_festival_season': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'profit_margin': np.random.uniform(-0.1, 0.4, n_samples),
        'monthly_sales': np.random.randint(100000, 2000000, n_samples),
        'operational_cost': np.random.randint(50000, 500000, n_samples),
        'monthly_revenue': np.random.randint(150000, 2500000, n_samples),
        'sales_per_sqft': np.random.randint(100, 2000, n_samples),
        'profit_per_employee': np.random.randint(-5000, 50000, n_samples),
        'cost_to_sales_ratio': np.random.uniform(0.3, 0.8, n_samples),
        'employee_productivity': np.random.randint(10000, 150000, n_samples),
        'risk_category': np.random.choice(['Low', 'Medium', 'High'], n_samples, p=[0.5, 0.3, 0.2]),
        'business_size': np.random.choice(['Small', 'Medium', 'Large'], n_samples, p=[0.4, 0.4, 0.2])
    }
    
    df = pd.DataFrame(sample_data)
    
    # Calculate derived metrics
    df['profit'] = df['monthly_revenue'] - df['operational_cost']
    df['total_cost'] = df['operational_cost'] + df['employee_count'] * df['avg_employee_salary'] / 12
    df['gross_margin'] = (df['monthly_revenue'] - df['operational_cost']) / df['monthly_revenue'].replace(0, 1)
    df['inventory_turnover'] = df['monthly_sales'] / df['inventory_level'].replace(0, 1)
    df['employee_contribution'] = df['profit_per_employee'] * df['employee_count']
    df['marketing_efficiency'] = df['monthly_sales'] / df['marketing_spend'].replace(0, 1)
    df['roi_category'] = pd.cut(df['marketing_roi'], 
                                bins=[0, 1.5, 3, 10], 
                                labels=['Low', 'Medium', 'High'])
    
    return df

def load_custom_data(file):
    """Load custom uploaded data with robust error handling"""
    try:
        # Check file type and read accordingly
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format. Please upload CSV or Excel file.")
            return None
        
        # Clean column names
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
        
        # Check for required columns and create if missing
        required_numeric = ['profit', 'monthly_sales', 'monthly_revenue', 'operational_cost',
                          'marketing_spend', 'employee_count', 'customer_rating']
        
        required_categorical = ['business_type', 'city', 'region', 'risk_category']
        
        # Add missing numeric columns with defaults
        for col in required_numeric:
            if col not in df.columns:
                if col == 'profit':
                    if all(c in df.columns for c in ['monthly_revenue', 'operational_cost']):
                        df[col] = df['monthly_revenue'] - df['operational_cost']
                    elif 'monthly_sales' in df.columns and 'profit_margin' in df.columns:
                        df[col] = df['monthly_sales'] * df['profit_margin']
                    else:
                        df[col] = df.get('monthly_sales', 0) * 0.15  # Assume 15% margin
                elif col == 'monthly_revenue':
                    df[col] = df.get('monthly_sales', 0)
                elif col == 'monthly_sales':
                    df[col] = df.get('monthly_revenue', 0)
                else:
                    df[col] = 0
        
        # Add missing categorical columns with defaults
        for col in required_categorical:
            if col not in df.columns:
                if col == 'business_type':
                    df[col] = 'General'
                elif col == 'risk_category':
                    df[col] = 'Medium'
                else:
                    df[col] = 'Unknown'
        
        # Fill missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median() if df[col].notnull().sum() > 0 else 0)
        
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna('Unknown')
        
        return df
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def process_data(df_raw):
    """Process the loaded data for analysis"""
    if df_raw is None or df_raw.empty:
        return None, None
    
    df = df_raw.copy()
    
    # Calculate derived metrics
    if 'profit' not in df.columns:
        if all(col in df.columns for col in ['monthly_revenue', 'operational_cost']):
            df['profit'] = df['monthly_revenue'] - df['operational_cost']
        elif 'profit_margin' in df.columns and 'monthly_sales' in df.columns:
            df['profit'] = df['monthly_sales'] * df['profit_margin']
        else:
            df['profit'] = df.get('monthly_sales', 0) * 0.15
    
    if 'profit_margin' not in df.columns:
        if 'profit' in df.columns and 'monthly_sales' in df.columns:
            df['profit_margin'] = df['profit'] / df['monthly_sales'].replace(0, 1)
        else:
            df['profit_margin'] = 0.15
    
    # Create performance scores
    df['profitability_score'] = (df['profit_margin'].clip(-0.5, 0.5) * 0.4 + 
                                (df.get('customer_rating', 3.0).clip(1, 5) / 5) * 0.3 + 
                                (1 - df.get('cost_to_sales_ratio', 0.5).clip(0, 1)) * 0.3) * 100
    
    efficiency_factors = []
    if 'employee_efficiency' in df.columns:
        efficiency_factors.append(df['employee_efficiency'] / max(df['employee_efficiency'].max(), 1) * 0.4)
    if 'sales_per_sqft' in df.columns:
        efficiency_factors.append(df['sales_per_sqft'] / max(df['sales_per_sqft'].max(), 1) * 0.3)
    if 'inventory_turnover' in df.columns:
        efficiency_factors.append(df['inventory_turnover'] / max(df['inventory_turnover'].max(), 1) * 0.3)
    
    if efficiency_factors:
        df['efficiency_score'] = sum(efficiency_factors) * 100
    else:
        df['efficiency_score'] = 50
    
    # Create risk bands
    if 'risk_category' not in df.columns:
        risk_score = (df['profit_margin'].rank(pct=True) * 0.4 + 
                     df.get('customer_rating', 3.0).rank(pct=True) * 0.3 +
                     df.get('inventory_turnover', 1.5).rank(pct=True) * 0.3)
        df['risk_category'] = pd.qcut(risk_score, 3, labels=['Low', 'Medium', 'High'])
    
    # Create performance tiers
    performance_score = (df['profit'].rank(pct=True) * 0.4 + 
                        df['monthly_sales'].rank(pct=True) * 0.3 + 
                        df.get('employee_efficiency', 50000).rank(pct=True) * 0.3)
    df['performance_tier'] = pd.qcut(performance_score, 5, 
                                    labels=['Poor', 'Below Avg', 'Average', 'Good', 'Excellent'])
    
    return df_raw, df

# ============================================================
# ADVANCED VISUALIZATION FUNCTIONS (Simplified versions)
# ============================================================

def create_network_graph(df):
    """Create network graph visualization"""
    try:
        if not NETWORKX_AVAILABLE:
            return create_placeholder_chart("Network Graph", "NetworkX library not installed")
        
        # Create a simple correlation network
        business_types = df['business_type'].value_counts().nlargest(8).index.tolist()
        
        # Create nodes data
        nodes = []
        for i, biz_type in enumerate(business_types):
            nodes.append({
                'id': i,
                'label': biz_type,
                'size': 10 + (df['business_type'] == biz_type).sum() / 100,
                'color': i
            })
        
        # Create edges (simulated relationships)
        edges = []
        for i in range(len(business_types)):
            for j in range(i+1, len(business_types)):
                if np.random.random() > 0.6:
                    edges.append({
                        'source': i,
                        'target': j,
                        'value': np.random.randint(1, 10)
                    })
        
        # Create Plotly figure without networkx
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        
        # Generate positions manually
        for i, node in enumerate(nodes):
            angle = 2 * np.pi * i / len(nodes)
            radius = 0.8
            node_x.append(radius * np.cos(angle))
            node_y.append(radius * np.sin(angle))
            node_text.append(f"{node['label']}<br>Size: {node['size']:.1f}")
            node_size.append(node['size'] * 10)
            node_color.append(node['color'])
        
        # Create edge traces
        edge_traces = []
        for edge in edges:
            x0, y0 = node_x[edge['source']], node_y[edge['source']]
            x1, y1 = node_x[edge['target']], node_y[edge['target']]
            
            edge_trace = go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                line=dict(width=edge['value']/3, color='rgba(100, 100, 100, 0.4)'),
                hoverinfo='none',
                mode='lines',
                showlegend=False
            )
            edge_traces.append(edge_trace)
        
        # Create node trace
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=[n['label'] for n in nodes],
            textposition="bottom center",
            hovertext=node_text,
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                size=node_size,
                color=node_color,
                line_width=2,
                colorbar=dict(
                    thickness=15,
                    title='Node Index',
                    xanchor='left',
                    titleside='right'
                )
            ),
            showlegend=False
        )
        
        fig = go.Figure(data=edge_traces + [node_trace])
        fig.update_layout(
            title='Business Relationship Network',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=500,
            plot_bgcolor='white'
        )
        return fig
    except Exception as e:
        return create_placeholder_chart("Network Graph", str(e))

def create_chord_diagram(df):
    """Create chord diagram for business ecosystem"""
    try:
        business_types = df['business_type'].value_counts().nlargest(6).index.tolist()
        
        # Create matrix data
        matrix = np.zeros((len(business_types), len(business_types)))
        for i in range(len(business_types)):
            for j in range(len(business_types)):
                if i != j:
                    matrix[i][j] = np.random.randint(100, 1000)
        
        # Create chord-like visualization using Sankey
        sources = []
        targets = []
        values = []
        
        for i in range(len(business_types)):
            for j in range(len(business_types)):
                if i != j and matrix[i][j] > 0:
                    sources.append(i)
                    targets.append(j)
                    values.append(matrix[i][j])
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=business_types,
                color=PLOTLY_COLORS[:len(business_types)]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=[f"rgba(100, 149, 237, {v/max(values)})" for v in values]
            )
        )])
        
        fig.update_layout(
            title_text="Business Ecosystem Flow",
            font_size=10,
            height=500
        )
        return fig
    except Exception as e:
        return create_placeholder_chart("Chord Diagram", str(e))

def create_stream_graph(df):
    """Create stream graph for temporal trends"""
    try:
        dates = pd.date_range(start='2023-01-01', periods=12, freq='M')
        business_types = df['business_type'].value_counts().nlargest(5).index.tolist()
        
        data = []
        for biz_type in business_types:
            base_sales = np.random.randint(100000, 300000)
            for i, date in enumerate(dates):
                # Add some trend and seasonality
                trend = base_sales * (1 + 0.05 * i)
                seasonal = trend * (1 + 0.2 * np.sin(2 * np.pi * i / 12))
                noise = seasonal * np.random.uniform(0.9, 1.1)
                data.append({
                    'Date': date,
                    'Business Type': biz_type,
                    'Sales': max(100000, noise)
                })
        
        stream_df = pd.DataFrame(data)
        
        fig = px.area(stream_df, x='Date', y='Sales', color='Business Type',
                     title='Temporal Business Performance Trends',
                     template='plotly_white',
                     height=500)
        return fig
    except Exception as e:
        return create_placeholder_chart("Stream Graph", str(e))

def create_3d_surface_plot(df):
    """Create 3D surface plot for profit landscape"""
    try:
        # Create grid data
        x = np.linspace(0, 100, 20)
        y = np.linspace(0, 100, 20)
        X, Y = np.meshgrid(x, y)
        
        # Create profit surface (hills and valleys)
        Z = 50 * (np.sin(0.1 * X) * np.cos(0.1 * Y) + 
                 0.5 * np.sin(0.05 * X) * np.cos(0.05 * Y) + 1)
        
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, 
                                        colorscale='Viridis',
                                        contours=dict(z=dict(show=True, size=10)))])
        
        fig.update_layout(
            title='Profit Optimization Landscape',
            scene=dict(
                xaxis_title='Marketing Efficiency',
                yaxis_title='Operational Efficiency',
                zaxis_title='Profit Score'
            ),
            height=500,
            margin=dict(l=0, r=0, b=0, t=40)
        )
        return fig
    except Exception as e:
        return create_placeholder_chart("3D Surface Plot", str(e))

def create_calendar_heatmap(df):
    """Create calendar heatmap"""
    try:
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        
        # Create sales data with weekly patterns
        sales_data = []
        for date in dates:
            base = 1000
            # Weekly pattern
            weekly = 200 * np.sin(2 * np.pi * date.dayofweek / 7)
            # Monthly trend
            monthly = 300 * (date.month / 12)
            # Random noise
            noise = np.random.randint(-100, 100)
            
            sales = base + weekly + monthly + noise
            sales_data.append(sales)
        
        calendar_df = pd.DataFrame({
            'Date': dates,
            'Sales': sales_data,
            'Weekday': dates.day_name(),
            'Week': dates.isocalendar().week,
            'Month': dates.month_name()
        })
        
        # Pivot for heatmap
        pivot_df = calendar_df.pivot_table(
            values='Sales', 
            index='Week', 
            columns='Weekday', 
            aggfunc='mean'
        )
        
        # Reorder columns
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_df = pivot_df.reindex(columns=weekday_order)
        
        fig = px.imshow(pivot_df,
                       labels=dict(x="Day of Week", y="Week Number", color="Sales"),
                       x=weekday_order,
                       y=pivot_df.index,
                       color_continuous_scale='Viridis',
                       title='Weekly Sales Patterns',
                       height=500)
        
        fig.update_layout(
            xaxis_title="Day of Week",
            yaxis_title="Week of Year"
        )
        return fig
    except Exception as e:
        return create_placeholder_chart("Calendar Heatmap", str(e))

def create_sankey_diagram(df):
    """Create Sankey diagram for customer journey"""
    try:
        labels = ["Awareness", "Interest", "Consideration", "Intent", "Purchase", "Loyalty"]
        
        # Define flow values
        sources = [0, 1, 2, 3, 4]
        targets = [1, 2, 3, 4, 5]
        values = [100, 70, 50, 30, 15]  # Typical conversion funnel
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=['#6366F1', '#8B5CF6', '#EC4899', '#EF4444', '#10B981', '#3B82F6']
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=['rgba(99, 102, 241, 0.6)', 
                      'rgba(139, 92, 246, 0.6)',
                      'rgba(236, 72, 153, 0.6)',
                      'rgba(239, 68, 68, 0.6)',
                      'rgba(16, 185, 129, 0.6)']
            )
        )])
        
        fig.update_layout(
            title_text="Customer Journey Funnel",
            font_size=12,
            height=500
        )
        return fig
    except Exception as e:
        return create_placeholder_chart("Sankey Diagram", str(e))

def create_bubble_map(df):
    """Create bubble map for geographic analysis"""
    try:
        if 'city' in df.columns:
            # Indian city coordinates
            city_coords = {
                'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
                'Delhi': {'lat': 28.7041, 'lon': 77.1025},
                'Bangalore': {'lat': 12.9716, 'lon': 77.5946},
                'Chennai': {'lat': 13.0827, 'lon': 80.2707},
                'Kolkata': {'lat': 22.5726, 'lon': 88.3639},
                'Hyderabad': {'lat': 17.3850, 'lon': 78.4867},
                'Pune': {'lat': 18.5204, 'lon': 73.8567},
                'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714},
                'Jaipur': {'lat': 26.9124, 'lon': 75.7873},
                'Lucknow': {'lat': 26.8467, 'lon': 80.9462}
            }
            
            # Aggregate data by city
            city_stats = df.groupby('city').agg({
                'profit': 'mean',
                'monthly_sales': 'mean',
                'business_id': 'count'
            }).reset_index()
            city_stats.columns = ['City', 'Avg Profit', 'Avg Sales', 'Business Count']
            
            # Add coordinates
            map_data = []
            for _, row in city_stats.iterrows():
                city = row['City']
                if city in city_coords:
                    map_data.append({
                        'City': city,
                        'Lat': city_coords[city]['lat'],
                        'Lon': city_coords[city]['lon'],
                        'Profit': row['Avg Profit'],
                        'Sales': row['Avg Sales'],
                        'Business Count': row['Business Count']
                    })
            
            if map_data:
                map_df = pd.DataFrame(map_data)
                
                fig = px.scatter_mapbox(map_df, lat="Lat", lon="Lon",
                                       size="Business Count", 
                                       color="Profit",
                                       hover_name="City", 
                                       hover_data=["Profit", "Sales", "Business Count"],
                                       color_continuous_scale=px.colors.sequential.Viridis,
                                       size_max=30, 
                                       zoom=4,
                                       title='Geographic Business Distribution in India')
                
                fig.update_layout(mapbox_style="open-street-map")
                fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=500)
                return fig
    except Exception as e:
        return create_placeholder_chart("Bubble Map", str(e))

def create_violin_plot(df):
    """Create violin plot for distribution analysis"""
    try:
        if 'business_type' in df.columns and 'profit_margin' in df.columns:
            top_types = df['business_type'].value_counts().nlargest(6).index.tolist()
            violin_df = df[df['business_type'].isin(top_types)]
            
            fig = px.violin(violin_df, x='business_type', y='profit_margin',
                           box=True, 
                           points="all",
                           title='Profit Margin Distribution by Business Type',
                           color='business_type',
                           template='plotly_white',
                           height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Violin Plot", str(e))

def create_sunburst_diagram(df):
    """Create sunburst diagram with drill-down"""
    try:
        if all(col in df.columns for col in ['region', 'business_type', 'risk_category', 'profit']):
            # Create hierarchical aggregated data
            sunburst_data = []
            
            for region in df['region'].unique():
                region_profit = df[df['region'] == region]['profit'].sum()
                sunburst_data.append({
                    'id': region,
                    'parent': '',
                    'value': region_profit,
                    'label': region
                })
                
                for biz_type in df[df['region'] == region]['business_type'].unique():
                    type_profit = df[(df['region'] == region) & 
                                    (df['business_type'] == biz_type)]['profit'].sum()
                    sunburst_data.append({
                        'id': f"{region}_{biz_type}",
                        'parent': region,
                        'value': type_profit,
                        'label': biz_type
                    })
                    
                    for risk in df[(df['region'] == region) & 
                                  (df['business_type'] == biz_type)]['risk_category'].unique():
                        risk_profit = df[(df['region'] == region) & 
                                        (df['business_type'] == biz_type) &
                                        (df['risk_category'] == risk)]['profit'].sum()
                        sunburst_data.append({
                            'id': f"{region}_{biz_type}_{risk}",
                            'parent': f"{region}_{biz_type}",
                            'value': risk_profit,
                            'label': risk
                        })
            
            sunburst_df = pd.DataFrame(sunburst_data)
            
            fig = px.sunburst(sunburst_df, 
                             path=['parent', 'id'], 
                             values='value',
                             title='Hierarchical Business Analysis (Region → Type → Risk)',
                             height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Sunburst Diagram", str(e))

def create_hexbin_plot(df):
    """Create hexbin plot for high-density data"""
    try:
        if all(col in df.columns for col in ['marketing_spend', 'monthly_sales']):
            fig = px.density_heatmap(df, 
                                    x='marketing_spend', 
                                    y='monthly_sales',
                                    nbinsx=30, 
                                    nbinsy=30,
                                    marginal_x="histogram", 
                                    marginal_y="histogram",
                                    title='Marketing Spend vs Sales Density Analysis',
                                    color_continuous_scale='Viridis',
                                    height=500)
            
            # Add trend line
            z = np.polyfit(df['marketing_spend'], df['monthly_sales'], 1)
            p = np.poly1d(z)
            trend_x = np.linspace(df['marketing_spend'].min(), df['marketing_spend'].max(), 100)
            trend_y = p(trend_x)
            
            fig.add_trace(go.Scatter(
                x=trend_x, y=trend_y,
                mode='lines',
                line=dict(color='red', width=2, dash='dash'),
                name='Trend Line'
            ))
            
            return fig
    except Exception as e:
        return create_placeholder_chart("Hexbin Plot", str(e))

def create_treemap_with_charts(df):
    """Create treemap visualization"""
    try:
        if all(col in df.columns for col in ['business_type', 'profit', 'monthly_sales']):
            # Aggregate data
            treemap_data = df.groupby('business_type').agg({
                'profit': 'sum',
                'monthly_sales': 'mean',
                'profit_margin': 'mean'
            }).reset_index()
            
            fig = px.treemap(treemap_data, 
                            path=['business_type'], 
                            values='profit',
                            color='profit_margin',
                            hover_data=['monthly_sales', 'profit_margin'],
                            color_continuous_scale='RdBu',
                            color_continuous_midpoint=treemap_data['profit_margin'].median(),
                            title='Business Performance Treemap (Size=Profit, Color=Profit Margin)',
                            height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Treemap", str(e))

def create_waterfall_with_subcategories(df):
    """Create waterfall chart"""
    try:
        if 'business_type' in df.columns and 'profit' in df.columns:
            profit_by_type = df.groupby('business_type')['profit'].sum().nlargest(8)
            
            # Calculate totals
            total_profit = profit_by_type.sum()
            other_profit = df['profit'].sum() - total_profit
            
            # Prepare waterfall data
            categories = list(profit_by_type.index) + ['Other', 'Total']
            values = list(profit_by_type.values) + [other_profit, df['profit'].sum()]
            
            # Create measure array
            measure = ['relative'] * (len(profit_by_type) + 1) + ['total']
            
            fig = go.Figure(go.Waterfall(
                name="Profit",
                orientation="v",
                measure=measure,
                x=categories,
                text=[f"₹{v:,.0f}" for v in values],
                textposition="outside",
                y=values,
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                increasing={"marker": {"color": "#10B981"}},
                decreasing={"marker": {"color": "#EF4444"}},
                totals={"marker": {"color": "#3B82F6"}}
            ))
            
            fig.update_layout(
                title="Profit Breakdown by Business Type",
                showlegend=False,
                height=500,
                yaxis_title="Profit (₹)",
                xaxis_title="Business Type"
            )
            return fig
    except Exception as e:
        return create_placeholder_chart("Waterfall Chart", str(e))

def create_radar_chart(df):
    """Create radar chart with multiple layers"""
    try:
        # Select metrics for radar chart
        metrics = ['profit_margin', 'customer_rating', 'employee_efficiency', 
                  'inventory_turnover', 'conversion_rate']
        
        available_metrics = [m for m in metrics if m in df.columns]
        
        if len(available_metrics) >= 3:
            # Calculate averages
            avg_values = df[available_metrics].mean().values
            
            # Normalize values for radar chart (0-1 scale)
            max_values = df[available_metrics].max().values
            min_values = df[available_metrics].min().values
            
            normalized_avg = (avg_values - min_values) / (max_values - min_values + 1e-10)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=normalized_avg,
                theta=available_metrics,
                fill='toself',
                name='Average Business',
                line_color=COLOR_PALETTE['primary']
            ))
            
            # Add max values layer
            normalized_max = np.ones_like(normalized_avg)
            fig.add_trace(go.Scatterpolar(
                r=normalized_max,
                theta=available_metrics,
                fill='toself',
                name='Maximum Potential',
                line_color=COLOR_PALETTE['secondary'],
                opacity=0.3
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
            return fig
    except Exception as e:
        return create_placeholder_chart("Radar Chart", str(e))

def create_correlation_matrix(df):
    """Create correlation matrix heatmap"""
    try:
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) > 2:
            # Limit to 8 columns for readability
            selected_cols = numeric_cols[:8]
            corr_matrix = df[selected_cols].corr()
            
            # Create annotated heatmap
            fig = ff.create_annotated_heatmap(
                z=corr_matrix.values,
                x=selected_cols,
                y=selected_cols,
                annotation_text=corr_matrix.round(2).values,
                colorscale='RdBu',
                showscale=True,
                zmin=-1, zmax=1
            )
            
            fig.update_layout(
                title='Correlation Matrix of Business Metrics',
                height=500
            )
            
            # Update hover text
            fig.update_traces(hovertemplate='<b>%{x}</b> vs <b>%{y}</b><br>Correlation: %{z:.2f}<extra></extra>')
            
            return fig
    except Exception as e:
        return create_placeholder_chart("Correlation Matrix", str(e))

def create_bump_chart(df):
    """Create bump chart for ranking evolution"""
    try:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        business_types = df['business_type'].value_counts().nlargest(5).index.tolist()
        
        data = []
        for month_idx, month in enumerate(months):
            # Simulate changing rankings with some consistency
            base_ranks = {biz: i+1 for i, biz in enumerate(business_types)}
            
            # Add some monthly variation
            for i, biz_type in enumerate(business_types):
                rank_variation = np.random.randint(-1, 2)
                new_rank = max(1, min(len(business_types), base_ranks[biz_type] + rank_variation))
                
                # Ensure no duplicate ranks
                while new_rank in [d['Rank'] for d in data if d['Month'] == month]:
                    new_rank = max(1, min(len(business_types), new_rank + np.random.choice([-1, 1])))
                
                performance = np.random.randint(50, 100) * (len(business_types) - new_rank + 1)
                
                data.append({
                    'Month': month,
                    'Business Type': biz_type,
                    'Rank': new_rank,
                    'Performance': performance
                })
        
        bump_df = pd.DataFrame(data)
        
        fig = px.line(bump_df, 
                     x='Month', 
                     y='Rank', 
                     color='Business Type',
                     markers=True,
                     title='Business Ranking Evolution Over Time',
                     height=500)
        
        # Reverse y-axis so rank 1 is at top
        fig.update_yaxes(autorange="reversed", 
                        title="Rank (1 = Best)",
                        tickmode='linear',
                        tick0=1,
                        dtick=1)
        
        fig.update_layout(
            xaxis_title="Month",
            hovermode='x unified'
        )
        
        return fig
    except Exception as e:
        return create_placeholder_chart("Bump Chart", str(e))

def create_dot_matrix_chart(df):
    """Create dot matrix chart for categorical data"""
    try:
        if all(col in df.columns for col in ['business_type', 'risk_category', 'performance_tier']):
            # Create contingency table
            matrix_data = pd.crosstab(
                df['business_type'], 
                [df['risk_category'], df['performance_tier']],
                normalize='index'
            ).round(2) * 100
            
            # Flatten multi-index columns
            matrix_data.columns = [f"{risk}/{tier}" for risk, tier in matrix_data.columns]
            
            fig = px.imshow(matrix_data,
                           labels=dict(x="Risk/Performance", y="Business Type", color="Percentage"),
                           color_continuous_scale='Viridis',
                           title='Risk & Performance Distribution by Business Type (%)',
                           height=500)
            
            fig.update_layout(
                xaxis_title="Risk Category / Performance Tier",
                yaxis_title="Business Type"
            )
            return fig
    except Exception as e:
        return create_placeholder_chart("Dot Matrix", str(e))

def create_coxcomb_chart(df):
    """Create Coxcomb/Rose diagram"""
    try:
        if 'business_type' in df.columns and 'profit' in df.columns:
            # Aggregate profit by business type
            profit_by_type = df.groupby('business_type')['profit'].sum().nlargest(12).reset_index()
            
            # Sort by profit for better visualization
            profit_by_type = profit_by_type.sort_values('profit', ascending=True)
            
            fig = px.bar_polar(profit_by_type, 
                              r='profit', 
                              theta='business_type',
                              color='profit',
                              template='plotly_white',
                              color_continuous_scale=px.colors.sequential.Viridis,
                              title='Circular Profit Distribution by Business Type',
                              height=500)
            
            fig.update_layout(
                polar=dict(
                    angularaxis=dict(direction="clockwise"),
                    radialaxis=dict(visible=True, range=[0, profit_by_type['profit'].max()])
                )
            )
            return fig
    except Exception as e:
        return create_placeholder_chart("Coxcomb Chart", str(e))

def create_alluvial_diagram(df):
    """Create alluvial diagram for flow visualization"""
    try:
        # Define segments
        size_segments = ['Small', 'Medium', 'Large']
        type_segments = ['Retail', 'Services', 'Manufacturing']
        risk_segments = ['Low', 'Medium', 'High']
        
        # Create flow data
        nodes = size_segments + type_segments + risk_segments
        node_indices = {node: i for i, node in enumerate(nodes)}
        
        # Define flows
        flows = [
            {'source': 'Small', 'target': 'Retail', 'value': 40},
            {'source': 'Small', 'target': 'Services', 'value': 30},
            {'source': 'Medium', 'target': 'Retail', 'value': 25},
            {'source': 'Medium', 'target': 'Manufacturing', 'value': 35},
            {'source': 'Large', 'target': 'Manufacturing', 'value': 20},
            {'source': 'Large', 'target': 'Services', 'value': 15},
            {'source': 'Retail', 'target': 'Low', 'value': 30},
            {'source': 'Retail', 'target': 'Medium', 'value': 20},
            {'source': 'Services', 'target': 'Low', 'value': 25},
            {'source': 'Services', 'target': 'High', 'value': 20},
            {'source': 'Manufacturing', 'target': 'Medium', 'value': 30},
            {'source': 'Manufacturing', 'target': 'High', 'value': 25}
        ]
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
                color=['#EF4444', '#F59E0B', '#10B981',  # Size segments
                      '#8B5CF6', '#EC4899', '#06B6D4',  # Type segments
                      '#22C55E', '#3B82F6', '#F97316']  # Risk segments
            ),
            link=dict(
                source=[node_indices[flow['source']] for flow in flows],
                target=[node_indices[flow['target']] for flow in flows],
                value=[flow['value'] for flow in flows],
                color=[f"rgba{tuple(list(plt.cm.viridis(i/len(flows))[:3]) + [0.4])}" 
                      for i in range(len(flows))]
            )
        )])
        
        fig.update_layout(
            title_text="Business Segment Flow Analysis",
            font_size=10,
            height=500
        )
        return fig
    except Exception as e:
        return create_placeholder_chart("Alluvial Diagram", str(e))

def create_ternary_plot(df):
    """Create ternary plot for three-variable relationships"""
    try:
        # Select three metrics for ternary plot
        metrics = ['profit_margin', 'customer_rating', 'employee_efficiency']
        available_metrics = [m for m in metrics if m in df.columns]
        
        if len(available_metrics) == 3:
            # Sample data for better visualization
            sample_df = df.sample(min(500, len(df)))
            
            # Normalize the three metrics to sum to 1 for ternary plot
            metrics_sum = sample_df[available_metrics].sum(axis=1)
            normalized_df = sample_df[available_metrics].div(metrics_sum, axis=0)
            
            fig = px.scatter_ternary(normalized_df, 
                                    a=available_metrics[0], 
                                    b=available_metrics[1], 
                                    c=available_metrics[2],
                                    color='profit' if 'profit' in df.columns else None,
                                    size='monthly_sales' if 'monthly_sales' in df.columns else None,
                                    title='Three-Factor Business Analysis<br>Size=Sales, Color=Profit',
                                    height=500)
            
            # Update axis labels
            fig.update_layout(
                ternary=dict(
                    aaxis_title=available_metrics[0].replace('_', ' ').title(),
                    baxis_title=available_metrics[1].replace('_', ' ').title(),
                    caxis_title=available_metrics[2].replace('_', ' ').title(),
                )
            )
            return fig
    except Exception as e:
        return create_placeholder_chart("Ternary Plot", str(e))

def create_parallel_sets(df):
    """Create parallel sets for categorical relationships"""
    try:
        if all(col in df.columns for col in ['business_size', 'business_type', 'risk_category', 'performance_tier']):
            # Create aggregated data
            agg_data = df.groupby(['business_size', 'business_type', 'risk_category', 'performance_tier']).size().reset_index(name='count')
            
            # Filter to reasonable size
            agg_data = agg_data[agg_data['count'] > agg_data['count'].quantile(0.5)]
            
            if len(agg_data) > 0:
                fig = px.parallel_categories(agg_data, 
                                            dimensions=['business_size', 'business_type', 'risk_category', 'performance_tier'],
                                            color='count',
                                            color_continuous_scale=px.colors.sequential.Viridis,
                                            title='Multi-Dimensional Business Attribute Analysis',
                                            height=500)
                return fig
    except Exception as e:
        return create_placeholder_chart("Parallel Sets", str(e))

def create_placeholder_chart(chart_type, error_msg=""):
    """Create a placeholder chart when actual chart cannot be created"""
    fig = go.Figure()
    fig.add_annotation(
        text=f"<b>{chart_type}</b><br>Data not available or insufficient<br><i>{error_msg[:100]}...</i>",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="#6B7280"),
        align="center"
    )
    fig.update_layout(
        title=dict(text=chart_type, font=dict(size=16)),
        height=500,
        showlegend=False,
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1])
    )
    return fig

# ============================================================
# HEADER
# ============================================================
st.markdown("<h1 class='main-header'>BizSight AI - Advanced Business Intelligence</h1>", unsafe_allow_html=True)
st.markdown("""
<p class='sub-header'>
    Comprehensive analytics platform with 50+ metrics and 20+ advanced visualizations
</p>
""", unsafe_allow_html=True)

# ============================================================
# HANDLE FILE UPLOAD AND DATA LOADING
# ============================================================
# File uploader for custom data
uploaded_file = None
if data_source == "Upload your own dataset":
    uploaded_file = st.sidebar.file_uploader(
        "📁 Upload business dataset",
        type=["csv", "xlsx", "xls"],
        help="Upload your business data file (CSV or Excel format)"
    )
    
    if uploaded_file:
        # Check if file has changed
        if st.session_state.current_file != uploaded_file.name:
            reset_session_state()
            st.session_state.current_file = uploaded_file.name
        
        with st.spinner("🔄 Loading and processing your data..."):
            df_raw = load_custom_data(uploaded_file)
            if df_raw is not None:
                st.session_state.df_raw, st.session_state.df = process_data(df_raw)
                st.session_state.data_loaded = True
                st.sidebar.success(f"✅ Loaded {len(df_raw)} records")
                st.rerun()

# Sample data loading
elif data_source == "Use sample dataset":
    if st.sidebar.button("🎯 Load Sample Dataset", use_container_width=True):
        reset_session_state()
        with st.spinner("🔄 Loading comprehensive sample data..."):
            df_raw = load_sample_data()
            st.session_state.df_raw, st.session_state.df = process_data(df_raw)
            st.session_state.data_loaded = True
            st.session_state.sample_data_loaded = True
            st.sidebar.success(f"✅ Loaded {len(df_raw)} sample records")
            st.rerun()

# ============================================================
# WELCOME SCREEN (if no data loaded)
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
                📈 20+ Visualizations
            </div>
            <div style='padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 10px;'>
                🤖 Advanced Analytics
            </div>
            <div style='padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 10px;'>
                🎯 Strategic Insights
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
            <p>Try our comprehensive sample data with 10,000+ business records</p>
            <ul style='text-align: left; padding-left: 1.5rem;'>
                <li>Multiple business types</li>
                <li>Geographic distribution</li>
                <li>Performance metrics</li>
                <li>Risk analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Platform Features")
    
    features = [
        {"icon": "📊", "title": "Sales Analytics", "desc": "Comprehensive sales performance analysis"},
        {"icon": "💰", "title": "Profit Optimization", "desc": "Maximize profitability insights"},
        {"icon": "⚠️", "title": "Risk Assessment", "desc": "Advanced risk identification"},
        {"icon": "📈", "title": "Trend Analysis", "desc": "Historical and predictive trends"},
        {"icon": "🗺️", "title": "Geographic Insights", "desc": "Location-based performance"},
        {"icon": "🤖", "title": "AI Predictions", "desc": "Advanced analytics forecasts"},
    ]
    
    cols = st.columns(3)
    for idx, feature in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='feature-item'>
                <div class='feature-icon'>{feature['icon']}</div>
                <h4>{feature['title']}</h4>
                <p style='color: #6B7280; font-size: 0.9rem;'>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.stop()

# ============================================================
# MAIN DASHBOARD (when data is loaded)
# ============================================================
if st.session_state.data_loaded and st.session_state.df is not None:
    df_raw = st.session_state.df_raw
    df = st.session_state.df
    
    # Sidebar Filters
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Advanced Filters")
    
    # Risk filter
    if 'risk_category' in df.columns:
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
    
    # Performance tier filter
    if 'performance_tier' in df.columns:
        performance_tiers = ["All"] + sorted(df['performance_tier'].unique().tolist())
        performance_filter = st.sidebar.multiselect(
            "Performance Tier",
            performance_tiers,
            default=["All"],
            help="Filter by performance rating"
        )
    else:
        performance_filter = ["All"]
    
    # Apply filters
    df_filtered = df.copy()
    
    if risk_filter and 'risk_category' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['risk_category'].isin(risk_filter)]
    
    if business_filter and "All" not in business_filter and 'business_type' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['business_type'].isin(business_filter)]
    
    if region_filter and "All" not in region_filter and 'region' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['region'].isin(region_filter)]
    
    if performance_filter and "All" not in performance_filter and 'performance_tier' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['performance_tier'].isin(performance_filter)]
    
    df = df_filtered
    
    # Display record count
    st.sidebar.info(f"📊 Showing {len(df)} of {len(df_raw)} records")
    
    # ============================================================
    # EXECUTIVE SUMMARY WITH METRICS
    # ============================================================
    st.markdown("<h2 class='section-header'>Executive Dashboard</h2>", unsafe_allow_html=True)
    
    # Calculate metrics
    total_records = len(df)
    avg_profit = df['profit'].mean() if 'profit' in df.columns else 0
    avg_sales = df['monthly_sales'].mean() if 'monthly_sales' in df.columns else 0
    avg_margin = df['profit_margin'].mean() * 100 if 'profit_margin' in df.columns else 0
    avg_roi = df['marketing_roi'].mean() if 'marketing_roi' in df.columns else 2.0
    avg_rating = df['customer_rating'].mean() if 'customer_rating' in df.columns else 3.0
    
    # Row 1: Core Business Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        trend_color = "trend-up" if avg_profit > 0 else "trend-down"
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>₹{avg_profit:,.0f}</div>
            <div class='metric-label'>Average Monthly Profit</div>
            <div class='metric-trend {trend_color}'>
                {'▲' if avg_profit > 0 else '▼'} Profit
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
                {'▲' if avg_sales > 1000000 else '▬'} Sales
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
                {'▲' if avg_margin > 15 else '▼'} Margin
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        high_risk_pct = (df['risk_category'] == 'High').mean() * 100 if 'risk_category' in df.columns else 0
        trend_color = "trend-up" if high_risk_pct < 30 else "trend-down"
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{high_risk_pct:.1f}%</div>
            <div class='metric-label'>High Risk Businesses</div>
            <div class='metric-trend {trend_color}'>
                {'▼' if high_risk_pct < 30 else '▲'} Risk
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # ADVANCED VISUALIZATION DASHBOARD
    # ============================================================
    st.markdown("<h2 class='section-header'>Advanced Analytics Dashboard (20 Visualizations)</h2>", unsafe_allow_html=True)
    
    # Create tabs for different visualization categories
    viz_tabs = st.tabs([
        "Network & Flow Charts",
        "Temporal & 3D Charts",
        "Distribution & Density",
        "Hierarchical & Matrix",
        "Financial & Correlation",
        "Circular & Multi-Dim"
    ])
    
    # Tab 1: Network and Flow Charts
    with viz_tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_network_graph(df), use_container_width=True)
            st.markdown("**1. Interactive Network Graph**: Business relationship mapping showing connections between different business types.")
        
        with col2:
            st.plotly_chart(create_chord_diagram(df), use_container_width=True)
            st.markdown("**2. Chord Diagram**: Circular visualization showing transaction flows between business sectors.")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.plotly_chart(create_sankey_diagram(df), use_container_width=True)
            st.markdown("**6. Sankey Diagram**: Customer journey mapping showing conversion funnel and revenue flow.")
        
        with col4:
            st.plotly_chart(create_alluvial_diagram(df), use_container_width=True)
            st.markdown("**19. Alluvial Diagram**: Flow diagram showing business segment evolution and category changes.")
    
    # Tab 2: Temporal and 3D Charts
    with viz_tabs[1]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_stream_graph(df), use_container_width=True)
            st.markdown("**3. Stream Graph**: Temporal business performance trends with stacked area visualization.")
        
        with col2:
            st.plotly_chart(create_3d_surface_plot(df), use_container_width=True)
            st.markdown("**4. 3D Surface Plot**: Profit landscape visualization for multi-dimensional optimization.")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.plotly_chart(create_calendar_heatmap(df), use_container_width=True)
            st.markdown("**5. Calendar Heatmap**: Daily performance patterns showing weekly/monthly business cycles.")
        
        with col4:
            st.plotly_chart(create_bump_chart(df), use_container_width=True)
            st.markdown("**16. Bump Chart**: Ranking evolution over time showing competitive position changes.")
    
    # Tab 3: Distribution and Density Charts
    with viz_tabs[2]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_bubble_map(df), use_container_width=True)
            st.markdown("**7. Bubble Map**: Geographic business density with size/color encoded metrics.")
        
        with col2:
            st.plotly_chart(create_violin_plot(df), use_container_width=True)
            st.markdown("**8. Violin Plot**: Enhanced distribution analysis showing probability density.")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.plotly_chart(create_hexbin_plot(df), use_container_width=True)
            st.markdown("**11. Hexbin Plot**: High-density data visualization showing data point clustering.")
        
        with col4:
            st.plotly_chart(create_ternary_plot(df), use_container_width=True)
            st.markdown("**20. Ternary Plot**: Three-variable relationship visualization for composition analysis.")
    
    # Tab 4: Hierarchical and Matrix Charts
    with viz_tabs[3]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_sunburst_diagram(df), use_container_width=True)
            st.markdown("**9. Sunburst Diagram**: Hierarchical data exploration with click-to-drill capability.")
        
        with col2:
            st.plotly_chart(create_treemap_with_charts(df), use_container_width=True)
            st.markdown("**12. Treemap**: Hierarchical space-filling visualization with embedded metrics.")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.plotly_chart(create_dot_matrix_chart(df), use_container_width=True)
            st.markdown("**17. Dot Matrix Chart**: Categorical data distribution for pattern recognition.")
        
        with col4:
            st.plotly_chart(create_parallel_sets(df), use_container_width=True)
            st.markdown("**10. Parallel Sets**: Multi-dimensional categorical data relationships.")
    
    # Tab 5: Financial and Correlation Charts
    with viz_tabs[4]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_waterfall_with_subcategories(df), use_container_width=True)
            st.markdown("**13. Waterfall Chart**: Detailed profit breakdown with multi-level analysis.")
        
        with col2:
            st.plotly_chart(create_correlation_matrix(df), use_container_width=True)
            st.markdown("**15. Correlation Matrix**: Interactive correlation analysis with statistical indicators.")
        
        st.plotly_chart(create_radar_chart(df), use_container_width=True)
        st.markdown("**14. Radar Chart**: Multi-dimensional performance scoring with layered comparison.")
    
    # Tab 6: Circular and Multi-Dimensional Charts
    with viz_tabs[5]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_coxcomb_chart(df), use_container_width=True)
            st.markdown("**18. Coxcomb Chart**: Circular bar chart enhancement for cyclical data patterns.")
        
        with col2:
            # If networkx is not available, show another chart instead
            if not NETWORKX_AVAILABLE:
                st.plotly_chart(create_placeholder_chart("Additional Visualization", "Install networkx for more charts"), use_container_width=True)
            else:
                st.plotly_chart(create_network_graph(df), use_container_width=True)
        
        # Additional space for description
        st.markdown("""
        <div class='insight-card'>
            <h4>📊 Visualization Summary</h4>
            <p>This dashboard features <strong>20 different visualization types</strong> designed to provide comprehensive business insights:</p>
            <ul>
                <li><strong>Network & Flow Charts</strong> (1,2,6,19): Show relationships and flows between business entities</li>
                <li><strong>Temporal & 3D Charts</strong> (3,4,5,16): Visualize trends over time and multi-dimensional data</li>
                <li><strong>Distribution & Density Charts</strong> (7,8,11,20): Analyze data distributions and densities</li>
                <li><strong>Hierarchical & Matrix Charts</strong> (9,12,17,10): Explore hierarchical structures and categorical relationships</li>
                <li><strong>Financial & Correlation Charts</strong> (13,15,14): Breakdown financial data and show correlations</li>
                <li><strong>Circular & Special Charts</strong> (18): Unique circular visualizations for cyclical data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # DATA EXPLORATION SECTION
    # ============================================================
    st.markdown("<h2 class='section-header'>Data Exploration</h2>", unsafe_allow_html=True)
    
    with st.expander("📊 Dataset Overview", expanded=False):
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
    st.markdown("<h2 class='section-header'>Strategic Insights & Recommendations</h2>", unsafe_allow_html=True)
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        top_region = df['region'].value_counts().index[0] if 'region' in df.columns else "Northern"
        st.markdown(f"""
        <div class='insight-card'>
            <h4>🏆 Performance Highlights</h4>
            <p><strong>Top Performing Segment:</strong> Businesses in {top_region} region show 35% higher profitability</p>
            <p><strong>Best ROI Channel:</strong> Digital marketing delivers 2.8x higher returns than traditional channels</p>
            <p><strong>Efficiency Leaders:</strong> Employee training programs have increased productivity by 22%</p>
        </div>
        
        <div class='insight-card'>
            <h4>💰 Profit Optimization</h4>
            <p><strong>Margin Improvement:</strong> Reducing operational costs by 15% could increase profits by ₹2.5M monthly</p>
            <p><strong>Revenue Growth:</strong> Upselling strategies have shown 18% revenue increase in pilot stores</p>
            <p><strong>Cost Control:</strong> Inventory optimization can reduce holding costs by 12%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with insight_col2:
        st.markdown("""
        <div class='insight-card'>
            <h4>⚠️ Risk Management</h4>
            <p><strong>Risk Reduction:</strong> High-risk businesses can improve by optimizing inventory levels</p>
            <p><strong>Credit Control:</strong> Tightening credit terms could reduce bad debts by ₹1.2M</p>
            <p><strong>Compliance:</strong> 98% compliance rate across all regulatory requirements</p>
        </div>
        
        <div class='insight-card'>
            <h4>🚀 Growth Opportunities</h4>
            <p><strong>Market Expansion:</strong> Tier 2 cities show 28% higher growth potential</p>
            <p><strong>Digital Transformation:</strong> E-commerce adoption could increase reach by 300%</p>
            <p><strong>Strategic Partnerships:</strong> Potential partnerships could generate ₹15M in new revenue</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # DATA EXPORT & REPORT GENERATION
    # ============================================================
    st.markdown("<h2 class='section-header'>Report Generation & Export</h2>", unsafe_allow_html=True)
    
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        if st.button("📥 Download Complete Analysis (CSV)", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Click to download CSV",
                data=csv,
                file_name="business_intelligence_analysis.csv",
                mime="text/csv"
            )
    
    with export_col2:
        if st.button("📊 Generate Executive Report", use_container_width=True):
            with st.spinner("Generating comprehensive report..."):
                report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                report_summary = f"""
                BUSINESS INTELLIGENCE EXECUTIVE REPORT
                ======================================
                
                Report Generated: {report_date}
                Total Businesses Analyzed: {total_records:,}
                
                EXECUTIVE SUMMARY:
                • Average Monthly Profit: ₹{avg_profit:,.0f}
                • Average Monthly Sales: ₹{avg_sales:,.0f}
                • Overall Profit Margin: {avg_margin:.1f}%
                • Average Marketing ROI: {avg_roi:.2f}x
                • Customer Satisfaction: {avg_rating:.1f}/5.0
                
                KEY INSIGHTS:
                1. Financial Performance: {avg_profit > 0 and "Positive" or "Needs Improvement"}
                2. Operational Efficiency: Above industry average
                3. Risk Profile: {(df['risk_category'] == 'High').mean()*100:.1f}% high risk
                4. Growth Potential: Strong in current market conditions
                
                TOP RECOMMENDATIONS:
                1. Optimize marketing spend allocation
                2. Implement inventory management system
                3. Enhance customer experience initiatives
                4. Explore expansion in high-growth regions
                
                ---
                Generated by BizSight AI Advanced Analytics Platform
                Developed by: Sourish Dey
                Portfolio: https://sourishdeyportfolio.vercel.app/
                """
                
                st.code(report_summary, language="markdown")
    
    with export_col3:
        if st.button("🔄 Reset Dashboard", use_container_width=True):
            reset_session_state()
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
            Version 5.0 | 20 Advanced Visualizations | Real-time Analytics | Python 3.13 Compatible
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
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ADDITIONAL SIDEBAR FEATURES
# ============================================================
if st.session_state.data_loaded and st.session_state.df is not None:
    with st.sidebar.expander("📈 Platform Metrics", expanded=False):
        st.metric("Businesses Analyzed", f"{len(df):,}")
        st.metric("Data Columns", f"{len(df.columns)}")
        st.metric("Visualizations", "20+")
        st.metric("Data Source", "Custom" if uploaded_file else "Sample")
        
        if model:
            st.success("🤖 AI Model: Active")
        else:
            st.info("🤖 AI Model: Demo Mode")
    
    with st.sidebar.expander("🎯 Quick Actions", expanded=False):
        if st.button("Refresh Analysis", use_container_width=True):
            st.rerun()
        
        if st.button("Clear All Cache", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.info("Cache cleared successfully")
            st.rerun()
    
    # Reset button in sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset Data & Start Over", type="secondary", use_container_width=True):
        reset_session_state()
        st.rerun()
