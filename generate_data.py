import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_nbfc_customers(n_customers=5000):
    """
    Generate synthetic NBFC customer data for PL and HL cross-sell analysis.
    Simulates realistic Indian NBFC customer profiles.
    """
    
    customers = []
    
    # City tiers and their distribution
    city_tiers = {
        'Tier 1': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune'],
        'Tier 2': ['Jaipur', 'Lucknow', 'Nagpur', 'Indore', 'Coimbatore', 'Kochi'],
        'Tier 3': ['Nashik', 'Rajkot', 'Mysore', 'Guwahati', 'Chandigarh', 'Bhopal']
    }
    
    for i in range(n_customers):
        customer_id = f"CUST{str(i+1).zfill(6)}"
        
        # Demographics
        age = np.random.normal(35, 8)
        age = int(np.clip(age, 23, 58))
        
        # Employment type
        employment_type = np.random.choice(['Salaried', 'Self-Employed'], p=[0.7, 0.3])
        
        # Income (higher for older, self-employed tend to show higher but variable)
        if employment_type == 'Salaried':
            base_income = 40000 + (age - 25) * 2000
            income = int(np.random.normal(base_income, 15000))
        else:
            base_income = 50000 + (age - 25) * 2500
            income = int(np.random.normal(base_income, 25000))
        
        income = max(25000, income)
        
        # City tier (higher income = more likely Tier 1)
        if income > 80000:
            tier = np.random.choice(['Tier 1', 'Tier 2', 'Tier 3'], p=[0.6, 0.3, 0.1])
        elif income > 50000:
            tier = np.random.choice(['Tier 1', 'Tier 2', 'Tier 3'], p=[0.4, 0.4, 0.2])
        else:
            tier = np.random.choice(['Tier 1', 'Tier 2', 'Tier 3'], p=[0.2, 0.4, 0.4])
        
        city = random.choice(city_tiers[tier])
        
        # Bureau score (higher for older, salaried)
        base_score = 680 + (age - 25) * 3
        if employment_type == 'Salaried':
            base_score += 20
        bureau_score = int(np.random.normal(base_score, 40))
        bureau_score = np.clip(bureau_score, 600, 850)
        
        # Personal Loan details (70% have PL)
        has_pl = np.random.random() < 0.7
        
        if has_pl:
            pl_vintage_months = np.random.randint(6, 48)
            pl_ticket_size = int(np.random.uniform(100000, min(income * 5, 1000000)))
            pl_tenure = np.random.choice([12, 18, 24, 36, 48, 60])
            
            # Repayment behavior (better for higher bureau score)
            repayment_score = min(100, int((bureau_score - 600) / 2.5 + np.random.normal(0, 10)))
            repayment_score = max(0, repayment_score)
            
            # DPD history
            if repayment_score > 80:
                dpd_last_12m = np.random.choice([0, 0, 0, 1], p=[0.85, 0.10, 0.03, 0.02])
            elif repayment_score > 60:
                dpd_last_12m = np.random.choice([0, 1, 2, 3], p=[0.60, 0.25, 0.10, 0.05])
            else:
                dpd_last_12m = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.40, 0.25, 0.15, 0.10, 0.05, 0.05])
        else:
            pl_vintage_months = 0
            pl_ticket_size = 0
            pl_tenure = 0
            repayment_score = 0
            dpd_last_12m = 0
        
        # Digital engagement (younger = more engaged)
        digital_engagement_score = int(100 - (age - 23) * 1.5 + np.random.normal(0, 15))
        digital_engagement_score = np.clip(digital_engagement_score, 0, 100)
        
        # App logins last 90 days
        if digital_engagement_score > 70:
            app_logins_90d = np.random.poisson(15)
        elif digital_engagement_score > 40:
            app_logins_90d = np.random.poisson(6)
        else:
            app_logins_90d = np.random.poisson(2)
        
        # HL calculator usage (intent signal)
        hl_calculator_used = np.random.random() < (0.05 + (age - 23) * 0.01)
        
        # FOIR estimate (lower is better for eligibility)
        existing_obligations = pl_ticket_size / pl_tenure if pl_tenure > 0 else 0
        foir = (existing_obligations / income) * 100 if income > 0 else 0
        foir = min(foir, 60)
        
        # Home Loan propensity factors
        # Key signals: age 30-45, stable income, good repayment, Tier 1/2 city, HL calculator usage
        hl_propensity_base = 0
        
        # Age factor (peak at 32-42)
        if 30 <= age <= 42:
            hl_propensity_base += 25
        elif 28 <= age <= 45:
            hl_propensity_base += 15
        else:
            hl_propensity_base += 5
        
        # Income factor
        if income > 75000:
            hl_propensity_base += 20
        elif income > 50000:
            hl_propensity_base += 10
        
        # City tier factor
        if tier == 'Tier 1':
            hl_propensity_base += 15
        elif tier == 'Tier 2':
            hl_propensity_base += 10
        
        # Repayment behavior
        if repayment_score > 80:
            hl_propensity_base += 20
        elif repayment_score > 60:
            hl_propensity_base += 10
        
        # Digital engagement / intent
        if hl_calculator_used:
            hl_propensity_base += 25
        
        if digital_engagement_score > 60:
            hl_propensity_base += 10
        
        # FOIR (lower is better)
        if foir < 30:
            hl_propensity_base += 15
        elif foir < 40:
            hl_propensity_base += 5
        
        # Add noise
        hl_propensity = hl_propensity_base + np.random.normal(0, 10)
        hl_propensity = np.clip(hl_propensity, 0, 100)
        
        # Actual HL taken (probabilistic based on propensity)
        hl_conversion_prob = hl_propensity / 100 * 0.4  # Scale down for realism
        took_hl = np.random.random() < hl_conversion_prob
        
        if took_hl:
            hl_ticket_size = int(np.random.uniform(500000, min(income * 60, 5000000)))
            hl_tenure = np.random.choice([120, 180, 240, 300])
            hl_vintage_months = np.random.randint(1, 24)
        else:
            hl_ticket_size = 0
            hl_tenure = 0
            hl_vintage_months = 0
        
        # Segment labels
        if hl_propensity > 70:
            segment = "Ready for Home"
        elif hl_propensity > 50:
            segment = "High Potential"
        elif hl_propensity > 30:
            segment = "Medium Potential"
        else:
            segment = "Low Intent"
        
        customers.append({
            'customer_id': customer_id,
            'age': age,
            'employment_type': employment_type,
            'monthly_income': income,
            'city': city,
            'city_tier': tier,
            'bureau_score': int(bureau_score),
            'has_pl': has_pl,
            'pl_ticket_size': pl_ticket_size,
            'pl_tenure_months': pl_tenure,
            'pl_vintage_months': pl_vintage_months,
            'repayment_score': repayment_score,
            'dpd_last_12m': dpd_last_12m,
            'foir_percent': round(foir, 2),
            'digital_engagement_score': digital_engagement_score,
            'app_logins_90d': app_logins_90d,
            'hl_calculator_used': hl_calculator_used,
            'hl_propensity_score': round(hl_propensity, 2),
            'took_hl': took_hl,
            'hl_ticket_size': hl_ticket_size,
            'hl_tenure_months': hl_tenure,
            'hl_vintage_months': hl_vintage_months,
            'segment': segment
        })
    
    df = pd.DataFrame(customers)
    return df

if __name__ == "__main__":
    print("Generating synthetic NBFC customer data...")
    df = generate_nbfc_customers(5000)
    
    # Save to CSV
    df.to_csv('nbfc_customers.csv', index=False)
    
    print(f"\n✓ Generated {len(df)} customer records")
    print(f"\n📊 Dataset Summary:")
    print(f"  - Customers with PL: {df['has_pl'].sum()} ({df['has_pl'].mean()*100:.1f}%)")
    print(f"  - Customers who took HL: {df['took_hl'].sum()} ({df['took_hl'].mean()*100:.1f}%)")
    print(f"  - Average HL propensity: {df['hl_propensity_score'].mean():.1f}")
    print(f"\n📈 Segment Distribution:")
    print(df['segment'].value_counts())
    print(f"\n💾 Saved to: nbfc_customers.csv")
