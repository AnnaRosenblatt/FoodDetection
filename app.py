from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_chatbot_response(user_message):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You are an empathetic nutrition chatbot for students at school. "
                    "Give supportive, practical, simple advice about healthy eating. "
                    "Answer questions about foods like chicken tenders, tacos, chicken sandwiches, fries, and quesadillas. "
                    "Give basic nutrition facts and realistic healthy habits. "
                    "Do not promote extreme dieting."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.output_text

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    reply = get_chatbot_response(user_message)
    return jsonify({'reply': reply})

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/info")
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run(debug=True)