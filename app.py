import os
from dotenv import load_dotenv   # ✅ ADD THIS

from flask import Flask, render_template, request, jsonify
from google import genai

load_dotenv()   # ✅ ADD THIS (must be before os.getenv)

app = Flask(__name__)

# Read API key safely
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not set. Check your .env file.")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"reply": "Please type something."})

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)