import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_simple_working_model():
    """Create a simple but working fraud detection model"""
    print("=== Creating Simple Working Fraud Detection Model ===")
    
    # Generate realistic fraud data with clear patterns
    np.random.seed(42)  # For reproducible results
    n_samples = 10000
    
    # Generate features
    data = []
    
    for i in range(n_samples):
        # 20% fraud rate
        is_fraud = np.random.choice([0, 1], p=[0.8, 0.2])
        
        if is_fraud == 1:
            # FRAUD patterns - make them clearly distinguishable
            amount = np.random.uniform(3000, 50000)  # Higher amounts
            hour = np.random.choice([0, 1, 2, 3, 4, 5, 22, 23])  # Unusual hours
            payment_method_risk = np.random.uniform(0.5, 1.0)  # High risk methods
            location_risk = np.random.uniform(0.6, 1.0)  # High risk locations
            device_risk = np.random.uniform(0.4, 1.0)  # Higher device risk
            ip_risk = np.random.uniform(0.6, 1.0)  # High IP risk
            age_risk = np.random.choice([0, 1], p=[0.3, 0.7])  # More age risk
            account_age_risk = np.random.choice([0, 1], p=[0.2, 0.8])  # New accounts
            frequency = np.random.choice([0, 1], p=[0.2, 0.8])  # High frequency
            amount_deviation = np.random.uniform(3, 10)  # Large deviations
            merchant_risk = np.random.uniform(0.5, 1.0)  # High merchant risk
            
        else:
            # SAFE patterns - clearly normal
            amount = np.random.uniform(5, 2000)  # Normal amounts
            hour = np.random.choice(range(8, 20))  # Business hours
            payment_method_risk = np.random.uniform(0.0, 0.3)  # Low risk methods
            location_risk = np.random.uniform(0.0, 0.3)  # Low risk locations
            device_risk = np.random.uniform(0.0, 0.3)  # Low device risk
            ip_risk = np.random.uniform(0.0, 0.4)  # Low IP risk
            age_risk = np.random.choice([0, 1], p=[0.8, 0.2])  # Less age risk
            account_age_risk = np.random.choice([0, 1], p=[0.9, 0.1])  # Established accounts
            frequency = np.random.choice([0, 1], p=[0.9, 0.1])  # Normal frequency
            amount_deviation = np.random.uniform(0, 2)  # Small deviations
            merchant_risk = np.random.uniform(0.0, 0.3)  # Low merchant risk
        
        # Create 13 features to match preprocessing
        features = [
            min(amount / 10000, 20),        # 0: normalized_amount
            1 if amount > 5000 else 0,      # 1: high_amount_flag
            hour,                          # 2: hour_of_day
            1 if hour < 6 or hour > 22 else 0,  # 3: unusual_hour_flag
            payment_method_risk,           # 4: payment_method_risk
            location_risk,                 # 5: location_risk
            device_risk,                   # 6: device_risk
            ip_risk,                       # 7: ip_risk
            age_risk,                      # 8: age_risk
            account_age_risk,              # 9: account_age_risk
            frequency,                     # 10: frequency
            amount_deviation,              # 11: amount_deviation
            merchant_risk                  # 12: merchant_risk
        ]
        
        data.append(features + [is_fraud])
    
    # Create DataFrame
    columns = [
        'normalized_amount', 'high_amount_flag', 'hour_of_day', 'unusual_hour_flag',
        'payment_method_risk', 'location_risk', 'device_risk', 'ip_risk',
        'age_risk', 'account_age_risk', 'frequency', 'amount_deviation', 
        'merchant_risk', 'is_fraud'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    
    print(f"Dataset created: {len(df)} samples")
    print(f"Fraud rate: {df['is_fraud'].mean():.1%}")
    
    # Prepare data
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("Training model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    train_pred = model.predict(X_train_scaled)
    test_pred = model.predict(X_test_scaled)
    
    train_acc = accuracy_score(y_train, train_pred)
    test_acc = accuracy_score(y_test, test_pred)
    
    print(f"Training accuracy: {train_acc:.3f}")
    print(f"Testing accuracy: {test_acc:.3f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, test_pred, target_names=['Safe', 'Fraud']))
    
    # Test with extreme examples
    print("\n=== Testing Extreme Cases ===")
    
    # Very high risk transaction
    high_risk = np.array([[20.0, 1, 2, 1, 0.9, 0.9, 0.8, 0.9, 1, 1, 1, 9.0, 0.9]])
    high_risk_scaled = scaler.transform(high_risk)
    high_pred = model.predict(high_risk_scaled)[0]
    high_prob = model.predict_proba(high_risk_scaled)[0][1]
    print(f"HIGH RISK: Prediction={high_pred} (1=Fraud), Probability={high_prob:.3f}")
    
    # Very low risk transaction
    low_risk = np.array([[0.1, 0, 12, 0, 0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0.5, 0.1]])
    low_risk_scaled = scaler.transform(low_risk)
    low_pred = model.predict(low_risk_scaled)[0]
    low_prob = model.predict_proba(low_risk_scaled)[0][1]
    print(f"LOW RISK: Prediction={low_pred} (0=Safe), Probability={low_prob:.3f}")
    
    # Save model
    joblib.dump(model, '../models/fraud_detection_model.pkl')
    joblib.dump(scaler, '../models/scaler.pkl')
    
    print("\n✅ Model saved successfully!")
    print("Model should now properly detect fraud vs safe transactions")
    
    return model, scaler

if __name__ == "__main__":
    try:
        model, scaler = create_simple_working_model()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()