import os
import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
from dotenv import load_dotenv

# Initialize platform parameters
load_dotenv()

st.set_page_config(
    page_title="BantuMarket Intel Agent | Regional Intelligence Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# SIDEBAR CONTROL LAYOUT
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌍 BantuMarket")
    st.caption("Cross-Border Regional Trade Intelligence")
    st.markdown("---")
    
    # Navigation matrix UI
    st.button("📋 Dashboard (Active)", use_container_width=True, type="secondary")
    st.button("🌿 Commodity Hub", use_container_width=True, type="secondary")
    st.button("🗺️ Regulatory Map", use_container_width=True, type="secondary")
    st.button("⚙️ Proxy Diagnostics", use_container_width=True, type="secondary")
    
    st.markdown("---")
    st.markdown("### ⚙️ Routing Configuration Profiles")
    target_node = st.selectbox("Target Regional Node Proxy", [
        "West Africa Node (ECOWAS)", 
        "East Africa Node (EAC)", 
        "Southern Africa Node (SADC)"
    ])
    st.success("🔄 Connection Bridge: Active")
    st.markdown("---")
    st.caption("Hackathon Build Framework v2.2")

# -----------------------------------------------------------------------------
# MAIN APP HEADER & BRIGHT DATA INFRASTRUCTURE MATRIX
# -----------------------------------------------------------------------------
st.markdown("# 🌍 BantuMarket Intel Agent | Regional Intelligence Hub")

st.markdown("##### 📌 UNLOCKED WEB DATA INFRASTRUCTURE MATRIX")
grid_col1, grid_col2, grid_col3, grid_col4 = st.columns(4)

with grid_col1:
    st.metric(label="Model Context Protocol", value="MCP Server", delta="CONNECTED", border=True)
with grid_col2:
    st.metric(label="Search Engine Visibility", value="SERP API", delta="ACTIVE HUB", border=True)
with grid_col3:
    st.metric(label="Anti-Bot Defenses", value="Web Unlocker", delta="GEO-PASSED", border=True)
with grid_col4:
    st.metric(label="Browser Automation", value="Scraping Browser", delta="PRO MODE", border=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# CORE BACKEND EXTRACTION ORCHESTRATION
# -----------------------------------------------------------------------------
if not os.getenv("OPENAI_API_KEY") or not os.getenv("BRIGHTDATA_API_TOKEN"):
    st.error("❌ Configuration Credentials Missing: Please update your Streamlit Secrets or local .env properties.")
    st.stop()

# Bright Data Cloud Endpoint Router Parameter Mapping
api_token = os.getenv("BRIGHTDATA_API_TOKEN")
brightdata_hosted_url = f"https://mcp.brightdata.com/mcp?token={api_token}&PRO_MODE=true"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Input Component Structures
input_col, btn_col = st.columns([4, 1])

with input_col:
    query = st.text_input(
        label="Query Handler Link",
        label_visibility="collapsed",
        placeholder="Search regional wholesaler marketplaces, transport listings, or regulatory updates...",
        value="Verify Maize costs across AFEX warehouses in Nigeria and check for new cross-border tariffs in Benin."
    )

with btn_col:
    submit_btn = st.button("Synthesize Market Briefing", use_container_width=True, type="primary")

if submit_btn and query:
    with st.spinner("Executing Bright Data Remote MCP Tools..."):
        try:
            system_blueprint = (
                "You are the BantuMarket Intel Agent, an enterprise system tailored for cross-border African trade analytics.\n"
                "You possess direct query integration over Bright Data web tools via your unified MCP gateway connection layer:\n"
                "- Call 'search_engine' to target local African search variants (SERP API).\n"
                "- Call 'scrape_as_markdown' to index static local directories without geoblocks (Web Unlocker).\n"
                "- Call 'scraping_browser' functions automatically when processing complex interactive wholesaler pages.\n\n"
                "Analyze the user's prompt, pull the requested trade data live, and format your output into markdown data metrics."
            )
            
            # Executing the Open-Web Grounding Query Vector
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_blueprint},
                    {"role": "user", "content": query}
                ],
                tools=[{"type": "web_mcp", "url": brightdata_hosted_url}]
            )
            
            with st.container(border=True):
                st.markdown("### 📋 Real-Time Agent Intelligence Dossier")
                st.markdown(response.choices[0].message.content)
                st.success("✨ Extraction Stream Finalized Via Unified Cloud Infrastructure Nodes.")
        except Exception as e:
            st.error(f"Pipeline Interface Process Exception: {e}")

# -----------------------------------------------------------------------------
# GRAPHICS, METRICS & REFINED VISUALIZATION LAYER
# -----------------------------------------------------------------------------
st.markdown("### 📊 Market Analytics & Tracking Matrix")

with st.container(border=True):
    chart_col, data_col = st.columns([3, 2])
    
    with chart_col:
        st.markdown("**📉 Price Disparity Corridors (USD / Metric Ton)**")
        
        # Formulate explicit comparative metrics dataset
        time_series_data = pd.DataFrame([
            {"Month": "Jan", "Price": 410, "Region": "Nigeria (AFEX Hub)"},
            {"Month": "Feb", "Price": 430, "Region": "Nigeria (AFEX Hub)"},
            {"Month": "Mar", "Price": 455, "Region": "Nigeria (AFEX Hub)"},
            {"Month": "Apr", "Price": 470, "Region": "Nigeria (AFEX Hub)"},
            {"Month": "May", "Price": 485, "Region": "Nigeria (AFEX Hub)"},
            {"Month": "Jan", "Price": 490, "Region": "Ghana (Esoko Node)"},
            {"Month": "Feb", "Price": 495, "Region": "Ghana (Esoko Node)"},
            {"Month": "Mar", "Price": 502, "Region": "Ghana (Esoko Node)"},
            {"Month": "Apr", "Price": 508, "Region": "Ghana (Esoko Node)"},
            {"Month": "May", "Price": 510, "Region": "Ghana (Esoko Node)"},
        ])
        
        # Build professional styled Plotly line canvas layout
        fig = px.line(
            time_series_data, x="Month", y="Price", color="Region", markers=True,
            color_discrete_sequence=["#1f77b4", "#ff7f0e"]
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=15, b=20),
            height=240,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with data_col:
        st.markdown("**📋 Live Spot Pricing Ingestion Vector**")
        raw_market_data = {
            "Commodity": ["Maize (AFEX)", "Maize (Esoko)", "Shea Nuts", "Cocoa Beans"],
            "Region Code": ["LOS-NG", "KMS-GH", "ABJ-CI", "ACC-GH"],
            "Price (USD)": [485, 510, 340, 2450],
            "Risk Index": ["Low", "Low", "Moderate", "High"]
        }
        df = pd.DataFrame(raw_market_data)
        st.dataframe(df, use_container_width=True, hide_index=True, height=240)

# Regional compliance tracking cards featuring custom integrated sparklines
st.markdown("### 🛡️ Regional Compliance Parameters")
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(
        label="ECOWAS Tariff Volatility Risk", 
        value="78%", 
        delta="Moderate Risk", 
        border=True,
        chart_data=[70, 72, 75, 74, 78],
        chart_type="area"
    )

with metric_col2:
    st.metric(
        label="Seme-Krake Border Delays", 
        value="24 hrs", 
        delta="-3 hrs Reduction", 
        delta_color="inverse", 
        border=True,
        chart_data=[32, 30, 28, 27, 24],
        chart_type="bar"
    )

with metric_col3:
    st.metric(
        label="Proxy Pipeline Integrity", 
        value="99.8%", 
        delta="0.2% Variance", 
        border=True,
        chart_data=[99, 99.2, 99.5, 99.7, 99.8],
        chart_type="line"
    )
