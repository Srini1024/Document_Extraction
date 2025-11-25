import os
from dotenv import load_dotenv

load_dotenv()

# Test 1: Check if API key is loaded
api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key loaded: {api_key[:10]}..." if api_key else "API Key NOT found!")
print()

# Test 2: List available models using google-generativeai
try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    
    print("=" * 60)
    print("AVAILABLE MODELS:")
    print("=" * 60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description[:100]}...")
            print()
    
except Exception as e:
    print(f"Error listing models: {e}")

print()
print("=" * 60)
print("TEST: Try generating with a model")
print("=" * 60)

# Test 3: Try generating content with different models
test_models = ["gemini-pro", "gemini-1.5-flash", "gemini-1.5-pro"]

for model_name in test_models:
    try:
        print(f"\nTrying model: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Hello' in one word")
        print(f"✅ SUCCESS! Response: {response.text}")
        print(f"   --> Use this model: {model_name}")
        break
    except Exception as e:
        print(f"❌ Failed: {e}")

print("\n" + "=" * 60)

