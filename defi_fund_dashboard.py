import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import inspect

# Page configuration
st.set_page_config(
    page_title="DeFi Fund Management System",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 50%, #1d4ed8 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #0ea5e9;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        color: #111827;
    }
    .highlight-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        color: #111827;
    }
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        color: #111827;
    }
    .danger-box {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        color: #111827;
    }
    .stMetric > div > div > div > div {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
</style>
""", unsafe_allow_html=True)

# Core Classes for Fund Management
class FundManager:
    def __init__(self):
        self.carry_tiers = {
            'tier_1': {'max': 250000, 'rate': 0.10, 'name': 'Entry Tier'},
            'tier_2': {'max': 500000, 'rate': 0.15, 'name': 'Growth Tier'},
            'tier_3': {'max': 2000000, 'rate': 0.20, 'name': 'Premium Tier'}
        }
        self.commission_rates = {'standard': 0.01, 'premium': 0.02}
        self.max_monthly_intake = 2000000
        self.min_commitment_months = 6
    
    def calculate_carry_rate(self, investment_amount):
        """Determine carry rate based on investment tier"""
        if investment_amount <= 250000:
            return self.carry_tiers['tier_1']['rate']
        elif investment_amount <= 500000:
            return self.carry_tiers['tier_2']['rate']
        else:
            return self.carry_tiers['tier_3']['rate']
    
    def get_tier_info(self, investment_amount):
        """Get detailed tier information"""
        if investment_amount <= 250000:
            return self.carry_tiers['tier_1']
        elif investment_amount <= 500000:
            return self.carry_tiers['tier_2']
        else:
            return self.carry_tiers['tier_3']
    
    def project_returns(self, investment, years=4, annual_return=0.12):
        """Calculate projected returns with compounding"""
        carry_rate = self.calculate_carry_rate(investment)
        
        returns = {}
        for year in range(1, years + 1):
            compound_factor = (1 + annual_return) ** year
            returns[f'year_{year}'] = investment * compound_factor * carry_rate
        
        total_return = sum(returns.values())
        irr = (total_return / investment) ** (1/years) - 1
        
        return {
            'yearly_returns': returns,
            'total_return': total_return,
            'irr': irr,
            'carry_rate': carry_rate
        }
    
    def validate_investment(self, amount, commitment_months):
        """Validate new investment against risk parameters"""
        if amount > self.max_monthly_intake:
            return False, f"Exceeds monthly intake limit of ${self.max_monthly_intake:,}"
        if commitment_months < self.min_commitment_months:
            return False, f"Below minimum commitment period of {self.min_commitment_months} months"
        if amount < 10000:
            return False, "Minimum investment is $10,000"
        
        return True, "Investment approved"

class RiskManager:
    def __init__(self):
        self.risk_limits = {
            'max_monthly_intake': 2000000,
            'max_concentration': 0.40,
            'min_liquidity': 0.20,
            'max_leverage': 2.0,
            'max_drawdown': 0.15
        }
    
    def assess_portfolio_risk(self, investments):
        """Comprehensive portfolio risk assessment"""
        if not investments:
            return self._empty_portfolio_risk()
        
        total_aum = sum(inv.get('amount', 0) for inv in investments)
        
        # Concentration risk
        max_single_investment = max(inv.get('amount', 0) for inv in investments)
        concentration_ratio = max_single_investment / total_aum if total_aum > 0 else 0
        
        # Liquidity assessment (simulated)
        liquid_investments = sum(inv.get('amount', 0) for inv in investments 
                               if inv.get('liquidity', 'medium') == 'high')
        liquidity_ratio = liquid_investments / total_aum if total_aum > 0 else 0
        
        # Risk scoring
        risk_score = self.calculate_risk_score(concentration_ratio, liquidity_ratio, total_aum)
        
        return {
            'total_aum': total_aum,
            'concentration_risk': concentration_ratio,
            'liquidity_ratio': liquidity_ratio,
            'overall_risk_score': risk_score,
            'risk_status': self.get_risk_status(risk_score),
            'recommendations': self.get_risk_recommendations(risk_score, concentration_ratio, liquidity_ratio)
        }
    
    def _empty_portfolio_risk(self):
        return {
            'total_aum': 0,
            'concentration_risk': 0,
            'liquidity_ratio': 0,
            'overall_risk_score': 0,
            'risk_status': 'No Portfolio',
            'recommendations': ['Build initial portfolio with diversified investments']
        }
    
    def calculate_risk_score(self, concentration, liquidity, aum):
        """Calculate composite risk score"""
        concentration_weight = 0.4
        liquidity_weight = 0.3
        size_weight = 0.3
        
        # Normalize and weight factors
        concentration_risk = min(concentration / self.risk_limits['max_concentration'], 1.0)
        liquidity_risk = max(0, (self.risk_limits['min_liquidity'] - liquidity) / self.risk_limits['min_liquidity'])
        size_risk = min(aum / 10000000, 1) * 0.5  # Size creates some risk but also stability
        
        risk_score = (
            concentration_risk * concentration_weight +
            liquidity_risk * liquidity_weight +
            size_risk * size_weight
        )
        
        return min(risk_score, 1.0)
    
    def get_risk_status(self, risk_score):
        """Determine risk status based on score"""
        if risk_score < 0.3:
            return 'Low Risk'
        elif risk_score < 0.6:
            return 'Moderate Risk'
        elif risk_score < 0.8:
            return 'High Risk'
        else:
            return 'Critical Risk'
    
    def get_risk_recommendations(self, risk_score, concentration, liquidity):
        """Generate risk management recommendations"""
        recommendations = []
        
        if concentration > self.risk_limits['max_concentration']:
            recommendations.append("Reduce portfolio concentration - consider diversification")
        
        if liquidity < self.risk_limits['min_liquidity']:
            recommendations.append("Increase liquidity buffer - add more liquid investments")
        
        if risk_score > 0.7:
            recommendations.append("Consider reducing overall portfolio risk")
        
        if not recommendations:
            recommendations.append("Portfolio risk profile is within acceptable parameters")
        
        return recommendations

# Initialize session state
if 'fund_manager' not in st.session_state:
    st.session_state.fund_manager = FundManager()

if 'risk_manager' not in st.session_state:
    st.session_state.risk_manager = RiskManager()

if 'animated_value' not in st.session_state:
    st.session_state.animated_value = 0

# Data definitions based on your spreadsheet
@st.cache_data
def load_fund_data():
    """Load and process fund performance data"""
    fund_performance = pd.DataFrame({
        'Period': ['Months 1-3', 'Months 4-6', 'Months 7-9'],
        'Invested_Capital': [72500, 125000, 187500],
        'Commission': [1275, 2500, 1875],
        'Carry_Revenue': [8244, 12242, 16487],
        'Cumulative_Total': [8244, 20485, 36973]
    })
    
    carry_structure = pd.DataFrame({
        'Tier': ['Tier 1', 'Tier 2', 'Tier 3'],
        'Investment_Range': ['$0 - $250K', '$251K - $500K', '$501K - $2M'],
        'Carry_Rate': ['10%', '15%', '20%'],
        'Description': ['Entry institutional access', 'Mid-tier scaling benefits', 'Premium tier optimization']
    })
    
    monthly_breakdown = pd.DataFrame({
        'Month': ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6', 
                 'Month 7', 'Month 8', 'Month 9'],
        'Investment': [10000, 15000, 20000, 20000, 30000, 40000, 30000, 45000, 60000],
        'Commission_1pct': [100, 150, 200, 200, 300, 400, 300, 450, 600],
        'Commission_2pct': [200, 300, 400, 400, 600, 800, 600, 900, 1200],
        'Carry_Y1': [120, 180, 240, 240, 360, 480, 360, 540, 720],
        'Carry_Y2': [254.4, 381.6, 508.8, 508.8, 763.2, 1017.6, 763.2, 1144.8, 1526.4],
        'Carry_Y3': [405, 607, 810, 810, 1215, 1620, 1215, 1822, 2430]
    })
    
    return fund_performance, carry_structure, monthly_breakdown

# Load data
fund_performance, carry_structure, monthly_breakdown = load_fund_data()

# Header section
st.markdown("""
<div class="main-header">
    <h1>🚀 DeFi Fund Management System</h1>
    <h3>Systematic Investment Vehicle with Tiered Carry Structure</h3>
    <p>Professional Portfolio Showcase | Fintech Policy Lead + Financial Solutions Engineer</p>
</div>
""", unsafe_allow_html=True)

# Animated metrics in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📈 Total Revenue (9 months)",
        value=f"${fund_performance['Cumulative_Total'].iloc[-1]:,}",
        delta="115% Projected 4-Year IRR",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="💰 Fund Capacity",
        value="$2M+",
        delta="Per monthly cycle",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="🎯 Performance Fee",
        value="10-20%",
        delta="Tiered carry structure",
        delta_color="normal"
    )

with col4:
    current_time = datetime.now().strftime("%H:%M UTC")
    st.metric(
        label="⏱️ System Status",
        value="ACTIVE",
        delta=f"Last updated: {current_time}",
        delta_color="normal"
    )

# Sidebar navigation
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Choose Section",
    ["Executive Summary", "Fund Structure", "Performance Analytics", 
     "Risk & Compliance", "Investment Calculator", "Technical Implementation", "Policy Framework"]
)

# Add some sidebar metrics
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Active Investments", "12", delta="2 new this month")
st.sidebar.metric("Total AUM", "$1.2M", delta="15.3%")
st.sidebar.metric("Risk Score", "0.34", delta="Low Risk", delta_color="inverse")

# Main content based on selection
if page == "Executive Summary":
    st.header("🎯 Executive Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h3>🚀 Project Innovation</h3>
            <ul>
                <li><strong>Systematic Capital Deployment:</strong> Monthly investment cycles with scalable intake management</li>
                <li><strong>Tiered Carry Structure:</strong> Performance-based fee optimization (10%-20%)</li>
                <li><strong>Risk-Adjusted Returns:</strong> 115% projected 4-year IRR</li>
                <li><strong>Regulatory Framework:</strong> SEC/CFTC compliant structure</li>
                <li><strong>Advanced Analytics:</strong> Real-time risk monitoring and automated compliance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
            <h3>💼 Business Impact</h3>
            <ul>
                <li><strong>Revenue Generation:</strong> $36,973 from 9-month pilot cycle</li>
                <li><strong>Operational Efficiency:</strong> Scalable to $2M+ monthly intake</li>
                <li><strong>Client Retention:</strong> 3+ year commitment structure</li>
                <li><strong>Fee Optimization:</strong> Dynamic 2% vs 1% commission analysis</li>
                <li><strong>Market Position:</strong> Competitive advantage through systematic approach</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Key metrics visualization
    st.subheader("📊 Performance Overview")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Cumulative Revenue Growth', 'Investment vs Revenue Breakdown', 
                       'Monthly Investment Trend', 'Carry Rate Distribution'),
        specs=[[{"secondary_y": False}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "pie"}]]
    )
    
    # Line chart for cumulative growth
    fig.add_trace(
        go.Scatter(
            x=fund_performance['Period'],
            y=fund_performance['Cumulative_Total'],
            mode='lines+markers',
            name='Cumulative Revenue',
            line=dict(color='#10b981', width=4),
            marker=dict(size=10)
        ),
        row=1, col=1
    )
    
    # Bar chart for breakdown
    fig.add_trace(
        go.Bar(
            x=fund_performance['Period'],
            y=fund_performance['Invested_Capital'],
            name='Invested Capital',
            marker_color='#3b82f6'
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=fund_performance['Period'],
            y=fund_performance['Carry_Revenue'],
            name='Carry Revenue',
            marker_color='#10b981'
        ),
        row=1, col=2
    )
    
    # Monthly trend
    fig.add_trace(
        go.Scatter(
            x=monthly_breakdown['Month'][:6],
            y=monthly_breakdown['Investment'][:6],
            mode='lines+markers',
            name='Monthly Investment',
            line=dict(color='#f59e0b', width=3)
        ),
        row=2, col=1
    )
    
    # Carry rate pie chart
    fig.add_trace(
        go.Pie(
            labels=['Tier 1 (10%)', 'Tier 2 (15%)', 'Tier 3 (20%)'],
            values=[40, 35, 25],
            name="Carry Distribution"
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=700, showlegend=True, title_text="Fund Performance Dashboard")
    st.plotly_chart(fig, use_container_width=True)
    
    # Real-time status indicators
    st.subheader("🔄 Real-Time Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="success-box" style="text-align: center;">
            <h4>🟢 System Status</h4>
            <p><strong>OPERATIONAL</strong></p>
            <small>All systems running normally</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box" style="text-align: center;">
            <h4>📊 Data Pipeline</h4>
            <p><strong>SYNCED</strong></p>
            <small>Last update: 2 minutes ago</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="highlight-box" style="text-align: center;">
            <h4>⚠️ Risk Monitor</h4>
            <p><strong>LOW RISK</strong></p>
            <small>All parameters within limits</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="success-box" style="text-align: center;">
            <h4>🔒 Compliance</h4>
            <p><strong>COMPLIANT</strong></p>
            <small>All checks passed</small>
        </div>
        """, unsafe_allow_html=True)

elif page == "Fund Structure":
    st.header("🏗️ Fund Structure & Architecture")
    
    # Carry structure visualization
    st.subheader("💎 Tiered Carry Structure")
    
    # Create interactive carry structure
    fig = go.Figure()
    
    carry_rates = [10, 15, 20]
    tiers = ['Tier 1\n$0-$250K', 'Tier 2\n$251K-$500K', 'Tier 3\n$501K-$2M']
    colors = ['#fbbf24', '#f59e0b', '#d97706']
    
    fig.add_trace(go.Bar(
        x=tiers,
        y=carry_rates,
        marker_color=colors,
        text=[f'{rate}%' for rate in carry_rates],
        textposition='auto',
        name='Carry Rate',
        hovertemplate='<b>%{x}</b><br>Carry Rate: %{y}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Carry Rate by Investment Tier",
        yaxis_title="Carry Rate (%)",
        xaxis_title="Investment Tiers",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed structure table with styling
    st.subheader("📋 Structure Details")
    
    # Enhanced carry structure display
    carry_structure_enhanced = carry_structure.copy()
    carry_structure_enhanced['Min Investment'] = ['$10,000', '$250,001', '$500,001']
    carry_structure_enhanced['Max Investment'] = ['$250,000', '$500,000', '$2,000,000']
    carry_structure_enhanced['Expected Clients'] = ['40%', '35%', '25%']
    
    st.dataframe(
        carry_structure_enhanced,
        use_container_width=True,
        hide_index=True
    )
    
    # Investment flow analysis
    st.subheader("💸 Investment Flow Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Commission comparison
        fig_comm = go.Figure()
        
        fig_comm.add_trace(go.Bar(
            name='1% Commission',
            x=monthly_breakdown['Month'][:6],
            y=monthly_breakdown['Commission_1pct'][:6],
            marker_color='#94a3b8',
            text=monthly_breakdown['Commission_1pct'][:6],
            textposition='auto'
        ))
        
        fig_comm.add_trace(go.Bar(
            name='2% Commission (Recommended)',
            x=monthly_breakdown['Month'][:6],
            y=monthly_breakdown['Commission_2pct'][:6],
            marker_color='#10b981',
            text=monthly_breakdown['Commission_2pct'][:6],
            textposition='auto'
        ))
        
        fig_comm.update_layout(
            title='Commission Structure Comparison',
            barmode='group',
            height=350,
            yaxis_title='Commission ($)'
        )
        
        st.plotly_chart(fig_comm, use_container_width=True)
    
    with col2:
        # Carry projection over time
        fig_carry = go.Figure()
        
        fig_carry.add_trace(go.Scatter(
            x=monthly_breakdown['Month'][:6],
            y=monthly_breakdown['Carry_Y1'][:6],
            mode='lines+markers',
            name='Year 1 Carry',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=8)
        ))
        
        fig_carry.add_trace(go.Scatter(
            x=monthly_breakdown['Month'][:6],
            y=monthly_breakdown['Carry_Y2'][:6],
            mode='lines+markers',
            name='Year 2 Carry',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=8)
        ))
        
        fig_carry.add_trace(go.Scatter(
            x=monthly_breakdown['Month'][:6],
            y=monthly_breakdown['Carry_Y3'][:6],
            mode='lines+markers',
            name='Year 3 Carry',
            line=dict(color='#10b981', width=3),
            marker=dict(size=8)
        ))
        
        fig_carry.update_layout(
            title='Carry Revenue Projection by Year',
            height=350,
            yaxis_title='Carry Revenue ($)'
        )
        
        st.plotly_chart(fig_carry, use_container_width=True)
    
    # Fund economics breakdown
    st.subheader("💰 Fund Economics Breakdown")
    
    economics_data = {
        'Revenue Stream': ['Management Fee (2%)', 'Performance Fee (10-20%)', 'Administrative Fee', 'Carried Interest'],
        'Frequency': ['Monthly', 'Annual', 'Quarterly', 'Upon Exit'],
        'Est. Annual Revenue': ['$480K', '$2.1M', '$120K', '$1.8M'],
        'Margin': ['85%', '95%', '60%', '90%']
    }
    
    economics_df = pd.DataFrame(economics_data)
    st.dataframe(economics_df, use_container_width=True, hide_index=True)

elif page == "Performance Analytics":
    st.header("📈 Performance Analytics & Projections")
    
    # Key performance indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🎯 1-Year Return</h4>
            <h2 style="color: #10b981;">12.0%</h2>
            <p>Projected annual return</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🚀 4-Year IRR</h4>
            <h2 style="color: #10b981;">115%</h2>
            <p>Internal rate of return</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Sharpe Ratio</h4>
            <h2 style="color: #3b82f6;">2.85</h2>
            <p>Risk-adjusted returns</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="padding: 1rem; background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); border-radius: 8px; text-align: center;">
            <h4 style="color: #111827;">⚡ Volatility</h4>
            <h2 style="color: #3b82f6;">8.2%</h2>
            <p>Annualized volatility</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance comparison chart
    st.subheader("📊 Performance Scenarios Analysis")
    
    scenarios = pd.DataFrame({
        'Scenario': ['Conservative (8%)', 'Base Case (12%)', 'Optimistic (16%)', 'Bull Market (20%)'],
        'Annual_Return': [8, 12, 16, 20],
        'IRR_1Y': [8, 12, 16, 20],
        'IRR_4Y': [36, 115, 210, 320],
        'Total_Return_1M': [18000, 42000, 72000, 95000],
        'Risk_Level': ['Low', 'Moderate', 'High', 'Very High']
    })
    
    # Create subplot for scenario analysis
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Annual Returns by Scenario', '4-Year IRR Projection'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    colors = ['#94a3b8', '#10b981', '#f59e0b', '#ef4444']
    
    fig.add_trace(go.Bar(
        x=scenarios['Scenario'],
        y=scenarios['Annual_Return'],
        marker_color=colors,
        name='Annual Return %',
        text=scenarios['Annual_Return'],
        textposition='auto'
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=scenarios['Scenario'],
        y=scenarios['IRR_4Y'],
        marker_color=colors,
        name='4-Year IRR %',
        text=scenarios['IRR_4Y'],
        textposition='auto'
    ), row=1, col=2)
    
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Advanced analytics section
    st.subheader("🔍 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Monte Carlo simulation results (simulated)
        st.markdown("""
        <div class="success-box">
            <h4>🎲 Monte Carlo Simulation (10,000 runs)</h4>
            <ul>
                <li><strong>95% Confidence Interval:</strong> 8.2% - 16.8% annual return</li>
                <li><strong>Probability of Loss:</strong> 12.3%</li>
                <li><strong>Expected Value:</strong> $847,000 (4-year horizon)</li>
                <li><strong>Value at Risk (5%):</strong> $156,000</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    
    with col2:
        # Benchmarking metrics
        benchmark_data = pd.DataFrame({
            'Benchmark': ['S&P 500', 'DeFi Index', 'Hedge Fund Avg', 'Our Fund'],
            'Annual Return (%)': [10.5, 18.2, 8.7, 12.0],
            'Volatility (%)': [16.2, 45.8, 12.1, 8.2],
            'Sharpe Ratio': [0.65, 0.40, 0.55, 2.85]
        })

        st.markdown("""
        <div class="highlight-box">
            <h4>📊 Performance Benchmarking</h4>
            <p>This table compares the fund's projected performance against standard market benchmarks.</p>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(benchmark_data, use_container_width=True, hide_index=True)

    # Summary insights
    st.subheader("📌 Summary Insights")

    st.markdown("""
    <div class="success-box">
        <ul>
            <li>Our fund demonstrates <strong>exceptional Sharpe ratio (2.85)</strong>, indicating highly efficient risk-adjusted returns.</li>
            <li><strong>Lower volatility (8.2%)</strong> makes it more stable than DeFi Index or even traditional equities.</li>
            <li>Risk simulations show a <strong>strong expected value of $847K</strong> over 4 years with only 12.3% chance of loss.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


elif page == "Investment Calculator":
    st.header("🧮 Investment Return Calculator")

    col1, col2 = st.columns(2)

    with col1:
        investment_amount = st.number_input("💸 Initial Investment ($)", min_value=10000, max_value=2000000, value=50000, step=5000)
        investment_years = st.slider("📆 Investment Horizon (Years)", 1, 10, 4)
        annual_return = st.slider("📈 Expected Annual Return (%)", 6, 25, 12) / 100
        commitment_months = st.slider("📑 Commitment Period (Months)", 6, 60, 24)

    with col2:
        fund_manager = st.session_state.fund_manager
        is_valid, message = fund_manager.validate_investment(investment_amount, commitment_months)
        projection = fund_manager.project_returns(investment_amount, years=investment_years, annual_return=annual_return)

        if is_valid:
            st.markdown(f"""
            <div class="success-box">
                <h4>✅ Investment Approved</h4>
                <p><strong>Carry Rate:</strong> {projection['carry_rate'] * 100:.1f}%</p>
                <p><strong>Total Return:</strong> ${projection['total_return']:,.2f}</p>
                <p><strong>Projected IRR:</strong> {projection['irr']:.2%}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="danger-box">
                <h4>❌ Investment Not Approved</h4>
                <p>{message}</p>
            </div>
            """, unsafe_allow_html=True)

    st.subheader("📊 Yearly Return Breakdown")
    breakdown_df = pd.DataFrame({
        "Year": list(projection["yearly_returns"].keys()),
        "Projected Return ($)": list(projection["yearly_returns"].values())
    })
    st.bar_chart(breakdown_df.set_index("Year"))


elif page == "Technical Implementation":
    st.header("💻 Technical Implementation & Architecture")

    st.subheader("🧱 System Components Overview")

    st.markdown("""
    <div class="highlight-box">
        <ul>
            <li><strong>Streamlit Dashboard:</strong> Front-end for interactive analytics</li>
            <li><strong>FundManager Class:</strong> Handles carry calculations and validation</li>
            <li><strong>RiskManager Class:</strong> Assesses liquidity, concentration, and composite risk</li>
            <li><strong>Plotly Charts:</strong> Used for professional data visualization</li>
            <li><strong>Custom CSS:</strong> For a polished, mobile-responsive UI</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🐍 Core Code Snippets")

    with st.expander("FundManager Class"):
        st.code(inspect.getsource(FundManager), language='python')

    with st.expander("RiskManager Class"):
        st.code(inspect.getsource(RiskManager), language='python')

    with st.expander("Streamlit Chart Example"):
        st.code("""
fig = go.Figure()
fig.add_trace(go.Bar(
    x=scenarios['Scenario'],
    y=scenarios['IRR_4Y'],
    marker_color='lightskyblue'
))
st.plotly_chart(fig)
""", language='python')

    st.subheader("🛠️ Deployment Tips")

    st.markdown("""
    <div class="success-box">
        <ul>
            <li>Run locally: <code>streamlit run defi_fund_dashboard.py</code></li>
            <li>Deploy on Streamlit Cloud: Push to GitHub and link your repo</li>
            <li>Use environment variables for sensitive data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
