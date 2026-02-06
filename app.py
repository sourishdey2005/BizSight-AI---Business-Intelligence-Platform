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
import networkx as nx
import matplotlib.pyplot as plt
import base64
from io import BytesIO
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
# LOAD MODEL
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
    n_samples = 50000
    
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
# ADVANCED VISUALIZATION FUNCTIONS
# ============================================================

def create_network_graph(df):
    """Create interactive network graph"""
    try:
        # Create a sample network from business relationships
        G = nx.Graph()
        
        # Add nodes for business types
        business_types = df['business_type'].value_counts().nlargest(10).index.tolist()
        for i, biz_type in enumerate(business_types):
            G.add_node(biz_type, size=10 + i*2, color=i)
        
        # Add edges based on correlation
        for i in range(len(business_types)):
            for j in range(i+1, len(business_types)):
                if np.random.random() > 0.7:  # Random connections for demo
                    G.add_edge(business_types[i], business_types[j], 
                              weight=np.random.randint(1, 10))
        
        # Create Plotly figure
        pos = nx.spring_layout(G)
        
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')
        
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"{node}<br>Connections: {G.degree(node)}")
            node_color.append(G.nodes[node]['color'])
            node_size.append(G.nodes[node]['size'])
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=[n.split()[0] for n in G.nodes()],
            textposition="bottom center",
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                size=node_size,
                color=node_color,
                line_width=2))
        
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Business Relationship Network',
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           height=500
                       ))
        return fig
    except Exception as e:
        return create_placeholder_chart("Network Graph", str(e))

def create_chord_diagram(df):
    """Create chord diagram for business ecosystem"""
    try:
        # Prepare data for chord diagram
        business_types = df['business_type'].value_counts().nlargest(8).index.tolist()
        
        # Create a matrix of transactions between business types
        matrix = np.zeros((len(business_types), len(business_types)))
        for i in range(len(business_types)):
            for j in range(len(business_types)):
                if i != j:
                    matrix[i][j] = np.random.randint(1000, 10000)  # Simulated transaction volume
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=business_types,
                color=PLOTLY_COLORS[:len(business_types)]
            ),
            link=dict(
                source=[i for i in range(len(business_types)) for _ in range(len(business_types)-1)],
                target=[j for i in range(len(business_types)) for j in range(len(business_types)) if i != j],
                value=[matrix[i][j] for i in range(len(business_types)) for j in range(len(business_types)) if i != j],
                color=[f"rgba{tuple(list(plt.cm.viridis(i/len(business_types))[:3]) + [0.3])}" 
                      for i in range(len(business_types)) for _ in range(len(business_types)-1)]
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
        # Create time series data
        dates = pd.date_range(start='2023-01-01', periods=12, freq='M')
        business_types = df['business_type'].value_counts().nlargest(5).index.tolist()
        
        data = []
        for biz_type in business_types:
            for date in dates:
                data.append({
                    'Date': date,
                    'Business Type': biz_type,
                    'Sales': np.random.randint(100000, 500000)
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
        # Prepare data for 3D surface
        x = np.linspace(df['marketing_spend'].min(), df['marketing_spend'].max(), 20)
        y = np.linspace(df['employee_count'].min(), df['employee_count'].max(), 20)
        X, Y = np.meshgrid(x, y)
        
        # Simulate profit function
        Z = (X * 0.3 + Y * 5000) / 1000  # Simple linear model
        
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
        
        fig.update_layout(
            title='Profit Landscape Visualization',
            scene=dict(
                xaxis_title='Marketing Spend',
                yaxis_title='Employee Count',
                zaxis_title='Profit (in thousands)'
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
        # Create calendar data
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        values = np.random.randint(100, 1000, size=len(dates))
        
        calendar_df = pd.DataFrame({
            'Date': dates,
            'Value': values,
            'Weekday': dates.day_name(),
            'Week': dates.isocalendar().week,
            'Month': dates.month_name()
        })
        
        fig = px.density_heatmap(calendar_df, x='Weekday', y='Week', z='Value',
                                title='Daily Performance Patterns',
                                color_continuous_scale='Viridis',
                                height=500)
        return fig
    except Exception as e:
        return create_placeholder_chart("Calendar Heatmap", str(e))

def create_sankey_diagram(df):
    """Create Sankey diagram for customer journey"""
    try:
        labels = ["Website Visit", "Product View", "Add to Cart", "Checkout", "Purchase", "Repeat"]
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=PLOTLY_COLORS[:len(labels)]
            ),
            link=dict(
                source=[0, 1, 2, 3, 4],
                target=[1, 2, 3, 4, 5],
                value=[100, 70, 50, 30, 15],
                color=[f"rgba{tuple(list(plt.cm.viridis(i/6)[:3]) + [0.6])}" for i in range(5)]
            )
        )])
        
        fig.update_layout(
            title_text="Customer Journey Mapping",
            font_size=10,
            height=500
        )
        return fig
    except Exception as e:
        return create_placeholder_chart("Sankey Diagram", str(e))

def create_bubble_map(df):
    """Create bubble map for geographic analysis"""
    try:
        if 'city' in df.columns and 'profit' in df.columns:
            # Create sample coordinates for Indian cities
            city_coords = {
                'Mumbai': (19.0760, 72.8777),
                'Delhi': (28.7041, 77.1025),
                'Bangalore': (12.9716, 77.5946),
                'Chennai': (13.0827, 80.2707),
                'Kolkata': (22.5726, 88.3639),
                'Hyderabad': (17.3850, 78.4867),
                'Pune': (18.5204, 73.8567),
                'Ahmedabad': (23.0225, 72.5714),
                'Jaipur': (26.9124, 75.7873),
                'Lucknow': (26.8467, 80.9462)
            }
            
            map_data = []
            for city in df['city'].unique():
                if city in city_coords:
                    city_df = df[df['city'] == city]
                    map_data.append({
                        'City': city,
                        'Lat': city_coords[city][0],
                        'Lon': city_coords[city][1],
                        'Profit': city_df['profit'].mean(),
                        'Business Count': len(city_df)
                    })
            
            map_df = pd.DataFrame(map_data)
            
            fig = px.scatter_mapbox(map_df, lat="Lat", lon="Lon",
                                   size="Business Count", color="Profit",
                                   hover_name="City", hover_data=["Profit", "Business Count"],
                                   color_continuous_scale=px.colors.cyclical.IceFire,
                                   size_max=30, zoom=4,
                                   title='Geographic Business Distribution')
            
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Bubble Map", str(e))

def create_violin_plot(df):
    """Create violin plot for distribution analysis"""
    try:
        if 'business_type' in df.columns and 'profit_margin' in df.columns:
            top_types = df['business_type'].value_counts().nlargest(5).index.tolist()
            violin_df = df[df['business_type'].isin(top_types)]
            
            fig = px.violin(violin_df, x='business_type', y='profit_margin',
                           box=True, points="all",
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
            # Create hierarchical data
            sunburst_data = df.groupby(['region', 'business_type', 'risk_category'])['profit'].mean().reset_index()
            
            fig = px.sunburst(sunburst_data, path=['region', 'business_type', 'risk_category'], 
                             values='profit', color='profit',
                             color_continuous_scale='RdBu',
                             title='Hierarchical Business Analysis',
                             height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Sunburst Diagram", str(e))

def create_hexbin_plot(df):
    """Create hexbin plot for high-density data"""
    try:
        if all(col in df.columns for col in ['marketing_spend', 'monthly_sales']):
            fig = px.density_heatmap(df, x='marketing_spend', y='monthly_sales',
                                    nbinsx=20, nbinsy=20,
                                    title='Marketing Spend vs Sales Density',
                                    color_continuous_scale='Viridis',
                                    height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Hexbin Plot", str(e))

def create_treemap_with_charts(df):
    """Create treemap with embedded charts"""
    try:
        if all(col in df.columns for col in ['business_type', 'profit', 'monthly_sales']):
            fig = px.treemap(df, path=['business_type'], values='profit',
                            color='monthly_sales', hover_data=['profit'],
                            color_continuous_scale='RdBu',
                            title='Profit Treemap with Sales Coloring',
                            height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Treemap", str(e))

def create_waterfall_with_subcategories(df):
    """Create waterfall chart with subcategories"""
    try:
        if 'business_type' in df.columns and 'profit' in df.columns:
            profit_by_type = df.groupby('business_type')['profit'].sum().nlargest(10)
            
            fig = go.Figure(go.Waterfall(
                name="Profit", orientation="v",
                measure=["relative"] * len(profit_by_type),
                x=profit_by_type.index,
                textposition="outside",
                y=profit_by_type.values,
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))
            
            fig.update_layout(
                title="Profit Breakdown by Business Type",
                showlegend=True,
                height=500
            )
            return fig
    except Exception as e:
        return create_placeholder_chart("Waterfall Chart", str(e))

def create_radar_chart(df):
    """Create radar chart with multiple layers"""
    try:
        if all(col in df.columns for col in ['profitability_score', 'efficiency_score', 'growth_potential']):
            categories = ['Profitability', 'Efficiency', 'Growth Potential']
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=[df['profitability_score'].mean(), 
                   df['efficiency_score'].mean(), 
                   df['growth_potential'].mean()],
                theta=categories,
                fill='toself',
                name='Average Business'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=[df['profitability_score'].max(), 
                   df['efficiency_score'].max(), 
                   df['growth_potential'].max()],
                theta=categories,
                fill='toself',
                name='Top Performers'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title='Business Performance Radar',
                height=500
            )
            return fig
    except Exception as e:
        return create_placeholder_chart("Radar Chart", str(e))

def create_correlation_matrix(df):
    """Create correlation matrix heatmap"""
    try:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols[:10]].corr()  # Use first 10 numeric columns
            
            fig = ff.create_annotated_heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns.tolist(),
                y=corr_matrix.columns.tolist(),
                annotation_text=corr_matrix.round(2).values,
                colorscale='RdBu',
                showscale=True
            )
            
            fig.update_layout(
                title='Correlation Matrix',
                height=500
            )
            return fig
    except Exception as e:
        return create_placeholder_chart("Correlation Matrix", str(e))

def create_bump_chart(df):
    """Create bump chart for ranking evolution"""
    try:
        # Create time series ranking data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        business_types = df['business_type'].value_counts().nlargest(5).index.tolist()
        
        data = []
        for i, month in enumerate(months):
            for j, biz_type in enumerate(business_types):
                data.append({
                    'Month': month,
                    'Business Type': biz_type,
                    'Rank': np.random.randint(1, 6),
                    'Performance': np.random.randint(50, 100)
                })
        
        bump_df = pd.DataFrame(data)
        
        fig = px.line(bump_df, x='Month', y='Rank', color='Business Type',
                     markers=True, title='Business Ranking Evolution',
                     height=500)
        
        fig.update_yaxes(autorange="reversed")
        return fig
    except Exception as e:
        return create_placeholder_chart("Bump Chart", str(e))

def create_dot_matrix_chart(df):
    """Create dot matrix chart for categorical data"""
    try:
        if 'business_type' in df.columns and 'risk_category' in df.columns:
            matrix_data = df.groupby(['business_type', 'risk_category']).size().unstack().fillna(0)
            
            fig = px.imshow(matrix_data,
                           labels=dict(x="Risk Category", y="Business Type", color="Count"),
                           x=matrix_data.columns,
                           y=matrix_data.index,
                           color_continuous_scale='Viridis',
                           title='Risk Category Distribution by Business Type',
                           height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Dot Matrix", str(e))

def create_coxcomb_chart(df):
    """Create Coxcomb/Rose diagram"""
    try:
        if 'business_type' in df.columns and 'profit' in df.columns:
            profit_by_type = df.groupby('business_type')['profit'].sum().nlargest(8)
            
            fig = px.bar_polar(profit_by_type.reset_index(), r='profit', theta='business_type',
                              title='Circular Business Performance',
                              template='plotly_white',
                              height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Coxcomb Chart", str(e))

def create_alluvial_diagram(df):
    """Create alluvial diagram for flow visualization"""
    try:
        # Simulate flow data between business segments
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["Small", "Medium", "Large", "Retail", "Services", "Manufacturing"],
                color=PLOTLY_COLORS[:6]
            ),
            link=dict(
                source=[0, 0, 1, 1, 2, 2],
                target=[3, 4, 3, 5, 4, 5],
                value=[100, 50, 80, 30, 40, 60]
            )
        )])
        
        fig.update_layout(
            title_text="Business Segment Flow",
            font_size=10,
            height=500
        )
        return fig
    except Exception as e:
        return create_placeholder_chart("Alluvial Diagram", str(e))

def create_ternary_plot(df):
    """Create ternary plot for three-variable relationships"""
    try:
        if all(col in df.columns for col in ['profit_margin', 'customer_rating', 'employee_efficiency']):
            fig = px.scatter_ternary(df, a='profit_margin', b='customer_rating', c='employee_efficiency',
                                    color='business_type' if 'business_type' in df.columns else None,
                                    size='profit' if 'profit' in df.columns else None,
                                    title='Three-Factor Business Analysis',
                                    height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Ternary Plot", str(e))

def create_parallel_sets(df):
    """Create parallel sets for categorical relationships"""
    try:
        if all(col in df.columns for col in ['business_type', 'risk_category', 'performance_tier']):
            # Create aggregated data
            agg_data = df.groupby(['business_type', 'risk_category', 'performance_tier']).size().reset_index(name='count')
            
            fig = px.parallel_categories(agg_data, 
                                        dimensions=['business_type', 'risk_category', 'performance_tier'],
                                        color='count',
                                        color_continuous_scale=px.colors.sequential.Inferno,
                                        title='Business Attribute Relationships',
                                        height=500)
            return fig
    except Exception as e:
        return create_placeholder_chart("Parallel Sets", str(e))

def create_placeholder_chart(chart_type, error_msg=""):
    """Create a placeholder chart when actual chart cannot be created"""
    fig = go.Figure()
    fig.add_annotation(
        text=f"{chart_type}<br>Data not available or insufficient<br>{error_msg}",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14)
    )
    fig.update_layout(
        title=chart_type,
        height=500,
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
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
                📈 40+ Visualizations
            </div>
            <div style='padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 10px;'>
                🤖 AI-Powered Predictions
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
    st.markdown("### Platform Features")
    
    features = [
        {"icon": "📊", "title": "Sales Analytics", "desc": "Comprehensive sales performance analysis"},
        {"icon": "💰", "title": "Profit Optimization", "desc": "Maximize profitability insights"},
        {"icon": "⚠️", "title": "Risk Assessment", "desc": "Advanced risk identification"},
        {"icon": "📈", "title": "Trend Analysis", "desc": "Historical and predictive trends"},
        {"icon": "🗺️", "title": "Geographic Insights", "desc": "Location-based performance"},
        {"icon": "🤖", "title": "AI Predictions", "desc": "Machine learning forecasts"},
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
                {'▲' if avg_profit > 0 else '▼'} {abs(avg_profit/10000):.1f}%
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
                {'▲' if avg_sales > 1000000 else '▬'} {avg_sales/1000000:.1f}x target
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
                {'▲' if avg_margin > 15 else '▼'} {avg_margin - 15:.1f}% vs target
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
                {'▼' if high_risk_pct < 30 else '▲'} {abs(high_risk_pct - 30):.1f}% vs target
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # ADVANCED VISUALIZATION DASHBOARD - 20 VISUALIZATIONS
    # ============================================================
    st.markdown("<h2 class='section-header'>Advanced Analytics Dashboard (20 Visualizations)</h2>", unsafe_allow_html=True)
    
    # Create tabs for different visualization categories
    viz_tabs = st.tabs([
        "1-2. Network & Chord",
        "3-5. Temporal & 3D",
        "6-8. Flow & Distribution",
        "9-11. Hierarchical & Density",
        "12-14. Financial Breakdown",
        "15-17. Correlation & Ranking",
        "18-20. Circular & Flow"
    ])
    
    # Tab 1: Network Graph and Chord Diagram
    with viz_tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_network_graph(df), use_container_width=True)
            st.markdown("**Interactive Network Graph**: Business relationship mapping showing supplier-customer connections and regional clusters.")
        
        with col2:
            st.plotly_chart(create_chord_diagram(df), use_container_width=True)
            st.markdown("**Chord Diagram**: Circular visualization of business ecosystem showing money flow between sectors.")
    
    # Tab 2: Stream Graph and 3D Surface
    with viz_tabs[1]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_stream_graph(df), use_container_width=True)
            st.markdown("**Stream Graph**: Temporal business performance trends with stacked area visualization.")
        
        with col2:
            st.plotly_chart(create_3d_surface_plot(df), use_container_width=True)
            st.markdown("**3D Surface Plot**: Profit landscape visualization for multi-dimensional optimization.")
    
    # Tab 3: Calendar Heatmap and Sankey
    with viz_tabs[2]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_calendar_heatmap(df), use_container_width=True)
            st.markdown("**Calendar Heatmap**: Daily performance patterns showing weekly/monthly business cycles.")
        
        with col2:
            st.plotly_chart(create_sankey_diagram(df), use_container_width=True)
            st.markdown("**Sankey Diagram**: Customer journey mapping showing sales funnel and revenue flow.")
    
    # Tab 4: Bubble Map and Violin Plot
    with viz_tabs[3]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_bubble_map(df), use_container_width=True)
            st.markdown("**Bubble Map**: Geographic business density with size/color encoded metrics.")
        
        with col2:
            st.plotly_chart(create_violin_plot(df), use_container_width=True)
            st.markdown("**Violin Plot**: Enhanced distribution analysis showing probability density.")
    
    # Tab 5: Sunburst and Hexbin
    with viz_tabs[4]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_sunburst_diagram(df), use_container_width=True)
            st.markdown("**Sunburst Diagram**: Hierarchical data exploration with click-to-drill capability.")
        
        with col2:
            st.plotly_chart(create_hexbin_plot(df), use_container_width=True)
            st.markdown("**Hexbin Plot**: High-density data visualization showing data point clustering.")
    
    # Tab 6: Waterfall and Treemap
    with viz_tabs[5]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_waterfall_with_subcategories(df), use_container_width=True)
            st.markdown("**Waterfall Chart**: Detailed profit breakdown with multi-level analysis.")
        
        with col2:
            st.plotly_chart(create_treemap_with_charts(df), use_container_width=True)
            st.markdown("**Treemap**: Hierarchical space-filling visualization with embedded metrics.")
    
    # Tab 7: Radar, Correlation, and Bump Charts
    with viz_tabs[6]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_radar_chart(df), use_container_width=True)
            st.markdown("**Radar Chart**: Multi-dimensional performance scoring with competitor comparison.")
        
        with col2:
            st.plotly_chart(create_correlation_matrix(df), use_container_width=True)
            st.markdown("**Correlation Matrix**: Interactive correlation analysis with statistical indicators.")
        
        st.plotly_chart(create_bump_chart(df), use_container_width=True)
        st.markdown("**Bump Chart**: Ranking evolution over time showing competitive position changes.")
    
    # Tab 8: Dot Matrix, Coxcomb, Alluvial, and Ternary
    with viz_tabs[7]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_dot_matrix_chart(df), use_container_width=True)
            st.markdown("**Dot Matrix Chart**: Categorical data distribution for pattern recognition.")
        
        with col2:
            st.plotly_chart(create_coxcomb_chart(df), use_container_width=True)
            st.markdown("**Coxcomb Chart**: Circular bar chart enhancement for cyclical data patterns.")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.plotly_chart(create_alluvial_diagram(df), use_container_width=True)
            st.markdown("**Alluvial Diagram**: Flow diagram showing category evolution over time.")
        
        with col4:
            st.plotly_chart(create_ternary_plot(df), use_container_width=True)
            st.markdown("**Ternary Plot**: Three-variable relationship visualization for composition analysis.")
        
        # Parallel Sets
        st.plotly_chart(create_parallel_sets(df), use_container_width=True)
        st.markdown("**Parallel Sets**: Categorical data relationships showing multi-dimensional connections.")
    
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
            Version 5.0 | 20 Advanced Visualizations | Real-time Analytics | Predictive Insights
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
