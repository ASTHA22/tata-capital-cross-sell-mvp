# Tata Capital - PL to HL Cross-sell Propensity Model (MVP)

## Overview
This MVP demonstrates a complete cross-sell analytics solution for NBFC (Personal Loan → Home Loan). It includes:
- Synthetic NBFC customer data generation
- XGBoost propensity model
- Interactive Streamlit dashboard with Customer 360, segment analysis, and campaign simulator

## Features

### 1. Customer 360 View
- Individual customer profiles with propensity scores
- Recommended actions (offer, channel, timing, script)
- Engagement signals and intent indicators
- Real-time eligibility assessment

### 2. Segment Analysis
- Customer segmentation by propensity
- Conversion rate analysis by demographics
- Decile performance and lift analysis
- Feature-based insights

### 3. Campaign Simulator
- Interactive targeting filters
- ROI calculator
- Expected conversion estimates
- Cost-benefit analysis

## Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate Synthetic Data
```bash
python generate_data.py
```
This creates `nbfc_customers.csv` with 5,000 synthetic NBFC customers.

### Step 3: Train Propensity Model
```bash
python train_model.py
```
This trains an XGBoost model and generates `nbfc_customers_scored.csv` with propensity scores.

### Step 4: Launch Dashboard
```bash
streamlit run app.py
```
The dashboard will open in your browser at `http://localhost:8501`

## Dataset Details

### Synthetic Data Includes:
- **Demographics**: Age, employment type, income, city tier
- **Personal Loan**: Ticket size, tenure, vintage, repayment behavior
- **Bureau Data**: Credit score, DPD history
- **Engagement**: Digital score, app logins, HL calculator usage
- **Target**: Home Loan conversion (took_hl)

### Key Features for Propensity Model:
- Age and income patterns
- Repayment behavior and bureau score
- FOIR (Fixed Obligation to Income Ratio)
- Digital engagement signals
- Intent indicators (HL calculator usage)
- Life-stage proxies (age 30-42 = prime home-buying age)

## Model Performance
- **Algorithm**: XGBoost Classifier
- **Expected AUC**: ~0.75-0.85
- **Top Features**: HL calculator usage, age, repayment score, income, bureau score

## Dashboard Sections

### 1. Customer 360
- Search by customer ID
- View propensity score with gauge chart
- Get recommended next best action
- See complete customer profile

### 2. Segment Analysis
- 4 segments: "Ready for Home", "High Potential", "Medium Potential", "Low Intent"
- Conversion rates by segment
- Propensity distribution
- Decile lift analysis (Top 10% vs baseline)

### 3. Campaign Simulator
- Filter by propensity score, segment, city tier, bureau score
- Set cost per contact and revenue per loan
- Get ROI estimates
- See expected conversions and campaign breakdown

## Use Case for Demo

### Story:
> "Tata Capital has 50,000 active Personal Loan customers. We built a propensity model to identify the top 5,000 most likely to need a Home Loan in the next 6 months. By targeting high-propensity customers, we achieve 3-4x higher conversion rates compared to random targeting."

### Key Insights to Highlight:
1. **Top 10% propensity customers** convert at 35-40% vs 8-10% baseline
2. **"Ready for Home" segment** (age 30-42, high income, good repayment) shows highest lift
3. **HL calculator usage** is the strongest intent signal
4. **ROI-positive campaigns** when targeting propensity score > 50

## Next Steps (Phase 2 Ideas)
- Add call center sentiment analysis
- Build RM copilot with agentic AI
- Integrate real bureau data APIs
- Add uplift modeling (incremental vs natural conversion)
- Deploy early delinquency guard model

## Technical Stack
- **Data**: Pandas, NumPy
- **Modeling**: XGBoost, Scikit-learn
- **Visualization**: Plotly, Streamlit
- **Deployment**: Streamlit Cloud (optional)

## Files
- `generate_data.py` - Synthetic data generator
- `train_model.py` - Model training script
- `app.py` - Streamlit dashboard
- `requirements.txt` - Python dependencies
- `nbfc_customers.csv` - Generated customer data
- `nbfc_customers_scored.csv` - Scored data with propensity
- `hl_propensity_model.pkl` - Trained model
- `feature_cols.pkl` - Feature list
- `le_*.pkl` - Label encoders

## Demo Tips
1. Start with **Customer 360** - show high propensity customer with recommended action
2. Move to **Segment Analysis** - show decile lift chart (top 10% = 3-4x lift)
3. End with **Campaign Simulator** - demonstrate ROI calculation
4. Emphasize: "This is using synthetic data, but methodology applies to real Tata Capital data"

## Author
Built for Tata Capital cross-sell use case demonstration
