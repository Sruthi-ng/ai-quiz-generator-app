# backend/app.py
import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS # To allow our frontend to call the backend
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Allow requests from our frontend (we'll lock this down later)
CORS(app)

# Configure the Gemini API client
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    """
    Generates a 3-question quiz on a given topic using the Gemini API.
    Expects a JSON payload with a "topic" key.
    """
    if model is None:
        return jsonify({"error": "Gemini API not configured"}), 500

    # Get the topic from the frontend request
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({"error": "Topic not provided"}), 400
    topic = data['topic']

    # This is our prompt. We are asking the AI to return a specific JSON structure.
    # This is called "prompt engineering".
    prompt = f"""
    Generate a 3-question multiple-choice quiz about {topic}.
    Provide the response as a valid JSON object with a single key "questions".
    The value should be a list of objects, where each object has:
    - "question_text": The question text.
    - "options": A list of 4 strings.
    - "correct_answer": The string of the correct answer.

    Example format:
    {{
      "questions": [
        {{
          "question_text": "What is the capital of France?",
          "options": ["London", "Berlin", "Paris", "Madrid"],
          "correct_answer": "Paris"
        }}
      ]
    }}
    """

    try:
        # Send the prompt to the Gemini model
        response = model.generate_content(prompt)

        # Clean up the response to be valid JSON
        # Sometimes the model returns the JSON wrapped in ```json ... ```
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")

        return cleaned_response, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
