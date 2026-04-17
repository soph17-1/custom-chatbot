from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load local .env file for testing
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a virtual customer support assistant for the company 'MyBusiness'.
Your goal is to help users with information about our services: web development, digital marketing, and SEO.
If a user asks something unrelated to these services (for example: politics, recipes, history),
politely apologize and tell them that your knowledge is limited only to the services of 'MyBusiness'.
Be concise, clear, polite, and professional.
"""

# ADDED FOR LOCAL TESTING: Serve the HTML file
@app.route('/')
def home():
    with open('index.html', 'r', encoding='utf-8') as file:
        return file.read()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_messages = data.get('messages', [])
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + user_messages

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the server on port 5000
    app.run(host='0.0.0.0', port=5000)