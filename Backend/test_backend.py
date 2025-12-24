#!/usr/bin/env python3
"""
Test script for Feedback Analyzer backend
"""
import requests
import json
import time
import sys

def test_backend():
    base_url = "http://127.0.0.1:5500"
    
    print("🚀 Testing Feedback Analyzer Backend")
    print("=" * 50)
    
    # Test 1: Health check via data-view
    print("\n📊 Test 1: Database viewer...")
    try:
        response = requests.get(f"{base_url}/api/data-view", timeout=5)
        if response.status_code == 200:
            print("✅ Database viewer working")
        else:
            print(f"❌ Database viewer failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Database viewer connection failed: {e}")
    
    # Test 2: Analyze endpoint
    print("\n🤖 Test 2: Feedback analysis...")
    try:
        test_feedback = "This product is amazing! I love it!"
        response = requests.post(f"{base_url}/api/analyze", 
                               json={"feedback": test_feedback}, 
                               timeout=5)
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis working")
            print(f"   Feedback: {result.get('feedback', 'N/A')}")
            print(f"   Sentiment: {result.get('sentiment', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Analysis connection failed: {e}")
    
    # Test 3: User registration
    print("\n👤 Test 3: User registration...")
    try:
        user_data = {
            "email": "testuser@example.com",
            "password": "testpass123",
            "name": "Test User"
        }
        response = requests.post(f"{base_url}/api/auth/register", 
                               json=user_data, 
                               timeout=5)
        if response.status_code == 201:
            result = response.json()
            print("✅ Registration working")
            print(f"   User: {result.get('user', {}).get('email', 'N/A')}")
            token = result.get('token')
            if token:
                print("   Token received ✓")
        else:
            result = response.json()
            if "already exists" in result.get('error', ''):
                print("⚠️  User already exists (expected)")
            else:
                print(f"❌ Registration failed: {response.status_code}")
                print(f"   Response: {result}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Registration connection failed: {e}")
    
    # Test 4: User login with test user
    print("\n🔐 Test 4: User login...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        response = requests.post(f"{base_url}/api/auth/login", 
                               json=login_data, 
                               timeout=5)
        if response.status_code == 200:
            result = response.json()
            print("✅ Login working")
            print(f"   User: {result.get('user', {}).get('email', 'N/A')}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            result = response.json()
            print(f"   Error: {result.get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Login connection failed: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Backend testing complete!")

if __name__ == "__main__":
    test_backend()