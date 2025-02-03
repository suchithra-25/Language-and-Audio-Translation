from flask import Flask, request, jsonify, session
from flask_cors import CORS
from googletrans import Translator, LANGUAGES
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)
translator = Translator()
app.secret_key = "your_secret_key"

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_db"
mongo = PyMongo(app)

# Enable CORS
CORS(app)

@app.route('/test')
def test_db():
    user_count = mongo.db.users.count_documents({})
    return {"message": f"Connected to MongoDB! Users Count: {user_count}"}


# Register API
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Check if username already exists
    if mongo.db.users.find_one({"username": username}):
        return jsonify({"message": "Username already exists"}), 400

    # Hash password and save user
    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "Registration successful"}), 201

# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Check if user exists
    user = mongo.db.users.find_one({"username": username})
    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid username or password"}), 401

# Logout API
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"}), 200


@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    source_lang = data.get('sourceLang', 'auto')  # Default to auto-detection
    target_lang = data.get('targetLang')

    if not text or not target_lang:
        return jsonify({"error": "Invalid input"}), 400

    try:
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return jsonify({"translatedText": translation.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/languages', methods=['GET'])
def get_languages():
    # Return a dictionary of language codes and their names
    return jsonify(LANGUAGES)

@app.route('/audio-translate', methods=['POST'])
def audio_translate():
    data = request.get_json()
    text = data.get("text")
    source_lang = data.get("source_language")
    target_lang = data.get("target_language")

    try:
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return jsonify({"translated_text": translation.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


