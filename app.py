from flask import Flask, request, jsonify
from pymongo import MongoClient
import openai
import os

app = Flask(__name__)

# MongoDB connection (use environment variables for secure deployment)
mongodb_uri = os.environ.get('MONGODB_URI')
client = MongoClient(mongodb_uri)
db = client.education_system

# OpenAI API key from environment variable
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

    # Logic to generate a study plan based on the score
    study_plan = generate_study_plan(score)

    # Store in MongoDB
    db.student_data.insert_one({
        'student_id': student_id,
        'score': score,
        'answers': answers,
        'study_plan': study_plan
    })

    return jsonify({'message': 'Data processed successfully'}), 200

def generate_study_plan(score):
    if score < 50:
        return "Beginner Study Plan."
    elif score < 75:
        return "Intermediate Study Plan."
    else:
        return "Advanced Study Plan."

if __name__ == '__main__':
    app.run(port=5000, debug=True)

