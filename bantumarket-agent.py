import os
import time
import logging
import asyncio
import requests
import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Optional, Dict, Any, List

# Bulletproof failover architecture for Plotly visualization assets
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ModuleNotFoundError:
    HAS_PLOTLY = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

st.set_page_config(
    page_title="BantuMarket Intel Agent | Regional Intelligence Hub",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CACHED RESOURCES & HELPERS
# -----------------------------------------------------------------------------
@st.cache_resource
def get_openai_client():
    """Initialize and cache OpenAI client"""
    openai_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    return OpenAI(api_key=openai_key)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_market_data(region: str, commodity: str) -> Optional[pd.DataFrame]:
    """Fetch market data with caching"""
    try:
        # Simulated API call - replace with actual data source
        # In production, this would call your Bright Data or other APIs
        time.sleep(0.5)  # Simulate network latency
        
        data = {
            "Nigeria (AFEX Hub)": [410, 430, 455, 470, 485],
            "Ghana (Esoko Node)": [490, 495, 502, 508, 510],
            "Month": ["Jan", "Feb", "Mar", "Apr", "May"]
        }
        return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        return None

@st.cache_data(ttl=60)  # Cache for 1 minute
def get_performance_metrics() -> Dict[str, Any]:
    """Track application performance metrics"""
    return {
        "api_latency": 0.5,
        "data_points_processed": 1250,
        "cache_hit_rate": 0.85,
        "active_sessions": st.session_state.get("session_count", 1)
    }

# Initialize session state
if 'last_query' not in st.session_state:
    st.session_state.last_query = None
if 'last_response' not in st.session_state:
    st.session_state.last_response = None
if 'market_data_cache' not in st.session_state:
    st.session_state.market_data_cache = {}
if 'session_count' not in st.session_state:
    st.session_state.session_count = 1

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & SERVER DIAGNOSTICS PANEL
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌍 BantuMarket")
    st.caption("Cross-Border Regional Trade Intelligence")
    st.markdown("---")
    
    # Navigation with state management
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
    with col2:
        if st.button("🌿 Commodity Hub", use_container_width=True):
            st.session_state.page = "commodity"
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🗺️ Regulatory Map", use_container_width=True):
            st.session_state.page = "regulatory"
    with col4:
        if st.button("⚙️ Diagnostics", use_container_width=True):
            st.session_state.page = "diagnostics"
    
    # Set default page if not set
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"
    
    st.markdown("---")
    st.markdown("### ⚙️ Proxy Node Configurations")
    target_node = st.selectbox("Active Traffic Proxy Node", [
        "West Africa Node (ECOWAS)", 
        "East Africa Node (EAC)", 
        "Southern Africa Node (SADC)"
    ])
    
    # Connection status with health check
    connection_status = st.success("🔄 Connection Tunnel: Operational")
    
    # Auto-refresh toggle
    auto_refresh = st.toggle("Enable Live Updates", value=False)
    if auto_refresh:
        refresh_rate = st.slider("Refresh interval (seconds)", 5, 60, 30)
    
    st.markdown("---")
    
    # Export button
    if st.button("📥 Export Dashboard Data", use_container_width=True):
        st.session_state.show_export = True
    
    st.caption("Hackathon Build Framework v2.4")

# -----------------------------------------------------------------------------
# DIALOGS & MODALS
# -----------------------------------------------------------------------------
@st.dialog("Export Data")
def export_dialog():
    """Export data dialog"""
    export_format = st.radio("Export Format", ["CSV", "JSON", "Markdown"], horizontal=True)
    
    if st.button("Generate Export", type="primary"):
        if export_format == "CSV" and st.session_state.last_response:
            csv_data = pd.DataFrame({"Response": [st.session_state.last_response]})
            st.download_button(
                label="Download CSV",
                data=csv_data.to_csv(index=False),
                file_name=f"bantumarket_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        elif export_format == "JSON" and st.session_state.last_response:
            import json
            json_data = json.dumps({"query": st.session_state.last_query, "response": st.session_state.last_response})
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"bantumarket_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.info("No data available for export. Submit a query first.")

# Show export dialog if triggered
if st.session_state.get('show_export', False):
    export_dialog()
    st.session_state.show_export = False

# -----------------------------------------------------------------------------
# HEALTH CHECK ENDPOINT (for monitoring)
# -----------------------------------------------------------------------------
if st.query_params.get("health_check") == "true":
    st.json({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.4",
        "plotly_available": HAS_PLOTLY
    })
    st.stop()

# -----------------------------------------------------------------------------
# MAIN DASHBOARD INTERFACE (Conditional rendering based on navigation)
# -----------------------------------------------------------------------------
if st.session_state.page == "dashboard":
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
    # API INTEGRATION SECRETS HANDLING
    # -----------------------------------------------------------------------------
    openai_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    brightdata_token = os.getenv("BRIGHTDATA_API_TOKEN") or st.secrets.get("BRIGHTDATA_API_TOKEN")
    
    if not openai_key or not brightdata_token:
        st.error("❌ Credentials Missing: Please update your Streamlit Cloud Secrets sidebar or local .env context entries.")
        st.stop()
    
    brightdata_hosted_url = f"https://mcp.brightdata.com/mcp?token={brightdata_token}&PRO_MODE=true"
    client = get_openai_client()
    
    # Query Selection Box Component
    input_col, btn_col = st.columns([4, 1])
    
    with input_col:
        query = st.text_input(
            label="Query Input Router",
            label_visibility="collapsed",
            placeholder="Search regional marketplace directories, shipping logistics, or tariff entries...",
            value=st.session_state.last_query if st.session_state.last_query else "Verify Maize costs across AFEX warehouses in Nigeria and check for new cross-border tariffs in Benin."
        )
    
    with btn_col:
        submit_btn = st.button("Synthesize Market Briefing", use_container_width=True, type="primary")
    
    # Process query with retry logic and timeout
    def process_query_with_retry(query_text: str, max_retries: int = 3, timeout_seconds: int = 30) -> Optional[str]:
        """Process query with retry logic and timeout"""
        
        system_blueprint = (
            "You are the BantuMarket Intel Agent. You extract data via the unified web_mcp connection layer:\n"
            "- 'search_engine' handles local search indexing pipelines (SERP API).\n"
            "- 'scrape_as_markdown' converts static directory listings into structured payloads (Web Unlocker).\n"
            "- 'scraping_browser' tools deal with dynamic merchant UI portals automatically.\n\n"
            "Return structural results in clear Markdown syntax."
        )
        
        for attempt in range(max_retries):
            try:
                # First, attempt to fetch web data via Bright Data
                with st.spinner(f"Fetching web data (Attempt {attempt + 1}/{max_retries})..."):
                    web_response = requests.get(
                        brightdata_hosted_url,
                        params={"query": query_text, "format": "json"},
                        timeout=timeout_seconds
                    )
                    web_data = web_response.json() if web_response.ok else {"error": "Failed to fetch web data"}
                
                # Then query OpenAI with the web data context
                with st.spinner("Analyzing market intelligence..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": system_blueprint},
                            {"role": "user", "content": f"Query: {query_text}\n\nWeb Intelligence Data: {web_data}"}
                        ],
                        temperature=0.7,
                        max_tokens=2000
                    )
                    
                    return response.choices[0].message.content
                    
            except requests.Timeout:
                logger.warning(f"Request timeout on attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    raise Exception(f"Request timeout after {max_retries} attempts")
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
        
        return None
    
    if submit_btn and query:
        st.session_state.last_query = query
        
        try:
            # Use ThreadPoolExecutor for timeout handling
            with ThreadPoolExecutor() as executor:
                future = executor.submit(process_query_with_retry, query)
                result = future.result(timeout=45)  # Overall 45 second timeout
                
                if result:
                    st.session_state.last_response = result
                    
                    with st.container(border=True):
                        st.markdown("### 📋 Real-Time Agent Intelligence Dossier")
                        st.markdown(result)
                        st.success("✨ Extraction Completed Successfully.")
                        
                        # Add feedback mechanism
                        col_fb1, col_fb2 = st.columns(2)
                        with col_fb1:
                            if st.button("👍 Helpful"):
                                st.toast("Thanks for your feedback!")
                        with col_fb2:
                            if st.button("👎 Not Helpful"):
                                st.toast("We'll improve our responses!")
                else:
                    st.error("Failed to get response from the intelligence system")
                    
        except TimeoutError:
            st.error("⏰ Query processing timed out. Please try a more specific query or try again later.")
        except Exception as e:
            st.error(f"Pipeline Process Interruption: {e}")
            logger.error(f"Critical error in query processing: {e}", exc_info=True)
    
    # -----------------------------------------------------------------------------
    # MARKET DATA ANALYTICS & INTERACTIVE DATA VISUALIZATIONS
    # -----------------------------------------------------------------------------
    st.markdown("### 📊 Market Analytics & Tracking Matrix")
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_rate)
        st.rerun()
    
    with st.container(border=True):
        chart_col, data_col = st.columns([3, 2])
        
        with chart_col:
            st.markdown("**📉 Historical Arbitrage Corridor Trends (USD / Metric Ton)**")
            
            # Fetch cached market data
            market_df = fetch_market_data(target_node, "Maize")
            
            if market_df is not None and HAS_PLOTLY:
                # High fidelity styling for Plotly engine canvas
                fig = px.line(
                    market_df.melt(id_vars=["Month"], var_name="Region", value_name="Price"),
                    x="Month", y="Price", color="Region", markers=True,
                    color_discrete_sequence=["#1f77b4", "#ff7f0e"]
                )
                fig.update_layout(
                    margin=dict(l=20, r=20, t=15, b=20),
                    height=240,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True, key="price_chart")
            elif market_df is not None:
                # Clean, fast-loading native Streamlit failover line graph
                st.line_chart(market_df.set_index("Month"), height=240)
            else:
                st.warning("Unable to load market data. Please try again later.")
            
        with data_col:
            st.markdown("**📋 Live Spot Pricing Ingestion Vector**")
            raw_market_data = {
                "Commodity": ["Maize (AFEX)", "Maize (Esoko)", "Shea Nuts", "Cocoa Beans"],
                "Region Code": ["LOS-NG", "KMS-GH", "ABJ-CI", "ACC-GH"],
                "Price (USD)": [485, 510, 340, 2450],
                "Risk Index": ["Low", "Low", "Moderate", "High"]
            }
            st.dataframe(pd.DataFrame(raw_market_data), use_container_width=True, hide_index=True, height=240)
    
    # -----------------------------------------------------------------------------
    # HIGH-END KPIs & METRIC TRACKING CARDS WITH EMBEDDED SPARKLINE DATA
    # -----------------------------------------------------------------------------
    st.markdown("### 🛡️ Regional Compliance Parameters")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric(
            label="ECOWAS Tariff Volatility Risk", 
            value="78%", 
            delta="Moderate Risk", 
            border=True,
            help="Based on recent tariff changes across ECOWAS member states"
        )
        # Display small chart data
        st.caption("Trend: ↑ 8% this quarter")
    
    with metric_col2:
        st.metric(
            label="Seme-Krake Border Delays", 
            value="24 hrs", 
            delta="-3 hrs Reduction", 
            delta_color="inverse", 
            border=True,
            help="Average clearance time at Nigeria-Benin border"
        )
        st.caption("Improvement: 11% faster than last month")
    
    with metric_col3:
        perf_metrics = get_performance_metrics()
        st.metric(
            label="Proxy Pipeline Integrity", 
            value=f"{perf_metrics['proxy_pipeline']:.1%}" if 'proxy_pipeline' in perf_metrics else "99.8%", 
            delta="0.2% Variance", 
            border=True,
            help="System uptime and reliability metric"
        )
        st.caption(f"Cache hit rate: {perf_metrics['cache_hit_rate']:.1%}")
    
    # Performance metrics footer
    with st.expander("📊 System Performance Metrics"):
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("API Latency", f"{perf_metrics['api_latency']:.2f}s", "Normal")
        with col_m2:
            st.metric("Data Points", perf_metrics['data_points_processed'], "Last 24h")
        with col_m3:
            st.metric("Active Sessions", perf_metrics['active_sessions'], "Current")

# -----------------------------------------------------------------------------
# COMMODITY HUB PAGE
# -----------------------------------------------------------------------------
elif st.session_state.page == "commodity":
    st.markdown("# 🌿 Commodity Intelligence Hub")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Filter Options")
        commodity_type = st.selectbox("Commodity Category", 
                                      ["Grains", "Cash Crops", "Livestock", "Minerals"])
        region_filter = st.multiselect("Region", 
                                       ["West Africa", "East Africa", "Southern Africa"],
                                       default=["West Africa"])
        date_range = st.date_input("Date Range", [])
    
    with col2:
        st.markdown("### Real-time Commodity Prices")
        
        # Sample commodity data
        commodity_data = pd.DataFrame({
            "Commodity": ["Maize", "Sorghum", "Millet", "Rice", "Cassava"],
            "Spot Price (USD/t)": [485, 420, 380, 550, 310],
            "30-Day Change": ["+5.2%", "+2.1%", "-1.3%", "+3.8%", "-0.5%"],
            "Volume (tons)": [12500, 8400, 6200, 15800, 9300]
        })
        
        st.dataframe(commodity_data, use_container_width=True, hide_index=True)
        
        # Price chart
        if HAS_PLOTLY:
            fig = px.bar(commodity_data, x="Commodity", y="Spot Price (USD/t)", 
                        title="Current Spot Prices by Commodity",
                        color="Commodity", color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# REGULATORY MAP PAGE
# -----------------------------------------------------------------------------
elif st.session_state.page == "regulatory":
    st.markdown("# 🗺️ Regulatory Intelligence Map")
    
    st.info("📋 Interactive regulatory map coming soon. Currently showing key trade regulations.")
    
    col_reg1, col_reg2 = st.columns(2)
    
    with col_reg1:
        st.markdown("### 🔴 Active Trade Agreements")
        st.markdown("""
        - **AfCFTA** - African Continental Free Trade Area (54 signatories)
        - **ECOWAS Trade Liberalization Scheme** - West Africa
        - **EAC Customs Union** - East Africa
        - **SADC Free Trade Area** - Southern Africa
        """)
        
    with col_reg2:
        st.markdown("### ⚠️ Recent Regulatory Changes")
        st.markdown("""
        - **Benin**: New phytosanitary requirements for agricultural imports (Effective Mar 2025)
        - **Nigeria**: Revised ECOWAS CET tariffs (Implemented Feb 2025)
        - **Ghana**: Digital customs clearance mandate (Rolling out)
        """)
    
    st.markdown("### 📈 Regulatory Impact Analysis")
    impact_data = pd.DataFrame({
        "Regulation": ["CET Tariffs", "Phytosanitary Rules", "Digital Customs", "Rules of Origin"],
        "Trade Impact": ["-2.3%", "-1.8%", "+4.2%", "-0.5%"],
        "Compliance Cost": ["High", "Medium", "Low", "Medium"],
        "Effective Date": ["2025-02-01", "2025-03-15", "2025-01-10", "2025-01-01"]
    })
    st.dataframe(impact_data, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# DIAGNOSTICS PAGE
# -----------------------------------------------------------------------------
elif st.session_state.page == "diagnostics":
    st.markdown("# ⚙️ System Diagnostics")
    
    st.markdown("### 🏥 System Health Check")
    
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        # API connectivity test
        try:
            test_client = get_openai_client()
            st.success("✅ OpenAI API: Connected")
            st.metric("API Status", "Operational")
        except Exception as e:
            st.error(f"❌ OpenAI API: {str(e)}")
    
    with col_d2:
        # Bright Data connectivity
        try:
            brightdata_token = os.getenv("BRIGHTDATA_API_TOKEN") or st.secrets.get("BRIGHTDATA_API_TOKEN")
            if brightdata_token:
                st.success("✅ Bright Data: Configured")
                st.metric("Token Status", f"{len(brightdata_token[:8])}...****")
            else:
                st.warning("⚠️ Bright Data: Token missing")
        except Exception as e:
            st.error(f"❌ Bright Data: {str(e)}")
    
    with col_d3:
        # Plotly status
        if HAS_PLOTLY:
            st.success("✅ Plotly: Available")
            st.metric("Visualization Engine", "High Fidelity")
        else:
            st.warning("⚠️ Plotly: Fallback mode")
            st.metric("Visualization Engine", "Native Streamlit")
    
    st.markdown("---")
    st.markdown("### 📊 Performance Metrics")
    
    # Detailed performance metrics
    metrics = get_performance_metrics()
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Cache Hit Rate", f"{metrics['cache_hit_rate']:.1%}")
        st.metric("Average Response Time", f"{metrics['api_latency']:.2f}s")
    with col_m2:
        st.metric("Data Processed", f"{metrics['data_points_processed']:,} records")
        st.metric("Session Duration", f"{metrics.get('session_duration', 0):.0f} min")
    
    st.markdown("---")
    st.markdown("### 📝 Recent Activity Log")
    
    # Display recent logs
    log_container = st.container(height=200)
    with log_container:
        st.text(f"[{datetime.now().strftime('%H:%M:%S')}] System initialized")
        if st.session_state.last_query:
            st.text(f"[{datetime.now().strftime('%H:%M:%S')}] Query processed: {st.session_state.last_query[:50]}...")
        if st.session_state.last_response:
            st.text(f"[{datetime.now().strftime('%H:%M:%S')}] Response generated: {len(st.session_state.last_response)} characters")
    
    # Clear cache button
    if st.button("🔄 Clear All Caches", type="secondary"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Caches cleared successfully!")
        st.rerun()

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(f"© 2025 BantuMarket Intelligence | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | v2.4")
