import cohere
from cohere.responses.classify import Example
from dotenv import load_dotenv
import os

load_dotenv()

# Create a Cohere client using the API key
co = cohere.Client('op8uO8GTYEGoefH0CcV4DZU0oYK3UXOgMZQU4Ugi')

POSITIVE = "positive"
NEGATIVE = "negative"
NEUTRAL = "neutral"

# Define a list of example inputs and their corresponding labels for sentiment analysis
examples=[
    Example("I love this product", POSITIVE),
    Example("This is the best day of my life", POSITIVE),
    Example("I'm not happy with the service", NEGATIVE),
    Example("I hate waiting in line", NEGATIVE),
    Example("It's an average day", NEUTRAL),
    Example("I don't feel strongly about this", NEUTRAL),
    Example("I'm really looking forward to the weekend", POSITIVE),
    Example("I can't wait to use this new app", POSITIVE),
    Example("I'm so grateful for your help", POSITIVE),
    Example("I'm feeling really down today", NEGATIVE),
    Example("I'm not happy with the product quality", NEGATIVE),
    Example("I'm disappointed with the service", NEGATIVE),
    Example("I regret buying this product", NEGATIVE),
    Example("I don't have any strong feelings about this", NEUTRAL),
    Example("It's an average movie", NEUTRAL),
    Example("The product does its job", NEUTRAL),
    Example("It's not bad, but it's not great either", NEUTRAL),
    Example("You're an idiot", NEGATIVE),
    Example("I hate you", NEGATIVE),
    Example("You are stupid", NEGATIVE),
    Example("I will never forgive you", NEGATIVE),
    Example("What a loser", NEGATIVE),
    Example("You're an idiot", NEGATIVE),
    Example("I hate you", NEGATIVE),
    Example("You are stupid", NEGATIVE),
    Example("I will never forgive you", NEGATIVE),
    Example("What a loser", NEGATIVE),
    Example("I am feeling great today!", POSITIVE), 
    Example("I just got a promotion!", POSITIVE), 
    Example("I love spending time with my family", POSITIVE), 
    Example("I am so excited for tomorrow", POSITIVE), 
    Example("I am feeling content", POSITIVE), 
    Example("I had a wonderful time at the park", POSITIVE), 
    Example("I am looking forward to my vacation", POSITIVE), 
    Example("This meal was delicious", POSITIVE), 
    Example("I am so proud of my accomplishments", POSITIVE),
    Example("The weather is mild", NEUTRAL),
    Example("I ran for an hour", NEUTRAL),
    Example("The movie was average", NEUTRAL),
    Example("The store was closed", NEUTRAL),
    Example("I took the bus home", NEUTRAL),
    Example("The food was okay", NEUTRAL),
    Example("It was an average day", NEUTRAL)
]

# Function to classify the sentiment of a given text using Cohere's classify API
def classify_sentiment(text):
    response = co.classify(
        model='b82f1682-2ed9-4845-83f6-ddebd4458937-ft',
        inputs=[text]
    )
    return response.classifications[0]

# Function to get the sentiment scores (confidence) for a given text
def get_sentiment_scores(text):
    response = classify_sentiment(text)
    print("First label: ", response.labels)
    positive_score = response.labels[POSITIVE].confidence
    negative_score = response.labels[NEGATIVE].confidence
    neutral_score = response.labels[NEUTRAL].confidence
    return [negative_score, positive_score, neutral_score]

# Function to get the sentiment result (label) for a given text
def get_sentiment_result(text):
    response = classify_sentiment(text)
    return response.prediction
