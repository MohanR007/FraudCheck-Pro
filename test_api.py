"""
Test script for FraudCheck Web API
"""

import requests
import json
import time

def test_api():
    """Test the fraud detection API"""
    base_url = "http://localhost:5000"
    
    print("=== FraudCheck Web API Test ===\n")
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {health['status']}")
            print(f"   Model loaded: {health['model_loaded']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on localhost:5000")
        return False
    
    print()
    
    # Test cases
    test_cases = [
        {
            "name": "Low-risk transaction",
            "data": {
                "amount": 50.00,
                "payment_method": "credit_card",
                "location": "New York, USA",
                "device_info": "desktop"
            }
        },
        {
            "name": "High-risk transaction",
            "data": {
                "amount": 5000.00,
                "payment_method": "bank_transfer",
                "location": "Nigeria",
                "device_info": "mobile"
            }
        },
        {
            "name": "Medium-risk transaction",
            "data": {
                "amount": 500.00,
                "payment_method": "paypal",
                "location": "London, UK",
                "device_info": "tablet"
            }
        }
    ]
    
    # Test prediction endpoint
    print("2. Testing fraud prediction endpoint...")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['name']}")
        print(f"   Data: {json.dumps(test_case['data'], indent=10)}")
        
        try:
            response = requests.post(
                f"{base_url}/api/predict",
                headers={'Content-Type': 'application/json'},
                json=test_case['data']
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Prediction successful")
                print(f"   Is Fraud: {result['is_fraud']}")
                print(f"   Fraud Probability: {result['fraud_probability']:.3f}")
                print(f"   Confidence: {result['confidence']:.3f}")
                print(f"   Risk Level: {result['risk_level']}")
            else:
                print(f"   ❌ Prediction failed: {response.status_code}")
                print(f"   Error: {response.text}")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n=== Test Complete ===")
    return True

if __name__ == "__main__":
    test_api()