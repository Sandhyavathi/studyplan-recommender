from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from transformers import pipeline
import os

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient('mongodb+srv://sandhyavathi890:5DaeGniGuyjO0JKw@cluster0.lso1n.mongodb.net/education_system?retryWrites=true&w=majority')
db = client['education_system']

# Hugging Face model setup
generator = pipeline("text-generation", model="gpt2")  # Use GPT-2 for study plan generation

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    student_id = data.get('student_id')
    score = data.get('score')
    answers = data.get('answers')

    # Generate a study plan based on the student's score
    study_plan = generate_study_plan(score, answers)

    # Store data in MongoDB
    db.student_data.insert_one({
        'student_id': student_id,
        'score': score,
        'answers': answers,
        'study_plan': study_plan
    })

    return jsonify({'message': 'Data processed successfully', 'study_plan': study_plan}), 200

def generate_study_plan(score, answers):
    prompt = f"Generate a study plan for a student who scored {score}. The student's answers were: {answers}."
    generated = generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
    return generated

if __name__ == '__main__':
    app.run(port=5000, debug=True)
