# Feelify.AI

**Feelify.AI** is an AI-powered emotional assistant chatbot designed to provide mental health and emotional support to students. Built using Flask, Google Generative AI (Gemini API), and OpenCV, this application leverages natural language understanding to offer a safe, empathetic, and supportive space for users to share their feelings and receive personalized self-care suggestions.

## Features
- **Emotional Support Chatbot**: The chatbot interacts with students by responding empathetically to their messages. It helps students manage stress, track emotions, and offers motivational advice and self-care tips.
- **Emotion Detection via Webcam**: A video stream is used to analyze facial expressions, detecting emotions such as happy, sad, angry, and neutral. The background color changes dynamically based on the detected emotions.
- **Generative AI**: Utilizes the Google Gemini API to generate thoughtful, empathetic responses tailored to the user's emotional state.
- **Simple, Friendly UI**: A user-friendly interface where users can chat with the bot and see real-time emotion detection.

## Prerequisites

- Python 3.x
- Flask
- OpenCV
- Google Generative AI (Gemini API)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Feelify.AI.git
   cd Feelify.AI
   ```

2. **Install the Dependencies**

3. **Set up Google Generative AI**:
   - You need to get an API key from Google Generative AI (Gemini).
   - Add your API key in `app.py`:
     ```python
     GOOGLE_API_KEY = 'your-google-api-key'
     ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the Web App**:
   - Open your web browser and go to `http://127.0.0.1:5000/`.

## File Structure

```
Feelify.AI/
│
├── templates/
│   └── index.html       # HTML template for the user interface
├── static/
│   ├── css/
│   │   └── style.css    # Styling for the web app
├── app.py               # Main Flask application
└── README.md            # Project documentation
```

## API Endpoints

### `/`
- The home page of the application, providing the chat interface and webcam video feed.

### `/chatbot`
- **Method**: POST
- **Description**: Sends the user's message to the chatbot and returns a generative AI-based response.
- **Request Body**:
  ```json
  {
      "message": "Your message"
  }
  ```
- **Response**:
  ```json
  {
      "response": "Chatbot's reply"
  }
  ```

### `/video_feed`
- **Method**: GET
- **Description**: Streams the webcam video feed for emotion detection.

### `/get_emotion`
- **Method**: GET
- **Description**: Returns a random emotion from a predefined list for simulation purposes.
- **Response**:
  ```json
  {
      "emotion": "happy"
  }
  ```

## Technology Stack

- **Backend**: Flask, Google Generative AI (Gemini API)
- **Frontend**: HTML, CSS, JavaScript
- **Emotion Detection**: OpenCV
- **Video Feed**: OpenCV, HTML5 video element

## Future Enhancements
- **Improved Emotion Detection**: Integrate machine learning models for more accurate real-time emotion analysis.
- **Professional Referral System**: Escalate to crisis helplines based on detected distress.


**Developed by Neural Ninjas** 🎉
