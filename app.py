from flask import Flask, request, jsonify
import requests
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key
genai.configure(api_key="AIzaSyCPJIlX1AAv5yOr4NzRTZC3rqDi6Cvwacw")

# Load the Gemini Pro model and start a chat session
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


@app.route('/chat', methods=['POST'])
def chat_route():
    # Extract the message from the request
    message = request.json.get('message')

    # Send the message to the Gemini Pro model and get the response
    response = chat.send_message(message, stream=True)

    # Process the response from the model
    response_text = ""
    for chunk in response:
        response_text += f"{chunk.text}\n"

    # Return the response as JSON
    return jsonify({'response': response_text})


@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>Chat with the Gemmini Chatbot</h1>
            <form action="/chat" method="post" id="chatForm">
                <input type="text" name="message" id="message" placeholder="Type your message here" required>
                <button type="submit">Send</button>
            </form>
            <div id="response"></div>
            <script>
                document.getElementById('chatForm').onsubmit = async (e) => {
                    e.preventDefault();
                    const message = document.getElementById('message').value;
                    const responseDiv = document.getElementById('response');
                    responseDiv.innerHTML = 'Loading...';
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message })
                    });
                    const result = await response.json();
                    if (response.ok) {
                        responseDiv.innerHTML = result.response;
                    } else {
                        responseDiv.innerHTML = 'Error: ' + result.error;
                    }
                };
            </script>
        </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)