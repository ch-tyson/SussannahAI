from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

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
        
        # For testing, return a basic response
        response = {
            "sentiment": "positive",
            "spam": "not spam",
            "summary": "This is a test summary",
            "sentimentValue": [0.2, 0.6, 0.2],  # [negative, positive, neutral]
            "spamValue": [0.1, 0.9]  # [spam, not spam]
        }
        
        logger.info(f"Sending response: {response}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

# This is important for gunicorn
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000))) 