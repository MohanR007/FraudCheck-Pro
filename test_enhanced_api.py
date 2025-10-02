import requests
import json
import time

def test_enhanced_api():
    """Test the enhanced fraud detection API"""
    base_url = "http://localhost:5000"
    
    print("🔍 Testing Enhanced FraudCheck Pro API")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check passed!")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Version: {health_data.get('version')}")
            print(f"   Model loaded: {health_data.get('model_loaded')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test fraud detection with sample transactions
    test_transactions = [
        {
            "name": "Low Risk Transaction",
            "data": {
                "amount": 150.00,
                "currency": "USD",
                "payment_method": "credit_card", 
                "location": "New York",
                "country": "US",
                "device_info": "desktop",
                "customer_age": 35,
                "account_age": 365,
                "daily_transactions": 2,
                "weekly_transactions": 8,
                "avg_transaction": 120.00,
                "merchant_category": "grocery",
                "merchant_risk": "low",
                "ip_risk": 1,
                "vpn_usage": "no",
                "previous_fraud": "0",
                "international": "no",
                "weekend": "no",
                "transaction_time": "14:30",
                "transaction_date": "2025-01-02"
            }
        },
        {
            "name": "Medium Risk Transaction", 
            "data": {
                "amount": 2500.00,
                "currency": "USD",
                "payment_method": "digital_wallet",
                "location": "Los Angeles", 
                "country": "US",
                "device_info": "mobile",
                "customer_age": 22,
                "account_age": 45,
                "daily_transactions": 5,
                "weekly_transactions": 15,
                "avg_transaction": 300.00,
                "merchant_category": "online_shopping",
                "merchant_risk": "medium",
                "ip_risk": 4,
                "vpn_usage": "yes",
                "previous_fraud": "0",
                "international": "no", 
                "weekend": "yes",
                "transaction_time": "23:45",
                "transaction_date": "2025-01-02"
            }
        },
        {
            "name": "High Risk Transaction",
            "data": {
                "amount": 8500.00,
                "currency": "USD", 
                "payment_method": "cryptocurrency",
                "location": "Lagos",
                "country": "NG",
                "device_info": "mobile",
                "customer_age": 19,
                "account_age": 3,
                "daily_transactions": 12,
                "weekly_transactions": 45,
                "avg_transaction": 150.00,
                "merchant_category": "gambling",
                "merchant_risk": "high",
                "ip_risk": 9,
                "vpn_usage": "yes",
                "previous_fraud": "2",
                "international": "yes",
                "weekend": "yes", 
                "transaction_time": "03:15",
                "transaction_date": "2025-01-02"
            }
        }
    ]
    
    print(f"\n2. Testing Fraud Detection with {len(test_transactions)} sample transactions...")
    
    for i, transaction in enumerate(test_transactions, 1):
        print(f"\n   Test {i}: {transaction['name']}")
        print(f"   Amount: ${transaction['data']['amount']}")
        print(f"   Payment: {transaction['data']['payment_method']}")
        print(f"   Location: {transaction['data']['location']}, {transaction['data']['country']}")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{base_url}/api/predict",
                headers={"Content-Type": "application/json"},
                json=transaction['data']
            )
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                
                fraud_status = "🚨 FRAUD DETECTED" if result.get('is_fraud') else "✅ SAFE"
                probability = result.get('fraud_probability', 0) * 100
                confidence = result.get('confidence', 0) * 100
                risk_level = result.get('risk_level', 'Unknown')
                
                print(f"   Result: {fraud_status}")
                print(f"   Fraud Probability: {probability:.1f}%")
                print(f"   Confidence: {confidence:.1f}%")
                print(f"   Risk Level: {risk_level}")
                print(f"   Response Time: {response_time:.1f}ms")
                
                if result.get('fraud_reasons'):
                    print(f"   Fraud Reasons: {', '.join(result['fraud_reasons'])}")
                    
            else:
                print(f"   ❌ Request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Request error: {e}")
    
    # Test statistics endpoint
    print(f"\n3. Testing Statistics Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/statistics")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistics retrieved successfully!")
            print(f"   Total Transactions: {stats.get('total_transactions', 0)}")
            print(f"   Fraud Detected: {stats.get('fraud_detected', 0)}")
            print(f"   Fraud Rate: {stats.get('fraud_rate', 0)}%")
            print(f"   Amount Blocked: ${stats.get('amount_blocked', 0)}")
        else:
            print(f"❌ Statistics request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Statistics error: {e}")
    
    print(f"\n" + "=" * 50)
    print("🎉 Enhanced API testing completed!")
    print("🌐 Access the web interface at: http://localhost:5000")

if __name__ == "__main__":
    test_enhanced_api()