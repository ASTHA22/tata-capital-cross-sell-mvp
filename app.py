import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# Try to import Google Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Tata Capital - Cross-sell Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    /* Tata Capital Official Brand Colors - Light Theme */
    :root {
        --tata-blue: #0066CC;
        --tata-purple: #6B2C91;
        --tata-gold: #F7A800;
        --tata-navy: #003366;
        --tata-green: #00A651;
        --light-bg: #F8FAFC;
        --light-card: #FFFFFF;
        --dark-text: #1E293B;
        --border-color: #E2E8F0;
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%);
        color: #1E293B;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #0066CC 50%, #6B2C91 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 24px rgba(0, 102, 204, 0.2);
        border: 1px solid rgba(247, 168, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(247, 168, 0, 0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .main-header h1 {
        color: #FFFFFF !important;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header h1 * {
        color: #FFFFFF !important;
    }
    
    .main-header p {
        color: #F7A800 !important;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
    }
    
    .main-header p * {
        color: #F7A800 !important;
    }
    
    /* Metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #0066CC;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #64748B;
    }
    
    div[data-testid="stMetricDelta"] {
        color: #00A651;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
        border-right: 2px solid #E2E8F0;
    }
    
    section[data-testid="stSidebar"] .stRadio > label {
        background: #F8FAFC;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid transparent;
        transition: all 0.3s ease;
    }
    
    section[data-testid="stSidebar"] .stRadio > label:hover {
        background: #EFF6FF;
        border-left-color: #F7A800;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Cards and containers */
    .info-card {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #0066CC;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 102, 204, 0.15);
    }
    
    .success-card {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #00A651;
        border: 1px solid #86EFAC;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 166, 81, 0.1);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #F7A800;
        border: 1px solid #FCD34D;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(247, 168, 0, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0066CC 0%, #6B2C91 100%) !important;
        color: #FFFFFF !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
    }
    
    .stButton > button * {
        color: #FFFFFF !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0052A3 0%, #561F75 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 102, 204, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 1rem;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        color: #64748B;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #EFF6FF;
        color: #0066CC;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0066CC 0%, #6B2C91 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
    }
    
    .stTabs [aria-selected="true"] * {
        color: #FFFFFF !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        background-color: #FFFFFF;
        color: #1E293B;
        border: 1px solid #E2E8F0;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #0066CC, #F7A800, #6B2C91, transparent);
    }
    
    /* Section headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1E293B !important;
        font-weight: 700;
    }
    
    h2 {
        border-bottom: 2px solid #0066CC;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Text color */
    p, span, div, label {
        color: #1E293B;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        background-color: #FFFFFF;
        color: #1E293B;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: #0066CC;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
    }
    
    /* Multiselect tags/pills */
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #0066CC !important;
        color: #FFFFFF !important;
    }
    
    .stMultiSelect span[data-baseweb="tag"] * {
        color: #FFFFFF !important;
    }
    
    .stMultiSelect [role="button"] {
        color: #FFFFFF !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: #F8FAFC;
    }
    
    .stSlider > div > div > div > div {
        background-color: #0066CC;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* Number input */
    .stNumberInput > div > div > input {
        background-color: #FFFFFF;
        color: #1E293B;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
    }
    
    /* Accent elements */
    .stProgress > div > div > div {
        background-color: #0066CC;
    }
    
    /* Links */
    a {
        color: #0066CC;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: #003366;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load scored customer data"""
    import subprocess
    import sys
    
    # Check if scored data exists
    if not os.path.exists('nbfc_customers_scored.csv'):
        st.warning("🔄 First-time setup: Generating data and training model... This will take 2-3 minutes.")
        
        with st.spinner("Generating synthetic customer data..."):
            try:
                # Run generate_data.py
                subprocess.run([sys.executable, 'generate_data.py'], check=True, capture_output=True)
                st.success("✅ Data generated!")
            except subprocess.CalledProcessError as e:
                st.error(f"❌ Error generating data: {e.stderr.decode()}")
                st.stop()
        
        with st.spinner("Training propensity model..."):
            try:
                # Run train_model.py
                subprocess.run([sys.executable, 'train_model.py'], check=True, capture_output=True)
                st.success("✅ Model trained!")
            except subprocess.CalledProcessError as e:
                st.error(f"❌ Error training model: {e.stderr.decode()}")
                st.stop()
        
        st.success("🎉 Setup complete! Loading dashboard...")
    
    try:
        df = pd.read_csv('nbfc_customers_scored.csv')
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file not found even after generation. Please check the logs.")
        st.stop()

def format_currency(amount):
    """Format amount in Indian currency style"""
    if amount >= 10000000:
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:
        return f"₹{amount/100000:.2f} L"
    else:
        return f"₹{amount:,.0f}"

def customer_360_view(df):
    """Customer 360 Dashboard"""
    st.markdown("## 🔍 Customer 360 View")
    st.markdown("*Comprehensive customer profile with AI-powered recommendations*")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Select Customer")
        customer_id = st.selectbox(
            "Customer ID",
            options=df['customer_id'].tolist(),
            index=0,
            label_visibility="collapsed"
        )
    
    customer = df[df['customer_id'] == customer_id].iloc[0]
    
    with col2:
        metric_cols = st.columns(4)
        with metric_cols[0]:
            delta = f"+{customer['model_propensity_score'] - df['model_propensity_score'].mean():.1f}" if customer['model_propensity_score'] > df['model_propensity_score'].mean() else f"{customer['model_propensity_score'] - df['model_propensity_score'].mean():.1f}"
            st.metric("Propensity Score", f"{customer['model_propensity_score']:.1f}/100", delta=delta)
        with metric_cols[1]:
            st.metric("Bureau Score", int(customer['bureau_score']), delta="Excellent" if customer['bureau_score'] > 750 else "Good")
        with metric_cols[2]:
            st.metric("Repayment Score", f"{customer['repayment_score']:.0f}/100", delta="Strong" if customer['repayment_score'] > 80 else "Fair")
        with metric_cols[3]:
            status = "✅ Converted" if customer['took_hl'] else "🎯 Target"
            st.metric("Status", status)
    
    st.markdown("---")
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("### 📋 Customer Profile")
        
        profile_html = f"""
        <div class="info-card">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Customer ID</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{customer['customer_id']}</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Age</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{int(customer['age'])} years</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Employment</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{customer['employment_type']}</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Monthly Income</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{format_currency(customer['monthly_income'])}</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Location</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{customer['city']} ({customer['city_tier']})</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Segment</p>
                    <p style="color: #6B2C91; font-size: 1.125rem; font-weight: 700; margin: 0.25rem 0;">{customer['segment']}</p>
                </div>
            </div>
        </div>
        """
        st.markdown(profile_html, unsafe_allow_html=True)
        
        st.markdown("### 💳 Personal Loan Details")
        pl_html = f"""
        <div class="info-card">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Ticket Size</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{format_currency(customer['pl_ticket_size'])}</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Tenure</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{int(customer['pl_tenure_months'])} months</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Vintage</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{int(customer['pl_vintage_months'])} months</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">DPD (Last 12M)</p>
                    <p style="color: {'#00A651' if customer['dpd_last_12m'] == 0 else '#DC2626'}; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{int(customer['dpd_last_12m'])} days</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">FOIR</p>
                    <p style="color: {'#00A651' if customer['foir_percent'] < 40 else '#DC2626'}; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{customer['foir_percent']:.1f}%</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Repayment Score</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{customer['repayment_score']:.0f}/100</p>
                </div>
            </div>
        </div>
        """
        st.markdown(pl_html, unsafe_allow_html=True)
        
        st.markdown("### 📊 Engagement Signals")
        engagement_html = f"""
        <div class="info-card">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">Digital Score</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{customer['digital_engagement_score']:.0f}/100</p>
                </div>
                <div>
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">App Logins (90d)</p>
                    <p style="color: #1E293B; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{int(customer['app_logins_90d'])}</p>
                </div>
                <div style="grid-column: 1 / -1;">
                    <p style="color: #64748B; font-size: 0.875rem; margin: 0;">HL Calculator Used</p>
                    <p style="color: {'#00A651' if customer['hl_calculator_used'] else '#DC2626'}; font-size: 1.125rem; font-weight: 600; margin: 0.25rem 0;">{'✅ Yes - Strong Intent Signal!' if customer['hl_calculator_used'] else '❌ No'}</p>
                </div>
            </div>
        </div>
        """
        st.markdown(engagement_html, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("### 🎯 Cross-sell Intelligence")
        
        propensity = customer['model_propensity_score']
        
        # Enhanced gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=propensity,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "HL Propensity Score", 'font': {'size': 24, 'color': '#0066CC'}},
            delta={'reference': df['model_propensity_score'].mean(), 'increasing': {'color': "#00A651"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#0066CC"},
                'bar': {'color': "#0066CC", 'thickness': 0.75},
                'bgcolor': "#F8FAFC",
                'borderwidth': 2,
                'bordercolor': "#E2E8F0",
                'steps': [
                    {'range': [0, 30], 'color': "#FEE2E2"},
                    {'range': [30, 50], 'color': "#FEF3C7"},
                    {'range': [50, 70], 'color': "#D1FAE5"},
                    {'range': [70, 100], 'color': "#A7F3D0"}
                ],
                'threshold': {
                    'line': {'color': "#F7A800", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(
            height=350,
            paper_bgcolor="#FFFFFF",
            font={'color': "#1E293B", 'family': "Arial"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 💡 Recommended Action")
        
        if propensity >= 70:
            ticket_size = min(customer['monthly_income'] * 60, 5000000)
            action_html = f"""
            <div class="success-card">
                <h3 style="color: #00A651; margin: 0 0 1rem 0;">🎯 High Priority Target</h3>
                <div style="background: #F8FAFC; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #E2E8F0;">
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>💰 Offer:</strong> Pre-approved Home Loan up to {format_currency(ticket_size)}</p>
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>📱 Channel:</strong> RM Call + WhatsApp</p>
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>⏰ Timing:</strong> Within 7 days</p>
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>💬 Script:</strong> "Your excellent repayment history qualifies you for our best HL rates at 8.5% p.a."</p>
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>🎁 Incentive:</strong> Waive processing fee (₹10,000 value)</p>
                </div>
            </div>
            """
            st.markdown(action_html, unsafe_allow_html=True)
        elif propensity >= 50:
            action_html = """
            <div class="warning-card">
                <h3 style="color: #F7A800; margin: 0 0 1rem 0;">📞 Medium Priority</h3>
                <div style="background: #F8FAFC; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #E2E8F0;">
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>💰 Offer:</strong> Home Loan eligibility check</p>
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>📱 Channel:</strong> App Push + SMS</p>
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>⏰ Timing:</strong> Within 14 days</p>
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>💬 Message:</strong> "Check your Home Loan eligibility in 2 minutes"</p>
                </div>
            </div>
            """
            st.markdown(action_html, unsafe_allow_html=True)
        elif propensity >= 30:
            action_html = """
            <div class="info-card">
                <h3 style="color: #1E293B; margin: 0 0 1rem 0;">📧 Nurture Campaign</h3>
                <div style="background: #F8FAFC; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #E2E8F0;">
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>💰 Offer:</strong> HL calculator + educational content</p>
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>📱 Channel:</strong> Email + App banner</p>
                    <p style="margin: 0.5rem 0; color: #1E293B;"><strong>⏰ Timing:</strong> Monthly touchpoints</p>
                </div>
            </div>
            """
            st.markdown(action_html, unsafe_allow_html=True)
        else:
            st.error("⏸️ **Low Priority - Do Not Contact**")
            st.write("Focus resources on higher propensity customers for better ROI.")

def segment_analysis(df):
    """Segment Analysis Dashboard"""
    st.markdown("## 📊 Segment Analysis")
    st.markdown("*Deep dive into customer segments and conversion patterns*")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total PL Customers", f"{len(df):,}", delta=f"{len(df[df['model_propensity_score'] > 50]):,} high propensity")
    with col2:
        st.metric("HL Conversions", f"{df['took_hl'].sum():,}", delta=f"{df['took_hl'].mean()*100:.1f}% rate")
    with col3:
        top_decile_rate = df[df['propensity_decile'] == 10]['took_hl'].mean() * 100
        st.metric("Top Decile Conv.", f"{top_decile_rate:.1f}%", delta=f"{top_decile_rate / (df['took_hl'].mean()*100):.1f}x lift")
    with col4:
        st.metric("Avg Propensity", f"{df['model_propensity_score'].mean():.1f}", delta=f"σ={df['model_propensity_score'].std():.1f}")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Segment Overview", "📊 Propensity Distribution", "🎯 Decile Analysis", "🔍 Feature Analysis"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        
        with col_a:
            segment_stats = df.groupby('segment').agg({
                'customer_id': 'count',
                'took_hl': ['sum', 'mean'],
                'model_propensity_score': 'mean'
            }).round(2)
            
            segment_stats.columns = ['Count', 'Conversions', 'Conv_Rate', 'Avg_Propensity']
            segment_stats = segment_stats.reset_index()
            
            fig = px.bar(
                segment_stats,
                x='segment',
                y='Count',
                color='Avg_Propensity',
                text='Count',
                title="<b>Customer Count by Segment</b>",
                color_continuous_scale=[[0, '#003366'], [0.5, '#0066CC'], [1, '#6B2C91']]
            )
            fig.update_traces(textposition='outside', textfont_size=14)
            fig.update_layout(
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                font=dict(size=12, color='#1E293B'),
                title_font=dict(size=18, color='#1E293B'),
                xaxis_title="Segment",
                yaxis_title="Number of Customers",
                xaxis=dict(gridcolor='#E2E8F0'),
                yaxis=dict(gridcolor='#E2E8F0')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            fig = px.bar(
                segment_stats,
                x='segment',
                y='Conv_Rate',
                text=segment_stats['Conv_Rate'].apply(lambda x: f"{x*100:.1f}%"),
                title="<b>Conversion Rate by Segment</b>",
                color='Conv_Rate',
                color_continuous_scale=[[0, '#003366'], [0.5, '#00A651'], [1, '#0066CC']]
            )
            fig.update_traces(textposition='outside', textfont_size=14)
            fig.update_layout(
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                font=dict(size=12, color='#1E293B'),
                title_font=dict(size=18, color='#1E293B'),
                xaxis_title="Segment",
                yaxis_title="Conversion Rate",
                xaxis=dict(gridcolor='#E2E8F0'),
                yaxis=dict(gridcolor='#E2E8F0')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col_c, col_d = st.columns(2)
        
        with col_c:
            fig = px.histogram(
                df,
                x='model_propensity_score',
                nbins=50,
                title="<b>Propensity Score Distribution</b>",
                color_discrete_sequence=['#0066CC']
            )
            fig.update_layout(
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                font=dict(size=12, color='#1E293B'),
                title_font=dict(size=18, color='#1E293B'),
                xaxis_title="Propensity Score",
                yaxis_title="Number of Customers",
                showlegend=False,
                xaxis=dict(gridcolor='#E2E8F0'),
                yaxis=dict(gridcolor='#E2E8F0')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_d:
            fig = px.box(
                df,
                x='segment',
                y='model_propensity_score',
                title="<b>Propensity Score by Segment</b>",
                color='segment',
                color_discrete_sequence=['#0066CC', '#6B2C91', '#F7A800', '#00A651']
            )
            fig.update_layout(
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                font=dict(size=12, color='#1E293B'),
                title_font=dict(size=18, color='#1E293B'),
                xaxis_title="Segment",
                yaxis_title="Propensity Score",
                showlegend=False,
                xaxis=dict(gridcolor='#E2E8F0'),
                yaxis=dict(gridcolor='#E2E8F0')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        decile_analysis = df.groupby('propensity_decile').agg({
            'customer_id': 'count',
            'took_hl': ['sum', 'mean'],
            'model_propensity_score': 'mean'
        }).round(3)
        
        decile_analysis.columns = ['Total', 'Conversions', 'Conv_Rate', 'Avg_Propensity']
        decile_analysis = decile_analysis.reset_index()
        decile_analysis = decile_analysis.sort_values('propensity_decile', ascending=False)
        
        baseline_conv_rate = df['took_hl'].mean()
        decile_analysis['Lift'] = decile_analysis['Conv_Rate'] / baseline_conv_rate
        
        st.markdown("### 📈 Decile Performance Analysis")
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("<b>Conversion Rate by Decile</b>", "<b>Lift vs Baseline</b>")
        )
        
        fig.add_trace(
            go.Bar(
                x=decile_analysis['propensity_decile'],
                y=decile_analysis['Conv_Rate'] * 100,
                name='Conversion Rate',
                marker_color='#0066CC',
                text=decile_analysis['Conv_Rate'].apply(lambda x: f"{x*100:.1f}%"),
                textposition='outside'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=decile_analysis['propensity_decile'],
                y=decile_analysis['Lift'],
                name='Lift',
                marker_color='#00A651',
                text=decile_analysis['Lift'].apply(lambda x: f"{x:.1f}x"),
                textposition='outside'
            ),
            row=1, col=2
        )
        
        fig.add_hline(y=1, line_dash="dash", line_color="#EF4444", line_width=2, row=1, col=2)
        
        fig.update_xaxes(title_text="Propensity Decile", row=1, col=1)
        fig.update_xaxes(title_text="Propensity Decile", row=1, col=2)
        fig.update_yaxes(title_text="Conversion Rate (%)", row=1, col=1)
        fig.update_yaxes(title_text="Lift vs Baseline", row=1, col=2)
        
        fig.update_layout(
            height=450,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📋 Detailed Decile Breakdown")
        styled_df = decile_analysis.style.format({
            'Conv_Rate': '{:.1%}',
            'Avg_Propensity': '{:.1f}',
            'Lift': '{:.2f}x'
        }).background_gradient(subset=['Lift'], cmap='Greens')
        
        st.dataframe(styled_df, use_container_width=True)
    
    with tab4:
        col_e, col_f = st.columns(2)
        
        with col_e:
            age_bins = pd.cut(df['age'], bins=[20, 30, 35, 40, 45, 60])
            age_conv = df.groupby(age_bins)['took_hl'].mean() * 100
            
            fig = px.bar(
                x=age_conv.index.astype(str),
                y=age_conv.values,
                title="<b>Conversion Rate by Age Band</b>",
                labels={'x': 'Age Band', 'y': 'Conversion Rate (%)'},
                color=age_conv.values,
                color_continuous_scale=[[0, '#003366'], [0.5, '#0066CC'], [1, '#6B2C91']],
                text=age_conv.values.round(1)
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                title_font=dict(size=18, color='#1E293B'),
                showlegend=False,
                font=dict(color='#1E293B'),
                xaxis=dict(gridcolor='#E2E8F0'),
                yaxis=dict(gridcolor='#E2E8F0')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_f:
            city_conv = df.groupby('city_tier')['took_hl'].mean() * 100
            
            fig = px.bar(
                x=city_conv.index,
                y=city_conv.values,
                title="<b>Conversion Rate by City Tier</b>",
                labels={'x': 'City Tier', 'y': 'Conversion Rate (%)'},
                color=city_conv.values,
                color_continuous_scale=[[0, '#003366'], [0.5, '#00A651'], [1, '#0066CC']],
                text=city_conv.values.round(1)
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                title_font=dict(size=18, color='#1E293B'),
                showlegend=False,
                font=dict(color='#1E293B'),
                xaxis=dict(gridcolor='#E2E8F0'),
                yaxis=dict(gridcolor='#E2E8F0')
            )
            st.plotly_chart(fig, use_container_width=True)

def campaign_simulator(df):
    """Campaign Simulator"""
    st.markdown("## 🎯 Campaign Simulator")
    st.markdown("*Optimize your cross-sell campaigns with data-driven targeting*")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ Campaign Parameters")
        
        with st.container():
            min_propensity = st.slider(
                "Minimum Propensity Score",
                min_value=0,
                max_value=100,
                value=50,
                step=5,
                help="Target customers above this propensity threshold"
            )
            
            selected_segments = st.multiselect(
                "Target Segments",
                options=df['segment'].unique().tolist(),
                default=df['segment'].unique().tolist()
            )
            
            selected_tiers = st.multiselect(
                "City Tiers",
                options=df['city_tier'].unique().tolist(),
                default=df['city_tier'].unique().tolist()
            )
            
            min_bureau_score = st.slider(
                "Minimum Bureau Score",
                min_value=600,
                max_value=850,
                value=650,
                step=10
            )
        
        st.markdown("### 💰 Financial Parameters")
        
        with st.container():
            cost_per_contact = st.number_input(
                "Cost per Contact (₹)",
                min_value=10,
                max_value=500,
                value=50,
                step=10
            )
            
            avg_ticket_size = st.number_input(
                "Avg HL Ticket Size (₹)",
                min_value=500000,
                max_value=5000000,
                value=2000000,
                step=100000
            )
            
            revenue_per_loan = st.number_input(
                "Revenue per Loan (₹)",
                min_value=10000,
                max_value=200000,
                value=50000,
                step=5000,
                help="Processing fee + interest margin"
            )
    
    with col2:
        filtered_df = df[
            (df['model_propensity_score'] >= min_propensity) &
            (df['segment'].isin(selected_segments)) &
            (df['city_tier'].isin(selected_tiers)) &
            (df['bureau_score'] >= min_bureau_score)
        ]
        
        total_targets = len(filtered_df)
        expected_conversions = filtered_df['took_hl'].sum()
        conversion_rate = filtered_df['took_hl'].mean() if total_targets > 0 else 0
        
        baseline_conv_rate = df['took_hl'].mean()
        lift = conversion_rate / baseline_conv_rate if baseline_conv_rate > 0 else 0
        
        total_cost = total_targets * cost_per_contact
        total_revenue = expected_conversions * revenue_per_loan
        roi = ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0
        
        st.markdown("### 📊 Campaign Performance Metrics")
        
        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.metric("Target Customers", f"{total_targets:,}", delta=f"{(total_targets/len(df)*100):.1f}% of base")
        with metric_cols[1]:
            st.metric("Expected Conversions", f"{expected_conversions:,}", delta=f"{conversion_rate*100:.1f}% rate")
        with metric_cols[2]:
            st.metric("Lift vs Baseline", f"{lift:.2f}x", delta="Above avg" if lift > 1 else "Below avg")
        
        st.markdown("---")
        
        metric_cols2 = st.columns(3)
        with metric_cols2[0]:
            st.metric("Total Cost", format_currency(total_cost))
        with metric_cols2[1]:
            st.metric("Expected Revenue", format_currency(total_revenue))
        with metric_cols2[2]:
            net_profit = total_revenue - total_cost
            st.metric("Net Profit", format_currency(net_profit), delta=f"{roi:.1f}% ROI")
        
        if roi > 0:
            roi_html = f"""
            <div class="success-card">
                <h3 style="color: #065F46; margin: 0;">💰 Campaign is Profitable!</h3>
                <p style="font-size: 2rem; font-weight: 700; color: #10B981; margin: 1rem 0;">ROI: {roi:.1f}%</p>
                <p style="color: #065F46; margin: 0;">Expected net profit: {format_currency(net_profit)}</p>
            </div>
            """
            st.markdown(roi_html, unsafe_allow_html=True)
        else:
            st.error(f"💸 **ROI: {roi:.1f}%** - Campaign not profitable. Adjust targeting parameters.")
        
        st.markdown("---")
        st.markdown("### 📈 Campaign Breakdown")
        
        if total_targets > 0:
            segment_breakdown = filtered_df.groupby('segment').agg({
                'customer_id': 'count',
                'took_hl': 'sum',
                'model_propensity_score': 'mean'
            }).reset_index()
            
            segment_breakdown.columns = ['Segment', 'Targets', 'Expected_Conv', 'Avg_Propensity']
            
            fig = px.bar(
                segment_breakdown,
                x='Segment',
                y='Targets',
                color='Avg_Propensity',
                text='Targets',
                title="<b>Target Distribution by Segment</b>",
                color_continuous_scale=[[0, '#003366'], [0.5, '#0066CC'], [1, '#6B2C91']]
            )
            fig.update_traces(textposition='outside', textfont_size=14)
            fig.update_layout(
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                title_font=dict(size=18, color='#1E293B'),
                font=dict(color='#1E293B'),
                xaxis=dict(gridcolor='#E2E8F0'),
                yaxis=dict(gridcolor='#E2E8F0')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(
                segment_breakdown.style.format({
                    'Avg_Propensity': '{:.1f}'
                }).background_gradient(subset=['Targets'], cmap='Purples'),
                use_container_width=True
            )
        else:
            st.warning("⚠️ No customers match the selected criteria. Please adjust filters.")

def ai_chat_assistant(df):
    """AI Chat Assistant for Cross-sell Recommendations"""
    st.markdown("## 🤖 AI Chat Assistant")
    
    # Check for Gemini API key
    gemini_key = os.environ.get('GEMINI_API_KEY') or st.secrets.get('GEMINI_API_KEY', None) if hasattr(st, 'secrets') else None
    
    if GEMINI_AVAILABLE and gemini_key:
        st.markdown("*Powered by Google Gemini AI* 🌟")
        if "gemini_model" not in st.session_state:
            genai.configure(api_key=gemini_key)
            st.session_state.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    else:
        st.markdown("*Get instant insights and recommendations powered by AI*")
        if not GEMINI_AVAILABLE:
            st.info("💡 Install `google-generativeai` and add GEMINI_API_KEY for real AI chat. Currently using rule-based responses.")
    
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "👋 Hello! I'm your AI assistant for cross-sell analytics. I can help you with:\n\n• Customer recommendations\n• Propensity score explanations\n• Campaign strategy suggestions\n• Data insights and trends\n\nWhat would you like to know?"
        })
    
    # Quick action buttons
    st.markdown("### 💡 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Top 10 Prospects"):
            prompt = "Show me the top 10 customers most likely to convert to home loan"
            st.session_state.messages.append({"role": "user", "content": prompt})
    
    with col2:
        if st.button("📊 Conversion Insights"):
            prompt = "What are the key factors driving home loan conversions?"
            st.session_state.messages.append({"role": "user", "content": prompt})
    
    with col3:
        if st.button("💰 ROI Strategy"):
            prompt = "Suggest a campaign strategy to maximize ROI"
            st.session_state.messages.append({"role": "user", "content": prompt})
    
    st.markdown("---")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about cross-sell analytics..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
    # Generate AI response
    if st.session_state.messages[-1]["role"] == "user":
        user_query = st.session_state.messages[-1]["content"]
        
        # Generate contextual response based on data
        with st.chat_message("assistant"):
            # Try Gemini first, fallback to rule-based
            if GEMINI_AVAILABLE and gemini_key and "gemini_model" in st.session_state:
                response = generate_gemini_response(user_query, df, st.session_state.gemini_model)
            else:
                response = generate_ai_response(user_query.lower(), df)
            
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

def generate_gemini_response(query, df, model):
    """Generate response using Google Gemini AI"""
    
    # Prepare context with data summary
    data_context = f"""
You are an AI assistant for Tata Capital's cross-sell analytics dashboard. You help analyze customer data for Personal Loan to Home Loan cross-sell campaigns.

Current Dataset Summary:
- Total Customers: {len(df):,}
- HL Conversions: {df['took_hl'].sum():,}
- Conversion Rate: {df['took_hl'].mean()*100:.1f}%
- Average Propensity Score: {df['model_propensity_score'].mean():.1f}

Top 5 Customers by Propensity:
{df.nlargest(5, 'model_propensity_score')[['customer_id', 'model_propensity_score', 'segment', 'bureau_score']].to_string()}

Segment Performance:
{df.groupby('segment')['took_hl'].agg(['count', 'mean']).to_string()}

User Question: {query}

Provide a helpful, data-driven response. Use markdown formatting. Be concise but informative.
"""
    
    try:
        response = model.generate_content(data_context)
        return response.text
    except Exception as e:
        return f"⚠️ Error connecting to Gemini AI: {str(e)}\n\nFalling back to rule-based responses. Try asking about:\n• Top customers\n• Conversion insights\n• Campaign strategy"

def generate_ai_response(query, df):
    """Generate AI response based on query and data (rule-based fallback)"""
    
    # Top prospects query
    if "top" in query and ("customer" in query or "prospect" in query):
        top_customers = df.nlargest(10, 'model_propensity_score')[
            ['customer_id', 'model_propensity_score', 'bureau_score', 'monthly_income', 'segment']
        ]
        
        response = "### 🎯 Top 10 High-Propensity Customers\n\n"
        response += "Here are your best prospects for home loan cross-sell:\n\n"
        
        for idx, row in top_customers.iterrows():
            response += f"**{row['customer_id']}** - Propensity: {row['model_propensity_score']:.1f}/100\n"
            response += f"  • Bureau Score: {int(row['bureau_score'])} | Income: ₹{row['monthly_income']:,.0f} | Segment: {row['segment']}\n\n"
        
        response += "\n💡 **Recommendation:** Prioritize RM calls for these customers within 7 days with pre-approved offers."
        return response
    
    # Conversion insights query
    elif "factor" in query or "insight" in query or "conversion" in query:
        high_conv = df[df['took_hl'] == True]
        
        response = "### 📊 Key Conversion Drivers\n\n"
        response += f"**Conversion Rate:** {df['took_hl'].mean()*100:.1f}%\n\n"
        response += "**Top Factors:**\n\n"
        response += f"1. **Age 30-42 (Prime Age):** {high_conv['age'].between(30, 42).mean()*100:.1f}% of converters\n"
        response += f"2. **HL Calculator Usage:** {high_conv['hl_calculator_used'].mean()*100:.1f}% used the calculator\n"
        response += f"3. **Low DPD:** {(high_conv['dpd_last_12m'] == 0).mean()*100:.1f}% have zero DPD\n"
        response += f"4. **High Digital Engagement:** Avg score {high_conv['digital_engagement_score'].mean():.1f}/100\n"
        response += f"5. **Tier 1 Cities:** {(high_conv['city_tier'] == 'Tier 1').mean()*100:.1f}% from Tier 1\n\n"
        response += "💡 **Insight:** Focus on digitally engaged customers aged 30-42 with clean repayment history."
        return response
    
    # ROI/Strategy query
    elif "roi" in query or "strategy" in query or "campaign" in query:
        high_prop = df[df['model_propensity_score'] >= 60]
        expected_conv = high_prop['took_hl'].sum()
        
        response = "### 💰 Recommended Campaign Strategy\n\n"
        response += "**Target Segment:** Propensity Score ≥ 60\n\n"
        response += f"• **Target Size:** {len(high_prop):,} customers\n"
        response += f"• **Expected Conversions:** {expected_conv:,} customers\n"
        response += f"• **Conversion Rate:** {(expected_conv/len(high_prop)*100):.1f}%\n\n"
        response += "**Channel Strategy:**\n\n"
        response += "1. **Score 70-100 (High):** RM Call + WhatsApp + Pre-approved offer\n"
        response += "2. **Score 60-69 (Medium):** App Push + SMS + Eligibility checker\n\n"
        response += "**Expected ROI:**\n"
        response += f"• Cost @ ₹50/contact: ₹{len(high_prop)*50:,.0f}\n"
        response += f"• Revenue @ ₹50k/loan: ₹{expected_conv*50000:,.0f}\n"
        response += f"• **Net Profit:** ₹{(expected_conv*50000 - len(high_prop)*50):,.0f}\n"
        response += f"• **ROI:** {((expected_conv*50000 - len(high_prop)*50)/(len(high_prop)*50)*100):.1f}%\n\n"
        response += "💡 **Recommendation:** Launch campaign in phases, starting with score ≥70 first."
        return response
    
    # Segment analysis query
    elif "segment" in query:
        segment_stats = df.groupby('segment').agg({
            'took_hl': 'mean',
            'model_propensity_score': 'mean',
            'customer_id': 'count'
        }).round(2)
        
        response = "### 📈 Segment Performance Analysis\n\n"
        for segment in segment_stats.index:
            conv_rate = segment_stats.loc[segment, 'took_hl'] * 100
            avg_prop = segment_stats.loc[segment, 'model_propensity_score']
            count = int(segment_stats.loc[segment, 'customer_id'])
            
            response += f"**{segment}**\n"
            response += f"  • Customers: {count:,} | Conv Rate: {conv_rate:.1f}% | Avg Propensity: {avg_prop:.1f}\n\n"
        
        response += "💡 **Insight:** Focus resources on segments with highest conversion rates for better efficiency."
        return response
    
    # Customer lookup query
    elif "customer" in query and any(char.isdigit() for char in query):
        # Extract customer ID from query
        import re
        cust_ids = re.findall(r'CUST\d+', query.upper())
        
        if cust_ids:
            cust_id = cust_ids[0]
            if cust_id in df['customer_id'].values:
                cust = df[df['customer_id'] == cust_id].iloc[0]
                
                response = f"### 👤 Customer Profile: {cust_id}\n\n"
                response += f"**Propensity Score:** {cust['model_propensity_score']:.1f}/100\n"
                response += f"**Segment:** {cust['segment']}\n"
                response += f"**Age:** {int(cust['age'])} | **Income:** ₹{cust['monthly_income']:,.0f}\n"
                response += f"**Bureau Score:** {int(cust['bureau_score'])} | **Repayment Score:** {cust['repayment_score']:.0f}/100\n\n"
                
                if cust['model_propensity_score'] >= 70:
                    response += "🎯 **Recommendation:** HIGH PRIORITY - Contact within 7 days with pre-approved offer"
                elif cust['model_propensity_score'] >= 50:
                    response += "📞 **Recommendation:** MEDIUM PRIORITY - Send app push notification"
                else:
                    response += "📧 **Recommendation:** NURTURE - Add to email campaign"
                
                return response
    
    # Default response
    response = "I can help you with:\n\n"
    response += "• **Top prospects:** Ask 'Show me top customers'\n"
    response += "• **Conversion insights:** Ask 'What drives conversions?'\n"
    response += "• **Campaign strategy:** Ask 'Suggest a campaign strategy'\n"
    response += "• **Segment analysis:** Ask 'Analyze segments'\n"
    response += "• **Customer lookup:** Ask 'Tell me about CUST000001'\n\n"
    response += "Try one of the quick action buttons above or ask me anything!"
    
    return response

def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🏦 Tata Capital Cross-sell Analytics</h1>
            <p>Personal Loan → Home Loan | AI-Powered Propensity Model</p>
        </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        page = st.radio(
            "Select View",
            ["Customer 360", "Segment Analysis", "Campaign Simulator", "AI Chat Assistant"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("## 📊 Dataset Overview")
        
        st.metric("Total Customers", f"{len(df):,}")
        st.metric("HL Conversions", f"{df['took_hl'].sum():,}")
        st.metric("Conversion Rate", f"{df['took_hl'].mean()*100:.1f}%")
    
    # Main content
    if page == "Customer 360":
        customer_360_view(df)
    elif page == "Segment Analysis":
        segment_analysis(df)
    elif page == "Campaign Simulator":
        campaign_simulator(df)
    elif page == "AI Chat Assistant":
        ai_chat_assistant(df)

if __name__ == "__main__":
    main()
