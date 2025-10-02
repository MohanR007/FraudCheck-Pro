# Test Cases for FraudCheck Pro - Enhanced Fraud Detection System

## Overview
This document contains comprehensive test cases for the FraudCheck Pro fraud detection system. These test cases cover various scenarios from low-risk legitimate transactions to high-risk fraud attempts.

## Test Environment Setup
- **Application URL**: http://localhost:5000
- **Required**: Enhanced model must be trained and loaded
- **Browser**: Chrome, Firefox, Safari, or Edge
- **Data**: Tests use real transaction scenarios

---

## 1. Low Risk Transactions (Expected: SAFE)

### Test Case 1.1: Regular Grocery Purchase
**Description**: Typical grocery store transaction during business hours
```json
{
  "amount": 87.45,
  "currency": "USD",
  "payment_method": "credit_card",
  "location": "New York",
  "country": "US",
  "device_info": "desktop",
  "customer_age": 35,
  "account_age": 1095,
  "daily_transactions": 1,
  "weekly_transactions": 4,
  "avg_transaction": 95.00,
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
```
**Expected Results**:
- Status: SAFE ✅
- Fraud Probability: < 20%
- Risk Level: Very Low or Low
- Confidence: > 80%

### Test Case 1.2: Coffee Shop Purchase
**Description**: Small transaction at a local coffee shop
```json
{
  "amount": 12.50,
  "currency": "USD",
  "payment_method": "debit_card",
  "location": "Seattle",
  "country": "US",
  "device_info": "mobile",
  "customer_age": 28,
  "account_age": 730,
  "daily_transactions": 2,
  "weekly_transactions": 8,
  "avg_transaction": 25.00,
  "merchant_category": "restaurant",
  "merchant_risk": "low",
  "ip_risk": 0,
  "vpn_usage": "no",
  "previous_fraud": "0",
  "international": "no",
  "weekend": "no",
  "transaction_time": "08:15",
  "transaction_date": "2025-01-02"
}
```
**Expected Results**:
- Status: SAFE ✅
- Fraud Probability: < 15%
- Risk Level: Very Low
- Confidence: > 85%

### Test Case 1.3: Gas Station Fill-up
**Description**: Regular gas station transaction
```json
{
  "amount": 45.75,
  "currency": "USD",
  "payment_method": "credit_card",
  "location": "Dallas",
  "country": "US",
  "device_info": "pos",
  "customer_age": 42,
  "account_age": 2190,
  "daily_transactions": 1,
  "weekly_transactions": 3,
  "avg_transaction": 50.00,
  "merchant_category": "gas_station",
  "merchant_risk": "low",
  "ip_risk": 1,
  "vpn_usage": "no",
  "previous_fraud": "0",
  "international": "no",
  "weekend": "yes",
  "transaction_time": "16:45",
  "transaction_date": "2025-01-04"
}
```
**Expected Results**:
- Status: SAFE ✅
- Fraud Probability: < 20%
- Risk Level: Low
- Confidence: > 80%

---

## 2. Medium Risk Transactions (Expected: SAFE with Caution)

### Test Case 2.1: Late Night Online Shopping
**Description**: Online purchase made late at night with higher amount
```json
{
  "amount": 299.99,
  "currency": "USD",
  "payment_method": "credit_card",
  "location": "Chicago",
  "country": "US",
  "device_info": "mobile",
  "customer_age": 24,
  "account_age": 180,
  "daily_transactions": 3,
  "weekly_transactions": 12,
  "avg_transaction": 150.00,
  "merchant_category": "online_shopping",
  "merchant_risk": "medium",
  "ip_risk": 3,
  "vpn_usage": "no",
  "previous_fraud": "0",
  "international": "no",
  "weekend": "yes",
  "transaction_time": "23:30",
  "transaction_date": "2025-01-05"
}
```
**Expected Results**:
- Status: SAFE ✅ (but with higher probability)
- Fraud Probability: 20-40%
- Risk Level: Medium
- Confidence: 60-80%

### Test Case 2.2: International Transaction
**Description**: Purchase made while traveling internationally
```json
{
  "amount": 150.00,
  "currency": "EUR",
  "payment_method": "credit_card",
  "location": "Paris",
  "country": "FR",
  "device_info": "mobile",
  "customer_age": 35,
  "account_age": 1095,
  "daily_transactions": 2,
  "weekly_transactions": 6,
  "avg_transaction": 120.00,
  "merchant_category": "restaurant",
  "merchant_risk": "low",
  "ip_risk": 4,
  "vpn_usage": "no",
  "previous_fraud": "0",
  "international": "yes",
  "weekend": "no",
  "transaction_time": "19:15",
  "transaction_date": "2025-01-02"
}
```
**Expected Results**:
- Status: SAFE ✅
- Fraud Probability: 25-45%
- Risk Level: Medium
- Confidence: 60-75%

### Test Case 2.3: Digital Wallet High Amount
**Description**: Large transaction using digital wallet
```json
{
  "amount": 750.00,
  "currency": "USD",
  "payment_method": "digital_wallet",
  "location": "Los Angeles",
  "country": "US",
  "device_info": "mobile",
  "customer_age": 29,
  "account_age": 365,
  "daily_transactions": 4,
  "weekly_transactions": 15,
  "avg_transaction": 200.00,
  "merchant_category": "retail",
  "merchant_risk": "medium",
  "ip_risk": 2,
  "vpn_usage": "yes",
  "previous_fraud": "0",
  "international": "no",
  "weekend": "no",
  "transaction_time": "15:30",
  "transaction_date": "2025-01-02"
}
```
**Expected Results**:
- Status: SAFE ✅ (borderline)
- Fraud Probability: 30-50%
- Risk Level: Medium
- Confidence: 50-70%

---

## 3. High Risk Transactions (Expected: FRAUD DETECTED)

### Test Case 3.1: High-Risk Country + Large Amount
**Description**: Large transaction from a high-risk country with suspicious patterns
```json
{
  "amount": 5000.00,
  "currency": "USD",
  "payment_method": "credit_card",
  "location": "Lagos",
  "country": "NG",
  "device_info": "mobile",
  "customer_age": 21,
  "account_age": 15,
  "daily_transactions": 8,
  "weekly_transactions": 35,
  "avg_transaction": 100.00,
  "merchant_category": "online_shopping",
  "merchant_risk": "medium",
  "ip_risk": 8,
  "vpn_usage": "yes",
  "previous_fraud": "1",
  "international": "yes",
  "weekend": "yes",
  "transaction_time": "03:15",
  "transaction_date": "2025-01-06"
}
```
**Expected Results**:
- Status: FRAUD DETECTED 🚨
- Fraud Probability: > 70%
- Risk Level: Very High
- Confidence: > 80%
- Fraud Reasons: High-risk country, Large amount, New account, High frequency, Unusual time

### Test Case 3.2: Cryptocurrency Gambling
**Description**: Large cryptocurrency transaction for gambling
```json
{
  "amount": 2500.00,
  "currency": "USD",
  "payment_method": "cryptocurrency",
  "location": "Bucharest",
  "country": "RO",
  "device_info": "desktop",
  "customer_age": 19,
  "account_age": 7,
  "daily_transactions": 12,
  "weekly_transactions": 50,
  "avg_transaction": 300.00,
  "merchant_category": "gambling",
  "merchant_risk": "high",
  "ip_risk": 9,
  "vpn_usage": "yes",
  "previous_fraud": "2",
  "international": "yes",
  "weekend": "yes",
  "transaction_time": "02:45",
  "transaction_date": "2025-01-06"
}
```
**Expected Results**:
- Status: FRAUD DETECTED 🚨
- Fraud Probability: > 85%
- Risk Level: Very High
- Confidence: > 90%
- Fraud Reasons: Cryptocurrency, High-risk country, Gambling, Very new account, Multiple previous fraud

### Test Case 3.3: Card Testing Pattern
**Description**: Multiple small transactions typical of card testing
```json
{
  "amount": 1.00,
  "currency": "USD",
  "payment_method": "credit_card",
  "location": "Moscow",
  "country": "RU",
  "device_info": "mobile",
  "customer_age": 18,
  "account_age": 1,
  "daily_transactions": 25,
  "weekly_transactions": 100,
  "avg_transaction": 5.00,
  "merchant_category": "online_shopping",
  "merchant_risk": "medium",
  "ip_risk": 10,
  "vpn_usage": "yes",
  "previous_fraud": "0",
  "international": "yes",
  "weekend": "no",
  "transaction_time": "04:30",
  "transaction_date": "2025-01-02"
}
```
**Expected Results**:
- Status: FRAUD DETECTED 🚨
- Fraud Probability: > 75%
- Risk Level: Very High
- Confidence: > 85%
- Fraud Reasons: High-risk country, Very new account, Extremely high frequency, Unusual time

---

## 4. Edge Cases and Boundary Tests

### Test Case 4.1: Exactly $5000 Transaction
**Description**: Test the high-amount threshold boundary
```json
{
  "amount": 5000.00,
  "currency": "USD",
  "payment_method": "bank_transfer",
  "location": "New York",
  "country": "US",
  "device_info": "desktop",
  "customer_age": 45,
  "account_age": 3650,
  "daily_transactions": 1,
  "weekly_transactions": 2,
  "avg_transaction": 4800.00,
  "merchant_category": "retail",
  "merchant_risk": "low",
  "ip_risk": 0,
  "vpn_usage": "no",
  "previous_fraud": "0",
  "international": "no",
  "weekend": "no",
  "transaction_time": "10:00",
  "transaction_date": "2025-01-02"
}
```
**Expected Results**:
- Status: May be SAFE or flagged depending on other factors
- Should trigger high-amount flag in model

### Test Case 4.2: Weekend vs Weekday Same Transaction
**Description**: Test the same transaction on weekend vs weekday
```json
{
  "amount": 200.00,
  "currency": "USD",
  "payment_method": "credit_card",
  "location": "Denver",
  "country": "US",
  "device_info": "mobile",
  "customer_age": 30,
  "account_age": 365,
  "daily_transactions": 3,
  "weekly_transactions": 10,
  "avg_transaction": 180.00,
  "merchant_category": "entertainment",
  "merchant_risk": "medium",
  "ip_risk": 2,
  "vpn_usage": "no",
  "previous_fraud": "0",
  "international": "no",
  "weekend": "yes", // Change to "no" for weekday test
  "transaction_time": "20:00",
  "transaction_date": "2025-01-05" // Saturday
}
```
**Expected Results**:
- Weekend version should have slightly higher risk
- Compare fraud probabilities between weekend/weekday versions

### Test Case 4.3: New Account (30 days) Boundary
**Description**: Test new account threshold
```json
{
  "amount": 500.00,
  "currency": "USD",
  "payment_method": "credit_card",
  "location": "Miami",
  "country": "US",
  "device_info": "mobile",
  "customer_age": 25,
  "account_age": 30, // Exactly at boundary
  "daily_transactions": 2,
  "weekly_transactions": 8,
  "avg_transaction": 400.00,
  "merchant_category": "retail",
  "merchant_risk": "low",
  "ip_risk": 1,
  "vpn_usage": "no",
  "previous_fraud": "0",
  "international": "no",
  "weekend": "no",
  "transaction_time": "14:00",
  "transaction_date": "2025-01-02"
}
```

---

## 5. Performance Tests

### Test Case 5.1: Response Time Test
**Description**: Measure API response times
- **Target**: < 100ms response time
- **Method**: Use browser DevTools Network tab or test_enhanced_api.py
- **Acceptance**: All predictions should complete within 100ms

### Test Case 5.2: Concurrent Transactions
**Description**: Test multiple simultaneous predictions
- **Method**: Open multiple browser tabs and submit transactions simultaneously
- **Acceptance**: All should process without errors

### Test Case 5.3: Large Dataset Handling
**Description**: Test with accumulated transaction history
- **Method**: Perform 50+ transactions and verify charts/statistics update correctly
- **Acceptance**: UI should remain responsive

---

## 6. UI/UX Test Cases

### Test Case 6.1: Navigation Testing
**Description**: Test all navigation links work correctly
- **Steps**:
  1. Click Home tab → Should show dashboard
  2. Click Detector tab → Should show fraud detection form
  3. Click History tab → Should show transaction history
  4. Click Analytics tab → Should show charts and statistics
- **Acceptance**: All pages load without errors

### Test Case 6.2: Form Validation
**Description**: Test form validation works
- **Steps**:
  1. Try submitting empty form
  2. Enter invalid amounts (negative, non-numeric)
  3. Leave required fields empty
- **Acceptance**: Appropriate validation messages appear

### Test Case 6.3: Responsive Design
**Description**: Test on different screen sizes
- **Steps**:
  1. Test on desktop (1920x1080)
  2. Test on tablet (768x1024)
  3. Test on mobile (375x667)
- **Acceptance**: Layout adapts appropriately

### Test Case 6.4: Charts Update
**Description**: Verify charts update with real data
- **Steps**:
  1. Note current chart data
  2. Submit a new transaction
  3. Check analytics page
- **Acceptance**: Charts should reflect new transaction data

---

## 7. Data Persistence Tests

### Test Case 7.1: Browser Refresh
**Description**: Verify data persists after refresh
- **Steps**:
  1. Submit several transactions
  2. Refresh browser
  3. Check history tab
- **Acceptance**: Transaction history should be preserved

### Test Case 7.2: Clear History Function
**Description**: Test history clearing works
- **Steps**:
  1. Submit transactions
  2. Click "Clear History" button
  3. Confirm action
- **Acceptance**: All history should be cleared, charts should reset

---

## 8. Error Handling Tests

### Test Case 8.1: Server Unavailable
**Description**: Test behavior when backend is down
- **Steps**:
  1. Stop the Flask server
  2. Try submitting a transaction
- **Acceptance**: Should show error message gracefully

### Test Case 8.2: Invalid API Response
**Description**: Test handling of malformed responses
- **Method**: Mock invalid API responses if possible
- **Acceptance**: Should handle errors without breaking UI

---

## 9. Security Tests

### Test Case 9.1: Input Sanitization
**Description**: Test with potentially malicious inputs
- **Test Inputs**:
  - `<script>alert('xss')</script>` in location field
  - SQL injection attempts in text fields
  - Very large numbers in amount field
- **Acceptance**: Inputs should be sanitized, no code execution

### Test Case 9.2: CORS Testing
**Description**: Verify CORS is properly configured
- **Method**: Test API calls from different origins
- **Acceptance**: Should work from intended origins only

---

## 10. Automated Test Script

To run automated tests, use the provided `test_enhanced_api.py` script:

```bash
# Ensure server is running first
run_enhanced.bat

# In another terminal, run:
python test_enhanced_api.py
```

This script tests:
- Health endpoint functionality
- Fraud prediction with low, medium, and high-risk scenarios
- Statistics endpoint
- Response time measurements
- Error handling

---

## Test Execution Checklist

### Before Testing:
- [ ] Enhanced model is created and loaded
- [ ] Flask server is running on localhost:5000
- [ ] Browser is open to http://localhost:5000
- [ ] Clear any existing transaction history if needed

### During Testing:
- [ ] Record actual vs expected results
- [ ] Note any UI/UX issues
- [ ] Monitor browser console for errors
- [ ] Check network tab for API response times

### After Testing:
- [ ] Document any bugs or issues found
- [ ] Verify all test cases pass
- [ ] Check performance metrics
- [ ] Confirm data persistence works correctly

## Expected Overall System Performance:
- **Accuracy**: > 90% fraud detection accuracy
- **Response Time**: < 100ms average
- **Uptime**: 99.9% availability
- **User Experience**: Intuitive and responsive interface
- **Data Integrity**: All transactions properly stored and retrieved