from flask import Flask, render_template, Response, jsonify, request
import cv2
import random
import google.generativeai as genai

# Flask app initialization
app = Flask(__name__)

# Google Generative AI configuration
GOOGLE_API_KEY = "AIzaSyBLfrGUrdjzS8gOezGdrIYxs831cb_sQok"  # Set your API key here
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 200,
}

# Safety settings for the model
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

# Create a new Generative AI model instance
model = genai.GenerativeModel('gemini-1.5-pro', generation_config=generation_config)

# Route to capture video feed
def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Mock route for emotion detection
@app.route('/get_emotion')
def get_emotion():
    emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    return jsonify({'emotion': random.choice(emotions)})

# Chatbot route using the Generative AI model
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json['message']
    
    # Start conversation with the generative model
    convo = model.start_chat()
    response = convo.send_message(user_message)

    # Respond with the chatbot's generated response
    return jsonify({'response': convo.last.text})

# Main route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
