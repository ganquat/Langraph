from app import create_app
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Make sure GOOGLE_API_KEY is loaded before trying to run the app,
    # as agents.py will raise an error if it's missing.
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        print("--------------------------------------------------------------------------")
        print("WARNING: GOOGLE_API_KEY is not set or is still the placeholder.")
        print("Please set your actual GOOGLE_API_KEY in the .env file.")
        print("The application will likely fail or not work as expected without it.")
        print("--------------------------------------------------------------------------")

    # Port can be configured via environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
