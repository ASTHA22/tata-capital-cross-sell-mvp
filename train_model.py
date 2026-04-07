import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def prepare_features(df):
    """Prepare features for modeling"""
    
    # Create a copy for modeling
    model_df = df.copy()
    
    # Encode categorical variables
    le_employment = LabelEncoder()
    le_city_tier = LabelEncoder()
    
    model_df['employment_type_encoded'] = le_employment.fit_transform(model_df['employment_type'])
    model_df['city_tier_encoded'] = le_city_tier.fit_transform(model_df['city_tier'])
    
    # Feature engineering
    model_df['age_income_ratio'] = model_df['age'] / (model_df['monthly_income'] / 10000)
    model_df['pl_utilization'] = model_df['pl_ticket_size'] / (model_df['monthly_income'] * 12 + 1)
    model_df['is_prime_age'] = ((model_df['age'] >= 30) & (model_df['age'] <= 42)).astype(int)
    model_df['high_income'] = (model_df['monthly_income'] > 75000).astype(int)
    model_df['excellent_repayment'] = (model_df['repayment_score'] > 80).astype(int)
    model_df['low_foir'] = (model_df['foir_percent'] < 30).astype(int)
    
    # Select features for modeling
    feature_cols = [
        'age',
        'monthly_income',
        'bureau_score',
        'employment_type_encoded',
        'city_tier_encoded',
        'pl_ticket_size',
        'pl_vintage_months',
        'repayment_score',
        'dpd_last_12m',
        'foir_percent',
        'digital_engagement_score',
        'app_logins_90d',
        'hl_calculator_used',
        'age_income_ratio',
        'pl_utilization',
        'is_prime_age',
        'high_income',
        'excellent_repayment',
        'low_foir'
    ]
    
    return model_df, feature_cols, le_employment, le_city_tier

def train_propensity_model(data_path='nbfc_customers.csv'):
    """Train XGBoost propensity model for HL cross-sell"""
    
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Filter to only PL customers for cross-sell
    df_pl = df[df['has_pl'] == True].copy()
    print(f"Training on {len(df_pl)} PL customers")
    
    # Prepare features
    model_df, feature_cols, le_employment, le_city_tier = prepare_features(df_pl)
    
    X = model_df[feature_cols]
    y = model_df['took_hl']
    
    print(f"\nTarget distribution:")
    print(f"  - Took HL: {y.sum()} ({y.mean()*100:.1f}%)")
    print(f"  - Did not take HL: {(~y).sum()} ({(~y).mean()*100:.1f}%)")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining model...")
    
    # Train XGBoost
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    )
    
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)
    
    # Evaluation
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\n✓ Model trained successfully!")
    print(f"\n📊 Model Performance:")
    print(f"  - ROC-AUC Score: {auc_score:.3f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\n🎯 Top 10 Important Features:")
    print(feature_importance.head(10).to_string(index=False))
    
    # Save model and encoders
    print(f"\n💾 Saving model artifacts...")
    joblib.dump(model, 'hl_propensity_model.pkl')
    joblib.dump(feature_cols, 'feature_cols.pkl')
    joblib.dump(le_employment, 'le_employment.pkl')
    joblib.dump(le_city_tier, 'le_city_tier.pkl')
    
    # Generate predictions for all PL customers
    print(f"\n🔮 Generating propensity scores for all PL customers...")
    model_df_all, _, _, _ = prepare_features(df_pl)
    X_all = model_df_all[feature_cols]
    propensity_scores = model.predict_proba(X_all)[:, 1] * 100
    
    # Add to dataframe
    df_pl['model_propensity_score'] = propensity_scores
    df_pl['propensity_decile'] = pd.qcut(propensity_scores, q=10, labels=False, duplicates='drop') + 1
    
    # Save scored data
    df_pl.to_csv('nbfc_customers_scored.csv', index=False)
    
    print(f"\n✓ Scored data saved to: nbfc_customers_scored.csv")
    
    # Decile analysis
    print(f"\n📈 Propensity Decile Analysis:")
    decile_analysis = df_pl.groupby('propensity_decile').agg({
        'took_hl': ['count', 'sum', 'mean'],
        'model_propensity_score': 'mean'
    }).round(3)
    decile_analysis.columns = ['Total', 'Conversions', 'Conversion_Rate', 'Avg_Propensity']
    print(decile_analysis.sort_index(ascending=False))
    
    return model, feature_cols, auc_score

if __name__ == "__main__":
    model, features, auc = train_propensity_model()
    print(f"\n✅ Model training complete! AUC: {auc:.3f}")
