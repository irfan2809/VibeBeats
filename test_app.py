#!/usr/bin/env python3
"""
Simple test script to verify the Mood-to-Music Recommender application
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    try:
        from flask import Flask
        from flask_cors import CORS
        import openai
        import requests
        from dotenv import load_dotenv
        import json
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_structure():
    """Test if the application structure is correct"""
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_flask_app():
    """Test if Flask app can be created without errors"""
    try:
        # Import the app
        from app import app
        
        # Test basic app functionality
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Flask app created and basic route working")
                return True
            else:
                print(f"❌ Flask app route returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Mood-to-Music Recommender Application")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("File Structure", test_app_structure),
        ("Flask Application", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n🚀 To start the application:")
        print("1. Set up your OpenAI API key in a .env file")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 