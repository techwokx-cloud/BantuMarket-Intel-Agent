# 🚀 BantuMarket — Deploy in 2 Minutes

**Zero complexity. One-click deployment.**

---

## Step 1: Fork on GitHub (1 minute)

1. Copy all files to a new GitHub repo:
   ```bash
   git clone https://github.com/yourusername/bantumarket-intel-agent.git
   cd bantumarket-intel-agent
   ```

2. Push to your GitHub account (the repo will be public for Streamlit Cloud)

---

## Step 2: Deploy to Streamlit Cloud (1 minute)

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click **"New app"**
3. Connect your GitHub account
4. Select your repo: `bantumarket-intel-agent`
5. Select branch: `main`
6. Select file path: `bantumarket_app.py`
7. Click **"Deploy"**

---

## Step 3: Add Environment Variable (30 seconds)

1. After deployment starts, click **⚙️ Settings** (top right)
2. Go to **"Secrets"** tab
3. Add this (replace with your real API key):
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxx
   ```
4. Save and redeploy (automatic)

---

## Done! ✅

Your app is now live at:
```
https://[your-username]-bantumarket-intel-agent.streamlit.app
```

**No Docker. No servers. No ops.**

---

## Get Your API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create account or sign in
3. Navigate to **API Keys**
4. Click **"Create Key"**
5. Copy the key (starts with `sk-ant-`)
6. Paste into Streamlit Secrets (Step 3 above)

---

## Local Testing (Optional)

Before deploying, test locally:

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxxx
streamlit run bantumarket_app.py
```

Open `http://localhost:8501` in your browser.

---

## What's Included

✅ Professional UI (dark theme, clean navigation)
✅ AI agent with tool use (Claude)
✅ Mock market data (realistic, instant)
✅ Conversation history
✅ Export to JSON
✅ Zero configuration required
✅ Deploys in seconds

---

## That's It

You now have a **production-grade market intelligence tool** running live on the internet.

**Share the link with judges, investors, or users. Start taking queries immediately.**

---

Questions? Check `README.md` for more details.
