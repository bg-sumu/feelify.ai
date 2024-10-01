from flask import Flask, render_template, Response, jsonify, request
import cv2
import random
import google.generativeai as genai
from google_api_key import google_api_key

# Flask app initialization
app = Flask(__name__)

# Google Generative AI configuration
GOOGLE_API_KEY = google_api_key 
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
model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config,
                              system_instruction= "I want you to provide mental health and emotional support to students using your natural language understanding and empathy. You should respond in a friendly, non-judgmental way, always showing patience and understanding. Be inclusive, recognizing that students come from diverse cultural and social backgrounds, and personalize your responses to suit each individual's needs. Offer self-care tips, wellness routines, or study advice based on what the student shares. I want you to regularly check in on how they're feeling and help them track their emotions over time, offering insights and suggestions for improvement. Share helpful resources like articles, crisis helplines, or relaxation techniques when appropriate. It’s important that students feel safe talking to you, so emphasize confidentiality, and only escalate to crisis support when absolutely necessary. You should also create opportunities for peer support by allowing students to connect anonymously with others in similar situations, with you moderating these conversations. Keep things engaging by adding challenges or tasks that promote mental wellness, like mindfulness exercises or gratitude practices. Help students manage stress and anxiety by walking them through scenarios they might face in daily life, especially around exam time. Finally, motivate them by sending positive affirmations, quotes, and reminders to practice self-care. Be ready to refer them to professional help if you detect any signs of distress or risk of harm. Note that your response should always be less than 100 words.",
                              )

# Starter sentences for the conversation
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

# Function to capture video feed
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
# Chatbot route using the Generative AI model
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json['message']
    
    # Start conversation with the generative model
    convo = model.start_chat()
    
    # Check for a starter message if it's the first user input
    if user_message.lower() == "start":
        start_sentence = random.choice(start_sentences)
        response_text = start_sentence
    else:
        response = convo.send_message(user_message)
        
        # Modify the response text to format the questions properly
        response_text = response.text.replace("* ", "").replace("*", "").replace("?", "?\n")

    # Respond with the chatbot's generated response
    return jsonify({'response': response_text})

# Main route
@app.route('/')
def index():
    # Start with a conversation starter when the app is opened
    starter_sentence = random.choice(start_sentences)
    return render_template('index.html', starter_sentence=starter_sentence)

if __name__ == "__main__":
    app.run(debug=True)
