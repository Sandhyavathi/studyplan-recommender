import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# MongoDB connection
mongodb_uri = os.environ.get('mongodb+srv://sandhyavathi890:5DaeGniGuyjO0JKw@cluster0.lso1n.mongodb.net/education_system?retryWrites=true&w=majority')
client = MongoClient(mongodb_uri)
db = client.education_system

# Load the Hugging Face model for text generation
generator = pipeline("text-generation", model="distilgpt2")# Change to your preferred model

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

    # Generate recommendations using Hugging Face model
    recommendations = generator(f"Generate a study plan for a student who scored {score}. The student's answers were: {answers}.", max_length=50)

    # Store in MongoDB
    db.student_data.insert_one({
        'student_id': student_id,
        'score': score,
        'answers': answers,
        'study_plan': study_plan,
        'recommendations': recommendations[0]['generated_text']
    })

    return jsonify({'message': 'Data processed successfully', 'study_plan': study_plan, 'recommendations': recommendations[0]['generated_text']}), 200

def generate_study_plan(score):
    if score < 50:
        return "Beginner Study Plan."
    elif score < 75:
        return "Intermediate Study Plan."
    else:
        return "Advanced Study Plan."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
