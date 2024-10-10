from flask import Flask, request, jsonify
from pymongo import MongoClient
import openai
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

    # Logic to generate a study plan based on the score
    study_plan = generate_study_plan(score)

    # Generate recommendations from GPT
    recommendations = generate_recommendations(student_id, score, answers)

    # Store in MongoDB
    db.student_data.insert_one({
        'student_id': student_id,
        'score': score,
        'answers': answers,
        'study_plan': study_plan,
        'recommendations': recommendations
    })

    return jsonify({
        'message': 'Data processed successfully',
        'study_plan': study_plan,
        'recommendations': recommendations
    }), 200

def generate_study_plan(score):
    if score < 50:
        return "Beginner Study Plan."
    elif score < 75:
        return "Intermediate Study Plan."
    else:
        return "Advanced Study Plan."

def generate_recommendations(student_id, score, answers):
    prompt = f"Generate study recommendations for student {student_id} who scored {score}. The student's answers were: {answers}. Provide tailored study resources and strategies."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        recommendations = response['choices'][0]['message']['content'].strip()
        return recommendations
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
