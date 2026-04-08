import google.generativeai as genai
import os
import streamlit as st

# Try to get API key from secrets
try:
    if hasattr(st, 'secrets'):
        api_key = st.secrets.get('GEMINI_API_KEY', None)
    else:
        api_key = os.environ.get('GEMINI_API_KEY')
except:
    api_key = os.environ.get('GEMINI_API_KEY')

if not api_key:
    print("❌ No API key found!")
    print("\nPlease set your API key in one of these ways:")
    print("1. Add to .streamlit/secrets.toml:")
    print('   GEMINI_API_KEY = "your-key-here"')
    print("\n2. Or set environment variable:")
    print('   export GEMINI_API_KEY="your-key-here"')
    exit(1)

print(f"✅ API Key found: {api_key[:10]}...")

# Configure and list models
genai.configure(api_key=api_key)

print("\n📋 Available Gemini Models:\n")
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description}")
            print()
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("\nTrying common model names...")
    
    # Try common models
    for model_name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro', 'models/gemini-1.5-flash']:
        try:
            print(f"\nTesting: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello'")
            print(f"✅ {model_name} works!")
            print(f"Response: {response.text}")
            break
        except Exception as e:
            print(f"❌ {model_name} failed: {str(e)[:100]}")
