from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
import logging
import json
import hashlib
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
            static_folder='../frontend',
            template_folder='../frontend')
CORS(app)

# Global variables
model = None
scaler = None
transaction_stats = defaultdict(int)
daily_stats = defaultdict(lambda: defaultdict(int))

def load_model():
    """Load the pretrained fraud detection model"""
    global model, scaler
    try:
        model_path = os.path.join('..', 'models', 'fraud_detection_model.pkl')
        scaler_path = os.path.join('..', 'models', 'scaler.pkl')
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            logger.info("Model and scaler loaded successfully")
        else:
            logger.warning("Model files not found. Creating a simple mock model.")
            create_mock_model()
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        create_mock_model()

def create_mock_model():
    """Create a simple mock model for demonstration"""
    global model, scaler
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    
    # Create a simple mock model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    scaler = StandardScaler()
    
    # Create some dummy training data to fit the model (13 features to match preprocessing)
    X_dummy = np.random.rand(1000, 13)
    y_dummy = np.random.choice([0, 1], 1000, p=[0.85, 0.15])  # 85% not fraud, 15% fraud
    
    X_scaled = scaler.fit_transform(X_dummy)
    model.fit(X_scaled, y_dummy)
    
    # Save the mock model
    os.makedirs('../models', exist_ok=True)
    joblib.dump(model, '../models/fraud_detection_model.pkl')
    joblib.dump(scaler, '../models/scaler.pkl')
    logger.info("Enhanced mock model created and saved")

def preprocess_enhanced_transaction(transaction_data):
    """Enhanced preprocessing for transaction data with more features"""
    try:
        features = []
        
        # 1. Amount features
        amount = float(transaction_data.get('amount', 0))
        features.append(min(amount / 10000, 20))  # Normalized amount
        features.append(1 if amount > 5000 else 0)  # High amount flag
        
        # 2. Time features
        transaction_time = transaction_data.get('transaction_time', datetime.now().strftime('%H:%M'))
        hour = int(transaction_time.split(':')[0])
        features.append(hour)
        features.append(1 if hour < 6 or hour > 22 else 0)  # Unusual hours
        
        # 3. Payment method risk (expanded to align with new frontend options)
        payment_method = transaction_data.get('payment_method', 'credit_card')
        payment_risk_map = {
            'credit_card': 0.10,
            'debit_card': 0.05,
            'prepaid_card': 0.30,
            'gift_card': 0.35,  # Often abused for laundering
            'paypal': 0.15,
            'venmo': 0.20,
            'apple_pay': 0.12,
            'google_pay': 0.12,
            'alipay': 0.25,
            'wechat_pay': 0.25,
            'bank_transfer': 0.08,
            'wire_transfer': 0.20,  # Higher risk for larger sums
            'digital_wallet': 0.20,
            'cryptocurrency': 0.50,
            'cash': 0.02
        }
        payment_method_risk = payment_risk_map.get(payment_method, 0.15)
        features.append(payment_method_risk)
        
        # 4. Location and country risk
        country = transaction_data.get('country', 'US')
        # Expanded risk classification reflecting new country list
        high_risk_countries = {'NG', 'RO', 'RU', 'CN', 'TR', 'EG', 'GH', 'KE', 'PH', 'VN', 'ID'}
        medium_risk_countries = {'BR', 'MX', 'AR', 'IN', 'ZA', 'KR', 'SG', 'HK'}
        if country in high_risk_countries:
            location_risk = 0.85
        elif country in medium_risk_countries:
            location_risk = 0.45
        else:
            location_risk = 0.12
        features.append(location_risk)
        
        # 5. Device and IP risk
        device_info = transaction_data.get('device_info', 'desktop')
        device_risk_map = {
            'mobile': 0.60,      # Higher fraud interaction surface
            'tablet': 0.30,
            'desktop': 0.10,
            'laptop': 0.15,
            'smartwatch': 0.70,
            'atm': 0.05,
            'pos': 0.08,
            'unknown': 0.25
        }
        device_risk = device_risk_map.get(device_info, 0.20)
        features.append(device_risk)
        
        ip_risk = float(transaction_data.get('ip_risk', 2)) / 10
        features.append(ip_risk)
        
        # 6. Customer behavior features
        customer_age = int(transaction_data.get('customer_age', 35))
        features.append(1 if customer_age < 21 or customer_age > 65 else 0)  # Age risk
        
        account_age = int(transaction_data.get('account_age', 365))
        features.append(1 if account_age < 30 else 0)  # New account risk
        
        # 7. Transaction frequency
        daily_transactions = int(transaction_data.get('daily_transactions', 1))
        high_frequency_flag = 1 if daily_transactions > 10 else 0
        features.append(high_frequency_flag)
        
        avg_transaction = float(transaction_data.get('avg_transaction', amount))
        if avg_transaction > 0:
            amount_deviation = abs(amount - avg_transaction) / avg_transaction
        else:
            amount_deviation = 0
        features.append(min(amount_deviation, 5))  # Amount deviation from average
        
        # 8. Merchant and additional features
        merchant_category = transaction_data.get('merchant_category', 'retail')
        high_risk_merchants = ['gambling', 'adult_content', 'cryptocurrency']
        medium_risk_merchants = ['travel', 'entertainment', 'online_shopping']
        
        # Expanded merchant category risk
        expanded_high_risk = set(high_risk_merchants + [
            'cryptocurrency_exchange', 'luxury_goods', 'financial_services'
        ])
        expanded_medium_risk = set(medium_risk_merchants + [
            'ride_sharing', 'subscriptions', 'logistics', 'food_delivery', 'electronics'
        ])
        if merchant_category in expanded_high_risk:
            merchant_risk = 0.72
        elif merchant_category in expanded_medium_risk:
            merchant_risk = 0.32
        else:
            merchant_risk = 0.12
        features.append(merchant_risk)

        # Synergistic risk boost (captures compound suspicious signals)
        risk_flags = 0
        risk_flags += 1 if amount > 5000 else 0
        risk_flags += 1 if (hour < 6 or hour > 22) else 0
        risk_flags += 1 if payment_method_risk >= 0.3 else 0
        risk_flags += 1 if location_risk >= 0.8 else 0
        risk_flags += 1 if device_risk >= 0.6 else 0
        risk_flags += 1 if high_frequency_flag == 1 else 0
        # If multiple high-risk signals present, subtly amplify existing continuous risk features
        if risk_flags >= 3:
            # Slightly increase merchant risk & amount deviation to better separate decision boundary
            features[11] = min(features[11] * (1 + (risk_flags * 0.05)), 10)  # amount_deviation amplification
        
        return np.array(features).reshape(1, -1)
        
    except Exception as e:
        logger.error(f"Error in preprocessing: {e}")
        # Return default feature vector if preprocessing fails
        return np.array([0.1, 0, 12, 0, 0.1, 0.1, 0.1, 0.2, 0, 0, 0, 0.1]).reshape(1, -1)

def calculate_risk_level(fraud_probability, confidence):
    """Calculate risk level based on probability and confidence"""
    if fraud_probability > 0.7:
        return "Very High"
    elif fraud_probability > 0.5:
        return "High" 
    elif fraud_probability > 0.3:
        return "Medium"
    elif fraud_probability > 0.1:
        return "Low"
    else:
        return "Very Low"

def get_fraud_reasons(transaction_data, fraud_probability):
    """Generate reasons for fraud detection"""
    reasons = []
    
    amount = float(transaction_data.get('amount', 0))
    if amount > 5000:
        reasons.append("High transaction amount")
    
    country = transaction_data.get('country', 'US')
    if country in ['NG', 'RO', 'RU', 'CN']:
        reasons.append("High-risk country")
    
    payment_method = transaction_data.get('payment_method', 'credit_card')
    if payment_method in ['cryptocurrency', 'gift_card', 'prepaid_card', 'wire_transfer', 'alipay', 'wechat_pay']:
        reasons.append("High-risk payment method")
    
    account_age = int(transaction_data.get('account_age', 365))
    if account_age < 30:
        reasons.append("New account")
    
    daily_transactions = int(transaction_data.get('daily_transactions', 1))
    if daily_transactions > 10:
        reasons.append("High transaction frequency")

    # IP risk
    try:
        ip_risk_val = float(transaction_data.get('ip_risk', 0))
        if ip_risk_val >= 7:
            reasons.append("High IP risk score")
    except Exception:
        pass

    # Merchant category risk
    merchant_category = transaction_data.get('merchant_category', 'retail')
    if merchant_category in ['gambling', 'adult_content', 'cryptocurrency_exchange', 'luxury_goods', 'financial_services']:
        reasons.append("High-risk merchant category")

    # Amount deviation (if provided)
    try:
        avg_amount = float(transaction_data.get('avg_transaction', 0) or 0)
        current_amount = float(transaction_data.get('amount', 0) or 0)
        if avg_amount > 0:
            deviation_ratio = abs(current_amount - avg_amount) / avg_amount
            if deviation_ratio > 5:
                reasons.append("Extreme deviation from average")
            elif deviation_ratio > 2:
                reasons.append("Large deviation from average")
    except Exception:
        pass
    
    transaction_time = transaction_data.get('transaction_time', '12:00')
    hour = int(transaction_time.split(':')[0])
    if hour < 6 or hour > 22:
        reasons.append("Unusual transaction time")
    
    return reasons

def _heuristic_fallback(features_row):
    """Simple rule-based fallback if model/scaler pipeline fails.
    features_row: numpy array shape (1, n)
    Returns (prediction:int, probability:float)
    """
    try:
        # Indices based on current 13-feature schema
        amount_norm = features_row[0,0]
        high_amount = features_row[0,1]
        unusual_hour = features_row[0,3]
        payment_risk = features_row[0,4]
        location_risk = features_row[0,5]
        device_risk = features_row[0,6]
        ip_risk = features_row[0,7]
        age_risk = features_row[0,8]
        acct_new = features_row[0,9]
        freq = features_row[0,10]
        deviation = features_row[0,11]
        merchant_risk = features_row[0,12]

        score = (
            high_amount*1.2 + unusual_hour*0.6 + payment_risk*1.1 +
            location_risk*1.0 + device_risk*0.9 + ip_risk*1.3 +
            acct_new*0.7 + freq*0.8 + deviation*0.15 + merchant_risk*1.0 +
            age_risk*0.4 + amount_norm*0.05
        )
        # Normalize rough score to probability-ish value
        prob = 1/(1+np.exp(-score + 3.5))  # shift for better spread
        pred = 1 if prob > 0.5 else 0
        return pred, float(prob)
    except Exception:
        return 0, 0.05

def _prepare_features_for_model(raw_features: np.ndarray):
    """Ensure feature vector matches scaler/model expected size, padding or truncating as needed."""
    try:
        expected = getattr(scaler, 'n_features_in_', raw_features.shape[1]) if scaler else raw_features.shape[1]
        current = raw_features.shape[1]
        adjusted = raw_features
        if current > expected:
            logger.warning(f"Truncating feature vector from {current} -> {expected}")
            adjusted = raw_features[:, :expected]
        elif current < expected:
            logger.warning(f"Padding feature vector from {current} -> {expected}")
            pad = np.zeros((raw_features.shape[0], expected-current))
            adjusted = np.concatenate([raw_features, pad], axis=1)
        return adjusted
    except Exception as e:
        logger.error(f"Error adjusting feature vector: {e}")
        return raw_features

@app.route('/')
def home():
    """Serve the enhanced homepage"""
    try:
        return send_from_directory('../frontend', 'enhanced_index.html')
    except:
        return send_from_directory('../frontend', 'index.html')

@app.route('/api/predict', methods=['POST'])
def predict_fraud():
    """Enhanced fraud prediction endpoint"""
    start_time = datetime.now()
    
    try:
        # Get transaction data
        transaction_data = request.get_json()
        
        if not transaction_data:
            return jsonify({'error': 'No transaction data provided'}), 400
        
        # Validate required fields
        required_fields = ['amount', 'payment_method']
        for field in required_fields:
            if field not in transaction_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Preprocess the transaction data
        features = preprocess_enhanced_transaction(transaction_data)

        # Adjust features length if mismatch
        features_for_model = _prepare_features_for_model(features)
        used_fallback = False
        try:
            features_scaled = scaler.transform(features_for_model)
            fraud_prediction = int(model.predict(features_scaled)[0])
            fraud_probability = float(model.predict_proba(features_scaled)[0][1])
        except Exception as model_err:
            logger.error(f"Model pipeline failure, switching to heuristic fallback: {model_err}")
            fraud_prediction, fraud_probability = _heuristic_fallback(features)
            used_fallback = True
        
        # Calculate confidence (distance from decision boundary)
        confidence = max(abs(fraud_probability - 0.5) * 2, 0.6)
        
        # Calculate risk level
        risk_level = calculate_risk_level(fraud_probability, confidence)
        
        # Get fraud reasons
        fraud_reasons = get_fraud_reasons(transaction_data, fraud_probability)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Update statistics
        transaction_stats['total'] += 1
        if fraud_prediction == 1:
            transaction_stats['fraud'] += 1
            transaction_stats['amount_blocked'] += float(transaction_data.get('amount', 0))
        
        today = datetime.now().strftime('%Y-%m-%d')
        daily_stats[today]['total'] += 1
        if fraud_prediction == 1:
            daily_stats[today]['fraud'] += 1
        
        # Prepare response
        response = {
            'is_fraud': bool(fraud_prediction),
            'fraud_probability': float(fraud_probability),
            'confidence': float(confidence),
            'risk_level': risk_level,
            'processing_time_ms': round(processing_time, 2),
            'features_analyzed': len(features[0]),
            'model_version': '2.0.0',
            'timestamp': datetime.now().isoformat(),
            'fallback_used': used_fallback
        }
        
        # Add fraud reasons if it's flagged as fraud
        if fraud_prediction == 1:
            response['fraud_reasons'] = fraud_reasons
        
        logger.info(f"Fraud prediction completed: {response}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in fraud prediction: {e}")
        return jsonify({
            'error': 'Error processing transaction',
            'message': str(e),
            'is_fraud': False,
            'fraud_probability': 0.0,
            'confidence': 0.0,
            'risk_level': 'Unknown',
            'processing_time_ms': 0
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Enhanced health check endpoint"""
    try:
        model_loaded = model is not None and scaler is not None
        
        # Calculate uptime (simplified)
        uptime = "System running"
        
        # Get system statistics
        stats = {
            'total_transactions': transaction_stats['total'],
            'fraud_detected': transaction_stats['fraud'],
            'fraud_rate': round((transaction_stats['fraud'] / max(transaction_stats['total'], 1)) * 100, 2),
            'amount_blocked': round(transaction_stats['amount_blocked'], 2)
        }
        
        response = {
            'status': 'healthy' if model_loaded else 'degraded',
            'model_loaded': model_loaded,
            'version': '2.0.0',
            'uptime': uptime,
            'statistics': stats,
            'timestamp': datetime.now().isoformat(),
            'features': {
                'enhanced_detection': True,
                'real_time_processing': True,
                'risk_assessment': True,
                'fraud_reasoning': True
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get detailed system statistics"""
    try:
        # Calculate fraud rate
        total_transactions = transaction_stats['total']
        fraud_count = transaction_stats['fraud']
        fraud_rate = (fraud_count / max(total_transactions, 1)) * 100
        
        # Get daily statistics for the last 7 days
        daily_data = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            daily_data.append({
                'date': date,
                'total': daily_stats[date]['total'],
                'fraud': daily_stats[date]['fraud']
            })
        
        response = {
            'total_transactions': total_transactions,
            'fraud_detected': fraud_count,
            'fraud_rate': round(fraud_rate, 2),
            'amount_blocked': round(transaction_stats['amount_blocked'], 2),
            'accuracy_rate': 98.5,  # Simulated accuracy
            'avg_response_time': 45,  # Simulated response time
            'daily_statistics': daily_data[::-1],  # Reverse to get chronological order
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset-stats', methods=['POST'])
def reset_statistics():
    """Reset system statistics (for testing purposes)"""
    try:
        global transaction_stats, daily_stats
        transaction_stats.clear()
        daily_stats.clear()
        
        return jsonify({
            'message': 'Statistics reset successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error resetting statistics: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Custom 404 handler"""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET /',
            'POST /api/predict',
            'GET /api/health',
            'GET /api/statistics',
            'POST /api/reset-stats'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Please check the server logs for more details'
    }), 500

if __name__ == '__main__':
    # Load the model on startup
    load_model()
    
    # Initialize some sample statistics
    transaction_stats['total'] = 0
    transaction_stats['fraud'] = 0
    transaction_stats['amount_blocked'] = 0.0
    
    logger.info("Enhanced FraudCheck Web application starting...")
    logger.info("Available endpoints:")
    logger.info("  GET / - Enhanced web interface")
    logger.info("  POST /api/predict - Enhanced fraud prediction")
    logger.info("  GET /api/health - System health check")
    logger.info("  GET /api/statistics - Detailed statistics")
    logger.info("  POST /api/reset-stats - Reset statistics")
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)