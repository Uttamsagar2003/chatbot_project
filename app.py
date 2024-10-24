from flask import Flask, request, jsonify
from utils import extract_course_data, create_vector_store

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Course Chatbot!"

@app.route("/courses", methods=["GET"])
def get_courses():
    course_data = extract_course_data()
    vector_store = create_vector_store(course_data)
    
    if vector_store is not None:
        return jsonify({"message": "Courses loaded successfully!", "courses": course_data}), 200
    else:
        return jsonify({"message": "Failed to load courses."}), 500

if __name__ == "__main__":
    app.run(debug=True)
