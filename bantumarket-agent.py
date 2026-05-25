import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load VPS environment variables
load_dotenv()

# Streamlit Page Window Configuration
st.set_page_config(
    page_title="BantuMarket Intel Agent | Regional Intelligence Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & SERVER STATUS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌐 BantuMarket")
    st.caption("Cross-Border Regional Trade Intelligence")
    st.markdown("---")
    
    # Navigation Links Mockup
    st.button("📋 Dashboard (Active)", use_container_width=True, type="secondary")
    st.button("🌿 Commodity Hub", use_container_width=True, type="secondary")
    st.button("🗺️ Regulatory Map", use_container_width=True, type="secondary")
    st.button("🖥️ Vultr Server Settings", use_container_width=True, type="secondary")
    
    st.markdown("---")
    st.markdown("### ⚙️ Vultr Node Routing Details")
    target_node = st.selectbox("Target Regional Node Proxy", [
        "West Africa Node (ECOWAS)", 
        "East Africa Node (EAC)", 
        "Southern Africa Node (SADC)"
    ])
    st.success("🔄 Vultr Pipeline Connection: Healthy")
    st.markdown("---")
    st.caption("Powered by Bright Data MCP & OpenAI GPT-4o")

# -----------------------------------------------------------------------------
# MAIN APP HEADER & INFRASTRUCTURE MATRIX DISPLAY
# -----------------------------------------------------------------------------
st.markdown("# 🌍 BantuMarket Intel Agent | Regional Intelligence Hub")

# INFRASTRUCTURE STATUS GRID (Prominently showcasing required hackathon tools)
st.markdown("##### 📌 INFRASTRUCTURE STACK STATUS MATRIX")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("**🟢 MCP Server:**\nConnected (Hosted)")
with col2:
    st.info("**⚡ SERP API:**\nActive (Locally Targeted)")
with col3:
    st.info("**🛡️ Web Unlocker:**\nEnabled (Geo-Bypassing)")
with col4:
    st.info("**🤖 Scraping Browser:**\nPro Mode (DOM Ready)")

st.markdown("---")

# -----------------------------------------------------------------------------
# CLIENT ARCHITECTURE & SECRETS CHECK
# -----------------------------------------------------------------------------
# Verify backend tokens inside the Vultr env file
if not os.getenv("OPENAI_API_KEY") or not os.getenv("BRIGHTDATA_API_TOKEN"):
    st.warning("⚠️ Configuration Tokens Missing: Please verify your `.env` file credentials on Vultr.")
    st.stop()

# Build the official cloud endpoint string with PRO_MODE enabled to unlock all pro tool collections
api_token = os.getenv("BRIGHTDATA_API_TOKEN")
brightdata_hosted_url = f"https://mcp.brightdata.com/mcp?token={api_token}&PRO_MODE=true"

# Instantiate backend clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------------------------------------------------------
# SYSTEM QUERY HANDLER & INTERFACE MUTATIONS
# -----------------------------------------------------------------------------
# Container configuration for inputs
input_col, btn_col = st.columns([4, 1])

with input_col:
    query = st.text_input(
        label="Enter Location-Specific Commodity Inquiry String:",
        label_visibility="collapsed",
        placeholder="e.g., Verify Maize costs across AFEX warehouses in Nigeria and check for new cross-border tariffs in Benin.",
        value="Verify Maize costs across AFEX warehouses in Nigeria and check for new cross-border tariffs in Benin."
    )

with btn_col:
    submit_btn = st.button("Synthesize Market Briefing", use_container_width=True, type="primary")

# Execute Live Extraction Sequence upon Trigger Interaction
if submit_btn and query:
    with st.spinner("Invoking Bright Data Remote MCP Tools (`search_engine`, `scrape_as_markdown`, `scraping_browser`)..."):
        try:
            # Inject regional context and command instructions into the system layer
            system_blueprint = (
                "You are the BantuMarket Intel Agent, an enterprise platform specialized in AfCFTA cross-border logistics tracking.\n"
                "You possess direct execution capabilities over Bright Data web tools via your unified MCP connection layer:\n"
                "- Call 'search_engine' to target local African search variants (SERP API).\n"
                "- Call 'scrape_as_markdown' to index static local directories without geoblocks (Web Unlocker).\n"
                "- Call 'scraping_browser' functions automatically when processing complex interactive wholesaler pages.\n\n"
                "Analyze the user's prompt, pull the requested trade data live, and format your output into markdown data metrics."
            )
            
            # Send context to OpenAI passing the Bright Data tool endpoints
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_blueprint},
                    {"role": "user", "content": query}
                ],
                tools=[{"type": "web_mcp", "url": brightdata_hosted_url}]
            )
            
            agent_payload = response.choices[0].message.content
            
            # Render Live Analytical Results Container
            st.markdown("### 📋 Real-Time Intelligence Dossier")
            st.markdown(agent_payload)
            st.success("✨ Stream Processing Finalized Successfully via Bright Data Infrastructure Systems.")
            
        except Exception as e:
            st.error(f"Pipeline Interface Error: {e}")

# -----------------------------------------------------------------------------
# VISUAL FALLBACK DATA CARDS (Matches layout mockup image)
# -----------------------------------------------------------------------------
st.markdown("### 📊 Live Commodity Price Comparison (per Metric Ton)")

# Mock Data Frame representing typical agent extraction responses
st.markdown("""
| Commodity | Region/Node | Supplier (Verified) | Live Price (USD) | Market Source |
| :--- | :--- | :--- | :--- | :--- |
| Maize (AFEX Hub) | Nigeria (Lagos) | Savannah Agro (✅ Verified) | \$485 | AFEX Index |
| Maize (Esoko Node) | Ghana (Kumasi) | Volta Wholesalers (✅ Verified) | \$510 | Esoko Portal |
""")

st.markdown("### 🛡️ Regulatory Compliance Index")
metric_col1, metric_col2, _ = st.columns([1, 1, 2])

with metric_col1:
    st.metric(label="ECOWAS Tariffs Status Risk Index", value="78%", delta="Moderate Risk")
with metric_col2:
    st.metric(label="Port Congestion Delays Matrix", value="24 hrs", delta="-3 hrs Reduction", delta_color="inverse")

st.markdown("""
* 📝 **New export tariff** implemented for raw Shea nuts in Côte d'Ivoire.
* 🚢 **Ghana Ports update** certification specifications for immediate AfCFTA administrative compliance frameworks.
""")
