# 🤖 Setting Up Real AI Chat with Google Gemini (FREE)

## Quick Setup (5 minutes)

### Step 1: Get Your Free API Key

1. Go to **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy your API key

### Step 2: Add API Key to Your Project

**Option A: Using Streamlit Secrets (Recommended)**

1. Open the file: `.streamlit/secrets.toml`
2. Uncomment the last line and add your key:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```

**Option B: Using Environment Variable**

```bash
export GEMINI_API_KEY="your-actual-api-key-here"
```

### Step 3: Install the Package

```bash
cd /Users/astha/Documents/tata_capital_cross_sell_mvp
source venv/bin/activate
pip install google-generativeai
```

### Step 4: Restart the Dashboard

```bash
streamlit run app.py
```

---

## ✅ How to Verify It's Working

1. Go to the **AI Chat Assistant** tab
2. You should see: **"Powered by Google Gemini AI 🌟"**
3. Ask any question - it will use real AI!

---

## 💡 What Changes?

**Before (Rule-based):**
- Only understands specific keywords
- Pre-programmed responses
- Limited flexibility

**After (Real AI):**
- Understands natural language
- Can answer ANY question about your data
- Conversational and context-aware
- Much smarter recommendations

---

## 🆓 Free Tier Limits

- **60 requests per minute**
- **1,500 requests per day**
- More than enough for demos and testing!

---

## 🔒 Security Note

Never commit your API key to Git! The `.streamlit/secrets.toml` file is already in `.gitignore`.

---

## 🚀 Try These Questions

Once set up, try asking:
- "Which customers should I prioritize this week?"
- "Why is customer CUST000001 a good prospect?"
- "Compare conversion rates across different age groups"
- "What's the best time to contact high-propensity customers?"

The AI will analyze your actual data and give intelligent responses!
