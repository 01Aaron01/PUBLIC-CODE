import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Jonah.Works Startup Nursery Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .success-metric {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .revenue-metric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .impact-metric {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    # Sample data based on the CSV structure
    data = {
        'Market Region': ['UK', 'UK', 'France', 'France', 'Caribbean'],
        'Market Type': ['Urban', 'Rural', 'North', 'South', 'Mixed'],
        'Products Tested': [85, 45, 35, 25, 10],
        'Validation Protocol Status': ['Implemented', 'Implemented', 'Implemented', 'Implemented', 'Implemented'],
        'Monthly Recurring Revenue (GBP)': [30000, 12000, 15000, 18000, 8000],
        'Client Retention Rate': ['95%', '97%', '96%', '94%', '93%'],
        'Regulatory Framework Status': ['Compliant', 'Compliant', 'Compliant', 'Compliant', 'Compliant'],
        'Community Impact Score': [4.5, 4.8, 4.2, 4.0, 4.6],
        'Strategic Partners': [
            'Local Council;Business Wales',
            'Welsh Government;AberInnovation',
            'French Tech Initiative',
            'Regional Innovation Hub',
            'Caribbean Development Bank'
        ],
        'Project Duration (Months)': [18, 24, 12, 15, 9],
        'Key Achievements': [
            'Market entry protocol established;High client retention',
            'Car-Y-Mor economic model success',
            'Cross-border expansion success',
            'Cultural adaptation framework',
            'New market penetration model'
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Clean and convert data
    df['Client Retention Rate'] = df['Client Retention Rate'].str.rstrip('%').astype(float)
    df['Partner Count'] = df['Strategic Partners'].str.count(';') + 1
    df['Achievement Count'] = df['Key Achievements'].str.count(';') + 1
    
    return df

df = load_data()

# Header
st.title("🚀 Jonah.Works Performance Dashboard 2019 - 2024, All Rights Reserved")
st.markdown("*Director's Executive View - Real-time Business Intelligence*")

# Sidebar filters
st.sidebar.header("📊 Dashboard Filters")
selected_regions = st.sidebar.multiselect(
    "Select Market Regions",
    options=df['Market Region'].unique(),
    default=df['Market Region'].unique()
)

selected_types = st.sidebar.multiselect(
    "Select Market Types",
    options=df['Market Type'].unique(),
    default=df['Market Type'].unique()
)

# Filter data
filtered_df = df[
    (df['Market Region'].isin(selected_regions)) & 
    (df['Market Type'].isin(selected_types))
]

# Key Metrics Row
st.header("📈 Executive Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = filtered_df['Monthly Recurring Revenue (GBP)'].sum()
    st.markdown(f"""
    <div class="metric-card revenue-metric">
        <h3>£{total_revenue:,}</h3>
        <p>Total Monthly Revenue</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_retention = filtered_df['Client Retention Rate'].mean()
    st.markdown(f"""
    <div class="metric-card success-metric">
        <h3>{avg_retention:.1f}%</h3>
        <p>Average Retention Rate</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_impact = filtered_df['Community Impact Score'].mean()
    st.markdown(f"""
    <div class="metric-card impact-metric">
        <h3>{avg_impact:.1f}/5.0</h3>
        <p>Community Impact Score</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_products = filtered_df['Products Tested'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <h3>{total_products}</h3>
        <p>Products Tested</p>
    </div>
    """, unsafe_allow_html=True)

# Create tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance Analytics", "🗺️ Geographic Insights", "🤝 Partnership Network", "🎯 Strategic Achievements"])

with tab1:
    st.header("Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Region
        fig_revenue = px.bar(
            filtered_df, 
            x='Market Region', 
            y='Monthly Recurring Revenue (GBP)',
            color='Market Type',
            title="Monthly Revenue by Region & Type",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_revenue.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Retention vs Impact Scatter
        fig_scatter = px.scatter(
            filtered_df,
            x='Client Retention Rate',
            y='Community Impact Score',
            size='Monthly Recurring Revenue (GBP)',
            color='Market Region',
            title="Retention Rate vs Community Impact",
            hover_data=['Market Type', 'Products Tested']
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Products tested vs Project Duration
    fig_products = px.scatter(
        filtered_df,
        x='Project Duration (Months)',
        y='Products Tested',
        size='Monthly Recurring Revenue (GBP)',
        color='Community Impact Score',
        title="Product Testing Efficiency: Duration vs Volume",
        color_continuous_scale='Viridis'
    )
    fig_products.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_products, use_container_width=True)

with tab2:
    st.header("Geographic Market Distribution")
    
    # Regional Performance Metrics at the top
    st.subheader("Regional Performance Summary")
    
    # Create columns for regional metrics
    metric_cols = st.columns(len(filtered_df['Market Region'].unique()))
    
    for idx, region in enumerate(filtered_df['Market Region'].unique()):
        region_data = filtered_df[filtered_df['Market Region'] == region]
        revenue = region_data['Monthly Recurring Revenue (GBP)'].sum()
        avg_impact = region_data['Community Impact Score'].mean()
        
        with metric_cols[idx]:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 12px;
                color: white;
                text-align: center;
                margin: 10px 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            ">
                <h3 style="margin: 0 0 15px 0; font-size: 1.4em;">{region}</h3>
                <p style="margin: 8px 0; font-size: 16px; font-weight: bold;">💰 £{revenue:,}</p>
                <p style="margin: 8px 0; font-size: 14px;">🎯 Impact: {avg_impact:.1f}/5.0</p>
                <p style="margin: 8px 0; font-size: 14px;">📊 Markets: {len(region_data)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Add spacing before map
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Map gets full width
    st.subheader("Global Market Presence & Performance")
    
    # Create a simple map representation
    # Since we don't have actual coordinates, we'll create a conceptual map
    fig_map = go.Figure()
    
    # Add markers for each region (conceptual positioning)
    region_coords = {
        'UK': {'lat': 54.7, 'lon': -2.8},
        'France': {'lat': 46.6, 'lon': 2.2},
        'Caribbean': {'lat': 18.2, 'lon': -66.5}
    }
    
    for _, row in filtered_df.iterrows():
        region = row['Market Region']
        if region in region_coords:
            fig_map.add_trace(go.Scattermapbox(
                lat=[region_coords[region]['lat']],
                lon=[region_coords[region]['lon']],
                mode='markers',
                marker=dict(
                    size=row['Monthly Recurring Revenue (GBP)']/1000,
                    color=row['Community Impact Score'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(
                        title="Impact Score",
                        orientation="h",  # Horizontal orientation
                        x=0.5,  # Center horizontally
                        y=-0.1,  # Position below the map
                        xanchor="center",
                        len=0.5,  # Make it shorter
                        thickness=15  # Make it thinner
                    )
                ),
                text=f"{region} - {row['Market Type']}<br>Revenue: £{row['Monthly Recurring Revenue (GBP)']:,}<br>Impact: {row['Community Impact Score']}/5",
                hoverinfo='text',
                name=f"{region} ({row['Market Type']})"
            ))
    
    fig_map.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=45, lon=-10),
            zoom=2
        ),
        height=500,
        margin=dict(l=0, r=0, t=0, b=50)  # Add bottom margin for horizontal colorbar
    )
    
    st.plotly_chart(fig_map, use_container_width=True)

with tab3:
    st.header("Partnership Network Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Partner count by region
        fig_partners = px.bar(
            filtered_df,
            x='Market Region',
            y='Partner Count',
            color='Market Type',
            title="Strategic Partners by Region"
        )
        st.plotly_chart(fig_partners, use_container_width=True)
    
    with col2:
        # Partnership efficiency (revenue per partner)
        filtered_df['Revenue per Partner'] = filtered_df['Monthly Recurring Revenue (GBP)'] / filtered_df['Partner Count']
        fig_efficiency = px.bar(
            filtered_df,
            x='Market Region',
            y='Revenue per Partner',
            color='Community Impact Score',
            title="Partnership ROI (Revenue per Partner)",
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_efficiency, use_container_width=True)
    
    # Detailed partnership table
    st.subheader("Partnership Details")
    partnership_table = filtered_df[['Market Region', 'Market Type', 'Strategic Partners', 'Partner Count', 'Monthly Recurring Revenue (GBP)']].copy()
    partnership_table['Strategic Partners'] = partnership_table['Strategic Partners'].str.replace(';', ', ')
    st.dataframe(partnership_table, use_container_width=True)

with tab4:
    st.header("Strategic Achievements & Outcomes")
    
    # Achievement metrics
    col1, col2 = st.columns(2)
    
    with col1:
        fig_achievements = px.bar(
            filtered_df,
            x='Market Region',
            y='Achievement Count',
            color='Project Duration (Months)',
            title="Achievement Density by Region",
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_achievements, use_container_width=True)
    
    with col2:
        # ROI analysis (revenue vs duration)
        filtered_df['Monthly ROI'] = filtered_df['Monthly Recurring Revenue (GBP)'] / filtered_df['Project Duration (Months)']
        fig_roi = px.scatter(
            filtered_df,
            x='Project Duration (Months)',
            y='Monthly ROI',
            size='Products Tested',
            color='Community Impact Score',
            title="Project ROI Analysis",
            color_continuous_scale='Plasma'
        )
        st.plotly_chart(fig_roi, use_container_width=True)
    
    # Detailed achievements
    st.subheader("Key Achievements by Market")
    for _, row in filtered_df.iterrows():
        with st.expander(f"🎯 {row['Market Region']} - {row['Market Type']} Market"):
            achievements = row['Key Achievements'].split(';')
            partners = row['Strategic Partners'].split(';')
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Key Achievements:**")
                for achievement in achievements:
                    st.write(f"• {achievement.strip()}")
            
            with col2:
                st.write("**Strategic Partners:**")
                for partner in partners:
                    st.write(f"• {partner.strip()}")
            
            st.write(f"**Project Metrics:**")
            st.write(f"Duration: {row['Project Duration (Months)']} months | Revenue: £{row['Monthly Recurring Revenue (GBP)']:,} | Impact Score: {row['Community Impact Score']}/5.0")

# Footer
st.markdown("---")
st.markdown("*Dashboard last updated: Real-time | Data source: Jonah Ocean Systems Ltd 2024, All Rights Reserved.*")
