from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
import os

app = Flask(__name__)

# MongoDB connection
mongodb_uri = os.environ.get('MONGODB_URI')
client = MongoClient(mongodb_uri)
db = client.education_system

# OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    student_id = data.get('student_id')
    score = data.get('score')
    answers = data.get('answers')

    # Generate study plan based on the score and answers
    study_plan = generate_study_plan(score, answers)

    # Save data to MongoDB (optional)
    db.student_data.insert_one({
        'student_id': student_id,
        'score': score,
        'answers': answers,
        'study_plan': study_plan
    })

    return jsonify({
        'message': 'Data processed successfully',
        'study_plan': study_plan
    }), 200

def generate_study_plan(score, answers):
    prompt = f"Generate a study plan for a student who scored {score}. The student's answers were: {answers}."
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"
    }
    data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7
    }
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        study_plan = response.json()['choices'][0]['text'].strip()
        return study_plan
    else:
        return "Error generating study plan"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
