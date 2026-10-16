import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("Set GOOGLE_API_KEY or GEMINI_API_KEY in your local .env file.")

genai.configure(api_key=api_key)

print("\n=== Testing API Key ===\n")
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
    print("\n✅ API Key is VALID!")
except Exception as e:
    print(f"❌ Error: {e}")