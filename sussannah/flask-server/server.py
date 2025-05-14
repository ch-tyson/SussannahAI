
from flask import Flask, request, redirect, url_for, request, jsonify
from flask_cors import CORS
from spam_classify import get_spam_result, get_spam_percentage
from sentiment_analysis import get_sentiment_scores, get_sentiment_result
from summarize import summarize

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# API routes and endpoints to get data
@app.route('/')
def index():
	return {'message': 'Hello, my name is SussannahAI!'}

@app.route("/spam", methods=["POST"])
def spam():
    options = request.json["options"]
    text = request.json["paragraph"]
    processed_text = text

    responseData = {}
    for option in options:
        if option == "spam":
            spam = get_spam_result(processed_text)
            spam_value = get_spam_percentage(processed_text)
            responseData["spam"] = spam
            responseData["spamValue"] = spam_value
        elif option == "summary":
            summary = summarize(processed_text)
            responseData["summary"] = summary
        elif option == "sentiment":
            sentiment = get_sentiment_result(processed_text)
            sentiment_value = get_sentiment_scores(processed_text)
            responseData["sentiment"] = sentiment
            responseData["sentimentValue"] = sentiment_value

    response = jsonify(responseData)
    
    return response

if __name__ == '__main__':
	app.run(debug=True)