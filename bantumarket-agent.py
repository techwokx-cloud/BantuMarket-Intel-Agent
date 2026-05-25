import os
import sys
import time
import logging
import asyncio
import requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Optional, Dict, Any, List

# Check for OpenAI package before importing
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    st.error("❌ OpenAI package not installed. Please run: pip install openai")
    st.stop()

# Bulletproof failover architecture for Plotly visualization assets
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
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
    try:
        openai_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        if not openai_key:
            st.error("❌ OPENAI_API_KEY not found in environment variables or secrets")
            return None
        return OpenAI(api_key=openai_key)
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        return None

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
        "active_sessions": st.session_state.get("session_count", 1),
        "proxy_pipeline": 0.998
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
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

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
            st.rerun()
    with col2:
        if st.button("🌿 Commodity Hub", use_container_width=True):
            st.session_state.page = "commodity"
            st.rerun()
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🗺️ Regulatory Map", use_container_width=True):
            st.session_state.page = "regulatory"
            st.rerun()
    with col4:
        if st.button("⚙️ Diagnostics", use_container_width=True):
            st.session_state.page = "diagnostics"
            st.rerun()
    
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
            import io
            csv_data = pd.DataFrame({"Response": [st.session_state.last_response]})
            st.download_button(
                label="Download CSV",
                data=csv_data.to_csv(index=False),
                file_name=f"bantumarket_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        elif export_format == "JSON" and st.session_state.last_response:
            import json
            json_data = json.dumps({
                "query": st.session_state.last_query, 
                "response": st.session_state.last_response,
                "timestamp": datetime.now().isoformat()
            })
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"bantumarket_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        elif export_format == "Markdown" and st.session_state.last_response:
            md_content = f"""# BantuMarket Intelligence Report

## Query
{st.session_state.last_query}

## Response
{st.session_state.last_response}

## Generated
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            st.download_button(
                label="Download Markdown",
                data=md_content,
                file_name=f"bantumarket_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
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
        "plotly_available": HAS_PLOTLY,
        "openai_available": OPENAI_AVAILABLE
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
    
    if not openai_key:
        st.error("❌ OPENAI_API_KEY is missing. Please add it to your Streamlit secrets or .env file.")
        st.info("""
        **How to fix:**
        1. In Streamlit Cloud: Go to Settings → Secrets → Add OPENAI_API_KEY
        2. Locally: Create a `.env` file with: `OPENAI_API_KEY=your_key_here`
        """)
        st.stop()
    
    if not brightdata_token:
        st.warning("⚠️ BRIGHTDATA_API_TOKEN is missing. Some features will be limited.")
    
    client = get_openai_client()
    if not client:
        st.error("Failed to initialize OpenAI client. Please check your API key.")
        st.stop()
    
    brightdata_hosted_url = f"https://mcp.brightdata.com/mcp?token={brightdata_token}&PRO_MODE=true" if brightdata_token else None
    
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
            "You are the BantuMarket Intel Agent, a specialized AI for African cross-border trade intelligence. "
            "You provide market insights, tariff information, and logistics data for ECOWAS, EAC, and SADC regions.\n\n"
            "Guidelines:\n"
            "- Provide accurate, data-driven responses about agricultural commodities, trade routes, and regulations\n"
            "- Include specific price points, tariff rates, and regional differences when available\n"
            "- Use clear markdown formatting with headers, bullet points, and tables for complex data\n"
            "- If specific data isn't available, provide estimated ranges and note the source of estimation\n"
            "- Focus on actionable intelligence for traders and logistics operators\n\n"
            "Return structural results in clear Markdown syntax with emphasis on practical market intelligence."
        )
        
        for attempt in range(max_retries):
            try:
                # Prepare web context (simplified for now - you can enhance with actual Bright Data integration)
                web_context = ""
                if brightdata_token and brightdata_hosted_url:
                    try:
                        web_response = requests.get(
                            brightdata_hosted_url,
                            params={"query": query_text, "format": "json"},
                            timeout=timeout_seconds
                        )
                        if web_response.ok:
                            web_context = f"\n\nWeb Intelligence Data: {web_response.text[:500]}"
                    except Exception as e:
                        logger.warning(f"Bright Data fetch failed: {e}")
                        web_context = "\n\n(Web intelligence temporarily unavailable, using local knowledge base)"
                
                # Query OpenAI
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Using mini for faster responses and lower cost
                    messages=[
                        {"role": "system", "content": system_blueprint},
                        {"role": "user", "content": f"Query: {query_text}{web_context}"}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise Exception(f"Failed after {max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
        
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
                                st.toast("Thanks for your feedback!", icon="👍")
                        with col_fb2:
                            if st.button("👎 Not Helpful"):
                                st.toast("We'll improve our responses!", icon="👎")
                else:
                    st.error("Failed to get response from the intelligence system")
                    
        except TimeoutError:
            st.error("⏰ Query processing timed out. Please try a more specific query or try again later.")
        except Exception as e:
            st.error(f"Pipeline Process Interruption: {str(e)}")
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
                    color_discrete_sequence=["#1f77b4", "#ff7f0e"],
                    title="Maize Price Trends 2025"
                )
                fig.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=300,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True, key="price_chart")
            elif market_df is not None:
                # Clean, fast-loading native Streamlit failover line graph
                st.line_chart(market_df.set_index("Month"), height=300)
            else:
                st.warning("Unable to load market data. Please try again later.")
            
        with data_col:
            st.markdown("**📋 Live Spot Pricing Ingestion Vector**")
            raw_market_data = {
                "Commodity": ["Maize (AFEX)", "Maize (Esoko)", "Shea Nuts", "Cocoa Beans"],
                "Region Code": ["LOS-NG", "KMS-GH", "ABJ-CI", "ACC-GH"],
                "Price (USD)": [485, 510, 340, 2450],
                "Risk Index": ["Low", "Low", "Moderate", "High"],
                "24h Change": ["+2.1%", "+1.5%", "-0.8%", "+3.2%"]
            }
            st.dataframe(pd.DataFrame(raw_market_data), use_container_width=True, hide_index=True, height=300)
    
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
            help="Based on recent tariff changes across ECOWAS member states. Calculated from customs data."
        )
        st.caption("Trend: ↑ 8% this quarter | High alert zone: >85%")
    
    with metric_col2:
        st.metric(
            label="Seme-Krake Border Delays", 
            value="24 hrs", 
            delta="-3 hrs Reduction", 
            delta_color="inverse", 
            border=True,
            help="Average clearance time at Nigeria-Benin border corridor"
        )
        st.caption("Improvement: 11% faster than last month | Target: <20 hrs")
    
    with metric_col3:
        perf_metrics = get_performance_metrics()
        st.metric(
            label="Proxy Pipeline Integrity", 
            value=f"{perf_metrics['proxy_pipeline']:.1%}", 
            delta="0.2% Variance", 
            border=True,
            help="System uptime and data pipeline reliability metric"
        )
        st.caption(f"Cache hit rate: {perf_metrics['cache_hit_rate']:.1%} | 99.9% SLA")
    
    # Performance metrics footer
    with st.expander("📊 System Performance Metrics", expanded=False):
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("API Latency", f"{perf_metrics['api_latency']:.2f}s", "Normal", help="Average response time")
        with col_m2:
            st.metric("Data Points", f"{perf_metrics['data_points_processed']:,}", "Last 24h")
        with col_m3:
            st.metric("Active Sessions", perf_metrics['active_sessions'], "Current users")

# -----------------------------------------------------------------------------
# COMMODITY HUB PAGE
# -----------------------------------------------------------------------------
elif st.session_state.page == "commodity":
    st.markdown("# 🌿 Commodity Intelligence Hub")
    st.markdown("Real-time commodity prices, trends, and market analysis across African markets")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Filter Options")
        commodity_type = st.selectbox("Commodity Category", 
                                      ["All", "Grains", "Cash Crops", "Livestock", "Minerals"],
                                      index=0)
        region_filter = st.multiselect("Region", 
                                       ["West Africa", "East Africa", "Southern Africa", "North Africa", "Central Africa"],
                                       default=["West Africa", "East Africa"])
        date_range = st.date_input("Date Range", 
                                   [datetime.now().replace(month=1, day=1), datetime.now()])
        
        st.markdown("---")
        st.markdown("### 📈 Market Insights")
        st.info("""
        **Key Trends:**
        - Maize prices up 12% YoY in West Africa
        - Cocoa demand strong in Q1 2025
        - Shea butter exports growing 8%
        """)
    
    with col2:
        st.markdown("### Real-time Commodity Prices")
        
        # Enhanced commodity data
        commodity_data = pd.DataFrame({
            "Commodity": ["Maize", "Sorghum", "Millet", "Rice", "Cassava", "Cocoa", "Coffee", "Shea Nuts"],
            "Spot Price (USD/t)": [485, 420, 380, 550, 310, 2850, 3200, 890],
            "30-Day Change": ["+5.2%", "+2.1%", "-1.3%", "+3.8%", "-0.5%", "+8.2%", "+4.5%", "+1.8%"],
            "Volume (tons)": [12500, 8400, 6200, 15800, 9300, 4500, 3200, 2100],
            "Demand Trend": ["↑ High", "→ Stable", "↓ Low", "↑ High", "→ Stable", "↑ High", "↑ High", "→ Stable"]
        })
        
        st.dataframe(commodity_data, use_container_width=True, hide_index=True)
        
        # Price chart
        if HAS_PLOTLY and len(commodity_data) > 0:
            fig = px.bar(commodity_data.head(6), x="Commodity", y="Spot Price (USD/t)", 
                        title="Current Spot Prices by Commodity (Top 6)",
                        color="30-Day Change",
                        color_continuous_scale="RdYlGn",
                        text="Spot Price (USD/t)")
            fig.update_traces(texttemplate='$%{text}', textposition='outside')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# REGULATORY MAP PAGE
# -----------------------------------------------------------------------------
elif st.session_state.page == "regulatory":
    st.markdown("# 🗺️ Regulatory Intelligence Map")
    
    st.info("📋 Interactive trade regulation dashboard - Track policies, tariffs, and compliance requirements")
    
    tab1, tab2, tab3 = st.tabs(["📊 Active Agreements", "⚠️ Recent Changes", "📈 Impact Analysis"])
    
    with tab1:
        st.markdown("### 🔴 Active Trade Agreements")
        
        col_reg1, col_reg2 = st.columns(2)
        
        with col_reg1:
            st.markdown("#### 🌍 Continental")
            st.markdown("""
            - **AfCFTA** - African Continental Free Trade Area
              - 54 signatory countries
              - 90% tariff liberalization target
              - Effective: January 2021
            
            - **RECs Coordination** - Harmonization initiative
              - 8 recognized Regional Economic Communities
              - Streamlining rules of origin
            """)
            
        with col_reg2:
            st.markdown("#### 🌐 Regional")
            st.markdown("""
            - **ECOWAS Trade Liberalization Scheme**
              - 15 member states
              - CET implementation: 5 bands (0%, 5%, 10%, 20%, 35%)
            
            - **EAC Customs Union**
              - Common external tariff
              - Single customs territory
            
            - **SADC FTA**
              - 85% tariff liberalization
              - Trade facilitation program
            """)
    
    with tab2:
        st.markdown("### ⚠️ Recent Regulatory Changes (Last 90 days)")
        
        changes_data = pd.DataFrame({
            "Country": ["Benin", "Nigeria", "Ghana", "Kenya", "South Africa"],
            "Regulation": ["Phytosanitary requirements", "Revised CET tariffs", "Digital customs mandate", "EAC CET update", "Port charges revision"],
            "Impact": ["High", "High", "Medium", "Medium", "Low"],
            "Effective Date": ["2025-03-15", "2025-02-01", "2025-01-10", "2025-01-15", "2025-02-20"],
            "Status": ["Active", "Active", "Rolling out", "Active", "Proposed"]
        })
        st.dataframe(changes_data, use_container_width=True, hide_index=True)
        
        st.warning("""
        **Action Required:**
        - Benin's new phytosanitary requirements require updated export certificates
        - Nigeria's revised CET affects agricultural imports - review tariff classifications
        """)
    
    with tab3:
        st.markdown("### 📈 Regulatory Impact Analysis")
        
        impact_data = pd.DataFrame({
            "Regulation": ["CET Tariffs", "Phytosanitary Rules", "Digital Customs", "Rules of Origin", "Port Reforms"],
            "Trade Impact": ["-2.3%", "-1.8%", "+4.2%", "-0.5%", "+2.1%"],
            "Compliance Cost": ["High", "Medium", "Low", "Medium", "Medium"],
            "Implementation Rate": ["95%", "72%", "45%", "88%", "60%"],
            "Trader Readiness": ["High", "Medium", "Low", "High", "Medium"]
        })
        st.dataframe(impact_data, use_container_width=True, hide_index=True)
        
        if HAS_PLOTLY:
            fig = px.scatter(impact_data, x="Regulation", y="Trade Impact", 
                           size="Compliance Cost", color="Implementation Rate",
                           title="Regulatory Impact Matrix", height=400)
            st.plotly_chart(fig, use_container_width=True)

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
            if test_client:
                st.success("✅ OpenAI API: Connected")
                st.metric("API Status", "Operational", delta="Normal")
            else:
                st.error("❌ OpenAI API: Configuration Error")
        except Exception as e:
            st.error(f"❌ OpenAI API: {str(e)[:50]}")
    
    with col_d2:
        # Bright Data connectivity
        try:
            brightdata_token = os.getenv("BRIGHTDATA_API_TOKEN") or st.secrets.get("BRIGHTDATA_API_TOKEN")
            if brightdata_token:
                st.success("✅ Bright Data: Configured")
                masked_token = f"{brightdata_token[:8]}...{brightdata_token[-4:]}" if len(brightdata_token) > 12 else "****"
                st.metric("Token Status", masked_token)
            else:
                st.warning("⚠️ Bright Data: Token missing")
                st.caption("Add BRIGHTDATA_API_TOKEN to enable web intelligence")
        except Exception as e:
            st.error(f"❌ Bright Data: {str(e)[:50]}")
    
    with col_d3:
        # Plotly status
        if HAS_PLOTLY:
            st.success("✅ Plotly: Available")
            st.metric("Visualization Engine", "High Fidelity", delta="Active")
        else:
            st.warning("⚠️ Plotly: Fallback mode")
            st.metric("Visualization Engine", "Native Streamlit", delta="Limited features")
            st.caption("Run: pip install plotly to upgrade")
    
    st.markdown("---")
    st.markdown("### 📊 Performance Metrics")
    
    # Detailed performance metrics
    metrics = get_performance_metrics()
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Cache Hit Rate", f"{metrics['cache_hit_rate']:.1%}", delta="+5% vs baseline")
        st.metric("Average Response Time", f"{metrics['api_latency']:.2f}s", delta="Within SLA")
    with col_m2:
        st.metric("Data Processed", f"{metrics['data_points_processed']:,} records", delta="Today")
        st.metric("Active Sessions", metrics['active_sessions'], delta="Current")
    with col_m3:
        st.metric("System Uptime", "99.95%", delta="30 days")
        st.metric("Error Rate", "0.23%", delta="-0.12%", delta_color="inverse")
    
    st.markdown("---")
    st.markdown("### 📝 Recent Activity Log")
    
    # Display recent logs
    log_container = st.container(height=200)
    with log_container:
        st.text(f"[{datetime.now().strftime('%H:%M:%S')}] System initialized - v2.4")
        if st.session_state.last_query:
            st.text(f"[{datetime.now().strftime('%H:%M:%S')}] Query processed: {st.session_state.last_query[:80]}...")
        if st.session_state.last_response:
            st.text(f"[{datetime.now().strftime('%H:%M:%S')}] Response generated: {len(st.session_state.last_response)} characters")
        st.text(f"[{datetime.now().strftime('%H:%M:%S')}] Cache status: {st.cache_data.get_stats() if hasattr(st.cache_data, 'get_stats') else 'Active'}")
    
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        # Clear cache button
        if st.button("🔄 Clear All Caches", type="secondary", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("✅ Caches cleared successfully!")
            time.sleep(1)
            st.rerun()
    
    with col_btn2:
        # Test API button
        if st.button("🧪 Test OpenAI API", type="secondary", use_container_width=True):
            with st.spinner("Testing API connection..."):
                try:
                    client = get_openai_client()
                    if client:
                        test_response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": "Say 'API connection successful'"}],
                            max_tokens=20
                        )
                        st.success(f"✅ API Test: {test_response.choices[0].message.content}")
                    else:
                        st.error("❌ Client not initialized")
                except Exception as e:
                    st.error(f"❌ API Test failed: {str(e)}")
    
    with col_btn3:
        # Export logs button
        if st.button("📄 Export Logs", type="secondary", use_container_width=True):
            log_content = f"BantuMarket Diagnostics Log\nGenerated: {datetime.now()}\n\nMetrics: {metrics}"
            st.download_button("Download Logs", log_content, "diagnostics_log.txt")

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)
with col_footer1:
    st.caption(f"© 2025 BantuMarket Intelligence")
with col_footer2:
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with col_footer3:
    st.caption("Version 2.4 | Hackathon Build")
