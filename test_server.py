#!/usr/bin/env python3
"""
Test script for CrewAI server
Tests the /predict endpoint with a simple query
"""
import requests
import json
import sys

# Server configuration
SERVER_URL = 'http://0.0.0.0:8000'

def test_server_health():
    """Test if server is running"""
    try:
        response = requests.get(f"{SERVER_URL}/")
        print("✅ Server health check: PASSED")
        print(f"   Status code: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Server health check: FAILED")
        print(f"   Error: {e}")
        return False

def test_predict_endpoint():
    """Test the /predict endpoint with a sample query"""
    print("\n" + "="*50)
    print("Testing /predict endpoint")
    print("="*50)
    
    test_query = "What is artificial intelligence?"
    
    payload = {
        "query": test_query
    }
    
    print(f"\n📤 Sending query: '{test_query}'")
    print("⏳ Waiting for response (this may take a moment)...\n")
    
    try:
        response = requests.post(
            f"{SERVER_URL}/predict", 
            json=payload,
            timeout=60  # 60 second timeout
        )
        response.raise_for_status()
        
        result = response.json()
        
        print("✅ Request successful!")
        print(f"\n📊 Response structure:")
        print(json.dumps(result, indent=2)[:500] + "..." if len(json.dumps(result, indent=2)) > 500 else json.dumps(result, indent=2))
        
        # Check if output exists
        if 'output' in result:
            print("\n✅ Output field exists")
            if 'raw' in result['output']:
                print("✅ Raw output exists")
                print(f"\n📝 Response preview:")
                print("-" * 50)
                raw_output = str(result['output']['raw'])
                print(raw_output[:300] + "..." if len(raw_output) > 300 else raw_output)
                print("-" * 50)
        else:
            print("\n⚠️  Warning: 'output' field not found in response")
        
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Test FAILED: Request timed out after 60 seconds")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Test FAILED: Request error")
        print(f"   Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response status: {e.response.status_code}")
            print(f"   Response body: {e.response.text[:200]}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Test FAILED: Invalid JSON response")
        print(f"   Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("CrewAI Server Test Suite")
    print("="*50 + "\n")
    
    # Test 1: Server health
    health_ok = test_server_health()
    if not health_ok:
        print("\n❌ Server is not running. Please start the server first.")
        print("   Run: python server.py")
        sys.exit(1)
    
    # Test 2: Predict endpoint
    predict_ok = test_predict_endpoint()
    
    # Summary
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    print(f"Health Check: {'✅ PASSED' if health_ok else '❌ FAILED'}")
    print(f"Predict Endpoint: {'✅ PASSED' if predict_ok else '❌ FAILED'}")
    
    if health_ok and predict_ok:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
