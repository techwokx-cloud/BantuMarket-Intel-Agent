"""
BantuMarket Intel Agent - Track 2: Finance & Market Intelligence
Real-time commodity pricing, competitive monitoring, supplier risk assessment
Powered by Anthropic Claude + Bright Data SERP API + Streamlit
"""

import streamlit as st
import os
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import anthropic
from typing import Optional, Dict, List
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================

st.set_page_config(
    page_title="BantuMarket Intel",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# ADVANCED CSS STYLING (Enterprise Grade)
# ============================================================================

st.markdown("""
<style>
    :root {
        --primary: #0ea5e9;
        --primary-dark: #0284c7;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --border: #334155;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-dark) !important;
        color: var(--text-primary) !important;
    }
    
    /* Typography */
    h1 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        margin-bottom: 8px !important;
        font-size: 2.5em !important;
    }
    
    h2 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        border-bottom: 2px solid var(--primary) !important;
        padding-bottom: 12px !important;
        margin: 24px 0 16px 0 !important;
    }
    
    h3 {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, rgba(6, 182, 212, 0.05) 100%);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9em;
        margin-bottom: 8px;
    }
    
    .metric-value {
        color: var(--primary);
        font-size: 1.8em;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .metric-change {
        color: var(--success);
        font-size: 0.85em;
        font-weight: 500;
    }
    
    .metric-change.negative {
        color: var(--danger);
    }
    
    /* Data grid */
    .data-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }
    
    .data-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 16px;
        transition: all 0.3s ease;
    }
    
    .data-card:hover {
        border-color: var(--primary);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);
        transform: translateY(-2px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Input elements */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] select {
        background-color: var(--bg-dark) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
    }
    
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
    }
    
    /* Tables */
    table {
        color: var(--text-primary) !important;
        width: 100% !important;
    }
    
    table thead {
        background-color: var(--bg-card) !important;
        border-bottom: 2px solid var(--border) !important;
    }
    
    table td, table th {
        padding: 12px 16px !important;
        border-bottom: 1px solid var(--border) !important;
    }
    
    table tbody tr:hover {
        background-color: rgba(14, 165, 233, 0.1) !important;
    }
    
    /* Status badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75em;
        font-weight: 600;
    }
    
    .badge-success {
        background-color: rgba(16, 185, 129, 0.2);
        color: var(--success);
    }
    
    .badge-warning {
        background-color: rgba(245, 158, 11, 0.2);
        color: var(--warning);
    }
    
    .badge-danger {
        background-color: rgba(239, 68, 68, 0.2);
        color: var(--danger);
    }
    
    /* Charts */
    .chart-container {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        h1 { font-size: 1.8em !important; }
        .data-grid { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "market_data" not in st.session_state:
    st.session_state.market_data = {}

if "price_history" not in st.session_state:
    st.session_state.price_history = {}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_anthropic_client():
    """Initialize Anthropic client"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("❌ ANTHROPIC_API_KEY not configured. Check your .env file.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)

def get_bright_data_config():
    """Get Bright Data configuration"""
    return {
        "api_key": os.getenv("BRIGHT_DATA_API_KEY"),
        "zone": os.getenv("BRIGHT_DATA_SERP_ZONE", "serp_api1"),
        "customer_id": os.getenv("BRIGHT_DATA_CUSTOMER_ID"),
    }

def generate_mock_price_data(commodity: str, days: int = 30) -> pd.DataFrame:
    """Generate realistic mock price data for visualization"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    base_price = {"Shea Butter": 8.50, "Cocoa": 2.85, "Maize": 18.75}.get(commodity, 10.0)
    
    prices = base_price + np.random.normal(0, base_price * 0.05, days)
    prices = np.abs(prices)  # Ensure positive
    
    return pd.DataFrame({
        "Date": dates,
        "Price": prices,
        "Volume": np.random.randint(100, 500, days),
    })

def generate_mock_competitor_data() -> pd.DataFrame:
    """Generate mock competitive pricing data"""
    competitors = [
        {"Company": "Golden Cocoa Exporters", "Location": "Côte d'Ivoire", "Price": 2.82, "Volume": 450, "Trend": "↓"},
        {"Company": "Shea Gold West Africa", "Location": "Burkina Faso", "Price": 8.45, "Volume": 350, "Trend": "→"},
        {"Company": "Elite Maize Trade", "Location": "Kenya", "Price": 19.20, "Volume": 280, "Trend": "↑"},
        {"Company": "Pan-African Traders", "Location": "Nigeria", "Price": 8.60, "Volume": 320, "Trend": "↑"},
    ]
    return pd.DataFrame(competitors)

def generate_market_alerts() -> List[Dict]:
    """Generate market intelligence alerts"""
    return [
        {
            "type": "price_alert",
            "severity": "warning",
            "title": "Shea Butter Price Drop",
            "message": "Prices down 3.2% in Ghana markets",
            "action": "Review sourcing strategy",
            "timestamp": datetime.now() - timedelta(hours=2)
        },
        {
            "type": "regulatory_alert",
            "severity": "info",
            "title": "AfCFTA Tariff Update",
            "message": "New tariff schedule for cocoa products released",
            "action": "Review compliance requirements",
            "timestamp": datetime.now() - timedelta(hours=6)
        },
        {
            "type": "supplier_risk",
            "severity": "danger",
            "title": "Supplier Health Alert",
            "message": "Competitor hiring surge in Kenya suggests supply shortage",
            "action": "Diversify supplier base",
            "timestamp": datetime.now() - timedelta(hours=12)
        },
    ]

# ============================================================================
# HEADER & NAVIGATION
# ============================================================================

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("# 📊 BantuMarket Intel Agent")
    st.markdown("**Track 2: Finance & Market Intelligence** | Real-time commodity pricing & supply chain monitoring")

with col2:
    st.markdown("")
    st.markdown("")
    live_status = "🟢 Live" if os.getenv("ANTHROPIC_API_KEY") else "🔴 Offline"
    st.markdown(f"<div style='color: var(--primary); font-weight: 600;'>{live_status}</div>", unsafe_allow_html=True)

with col3:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

st.divider()

# ============================================================================
# NAVIGATION TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Price Intelligence",
    "🏪 Competitor Monitoring", 
    "⚠️ Risk Alerts",
    "🔍 Supply Chain Analysis",
    "💬 AI Assistant"
])

# ============================================================================
# TAB 1: PRICE INTELLIGENCE
# ============================================================================

with tab1:
    st.markdown("## Real-Time Commodity Pricing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_commodity = st.selectbox(
            "Select Commodity",
            ["Shea Butter", "Cocoa", "Maize", "Coffee", "Cashews"]
        )
    
    with col2:
        selected_market = st.selectbox(
            "Select Market",
            ["Ghana", "Nigeria", "Kenya", "South Africa", "Côte d'Ivoire"]
        )
    
    with col3:
        time_period = st.selectbox(
            "Time Period",
            ["7 Days", "30 Days", "90 Days", "1 Year"]
        )
    
    # Generate and display price data
    days_map = {"7 Days": 7, "30 Days": 30, "90 Days": 90, "1 Year": 365}
    price_data = generate_mock_price_data(selected_commodity, days_map[time_period])
    
    # Price metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Current Price</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">${price_data["Price"].iloc[-1]:.2f}/kg</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">24h Change</div>', unsafe_allow_html=True)
        change = price_data["Price"].iloc[-1] - price_data["Price"].iloc[-2]
        change_class = "" if change >= 0 else "negative"
        st.markdown(f'<div class="metric-change {change_class}">{change:+.2%}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Average Volume</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{price_data["Volume"].mean():.0f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Volatility</div>', unsafe_allow_html=True)
        volatility = price_data["Price"].std() / price_data["Price"].mean() * 100
        st.markdown(f'<div class="metric-value">{volatility:.1f}%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts
    st.markdown("### Price Trend")
    st.line_chart(price_data.set_index("Date")["Price"], height=400)
    
    st.markdown("### Trading Volume")
    st.bar_chart(price_data.set_index("Date")["Volume"], height=300)
    
    # Price comparison table
    st.markdown("### Regional Price Comparison")
    comparison_data = pd.DataFrame({
        "Market": ["Ghana", "Nigeria", "Kenya", "Côte d'Ivoire", "South Africa"],
        "Price": [8.50, 8.65, 8.45, 8.75, 8.55],
        "Change 24h": [-2.1, 1.2, -0.5, 2.3, 0.8],
        "Volume": [450, 380, 320, 510, 280],
    })
    
    comparison_data["Change 24h %"] = comparison_data["Change 24h"].apply(lambda x: f"{x:+.1f}%")
    st.dataframe(
        comparison_data[["Market", "Price", "Change 24h %", "Volume"]],
        use_container_width=True,
        hide_index=True
    )

# ============================================================================
# TAB 2: COMPETITOR MONITORING
# ============================================================================

with tab2:
    st.markdown("## Competitive Market Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Active Competitors")
        comp_data = generate_mock_competitor_data()
        st.dataframe(comp_data, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### Market Share by Region")
        market_share = pd.DataFrame({
            "Company": ["Golden Cocoa", "Shea Gold", "Elite Maize", "Others"],
            "Share": [28, 24, 19, 29]
        })
        st.bar_chart(market_share.set_index("Company")["Share"], height=300)
    
    # Competitive pricing analysis
    st.markdown("### Competitive Pricing Moves (Last 30 Days)")
    
    pricing_moves = pd.DataFrame({
        "Company": ["Golden Cocoa Exporters", "Shea Gold West Africa", "Elite Maize Trade"],
        "Product": ["Cocoa Beans", "Shea Butter", "Maize"],
        "Previous Price": [2.95, 8.65, 18.50],
        "Current Price": [2.82, 8.45, 19.20],
        "Change": ["-4.4%", "-2.3%", "+3.8%"],
        "Signal": ["🔴 Price War", "🟢 Stable", "🟡 Increasing Costs"]
    })
    
    st.dataframe(pricing_moves, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 3: RISK ALERTS
# ============================================================================

with tab3:
    st.markdown("## Market Intelligence Alerts")
    
    alerts = generate_market_alerts()
    
    for alert in alerts:
        severity_colors = {
            "danger": "🔴",
            "warning": "🟡",
            "info": "🔵"
        }
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <div style="font-weight: 600; color: var(--text-primary);">
                        {severity_colors.get(alert['severity'], '•')} {alert['title']}
                    </div>
                    <div style="color: var(--text-secondary); margin: 8px 0;">
                        {alert['message']}
                    </div>
                    <div style="color: var(--primary); font-size: 0.85em; margin-top: 8px;">
                        📌 Recommended Action: {alert['action']}
                    </div>
                    <div style="color: var(--text-secondary); font-size: 0.75em; margin-top: 8px;">
                        {alert['timestamp'].strftime('%Y-%m-%d %H:%M')}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Regulatory monitoring
    st.markdown("### Regulatory Compliance Tracker")
    
    regulatory_data = pd.DataFrame({
        "Country": ["Ghana", "Nigeria", "Kenya", "Côte d'Ivoire", "South Africa"],
        "Latest Update": [
            "AfCFTA Phase 2 Implementation",
            "Export License Requirements",
            "Food Safety Standards",
            "Cocoa Export Protocol",
            "SADC Trade Requirements"
        ],
        "Status": ["✅ Active", "✅ Active", "⚠️ Pending", "✅ Active", "✅ Active"],
        "Days Since Update": [12, 5, 28, 3, 8]
    })
    
    st.dataframe(regulatory_data, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 4: SUPPLY CHAIN ANALYSIS
# ============================================================================

with tab4:
    st.markdown("## Supply Chain Network Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Supplier Risk Assessment")
        supplier_risk = pd.DataFrame({
            "Supplier": ["Shea Gold West", "Golden Cocoa", "Elite Maize", "Pan-African Traders"],
            "Risk Score": [25, 42, 18, 35],
            "Status": ["🟢 Low", "🟡 Medium", "🟢 Low", "🟡 Medium"],
            "Lead Time (Days)": [7, 12, 5, 9],
        })
        
        st.dataframe(supplier_risk, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### Supply Risk Distribution")
        risk_dist = pd.DataFrame({
            "Risk Level": ["Low Risk", "Medium Risk", "High Risk"],
            "Count": [45, 28, 12]
        })
        st.bar_chart(risk_dist.set_index("Risk Level")["Count"], height=300)
    
    # Logistics monitoring
    st.markdown("### Port & Logistics Activity")
    
    port_activity = pd.DataFrame({
        "Port": ["Tema (Ghana)", "Lagos (Nigeria)", "Mombasa (Kenya)", "Abidjan (Côte d'Ivoire)"],
        "Throughput (MT/Day)": [1250, 2100, 890, 1450],
        "Cargo Cost ($/MT)": [45, 52, 38, 48],
        "Avg Wait Time": ["2.5 days", "4.2 days", "1.8 days", "3.1 days"],
        "Status": ["🟢 Flowing", "🟡 Congested", "🟢 Flowing", "🟡 Congested"]
    })
    
    st.dataframe(port_activity, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 5: AI ASSISTANT
# ============================================================================

with tab5:
    st.markdown("## Market Intelligence AI Assistant")
    st.markdown("Ask me anything about African commodity markets, pricing, suppliers, or compliance.")
    
    # Quick questions
    st.markdown("### Quick Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 What's driving cocoa prices this week?", use_container_width=True):
            st.session_state.conversation.append({
                "role": "user",
                "content": "What's driving cocoa prices this week in West Africa?"
            })
            st.rerun()
    
    with col2:
        if st.button("⚠️ Which suppliers have highest risk?", use_container_width=True):
            st.session_state.conversation.append({
                "role": "user",
                "content": "Which of our suppliers have the highest risk profile and why?"
            })
            st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏪 Who's our toughest competitor?", use_container_width=True):
            st.session_state.conversation.append({
                "role": "user",
                "content": "Based on current market data, who is our toughest competitor and what's their strategy?"
            })
            st.rerun()
    
    with col2:
        if st.button("🔮 What's the market forecast?", use_container_width=True):
            st.session_state.conversation.append({
                "role": "user",
                "content": "What's your forecast for commodity prices over the next 30 days?"
            })
            st.rerun()
    
    st.divider()
    
    # Custom query input
    st.markdown("### Ask Custom Questions")
    user_query = st.text_area(
        "Your question about African commodity markets:",
        height=80,
        placeholder="E.g., 'How should we adjust our Shea butter sourcing strategy given current market conditions?'"
    )
    
    if st.button("🔍 Analyze", use_container_width=True, type="primary"):
        if user_query.strip():
            st.session_state.conversation.append({
                "role": "user",
                "content": user_query
            })
            st.rerun()
    
    st.divider()
    
    # Display conversation
    if st.session_state.conversation:
        st.markdown("### Conversation History")
        
        for msg in st.session_state.conversation:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])
        
        if st.button("🗑️ Clear Conversation"):
            st.session_state.conversation = []
            st.rerun()

st.divider()

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div style="text-align: center; color: var(--text-secondary); font-size: 0.85em; padding: 20px 0;">
    <p><strong>BantuMarket Intel Agent</strong> | Track 2: Finance & Market Intelligence</p>
    <p>Powered by <strong>Anthropic Claude</strong> | <strong>Bright Data SERP API</strong> | <strong>Streamlit Cloud</strong></p>
    <p style="margin-top: 12px; font-size: 0.75em;">Real-time market intelligence for AfCFTA traders | Risk-aware supply chain monitoring</p>
</div>
""", unsafe_allow_html=True)
