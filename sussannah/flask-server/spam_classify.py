import cohere
from cohere.responses.classify import Example
from dotenv import load_dotenv
import os

load_dotenv()

# Create a Cohere client using the API key
co = cohere.Client('op8uO8GTYEGoefH0CcV4DZU0oYK3UXOgMZQU4Ugi')

SPAM = "spam"
NOT_SPAM = "not_spam"

# Function to classify if a text is spam using Cohere's classify API
def classify_spam(text):
    response = co.classify(
        model='9ef292e2-8986-4a59-8530-e73b99609f27-ft',
        inputs=[text]
    )
    return response.classifications[0]

# Function to get the spam classification scores (confidence) for a given text
def get_spam_scores(text):
    response = classify_spam(text)
    print("Classification labels: ", response.labels)
    spam_score = response.labels[SPAM].confidence
    not_spam_score = response.labels[NOT_SPAM].confidence
    return [spam_score, not_spam_score]

# Function to get the spam classification result (label) for a given text
def get_spam_result(text):
    response = classify_spam(text)
    return response.prediction

# classify_spam("Win a free prize!")
# sample output The confidence levels of the labels are: [{'spam': 0.9999999999999999, 'non-spam': 1.1102230246251565e-16}]

def get_spam_percentage(text):
  response = classify_spam(text)
  print("First label: ", response.labels)
  spam_score = response.labels[SPAM].confidence
  non_spam_score = response.labels[NOT_SPAM].confidence
  return [spam_score, non_spam_score]

def get_spam_result(text):
  spam_score = get_spam_percentage(text)[0]
  if (spam_score > 0.5):
    return " spam"
  else:
    return " not spam"