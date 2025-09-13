from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from textblob import TextBlob

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Connect to MongoDB (running on port 27017)
client = MongoClient("mongodb://localhost:27017/")
db = client["taskmanager"]
tasks = db["tasks"]

# Home route → serves the frontend page
@app.route("/")
def home():
    return render_template("index.html")

# Add Task (with AI/NLP processing)
@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    user_input = data.get("title")

    # AI/NLP: Extract title + description automatically
    blob = TextBlob(user_input)
    sentences = blob.sentences

    if len(sentences) > 1:
        title = str(sentences[0])
        description = " ".join([str(s) for s in sentences[1:]])
    else:
        title = user_input
        description = data.get("description", "")

    task = {
        "title": title,
        "description": description,
        "status": "Todo"
    }
    tasks.insert_one(task)
    return jsonify({"message": "Task added successfully with AI"}), 201

# Get All Tasks
@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    all_tasks = list(tasks.find({}, {"_id": 0}))  # hide Mongo _id
    return jsonify(all_tasks), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
