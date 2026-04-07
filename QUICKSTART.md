# Quick Start Guide - NBFC Cross-sell MVP

## ⚡ Fastest Way to Run (Recommended)

### Option 1: Automated Setup (Mac/Linux)
```bash
cd /Applications/Slack.app/nbfc_cross_sell_mvp
chmod +x setup.sh
./setup.sh
```

Then launch the dashboard:
```bash
source venv/bin/activate
streamlit run app.py
```

### Option 2: Manual Setup (All Platforms)

**Step 1: Create virtual environment**
```bash
cd /Applications/Slack.app/nbfc_cross_sell_mvp
python3 -m venv venv
```

**Step 2: Activate virtual environment**
- Mac/Linux: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

**Step 3: Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 4: Generate data**
```bash
python generate_data.py
```

**Step 5: Train model**
```bash
python train_model.py
```

**Step 6: Launch dashboard**
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 🎯 What You'll See

### 1. Customer 360 View
- Search any customer by ID
- See their propensity score (0-100)
- Get recommended action (offer, channel, timing)
- View complete profile and engagement signals

### 2. Segment Analysis
- 4 segments: "Ready for Home", "High Potential", "Medium Potential", "Low Intent"
- Conversion rates by demographics
- **Decile lift analysis** - Top 10% = 3-4x higher conversion

### 3. Campaign Simulator
- Filter customers by propensity, segment, city tier
- Calculate ROI and expected conversions
- Optimize targeting strategy

---

## 📊 Demo Script (5 minutes)

### Part 1: Customer 360 (2 min)
1. Open dashboard → Customer 360 tab
2. Select a high-propensity customer (score > 70)
3. Show: "This customer has 85/100 propensity score"
4. Point to recommended action: "Pre-approved HL offer, contact via RM"
5. Highlight: HL calculator usage = strong intent signal

### Part 2: Segment Analysis (2 min)
1. Go to Segment Analysis → Decile Analysis tab
2. Show lift chart: "Top 10% converts at 35-40% vs 8% baseline"
3. Point out: "This is 4-5x lift by targeting high propensity"
4. Show segment breakdown by age/city tier

### Part 3: Campaign Simulator (1 min)
1. Go to Campaign Simulator
2. Set minimum propensity = 60
3. Show: "Targeting 1,500 customers → expect 450 conversions"
4. Show ROI calculation: "150% ROI with proper targeting"

### Key Message
> "By using propensity modeling, we can achieve 3-4x higher conversion rates and positive ROI on cross-sell campaigns. This methodology can be applied to real Tata Capital data."

---

## 🔧 Troubleshooting

### Issue: NumPy compatibility error
**Solution:** Use virtual environment (see Option 2 above)

### Issue: Module not found
**Solution:** Make sure you activated the virtual environment
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### Issue: Data file not found
**Solution:** Run the data generation first
```bash
python generate_data.py
python train_model.py
```

---

## 📁 Files Generated

After running setup, you'll have:
- `nbfc_customers.csv` - 5,000 synthetic customers
- `nbfc_customers_scored.csv` - Customers with propensity scores
- `hl_propensity_model.pkl` - Trained XGBoost model
- `feature_cols.pkl`, `le_*.pkl` - Model artifacts

---

## 🎨 Customization Ideas

Want to impress your team more? Try:

1. **Change company branding**: Edit `app.py` title and add logo
2. **Adjust data size**: Edit `generate_data.py` line 11 to generate more customers
3. **Add more segments**: Modify segment logic in `generate_data.py`
4. **Export reports**: Add download buttons in Streamlit

---

## 💡 Next Steps

After the demo, consider:
- Integrate real Tata Capital data
- Add call center sentiment analysis
- Build RM copilot with agentic AI
- Deploy to Streamlit Cloud for team access
- Add A/B testing framework

---

## 📞 Support

If you encounter issues:
1. Check that virtual environment is activated
2. Verify all files are in the same directory
3. Ensure Python 3.8+ is installed
4. Check terminal output for specific error messages
