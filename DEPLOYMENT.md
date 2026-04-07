# 🚀 Deploy to Streamlit Community Cloud (FREE)

Access your dashboard from anywhere in the world!

---

## ✅ Prerequisites

- GitHub account (free)
- Your project code

---

## 📋 Step-by-Step Deployment

### Step 1: Push to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   cd /Users/astha/Documents/tata_capital_cross_sell_mvp
   git init
   git add .
   git commit -m "Initial commit - Tata Capital Cross-sell MVP"
   ```

2. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Name: `tata-capital-cross-sell-mvp`
   - Keep it **Private** (recommended for business data)
   - Don't initialize with README (we already have one)
   - Click "Create repository"

3. **Push Your Code**:
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/tata-capital-cross-sell-mvp.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit: https://share.streamlit.io/
   - Click "Sign up" or "Sign in with GitHub"
   - Authorize Streamlit to access your GitHub

2. **Deploy Your App**:
   - Click "New app"
   - Select your repository: `tata-capital-cross-sell-mvp`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy!"

3. **Wait for Deployment** (2-3 minutes):
   - Streamlit will install dependencies
   - Generate data and train model automatically
   - Your app will be live!

### Step 3: Get Your Public URL

Your app will be available at:
```
https://YOUR-USERNAME-tata-capital-cross-sell-mvp.streamlit.app
```

Share this link with anyone!

---

## 🔐 Adding Gemini API Key (Optional)

To enable real AI chat on the deployed app:

1. In Streamlit Cloud dashboard, click your app
2. Click "Settings" → "Secrets"
3. Add:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
4. Click "Save"
5. App will auto-restart with AI enabled!

---

## ⚡ Important Notes

### Data Generation on Deployment

The deployment will automatically:
1. Run `generate_data.py` (creates synthetic data)
2. Run `train_model.py` (trains the model)
3. Start the dashboard

**First deployment takes ~5 minutes** due to model training.

### Free Tier Limits

- **1 GB RAM** (enough for this app)
- **1 CPU core**
- **Unlimited apps** (for private repos)
- **Always-on** (doesn't sleep)

---

## 🛠️ Updating Your Deployed App

Just push changes to GitHub:
```bash
git add .
git commit -m "Updated dashboard"
git push
```

Streamlit Cloud will auto-deploy the changes!

---

## 🎯 Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] Repository is set up (public or private)
- [ ] Deployed on Streamlit Cloud
- [ ] App is accessible via URL
- [ ] (Optional) Gemini API key added for AI chat

---

## 🔧 Troubleshooting

**Issue: "Module not found"**
- Check `requirements.txt` has all dependencies

**Issue: "Data file not found"**
- The app generates data automatically on first run
- Wait 5 minutes for initial setup

**Issue: "Memory limit exceeded"**
- Reduce dataset size in `generate_data.py` (change from 5000 to 3000 customers)

---

## 📱 Access From Anywhere

Once deployed, you can:
- ✅ Access from any device (phone, tablet, laptop)
- ✅ Share with your team
- ✅ Present in meetings without setup
- ✅ Demo to clients/stakeholders

**Your dashboard is now production-ready!** 🎉
