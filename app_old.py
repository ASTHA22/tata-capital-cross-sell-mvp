import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Tata Capital - Cross-sell Analytics",
    page_icon="🏦",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load scored customer data"""
    try:
        df = pd.read_csv('nbfc_customers_scored.csv')
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file not found. Please run generate_data.py and train_model.py first.")
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
    st.header("🔍 Customer 360 View")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        customer_id = st.selectbox(
            "Select Customer ID",
            options=df['customer_id'].tolist(),
            index=0
        )
    
    customer = df[df['customer_id'] == customer_id].iloc[0]
    
    with col2:
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.metric("Propensity Score", f"{customer['model_propensity_score']:.1f}/100")
        with metric_cols[1]:
            st.metric("Bureau Score", int(customer['bureau_score']))
        with metric_cols[2]:
            st.metric("Repayment Score", f"{customer['repayment_score']:.0f}/100")
        with metric_cols[3]:
            status = "✅ Converted" if customer['took_hl'] else "🎯 Target"
            st.metric("Status", status)
    
    st.divider()
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📋 Customer Profile")
        
        profile_data = {
            "Customer ID": customer['customer_id'],
            "Age": f"{int(customer['age'])} years",
            "Employment": customer['employment_type'],
            "Monthly Income": format_currency(customer['monthly_income']),
            "City": f"{customer['city']} ({customer['city_tier']})",
            "Bureau Score": int(customer['bureau_score']),
            "Segment": customer['segment']
        }
        
        for key, value in profile_data.items():
            st.text(f"{key}: {value}")
        
        st.subheader("💳 Personal Loan Details")
        pl_data = {
            "Ticket Size": format_currency(customer['pl_ticket_size']),
            "Tenure": f"{int(customer['pl_tenure_months'])} months",
            "Vintage": f"{int(customer['pl_vintage_months'])} months",
            "Repayment Score": f"{customer['repayment_score']:.0f}/100",
            "DPD (Last 12M)": int(customer['dpd_last_12m']),
            "FOIR": f"{customer['foir_percent']:.1f}%"
        }
        
        for key, value in pl_data.items():
            st.text(f"{key}: {value}")
    
    with col_right:
        st.subheader("🎯 Cross-sell Intelligence")
        
        propensity = customer['model_propensity_score']
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=propensity,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "HL Propensity Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 50], 'color': "lightyellow"},
                    {'range': [50, 70], 'color': "lightgreen"},
                    {'range': [70, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("💡 Recommended Action")
        
        if propensity >= 70:
            st.success("🎯 **High Priority Target**")
            ticket_size = min(customer['monthly_income'] * 60, 5000000)
            st.write(f"**Offer:** Pre-approved Home Loan up to {format_currency(ticket_size)}")
            st.write(f"**Channel:** RM Call + WhatsApp")
            st.write(f"**Timing:** Within 7 days")
            st.write(f"**Script Angle:** 'Your excellent repayment history qualifies you for our best HL rates'")
        elif propensity >= 50:
            st.info("📞 **Medium Priority**")
            st.write(f"**Offer:** Home Loan eligibility check")
            st.write(f"**Channel:** App Push + SMS")
            st.write(f"**Timing:** Within 14 days")
        elif propensity >= 30:
            st.warning("📧 **Nurture Campaign**")
            st.write(f"**Offer:** HL calculator + content marketing")
            st.write(f"**Channel:** Email + App banner")
        else:
            st.error("⏸️ **Low Priority - Do Not Contact**")
            st.write("Focus on higher propensity customers")
        
        st.subheader("📊 Engagement Signals")
        engagement_data = {
            "Digital Score": f"{customer['digital_engagement_score']:.0f}/100",
            "App Logins (90d)": int(customer['app_logins_90d']),
            "HL Calculator Used": "✅ Yes" if customer['hl_calculator_used'] else "❌ No"
        }
        
        for key, value in engagement_data.items():
            st.text(f"{key}: {value}")

def segment_analysis(df):
    """Segment Analysis Dashboard"""
    st.header("📊 Segment Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total PL Customers", f"{len(df):,}")
    with col2:
        st.metric("HL Conversions", f"{df['took_hl'].sum():,}")
    with col3:
        st.metric("Conversion Rate", f"{df['took_hl'].mean()*100:.1f}%")
    with col4:
        st.metric("Avg Propensity", f"{df['model_propensity_score'].mean():.1f}")
    
    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Segment Overview", "Propensity Distribution", "Decile Analysis", "Feature Analysis"])
    
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
                title="Customer Count by Segment",
                color_continuous_scale='Blues'
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            fig = px.bar(
                segment_stats,
                x='segment',
                y='Conv_Rate',
                text=segment_stats['Conv_Rate'].apply(lambda x: f"{x*100:.1f}%"),
                title="Conversion Rate by Segment",
                color='Conv_Rate',
                color_continuous_scale='Greens'
            )
            fig.update_traces(textposition='outside')
            fig.update_yaxes(title="Conversion Rate")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col_c, col_d = st.columns(2)
        
        with col_c:
            fig = px.histogram(
                df,
                x='model_propensity_score',
                nbins=50,
                title="Propensity Score Distribution",
                color_discrete_sequence=['steelblue']
            )
            fig.update_xaxes(title="Propensity Score")
            fig.update_yaxes(title="Number of Customers")
            st.plotly_chart(fig, use_container_width=True)
        
        with col_d:
            fig = px.box(
                df,
                x='segment',
                y='model_propensity_score',
                title="Propensity Score by Segment",
                color='segment'
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
        
        st.subheader("📈 Decile Performance")
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Conversion Rate by Decile", "Lift vs Baseline")
        )
        
        fig.add_trace(
            go.Bar(
                x=decile_analysis['propensity_decile'],
                y=decile_analysis['Conv_Rate'] * 100,
                name='Conversion Rate',
                marker_color='steelblue'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=decile_analysis['propensity_decile'],
                y=decile_analysis['Lift'],
                name='Lift',
                marker_color='green'
            ),
            row=1, col=2
        )
        
        fig.add_hline(y=1, line_dash="dash", line_color="red", row=1, col=2)
        
        fig.update_xaxes(title_text="Propensity Decile", row=1, col=1)
        fig.update_xaxes(title_text="Propensity Decile", row=1, col=2)
        fig.update_yaxes(title_text="Conversion Rate (%)", row=1, col=1)
        fig.update_yaxes(title_text="Lift vs Baseline", row=1, col=2)
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(
            decile_analysis.style.format({
                'Conv_Rate': '{:.1%}',
                'Avg_Propensity': '{:.1f}',
                'Lift': '{:.2f}x'
            }),
            use_container_width=True
        )
    
    with tab4:
        col_e, col_f = st.columns(2)
        
        with col_e:
            age_bins = pd.cut(df['age'], bins=[20, 30, 35, 40, 45, 60])
            age_conv = df.groupby(age_bins)['took_hl'].mean() * 100
            
            fig = px.bar(
                x=age_conv.index.astype(str),
                y=age_conv.values,
                title="Conversion Rate by Age Band",
                labels={'x': 'Age Band', 'y': 'Conversion Rate (%)'},
                color=age_conv.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_f:
            city_conv = df.groupby('city_tier')['took_hl'].mean() * 100
            
            fig = px.bar(
                x=city_conv.index,
                y=city_conv.values,
                title="Conversion Rate by City Tier",
                labels={'x': 'City Tier', 'y': 'Conversion Rate (%)'},
                color=city_conv.values,
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)

def campaign_simulator(df):
    """Campaign Simulator"""
    st.header("🎯 Campaign Simulator")
    
    st.write("Simulate targeting different customer segments and estimate campaign outcomes.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Campaign Parameters")
        
        min_propensity = st.slider(
            "Minimum Propensity Score",
            min_value=0,
            max_value=100,
            value=50,
            step=5
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
            step=5000
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
        
        st.subheader("📊 Campaign Estimates")
        
        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.metric("Target Customers", f"{total_targets:,}")
        with metric_cols[1]:
            st.metric("Expected Conversions", f"{expected_conversions:,}")
        with metric_cols[2]:
            st.metric("Conversion Rate", f"{conversion_rate*100:.1f}%")
        
        metric_cols2 = st.columns(3)
        with metric_cols2[0]:
            st.metric("Lift vs Baseline", f"{lift:.2f}x")
        with metric_cols2[1]:
            st.metric("Total Cost", format_currency(total_cost))
        with metric_cols2[2]:
            st.metric("Expected Revenue", format_currency(total_revenue))
        
        roi_col = st.columns(1)[0]
        with roi_col:
            if roi > 0:
                st.success(f"💰 **ROI: {roi:.1f}%** (Profitable)")
            else:
                st.error(f"💸 **ROI: {roi:.1f}%** (Not Profitable)")
        
        st.divider()
        
        st.subheader("📈 Campaign Breakdown")
        
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
                title="Target Distribution by Segment",
                color_continuous_scale='Blues'
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(
                segment_breakdown.style.format({
                    'Avg_Propensity': '{:.1f}'
                }),
                use_container_width=True
            )
        else:
            st.warning("No customers match the selected criteria. Please adjust filters.")

def main():
    st.title("🏦 Tata Capital - PL to HL Cross-sell Analytics")
    st.markdown("**Personal Loan → Home Loan Cross-sell Propensity Model**")
    
    df = load_data()
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["Customer 360", "Segment Analysis", "Campaign Simulator"]
    )
    
    st.sidebar.divider()
    st.sidebar.subheader("Dataset Overview")
    st.sidebar.metric("Total Customers", f"{len(df):,}")
    st.sidebar.metric("HL Conversions", f"{df['took_hl'].sum():,}")
    st.sidebar.metric("Conversion Rate", f"{df['took_hl'].mean()*100:.1f}%")
    
    if page == "Customer 360":
        customer_360_view(df)
    elif page == "Segment Analysis":
        segment_analysis(df)
    elif page == "Campaign Simulator":
        campaign_simulator(df)

if __name__ == "__main__":
    main()
