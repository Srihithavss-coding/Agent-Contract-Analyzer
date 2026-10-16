import google.generativeai as genai

# Paste your NEW API key here
API_KEY = "AIzaSyDxGk1JhAqpjwrKqeYqXyygGqdbJaN7pjY"  # Your actual key

genai.configure(api_key=API_KEY)

print("\n=== Testing API Key ===\n")
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
    print("\n✅ API Key is VALID!")
except Exception as e:
    print(f"❌ Error: {e}")