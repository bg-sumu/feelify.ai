from flask import Flask, render_template, Response, request, jsonify
import cv2
from deepface import DeepFace
import google.generativeai as genai
import random

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# Configure Google Generative AI for the chatbot
api_key = ""
genai.configure(api_key=api_key)
generation_config = {
    "temperature": 0.1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 200,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Create a new model
model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
convo = model.start_chat()

# Global variable to store detected emotion
detected_emotion = "neutral"

start_sentences = [
    "Hi there! How are you feeling today?",
    "Hello! I'm here to listen. What's on your mind?",
    "Hey, it's okay to share. How can I support you today?",
    "Hi! No pressure—just let me know how you're doing.",
    "Welcome! I'm here to help you feel heard. Want to talk?",
    "Hey, friend! Need a safe space to share what's on your mind?",
    "Hello! I'm all ears. How are things going today?",
    "Hi there! Whether it's a good or tough day, I'm here for you.",
    "Welcome! How can I help you feel better today?",
    "Hello! Let's chat—I'm here to listen and support you."
]

# Function to detect emotion using DeepFace
def detect_emotion(frame):
    try:
        # Resize the frame to ensure better performance and focus on the face area
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = DeepFace.analyze(rgb_frame, actions=['emotion'], enforce_detection=True)
        return result['dominant_emotion']
    except Exception as e:
        print("Error detecting emotion:", e)
        return "neutral"

# Function to generate video frames
def generate_frames():
    global detected_emotion
    while True:
        success, frame = camera.read()
        if not success:
            print("Camera not accessible")
            break
        else:
            # Detect emotion from the frame
            detected_emotion = detect_emotion(frame)

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Video feed route
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Get emotion route
@app.route('/get_emotion')
def get_emotion():
    global detected_emotion
    return jsonify(emotion=detected_emotion)

# Chatbot response route
@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        user_message = request.json.get("message")
        if user_message:
            response = convo.send_message(user_message)
            return jsonify(response=convo.last.text)
        else:
            start_sentence = random.choice(start_sentences)
            return jsonify(response=start_sentence)
    except Exception as e:
        print("Error generating chatbot response:", e)
        return jsonify(response="Sorry, I'm unable to respond at the moment.")

# Release camera on exit
@app.teardown_appcontext
def release_camera(exception=None):
    if camera.isOpened():
        camera.release()

if __name__ == "__main__":
    app.run(debug=True)
