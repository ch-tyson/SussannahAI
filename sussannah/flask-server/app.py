from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import cohere
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
CORS(app, 
     resources={r"/*": {
         "origins": ["https://sussannah-ai.vercel.app", "http://localhost:3000"],
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Accept"],
         "expose_headers": ["Content-Type"],
         "supports_credentials": True,
         "max_age": 3600
     }},
     supports_credentials=True)

# Initialize Cohere client
co = cohere.Client(os.getenv('COHERE_API_KEY'))

def analyze_sentiment(text):
    # Use TextBlob for sentiment analysis
    analysis = TextBlob(text)
    # Get polarity (-1 to 1)
    polarity = analysis.sentiment.polarity
    
    # Convert to percentages
    if polarity < 0:
        negative = abs(polarity)
        positive = 0
        neutral = 1 - negative
    elif polarity > 0:
        positive = polarity
        negative = 0
        neutral = 1 - positive
    else:
        neutral = 1
        positive = 0
        negative = 0
    
    # Determine sentiment label
    if polarity < -0.1:
        sentiment = "negative"
    elif polarity > 0.1:
        sentiment = "positive"
    else:
        sentiment = "neutral"
    
    return sentiment, [negative, positive, neutral]

def analyze_spam(text):
    # Use Cohere for spam detection
    response = co.classify(
        model='large',
        inputs=[text],
        examples=[
            {"text": "Buy now! Limited time offer!", "label": "spam"},
            {"text": "Your account has been compromised", "label": "spam"},
            {"text": "Congratulations! You've won!", "label": "spam"},
            {"text": "Meeting tomorrow at 2pm", "label": "not spam"},
            {"text": "Project update: Phase 1 complete", "label": "not spam"},
            {"text": "Please review the attached document", "label": "not spam"}
        ]
    )
    
    prediction = response.classifications[0]
    is_spam = prediction.prediction == "spam"
    confidence = prediction.confidence
    
    return "spam" if is_spam else "not spam", [confidence if is_spam else 1-confidence, 1-confidence if is_spam else confidence]

def generate_summary(text):
    # Use Cohere for text summarization
    response = co.summarize(
        text=text,
        length='short',
        format='paragraph',
        model='summarize-xlarge',
        additional_command='Focus on the main points and key details.'
    )
    
    return response.summary

@app.route('/spam', methods=['POST', 'OPTIONS'])
def analyze_text():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers.add('Access-Control-Allow-Origin', 'https://sussannah-ai.vercel.app')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Accept')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
        
    try:
        logger.info("Received request to /spam endpoint")
        data = request.get_json()
        logger.info(f"Request data: {data}")
        
        text = data.get('paragraph', '')
        options = data.get('options', [])
        
        response = {}
        
        if 'sentiment' in options:
            sentiment, sentiment_values = analyze_sentiment(text)
            response['sentiment'] = sentiment
            response['sentimentValue'] = sentiment_values
            
        if 'spam' in options:
            spam_result, spam_values = analyze_spam(text)
            response['spam'] = spam_result
            response['spamValue'] = spam_values
            
        if 'summary' in options:
            response['summary'] = generate_summary(text)
        
        logger.info(f"Sending response: {response}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

# This is important for gunicorn
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000))) 