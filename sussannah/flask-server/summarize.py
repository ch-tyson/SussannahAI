import cohere
from dotenv import load_dotenv
import os

load_dotenv()
co = cohere.Client(os.getenv('COHERE_API_KEY','5kgNUypL3OHefbOcf5IrbYnkBFhcBYpFs8vGDSFG'))

def summarize(text):
  response = co.summarize(
    text=text,
    #length, format, and extractiveness are all defaulted to auto to work best based on input text
  )

  return response.summary