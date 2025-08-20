"""
Test script to demonstrate the agentic fitness chatbot functionality
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_fitness_agent():
    # Test 1: Generate a workout plan
    print("=== Test 1: Generate Workout Plan ===")
    chat_request = {
        "message": "I want to create a workout plan. I'm a beginner, want to lose weight, and can work out 4 days a week with basic equipment at home.",
        "user_id": "test_user_123"
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=chat_request)
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['response'][:500]}...")
        session_id = result['session_id']
        print(f"Session ID: {session_id}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return
    
    # Test 2: Save the workout plan
    print("\n=== Test 2: Save Workout Plan ===")
    save_request = {
        "message": "Please save this workout plan for me.",
        "user_id": "test_user_123",
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=save_request)
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['response']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    # Test 3: Generate a nutrition plan
    print("\n=== Test 3: Generate Nutrition Plan ===")
    nutrition_request = {
        "message": "Can you create a nutrition plan for me? I'm 180 pounds, want to lose weight to 160 pounds, and I'm moderately active.",
        "user_id": "test_user_123",
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=nutrition_request)
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['response'][:500]}...")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    # Test 4: Save the nutrition plan
    print("\n=== Test 4: Save Nutrition Plan ===")
    save_nutrition_request = {
        "message": "Please save this nutrition plan too.",
        "user_id": "test_user_123",
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=save_nutrition_request)
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['response']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    # Test 5: Retrieve saved plans
    print("\n=== Test 5: Retrieve Saved Plans ===")
    retrieve_request = {
        "message": "Can you show me all my saved fitness plans?",
        "user_id": "test_user_123",
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=retrieve_request)
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['response']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    # Test 6: Direct API endpoint for fitness plans
    print("\n=== Test 6: Direct API Endpoint ===")
    response = requests.get(f"{BASE_URL}/fitness-plans/test_user_123")
    if response.status_code == 200:
        plans = response.json()
        print(f"Found {len(plans['plans'])} saved plans")
        for plan in plans['plans']:
            print(f"- {plan['plan_name']} ({plan['plan_type']})")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("Testing Agentic Fitness Chatbot...")
    print("Make sure the server is running at http://127.0.0.1:8000")
    print("You need to set your OpenAI API key in the .env file")
    print()
    
    # Test if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Server is running")
            test_fitness_agent()
        else:
            print("✗ Server health check failed")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure it's running.")
