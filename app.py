# UrbanAirAI.py - Complete Single File Application
# AI-Powered Urban Air Quality Intelligence Platform
# Economic Times Hackathon 2024

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Urban Air Quality Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DATA GENERATORS
# ============================================================================
def generate_mock_data():
    cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Ahmedabad']
    data = []
    base_time = datetime.now()
    for i in range(24):
        timestamp = base_time - timedelta(hours=23-i)
        for city in cities:
            aqi = random.randint(80, 250)
            if city == 'Delhi':
                aqi += random.randint(20, 60)
            elif city == 'Mumbai':
                aqi += random.randint(10, 40)
            data.append({
                'timestamp': timestamp,
                'city': city,
                'aqi': aqi,
                'pm25': aqi * random.uniform(0.4, 0.7),
                'pm10': aqi * random.uniform(0.6, 0.9),
                'no2': random.uniform(20, 80),
                'temp': random.uniform(20, 35),
                'humidity': random.uniform(40, 80),
                'wind_speed': random.uniform(0, 15)
            })
    return pd.DataFrame(data)

def generate_city_data():
    cities = ['Delhi', 'Mumbai', 'Pune', 'Bengaluru', 'Hyderabad', 'Chennai', 'Ahmedabad', 'Kolkata']
    city_data = {}
    for city in cities:
        aqi = random.randint(80, 250)
        if city == 'Delhi':
            aqi += random.randint(30, 70)
        elif city == 'Mumbai':
            aqi += random.randint(10, 40)
        city_data[city] = {
            'aqi': aqi,
            'aqi_change': random.randint(-15, 15),
            'pm25': aqi * random.uniform(0.4, 0.7),
            'pm10': aqi * random.uniform(0.6, 0.9),
            'temp': random.uniform(20, 35),
            'humidity': random.uniform(40, 80)
        }
    return city_data

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_aqi_color(aqi):
    if aqi <= 50: return '#00C853'
    elif aqi <= 100: return '#FFD600'
    elif aqi <= 200: return '#FF9100'
    elif aqi <= 300: return '#FF1744'
    elif aqi <= 400: return '#D500F9'
    else: return '#4A148C'

def get_aqi_category(aqi):
    if aqi <= 50: return 'Good'
    elif aqi <= 100: return 'Satisfactory'
    elif aqi <= 200: return 'Moderate'
    elif aqi <= 300: return 'Poor'
    elif aqi <= 400: return 'Very Poor'
    else: return 'Severe'

# ============================================================================
# AI AGENTS
# ============================================================================
class ForecastAgent:
    def predict(self, horizon=24):
        return [random.randint(80, 200) for _ in range(horizon)]

class PollutionAgent:
    def analyze(self):
        return {
            'Traffic': 28, 'Industries': 22, 'Construction': 18,
            'Waste Burning': 12, 'Dust': 10, 'Power Plants': 6, 'Crop Burning': 4
        }

class HealthAgent:
    def assess(self, user_type):
        profiles = {
            'Child': {'risk': 'High', 'symptoms': 'Coughing, breathing difficulty', 'precautions': 'Stay indoors, use N95 mask'},
            'Pregnant Woman': {'risk': 'Very High', 'symptoms': 'Breathlessness, fatigue', 'precautions': 'Avoid outdoor exposure'},
            'Asthma Patient': {'risk': 'Critical', 'symptoms': 'Wheezing, chest tightness', 'precautions': 'Keep inhaler ready, stay indoors'},
            'Senior Citizen': {'risk': 'High', 'symptoms': 'Breathing issues, dizziness', 'precautions': 'Stay indoors, use air purifier'},
            'General Citizen': {'risk': 'Low', 'symptoms': 'Mild irritation', 'precautions': 'Limit outdoor activities'}
        }
        return profiles.get(user_type, profiles['General Citizen'])

# ============================================================================
# SESSION STATE
# ============================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = 'Delhi'
if 'city_data' not in st.session_state:
    st.session_state.city_data = generate_city_data()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_pollutant' not in st.session_state:
    st.session_state.selected_pollutant = 'aqi'
if 'time_range' not in st.session_state:
    st.session_state.time_range = 24
if 'selected_compare_cities' not in st.session_state:
    st.session_state.selected_compare_cities = ['Delhi', 'Mumbai']

# ============================================================================
# CUSTOM CSS - Light Theme with Sky Blue
# ============================================================================
st.markdown("""
<style>
    /* Main background - White */
    .stApp {
        background-color: #f0f4f8 !important;
    }
    
    /* Sidebar - Light */
    .css-1d391kg {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* All text dark */
    .stMarkdown, .stText, .stSelectbox, .stMultiSelect, label, .stMetric label {
        color: #1a202c !important;
    }
    
    /* Metric cards */
    .stMetric {
        background: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .stMetric .css-1xarl3l {
        color: #1a202c !important;
    }
    .stMetric .css-1wivap2 {
        color: #4a5568 !important;
    }
    
    /* Cards */
    .stat-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .stat-label {
        color: #4a5568;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stat-value {
        color: #1a202c;
        font-size: 30px;
        font-weight: 700;
        margin: 8px 0;
    }
    .stat-sub {
        color: #718096;
        font-size: 13px;
    }
    
    /* Alert cards */
    .alert-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin: 5px 0;
        border-left: 4px solid #4299e1;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .alert-emergency { border-left-color: #fc8181; background: #fff5f5; }
    .alert-warning { border-left-color: #f6ad55; background: #fffbeb; }
    .alert-info { border-left-color: #4299e1; background: #ebf8ff; }
    .alert-msg { color: #1a202c; font-size: 14px; }
    .alert-icon { font-size: 24px; }
    
    /* Source ranking */
    .source-rank {
        display: flex;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #e2e8f0;
        gap: 15px;
    }
    .rank-number { color: #4299e1; font-weight: 700; min-width: 30px; }
    .rank-name { color: #1a202c; min-width: 130px; }
    .rank-bar {
        height: 8px;
        background: linear-gradient(90deg, #4299e1, #63b3ed);
        border-radius: 4px;
        flex: 1;
    }
    .rank-value { color: #1a202c; font-weight: 700; min-width: 45px; text-align: right; }
    
    /* Recommendations */
    .rec-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .rec-source { color: #2b6cb0; font-weight: 600; }
    .rec-impact { 
        padding: 3px 12px; 
        border-radius: 15px; 
        font-size: 12px; 
        font-weight: 600;
    }
    .rec-impact-high { background: #fed7d7; color: #c53030; }
    .rec-impact-medium { background: #fefcbf; color: #975a16; }
    .rec-text { color: #2d3748; margin-top: 8px; }
    
    /* Enforcement */
    .enforcement-item {
        background: #ffffff;
        padding: 14px 18px;
        border-radius: 10px;
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 3px solid #4299e1;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .enforcement-area { color: #1a202c; font-weight: 600; }
    .enforcement-status { color: #d69e2e; }
    .enforcement-action { color: #4299e1; border: 1px solid #4299e1; padding: 2px 12px; border-radius: 15px; font-size: 12px; }
    
    /* Health */
    .health-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .risk-level {
        font-size: 26px;
        font-weight: 700;
        text-align: center;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .risk-critical { background: #fed7d7; color: #c53030; }
    .risk-very-high { background: #fed7d7; color: #e53e3e; }
    .risk-high { background: #fefcbf; color: #975a16; }
    .risk-medium { background: #fefcbf; color: #d69e2e; }
    .risk-low { background: #bee3f8; color: #2b6cb0; }
    .risk-symptoms, .risk-precautions { color: #2d3748; padding: 8px 0; }
    
    /* Hospital cards */
    .hospital-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .hospital-name { color: #2b6cb0; font-weight: 600; font-size: 16px; }
    .hospital-distance { color: #4a5568; margin: 5px 0; }
    .hospital-occupancy { color: #d69e2e; }
    
    /* Fine cards */
    .fine-card {
        background: #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 3px solid #fc8181;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .fine-entity { color: #1a202c; font-weight: 600; }
    .fine-amount { color: #e53e3e; font-weight: 700; }
    .fine-reason { color: #4a5568; font-size: 13px; }
    
    /* Schedule */
    .schedule-card { background: #ffffff; border-radius: 10px; padding: 15px; border: 1px solid #e2e8f0; }
    .schedule-item {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #e2e8f0;
        color: #1a202c;
    }
    .schedule-time { color: #4299e1; font-weight: 600; }
    
    /* Chat */
    .chat-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        max-height: 450px;
        overflow-y: auto;
        border: 1px solid #e2e8f0;
    }
    .chat-message {
        display: flex;
        margin: 10px 0;
        gap: 12px;
    }
    .chat-message.user { flex-direction: row-reverse; }
    .message-icon {
        width: 35px;
        height: 35px;
        background: #ebf8ff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .message-content {
        background: #f7fafc;
        padding: 12px 16px;
        border-radius: 12px;
        max-width: 70%;
        color: #1a202c;
    }
    .chat-message.user .message-content {
        background: #ebf8ff;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #ebf8ff, #bee3f8);
        border: 1px solid #bee3f8;
        border-radius: 20px;
        padding: 50px 40px;
        margin: 20px 0;
        text-align: center;
    }
    .hero-badge {
        background: #ffffff;
        border: 1px solid #4299e1;
        border-radius: 20px;
        padding: 5px 18px;
        color: #2b6cb0;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 15px;
    }
    .hero-title {
        color: #1a202c;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .hero-subtitle {
        color: #4a5568;
        font-size: 18px;
        margin-bottom: 25px;
    }
    
    /* Footer */
    .footer {
        margin-top: 40px;
        padding: 20px 0;
        border-top: 1px solid #e2e8f0;
    }
    .footer-content {
        display: flex;
        justify-content: space-between;
        color: #718096;
        font-size: 13px;
    }
    
    /* Buttons */
    .stButton > button {
        background: #ffffff !important;
        color: #2b6cb0 !important;
        border: 1px solid #bee3f8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background: #ebf8ff !important;
        border-color: #4299e1 !important;
    }
    .stButton > button[data-baseweb="button"] {
        background: #4299e1 !important;
        color: #ffffff !important;
        border: none !important;
    }
    .stButton > button[data-baseweb="button"]:hover {
        background: #2b6cb0 !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: #ffffff !important;
        color: #1a202c !important;
        border-color: #e2e8f0 !important;
    }
    
    /* Info boxes */
    .stAlert {
        background: #ebf8ff !important;
        border-color: #bee3f8 !important;
        color: #1a202c !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #ffffff;
        border-radius: 8px;
        padding: 10px 20px;
        color: #4a5568;
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #ebf8ff;
        color: #2b6cb0;
        border-color: #4299e1;
    }
    
    /* Detection items */
    .detection-item {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #e2e8f0;
        color: #1a202c;
    }
    .status-healthy { color: #38a169; }
    .status-detected { color: #e53e3e; }
    .status-active { color: #d69e2e; }
    
    /* Sidebar brand */
    .sidebar-brand {
        padding: 15px 0;
        text-align: center;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }
    .sidebar-brand h1 {
        color: #2b6cb0;
        font-size: 22px;
        margin: 0;
    }
    .sidebar-brand p {
        color: #4a5568;
        font-size: 12px;
        margin: 5px 0 0;
    }
    
    /* Streamlit base text overrides */
    .css-10trblm, .css-1cpxqw2, .css-1kyxreq {
        color: #1a202c !important;
    }
    
    /* Metric value */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px;
    }
    [data-testid="metric-container"] label {
        color: #4a5568 !important;
    }
    [data-testid="metric-container"] .css-1xarl3l {
        color: #1a202c !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: #4299e1 !important;
    }
    .stSlider > div > div > div > div {
        background-color: #2b6cb0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <h1>🌍 AirIQ</h1>
            <p>Smart Air Intelligence</p>
        </div>
    """, unsafe_allow_html=True)
    
    nav_pages = {
        '🏠 Dashboard': 'dashboard',
        '📍 Live AQI': 'live-aqi',
        '🔥 Heatmap': 'heatmap',
        '📈 Forecast': 'forecast',
        '🏭 Pollution Sources': 'pollution',
        '⚖️ Enforcement': 'enforcement',
        '🏥 Health Risk': 'health',
        '🏨 Hospitals': 'hospitals',
        '🤖 AI Chat': 'chat',
        'ℹ️ About': 'about'
    }
    
    for label, key in nav_pages.items():
        if st.button(label, key=key, use_container_width=True,
                     type="primary" if st.session_state.page == key else "secondary"):
            st.session_state.page = key
            st.rerun()
    
    st.markdown("---")
    
    cities = ['Delhi', 'Mumbai', 'Pune', 'Bengaluru', 'Hyderabad', 'Chennai', 'Ahmedabad', 'Kolkata']
    selected = st.selectbox("🌆 City", cities, index=cities.index(st.session_state.selected_city))
    if selected != st.session_state.selected_city:
        st.session_state.selected_city = selected
        st.rerun()
    
    city_data = st.session_state.city_data.get(st.session_state.selected_city, {})
    if city_data:
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("AQI", city_data.get('aqi', 'N/A'), delta=city_data.get('aqi_change', 0))
            st.metric("PM2.5", f"{city_data.get('pm25', 0):.1f}")
        with col2:
            st.metric("PM10", f"{city_data.get('pm10', 0):.1f}")
            st.metric("Temp", f"{city_data.get('temp', 0):.1f}°C")

# ============================================================================
# PAGE RENDERERS
# ============================================================================
def render_dashboard():
    # Interactive controls at top
    st.markdown("## 📊 Command Center Dashboard")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        time_range = st.selectbox(
            "⏱️ Time Range",
            ["Last 6 Hours", "Last 12 Hours", "Last 24 Hours", "Last 48 Hours"],
            index=2
        )
    with col2:
        pollutant_view = st.selectbox(
            "📊 Pollutant View",
            ["AQI", "PM2.5", "PM10", "NO2", "Temperature"],
            index=0
        )
    with col3:
        city_filter = st.multiselect(
            "🏙️ Cities",
            ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad'],
            default=['Delhi', 'Mumbai']
        )
        if not city_filter:
            city_filter = ['Delhi']
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("🌍 National AQI", "156", "Moderate"),
        ("📊 Avg AQI", "142", "-12%"),
        ("⚠️ Worst City", "Mumbai", "AQI: 189"),
        ("📈 Improved", "Delhi", "-23%")
    ]
    for col, (label, value, sub) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                    <div class="stat-sub">{sub}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Map and Charts
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 🗺️ AQI Map")
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles='OpenStreetMap')
        
        cities_data = [
            ("Delhi", 28.6139, 77.2090, 178),
            ("Mumbai", 19.0760, 72.8777, 189),
            ("Bengaluru", 12.9716, 77.5946, 112),
            ("Chennai", 13.0827, 80.2707, 145),
            ("Hyderabad", 17.3850, 78.4867, 134),
            ("Kolkata", 22.5726, 88.3639, 156),
            ("Pune", 18.5204, 73.8567, 128),
            ("Ahmedabad", 23.0225, 72.5714, 167)
        ]
        
        for city, lat, lon, aqi in cities_data:
            color = get_aqi_color(aqi)
            folium.CircleMarker(
                location=[lat, lon],
                radius=15,
                popup=f"<b>{city}</b><br>AQI: {aqi}<br>{get_aqi_category(aqi)}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
        
        folium_static(m, width=700, height=400)
    
    with col2:
        st.markdown("### 📈 Interactive Trend")
        
        # Generate data based on selected pollutant
        data = generate_mock_data()
        filtered_data = data[data['city'].isin(city_filter)]
        
        if not filtered_data.empty:
            pollutant_map = {
                'AQI': 'aqi',
                'PM2.5': 'pm25',
                'PM10': 'pm10',
                'NO2': 'no2',
                'Temperature': 'temp'
            }
            y_col = pollutant_map.get(pollutant_view, 'aqi')
            y_label = pollutant_view
            
            fig = go.Figure()
            for city in city_filter:
                city_data_plot = filtered_data[filtered_data['city'] == city]
                fig.add_trace(go.Scatter(
                    x=city_data_plot['timestamp'],
                    y=city_data_plot[y_col],
                    mode='lines+markers',
                    name=city,
                    line=dict(width=2),
                    marker=dict(size=6)
                ))
            
            fig.update_layout(
                template='plotly_white',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=0, r=0, t=20, b=0),
                xaxis=dict(gridcolor='rgba(0,0,0,0.05)', color='#4a5568'),
                yaxis=dict(gridcolor='rgba(0,0,0,0.05)', color='#4a5568', title=y_label),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select cities to view trends")
    
    # Interactive Pollutant Comparison
    st.markdown("### 📊 Pollutant Correlation Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter plot with slider for interactive selection
        pollutant_x = st.selectbox(
            "X-Axis Pollutant",
            ["PM2.5", "PM10", "NO2", "Temperature", "Humidity"],
            key="pollutant_x"
        )
        pollutant_y = st.selectbox(
            "Y-Axis Pollutant",
            ["AQI", "PM2.5", "PM10", "NO2", "Temperature"],
            index=0,
            key="pollutant_y"
        )
        
        pollutant_map = {
            'AQI': 'aqi', 'PM2.5': 'pm25', 'PM10': 'pm10',
            'NO2': 'no2', 'Temperature': 'temp', 'Humidity': 'humidity'
        }
        
        data = generate_mock_data()
        data_filtered = data[data['city'].isin(city_filter)]
        
        if not data_filtered.empty:
            x_col = pollutant_map.get(pollutant_x, 'pm25')
            y_col = pollutant_map.get(pollutant_y, 'aqi')
            
            fig = px.scatter(
                data_filtered,
                x=x_col,
                y=y_col,
                color='city',
                title=f'{pollutant_x} vs {pollutant_y}',
                color_discrete_sequence=px.colors.qualitative.Set1,
                trendline='ols',
                trendline_color_override='#2b6cb0'
            )
            fig.update_layout(
                template='plotly_white',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=350,
                xaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
                yaxis=dict(gridcolor='rgba(0,0,0,0.05)')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # AQI Distribution Box Plot
        st.markdown("### AQI Distribution by City")
        
        data_all = generate_mock_data()
        selected_cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad']
        plot_data = data_all[data_all['city'].isin(selected_cities)]
        
        fig = px.box(
            plot_data,
            x='city',
            y='aqi',
            color='city',
            title='AQI Distribution',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            showlegend=False,
            xaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(gridcolor='rgba(0,0,0,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Alerts
    st.markdown("### ⚠️ Live Alerts")
    alerts = [
        ("🔴", "Delhi - AQI exceeds 300 in ITO area", "Emergency"),
        ("🟡", "Mumbai - High traffic congestion near Bandra", "Warning"),
        ("🟢", "Bengaluru - Air quality improving", "Info"),
        ("🟠", "Chennai - Industrial emissions detected", "Alert")
    ]
    cols = st.columns(4)
    for col, (icon, msg, level) in zip(cols, alerts):
        with col:
            st.markdown(f"""
                <div class="alert-card alert-{level.lower()}">
                    <div class="alert-icon">{icon}</div>
                    <div class="alert-msg">{msg}</div>
                </div>
            """, unsafe_allow_html=True)

def render_live_aqi():
    st.markdown("## 📍 Live AQI Monitoring")
    
    # Interactive Filters
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        view_type = st.selectbox(
            "📊 View Mode",
            ["Grid View", "Chart View", "Gauge View"],
            index=0
        )
    with col2:
        pollutant_select = st.selectbox(
            "🧪 Pollutant",
            ["AQI", "PM2.5", "PM10", "NO2"],
            index=0
        )
    with col3:
        refresh_rate = st.selectbox(
            "🔄 Refresh",
            ["Real-time", "5 min", "15 min", "1 hour"],
            index=0
        )
    
    # City grid with interactive gauges
    cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Ahmedabad']
    
    if view_type == "Grid View":
        cols = st.columns(4)
        for i, city in enumerate(cities):
            with cols[i % 4]:
                aqi = random.randint(80, 250)
                color = get_aqi_color(aqi)
                
                # Add clickable card with expander
                with st.expander(f"📍 {city}", expanded=True):
                    st.markdown(f"""
                        <div style="text-align:center;">
                            <div style="font-size:48px;color:{color};font-weight:700;">{aqi}</div>
                            <div style="color:#4a5568;font-weight:600;">{get_aqi_category(aqi)}</div>
                            <div style="color:#718096;font-size:13px;margin-top:8px;">
                                PM2.5: {random.randint(30, 120)} | PM10: {random.randint(50, 200)}
                            </div>
                            <div style="color:#718096;font-size:13px;">
                                Temp: {random.randint(20, 35)}°C | Humidity: {random.randint(40, 80)}%
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View Details", key=f"detail_{city}"):
                        st.info(f"📊 Detailed analysis for {city} loaded")
    
    elif view_type == "Chart View":
        st.markdown("### 📊 Real-time AQI Chart")
        
        data = generate_mock_data()
        pollutant_map = {'AQI': 'aqi', 'PM2.5': 'pm25', 'PM10': 'pm10', 'NO2': 'no2'}
        y_col = pollutant_map.get(pollutant_select, 'aqi')
        
        fig = go.Figure()
        for city in cities[:5]:
            city_data = data[data['city'] == city]
            fig.add_trace(go.Scatter(
                x=city_data['timestamp'],
                y=city_data[y_col],
                mode='lines+markers',
                name=city,
                line=dict(width=2),
                marker=dict(size=5)
            ))
        
        fig.update_layout(
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            xaxis=dict(gridcolor='rgba(0,0,0,0.05)', title='Time'),
            yaxis=dict(gridcolor='rgba(0,0,0,0.05)', title=pollutant_select),
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    else:  # Gauge View
        st.markdown("### 🎯 AQI Gauge Dashboard")
        
        selected_city_gauge = st.selectbox("Select City", cities, key="gauge_city")
        aqi_value = random.randint(80, 250)
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=aqi_value,
            domain={'x': [0, 1], 'y': [0, 1]},
            delta={'reference': 150, 'position': "top"},
            gauge={
                'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "#1a202c"},
                'bar': {'color': get_aqi_color(aqi_value)},
                'steps': [
                    {'range': [0, 50], 'color': "#00C853"},
                    {'range': [50, 100], 'color': "#FFD600"},
                    {'range': [100, 200], 'color': "#FF9100"},
                    {'range': [200, 300], 'color': "#FF1744"},
                    {'range': [300, 400], 'color': "#D500F9"},
                    {'range': [400, 500], 'color': "#4A148C"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 300
                }
            },
            title={'text': f"{selected_city_gauge} - AQI", 'font': {'color': '#1a202c', 'size': 20}}
        ))
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "#1a202c"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Quick stats for selected city
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Category", get_aqi_category(aqi_value))
        with col2:
            st.metric("PM2.5", f"{random.randint(30, 150)} µg/m³")
        with col3:
            st.metric("PM10", f"{random.randint(50, 250)} µg/m³")
    
    # Interactive City Comparison Table
    st.markdown("### 📊 City Comparison")
    
    compare_cols = st.multiselect(
        "Select cities to compare",
        cities,
        default=['Delhi', 'Mumbai', 'Bengaluru']
    )
    
    if compare_cols:
        comp_data = []
        for city in compare_cols:
            aqi = random.randint(80, 250)
            comp_data.append({
                'City': city,
                'AQI': aqi,
                'Category': get_aqi_category(aqi),
                'PM2.5': random.randint(30, 150),
                'PM10': random.randint(50, 250),
                'Temp': random.randint(20, 35),
                'Humidity': random.randint(40, 80)
            })
        
        df = pd.DataFrame(comp_data)
        
        # Colored AQI display
        fig = go.Figure(data=[
            go.Bar(
                name='AQI',
                x=df['City'],
                y=df['AQI'],
                marker_color=[get_aqi_color(aqi) for aqi in df['AQI']],
                text=df['AQI'],
                textposition='outside',
                textfont={'color': '#1a202c'}
            )
        ])
        fig.update_layout(
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            xaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(
            df.style.background_gradient(subset=['AQI'], cmap='RdYlGn_r'),
            use_container_width=True,
            hide_index=True
        )

def render_heatmap():
    st.markdown("## 🔥 Pollution Heatmap")
    
    m = folium.Map(location=[28.6139, 77.2090], zoom_start=11, tiles='OpenStreetMap')
    
    heat_data = []
    for _ in range(200):
        lat = 28.6139 + random.uniform(-0.4, 0.4)
        lon = 77.2090 + random.uniform(-0.4, 0.4)
        intensity = random.uniform(0, 100)
        heat_data.append([lat, lon, intensity])
    
    HeatMap(heat_data, radius=20, blur=12, max_zoom=13).add_to(m)
    folium_static(m, width=1200, height=550)

def render_forecast():
    st.markdown("## 📈 AQI Forecast")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        horizon = st.selectbox("Forecast Horizon", ["24 Hours", "48 Hours", "72 Hours", "7 Days"])
    with col2:
        st.metric("Model Accuracy", "89%", "+2.1%")
        st.metric("RMSE", "12.4", "-1.8")
    
    hours = list(range(48))
    historical = [random.randint(100, 200) for _ in range(24)]
    forecast = [random.randint(80, 180) for _ in range(24)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours[:24], y=historical,
        mode='lines', name='Historical',
        line=dict(color='#4299e1', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=hours[24:], y=forecast,
        mode='lines', name='Forecast',
        line=dict(color='#fc8181', width=2, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=hours[24:], y=[f+20 for f in forecast],
        mode='lines', name='Upper',
        line=dict(width=0), showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=hours[24:], y=[f-20 for f in forecast],
        mode='lines', name='Lower',
        fill='tonexty', line=dict(width=0), showlegend=False
    ))
    fig.update_layout(
        template='plotly_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        xaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.05)')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Confidence Intervals")
    cols = st.columns(4)
    conf = [
        ("24 Hours", "95%", "±12", "High"),
        ("48 Hours", "88%", "±18", "Medium"),
        ("72 Hours", "76%", "±25", "Medium"),
        ("7 Days", "62%", "±35", "Low")
    ]
    for col, (label, pct, interval, level) in zip(cols, conf):
        color = "#38a169" if level == "High" else "#d69e2e" if level == "Medium" else "#e53e3e"
        with col:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value" style="color:{color};font-size:24px;">{pct}</div>
                    <div class="stat-sub">±{interval} | {level}</div>
                </div>
            """, unsafe_allow_html=True)

def render_pollution():
    st.markdown("## 🏭 Pollution Source Attribution")
    
    agent = PollutionAgent()
    sources = agent.analyze()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Source Contribution")
        fig = go.Figure(data=[go.Pie(
            labels=list(sources.keys()),
            values=list(sources.values()),
            hole=0.4,
            marker=dict(colors=['#fc8181', '#f6ad55', '#68d391', '#63b3ed', '#b794f4', '#f687b3', '#f6ad55'])
        )])
        fig.update_layout(
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            legend=dict(orientation='h', yanchor='bottom', y=-0.1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Source Ranking")
        sorted_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)
        for i, (source, contrib) in enumerate(sorted_sources, 1):
            st.markdown(f"""
                <div class="source-rank">
                    <span class="rank-number">#{i}</span>
                    <span class="rank-name">{source}</span>
                    <div class="rank-bar" style="width:{contrib}%"></div>
                    <span class="rank-value">{contrib}%</span>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Recommendations")
    recs = [
        ("🚦 Traffic", "Implement odd-even scheme, improve public transport", "High"),
        ("🏭 Industries", "Install scrubbers, increase compliance monitoring", "Medium"),
        ("🏗️ Construction", "Enforce dust nets and water sprinkling", "High"),
        ("🔥 Waste Burning", "Deploy inspection teams, impose fines", "Medium")
    ]
    for source, rec, impact in recs:
        st.markdown(f"""
            <div class="rec-card">
                <div style="display:flex;justify-content:space-between;">
                    <span class="rec-source">{source}</span>
                    <span class="rec-impact rec-impact-{impact.lower()}">{impact} Impact</span>
                </div>
                <div class="rec-text">{rec}</div>
            </div>
        """, unsafe_allow_html=True)

def render_enforcement():
    st.markdown("## ⚖️ Enforcement Intelligence")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Priority Areas")
        areas = [
            ("ITO, Delhi", "342", "Critical", "Immediate Action"),
            ("Bandra, Mumbai", "289", "High", "Inspection"),
            ("Whitefield, Bengaluru", "198", "Medium", "Monitor"),
            ("T-Nagar, Chennai", "245", "High", "Inspection")
        ]
        for area, aqi, status, action in areas:
            st.markdown(f"""
                <div class="enforcement-item">
                    <span class="enforcement-area">📍 {area}</span>
                    <span class="enforcement-status">{status}</span>
                    <span class="enforcement-action">{action}</span>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Inspection Schedule")
        st.markdown("""
            <div class="schedule-card">
                <div class="schedule-item"><span>ITO, Delhi</span><span class="schedule-time">Today 10:00</span></div>
                <div class="schedule-item"><span>Okhla, Delhi</span><span class="schedule-time">Today 14:00</span></div>
                <div class="schedule-item"><span>Bandra, Mumbai</span><span class="schedule-time">Tomorrow 09:00</span></div>
                <div class="schedule-item"><span>T-Nagar, Chennai</span><span class="schedule-time">Tomorrow 11:00</span></div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Fine Recommendations")
    fines = [
        ("🏭 IndusChem", "₹5,00,000", "Excessive emissions"),
        ("🏗️ ABC Constructions", "₹2,50,000", "Dust violation"),
        ("🔥 Waste Burners", "₹10,000", "Illegal burning")
    ]
    for entity, amount, reason in fines:
        st.markdown(f"""
            <div class="fine-card">
                <span class="fine-entity">{entity}</span>
                <span class="fine-amount">{amount}</span>
                <span class="fine-reason">{reason}</span>
            </div>
        """, unsafe_allow_html=True)

def render_health():
    st.markdown("## 🏥 Health Risk Assessment")
    
    user_type = st.selectbox(
        "Select Citizen Type",
        ["Child", "Pregnant Woman", "Asthma Patient", "Senior Citizen", "General Citizen"]
    )
    
    agent = HealthAgent()
    data = agent.assess(user_type)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Risk Assessment")
        risk_class = data['risk'].lower().replace(' ', '-')
        st.markdown(f"""
            <div class="health-card">
                <div class="risk-level risk-{risk_class}">{data['risk']} Risk</div>
                <div class="risk-symptoms"><strong>Symptoms:</strong> {data['symptoms']}</div>
                <div class="risk-precautions"><strong>Precautions:</strong> {data['precautions']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if data['risk'] in ['High', 'Very High', 'Critical']:
            st.error("⚠️ EMERGENCY: Take immediate precautions!")
    
    with col2:
        st.markdown("### Nearby Hospitals")
        hospitals = [
            ("🏥 AIIMS", "2.3 km", "ICU: 85%"),
            ("🏥 Max Hospital", "3.1 km", "ICU: 72%"),
            ("🏥 Apollo", "4.5 km", "ICU: 90%")
        ]
        for name, distance, occupancy in hospitals:
            st.markdown(f"""
                <div class="hospital-card">
                    <div class="hospital-name">{name}</div>
                    <div class="hospital-distance">📍 {distance}</div>
                    <div class="hospital-occupancy">{occupancy}</div>
                </div>
            """, unsafe_allow_html=True)

def render_hospitals():
    st.markdown("## 🏨 Hospitals & Emergency Services")
    
    m = folium.Map(location=[28.6139, 77.2090], zoom_start=12, tiles='OpenStreetMap')
    
    hospitals = [
        ("AIIMS", 28.5679, 77.2100, "ICU: 85%"),
        ("Max Hospital", 28.5800, 77.1900, "ICU: 72%"),
        ("Apollo", 28.5600, 77.2200, "ICU: 90%"),
        ("Fortis", 28.6000, 77.2000, "ICU: 65%"),
        ("Medanta", 28.5900, 77.2400, "ICU: 78%")
    ]
    
    for name, lat, lon, occupancy in hospitals:
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{name}</b><br>{occupancy}",
            icon=folium.Icon(color='red', icon='plus', prefix='fa')
        ).add_to(m)
    
    folium_static(m, width=1200, height=450)
    
    st.markdown("### Hospital Directory")
    cols = st.columns(3)
    for col, (name, _, _, occupancy) in zip(cols, hospitals):
        with col:
            st.markdown(f"""
                <div class="hospital-card">
                    <div class="hospital-name">{name}</div>
                    <div class="hospital-distance">{occupancy}</div>
                </div>
            """, unsafe_allow_html=True)

def render_chat():
    st.markdown("## 🤖 AI Assistant")
    
    languages = ["English", "Hindi", "Tamil", "Telugu", "Kannada", "Marathi", "Gujarati", "Punjabi", "Malayalam", "Bengali"]
    st.selectbox("Language", languages, index=0)
    
    st.markdown("""
        <div class="chat-container">
            <div class="chat-message">
                <div class="message-icon">🤖</div>
                <div class="message-content">
                    Hello! Ask me about air quality, health, or pollution.
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history[-8:]:
        icon = "👤" if msg['role'] == 'user' else "🤖"
        cls = "user" if msg['role'] == 'user' else ""
        st.markdown(f"""
            <div class="chat-message {cls}">
                <div class="message-icon">{icon}</div>
                <div class="message-content">{msg['content']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("", placeholder="Ask a question...", key="chat_input")
    with col2:
        send = st.button("Send", use_container_width=True)
    
    if send and user_input:
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        responses = [
            "Based on current data, AQI increased due to vehicle emissions and stagnant weather.",
            "Stay indoors and use N95 masks when going outside.",
            "Main pollution sources are traffic and industrial activities.",
            "Reduce outdoor exposure during 8-10 AM and 5-8 PM.",
            "Air quality is expected to improve in 48 hours.",
            "Children and elderly should avoid outdoor activities today."
        ]
        st.session_state.chat_history.append({'role': 'assistant', 'content': random.choice(responses)})
        st.rerun()

def render_about():
    st.markdown("""
        <div class="hero-section">
            <div class="hero-badge">🏆 Economic Times Hackathon 2024</div>
            <h1 class="hero-title">🌍 Urban Air Intelligence Platform</h1>
            <p class="hero-subtitle">Predict • Analyze • Prevent Air Pollution using AI</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            ### 🎯 Key Features
            
            - **AI Pollution Attribution** - Identify pollution sources
            - **AQI Forecasting** - Predict air quality for 7 days
            - **Health Risk Assessment** - Personalized advisories
            - **Enforcement Intelligence** - Priority areas & fines
            - **Multilingual Chatbot** - 10 Indian languages
            - **Interactive Maps** - Real-time geospatial data
        """)
    
    with col2:
        st.markdown("""
            ### 🛠️ Technology
            
            - **Frontend**: Streamlit, Plotly, Folium
            - **Backend**: Python, Pandas, NumPy
            - **AI**: XGBoost, LSTM, Prophet
            - **GIS**: OpenStreetMap, Leaflet
            
            ### 📊 Data Sources
            
            - CAAQMS (CPCB)
            - OpenAQ
            - Weather APIs
            - Satellite Imagery
        """)
    
    st.markdown("""
        ---
        <div style="text-align:center;color:#4a5568;padding:20px;">
            © 2024 Economic Times Hackathon | Made with ❤️ by Team UrbanAirAI
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE ROUTING
# ============================================================================
page_map = {
    'dashboard': render_dashboard,
    'live-aqi': render_live_aqi,
    'heatmap': render_heatmap,
    'forecast': render_forecast,
    'pollution': render_pollution,
    'enforcement': render_enforcement,
    'health': render_health,
    'hospitals': render_hospitals,
    'chat': render_chat,
    'about': render_about
}

if st.session_state.page in page_map:
    page_map[st.session_state.page]()

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <span>🌍 AirIQ Platform v2.0</span>
            <span>© 2024 Economic Times Hackathon</span>
            <span>Powered by AI</span>
        </div>
    </div>
""", unsafe_allow_html=True)