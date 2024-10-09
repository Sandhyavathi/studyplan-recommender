from flask import Flask, request, jsonify
from pymongo import MongoClient
import openai

app = Flask(__name__)

# Connect to MongoDB (replace with your MongoDB connection string)
client = MongoClient('mongodb+srv://sandhyavathi890:5DaeGniGuyjO0JKw@cluster0.lso1n.mongodb.net/education_system?retryWrites=true&w=majority')
db = client['education_system']

# Set up GPT API key
openai.api_key = 'your_openai_api_key'

# Endpoint to handle quiz submissions
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.get_json()

    # Extract the data
    student_id = data.get('student_id')
    answers = data.get('answers')

    # Calculate the score (example logic)
    score = calculate_score(answers)

    # Store the data in MongoDB
    db.student_data.insert_one({
        'student_id': student_id,
        'answers': answers,
        'score': score
    })

    # Generate a study plan using GPT
    study_plan = generate_study_plan(score)

    # Return the study plan as a response
    return jsonify({
        'student_id': student_id,
        'score': score,
        'study_plan': study_plan
    })

# Example function to calculate the score
def calculate_score(answers):
    correct_answers = ['A', 'B', 'C']  # Example correct answers
    score = sum([1 if answers[i] == correct_answers[i] else 0 for i in range(len(answers))])
    return (score / len(correct_answers)) * 100  # Convert to percentage

# Example function to generate study plan using GPT
def generate_study_plan(score):
    if score < 50:
        level = 'beginner'
    elif score < 75:
        level = 'intermediate'
    else:
        level = 'advanced'

    # Generate study plan using GPT
    prompt = f"Create a {level} study plan for a student who scored {score}% on a quiz."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)
