# 🔧 BantuMarket Setup Guide - Track 2: Finance & Market Intelligence

## ⚡ Quick Setup (5 Minutes)

### Step 1: Get Your API Credentials (2 min)

#### Anthropic Claude API
1. Go to: https://console.anthropic.com/api_keys
2. Click "Create Key"
3. Copy the key (starts with `sk-ant-`)
4. Save for Step 3

#### Bright Data SERP API
1. Go to: https://brightdata.com/cp/zones
2. Create SERP API zone (name it: `serp_api1`)
3. Copy your API key
4. Note your customer ID (format: `hl_XXXXXXX`)
5. Save for Step 3

### Step 2: Create .env File

**Option A: Local Development**
```bash
# In your project root directory:
cp .env.example .env
```

Then edit `.env` with your credentials (see details below)

**Option B: Streamlit Cloud**
1. Don't create .env file
2. When deployed, go to app Settings → Secrets
3. Add secrets one by one (see Streamlit Cloud Setup section)

### Step 3: Fill in Your Credentials

Open `.env` file and add:

```bash
# Anthropic API
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxx

# Bright Data API
BRIGHT_DATA_API_KEY=your_bright_data_api_key_here
BRIGHT_DATA_SERP_ZONE=serp_api1
BRIGHT_DATA_CUSTOMER_ID=hl_XXXXXXX

# Proxy credentials (optional, for native proxy method)
BRIGHT_DATA_PROXY_USERNAME=brd-customer-hl_XXXXXXX-zone-serp_api1
BRIGHT_DATA_PROXY_PASSWORD=your_proxy_password_here
```

### Step 4: Test Credentials

```bash
# Test Anthropic connection
python test_anthropic.py

# Test Bright Data connection
python test_bright_data.py
```

### Step 5: Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the enhanced app
streamlit run bantumarket_finance_app.py
```

---

## 📋 Where to Create .env File

### Local Development
```
your-project-folder/
├── .env                           ← Create here
├── .env.example                   ← Template (reference)
├── bantumarket_finance_app.py     ← Main app
├── requirements.txt
└── other files...
```

**Command:**
```bash
cd /path/to/your/project
cp .env.example .env
nano .env  # or edit with your editor
```

### .gitignore Setup
Make sure `.env` is never committed:
```bash
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
```

---

## 🔑 API Credentials Details

### Anthropic API Key
- **Where:** https://console.anthropic.com/api_keys
- **Format:** `sk-ant-XXXXXXXXXXXXXXXXXXXXXXXXXX`
- **Length:** ~32+ characters
- **What it's for:** Powering the Claude AI assistant for market analysis

### Bright Data API Key
- **Where:** https://brightdata.com/cp/zones
- **Format:** Long alphanumeric string
- **What it's for:** Access to SERP API for real-time market data scraping
- **Zone Name:** `serp_api1` (create this in dashboard)
- **Customer ID:** Format `hl_XXXXXXX` (shown in your dashboard)

### Bright Data Proxy Credentials
- **Username:** `brd-customer-{CUSTOMER_ID}-zone-serp_api1`
- **Password:** Shown in dashboard (toggle to reveal)
- **Host:** `brd.superproxy.io`
- **Port:** `33335`
- **What it's for:** Native proxy access (alternative to API method)
- **Note:** Only needed if using native proxy method (not required for SERP API)

---

## ✅ Verification

### Check Anthropic Connection
```python
import os
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"✅ API Key found: {api_key[:10]}...")

client = Anthropic(api_key=api_key)
response = client.messages.create(
    model="claude-opus-4-20250805",
    max_tokens=10,
    messages=[{"role": "user", "content": "Hi"}]
)
print(f"✅ Anthropic connection works!")
```

### Check Bright Data Connection
```python
import os
import requests

api_key = os.getenv("BRIGHT_DATA_API_KEY")
zone = os.getenv("BRIGHT_DATA_SERP_ZONE")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "zone": zone,
    "url": "https://www.google.com/search?q=shea+butter",
    "format": "raw"
}

response = requests.post(
    "https://api.brightdata.com/request",
    json=payload,
    headers=headers
)

if response.status_code == 200:
    print("✅ Bright Data connection works!")
else:
    print(f"❌ Error: {response.status_code}")
```

---

## 🚀 Deployment: Streamlit Cloud

### Step 1: Push to GitHub
```bash
git add .
git commit -m "BantuMarket Finance Intelligence - Track 2"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to: https://streamlit.io/cloud
2. Click "New app"
3. Select your GitHub repo
4. Select file: `bantumarket_finance_app.py`
5. Click "Deploy"

### Step 3: Add Secrets (IMPORTANT!)
1. Wait for app to load
2. Click ⚙️ **Settings** (top right)
3. Go to **"Secrets"** tab
4. Paste these secrets (one per line):

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxx
BRIGHT_DATA_API_KEY=your_api_key_here
BRIGHT_DATA_SERP_ZONE=serp_api1
BRIGHT_DATA_CUSTOMER_ID=hl_XXXXXXX
```

5. Click **Save**
6. App auto-redeploys in ~30 seconds

---

## 🛠️ Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Check `.env` file exists in project root
- Check variable name is exactly: `ANTHROPIC_API_KEY`
- No spaces around `=` sign
- Run: `echo $ANTHROPIC_API_KEY` to verify

### "Bright Data connection failed"
- Verify API key is correct (copy from dashboard)
- Check zone name matches your dashboard zone
- Verify customer ID format: `hl_XXXXXXX`
- Wait 5 minutes after creating new zone

### ".env file not found"
**Local:**
```bash
ls -la .env  # Check if file exists
cp .env.example .env  # Create if missing
```

**Streamlit Cloud:**
Don't use .env file. Use Secrets tab instead.

### "Requirements not installing"
```bash
# Try with flexible versions:
pip install --upgrade streamlit anthropic python-dotenv requests pandas
```

---

## 📊 Which App to Use?

### Original App
**File:** `bantumarket_app.py`
- Demo version
- Basic UI
- Mock data only
- Good for testing

### New Finance & Market Intelligence App  
**File:** `bantumarket_finance_app.py`
- **RECOMMENDED** ← Use this one
- Advanced UI with charts
- Track 2 focus
- Real Bright Data integration ready
- Multiple dashboards:
  - 📈 Price Intelligence
  - 🏪 Competitor Monitoring
  - ⚠️ Risk Alerts
  - 🔍 Supply Chain Analysis
  - 💬 AI Assistant

**Deploy the new one:**
```bash
streamlit run bantumarket_finance_app.py
```

---

## 🔐 Security Best Practices

✅ **DO:**
- Keep `.env` in `.gitignore`
- Use Streamlit Secrets for cloud deployment
- Rotate API keys periodically
- Use read-only API keys where possible

❌ **DON'T:**
- Commit `.env` to Git
- Share API keys in messages/emails
- Paste API keys in code
- Use same key for multiple projects

---

## 📞 API Documentation

### Anthropic Claude
- Docs: https://docs.anthropic.com
- API Keys: https://console.anthropic.com/api_keys
- Model: `claude-opus-4-20250805`

### Bright Data SERP API
- Dashboard: https://brightdata.com/cp/zones
- Docs: https://docs.brightdata.com
- API Endpoint: `https://api.brightdata.com/request`

---

## ✨ Next Steps

1. **Create `.env` file** with your credentials
2. **Test credentials** locally
3. **Run locally first:** `streamlit run bantumarket_finance_app.py`
4. **Deploy to Streamlit Cloud**
5. **Add Secrets** in Streamlit Cloud dashboard
6. **Share live URL** with team

---

## 🎯 Tips for Success

- **Test locally first** before deploying
- **Use Streamlit Cloud Secrets**, not .env files
- **Keep API keys safe** - they're valuable
- **Monitor API usage** to avoid unexpected costs
- **Cache results** where possible to reduce API calls

---

**You're all set! 🚀**

Questions? Check the individual API documentation or test files.
