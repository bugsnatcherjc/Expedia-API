#!/usr/bin/env python3
"""
Flight API Test Runner
Uses flight_test_parameters.json to test all flight endpoints
"""

import json
import requests
import time
from urllib.parse import urlencode

def load_test_parameters():
    """Load test parameters from JSON file"""
    with open('flight_test_parameters.json', 'r') as f:
        return json.load(f)

def test_endpoint(base_url, endpoint, method, test_case, flight_id=None, flight_number=None):
    """Test a single endpoint with given parameters"""
    # Build URL
    if flight_id:
        url = f"{base_url}{endpoint.replace('{flight_id}', flight_id)}"
        params = {}
    elif flight_number:
        url = f"{base_url}{endpoint.replace('{flight_number}', flight_number)}"
        params = {}
    else:
        url = f"{base_url}{endpoint}"
        params = test_case.get('params', {})
    
    try:
        # Make request
        if method == 'GET':
            response = requests.get(url, params=params, timeout=10)
        else:
            response = requests.request(method, url, json=params, timeout=10)
        
        # Parse response
        try:
            data = response.json()
            flight_count = len(data.get('flights', [])) if 'flights' in data else ('flight' in data and 1 or 0)
        except:
            flight_count = 0
            data = {"error": "Invalid JSON response"}
        
        return {
            'status_code': response.status_code,
            'success': response.status_code == 200,
            'flight_count': flight_count,
            'response_size': len(response.text),
            'url': url,
            'params': params
        }
    
    except requests.exceptions.RequestException as e:
        return {
            'status_code': 0,
            'success': False,
            'error': str(e),
            'url': url,
            'params': params
        }

def run_tests():
    """Run all flight API tests"""
    params = load_test_parameters()
    base_url = params['base_url']
    
    print("🛫 Flight API Test Runner")
    print("=" * 60)
    print(f"Base URL: {base_url}")
    print()
    
    total_tests = 0
    passed_tests = 0
    
    # Test each endpoint category
    for category, config in params['endpoints'].items():
        print(f"📂 {category.upper().replace('_', ' ')} TESTS")
        print("-" * 40)
        
        endpoint = config['endpoint']
        method = config['method']
        test_cases = config['test_cases']
        
        for i, test_case in enumerate(test_cases, 1):
            test_name = test_case['name']
            print(f"{i}. {test_name}")
            
            # Determine test parameters
            flight_id = test_case.get('flight_id')
            flight_number = test_case.get('flight_number')
            
            # Run test
            result = test_endpoint(base_url, endpoint, method, test_case, flight_id, flight_number)
            total_tests += 1
            
            # Display result
            if result['success']:
                passed_tests += 1
                status = "✅ PASS"
                if result.get('flight_count', 0) > 0:
                    status += f" ({result['flight_count']} flights found)"
            else:
                status = f"❌ FAIL (Status: {result['status_code']})"
                if 'error' in result:
                    status += f" - {result['error']}"
            
            print(f"   {status}")
            
            # Show URL for debugging
            if result.get('params'):
                query_string = urlencode(result['params'])
                print(f"   URL: {result['url']}?{query_string}")
            else:
                print(f"   URL: {result['url']}")
            
            print()
            
            # Small delay between requests
            time.sleep(0.1)
        
        print()
    
    # Summary
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the server and test parameters.")

def test_specific_category(category_name):
    """Test only a specific category of endpoints"""
    params = load_test_parameters()
    
    if category_name not in params['endpoints']:
        print(f"❌ Category '{category_name}' not found!")
        print(f"Available categories: {', '.join(params['endpoints'].keys())}")
        return
    
    # Create a subset with only the requested category
    subset_params = {
        'base_url': params['base_url'],
        'endpoints': {category_name: params['endpoints'][category_name]}
    }
    
    # Temporarily replace full params
    original_load = load_test_parameters
    global load_test_parameters
    load_test_parameters = lambda: subset_params
    
    try:
        run_tests()
    finally:
        load_test_parameters = original_load

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test specific category
        category = sys.argv[1]
        test_specific_category(category)
    else:
        # Test all categories
        run_tests()
