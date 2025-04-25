import streamlit as st
import openai
from textblob import TextBlob  # For sentiment analysis
import re

# Set your OpenAI API key here
openai.api_key = "OPENAI_API_KEY"  # Replace with your actual OpenAI API key

# Function to get a translated review with emotional tone
def get_translated_review(review, tone):
    # Set up the system message to guide the assistant
    system_message = f"Translate the following review with a {tone} tone."

    # Set up the conversation history
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": review}
    ]

    # Call the OpenAI API for chat-based completion
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Or you can use gpt-3.5-turbo
        messages=messages
    )

    translated_review = response['choices'][0]['message']['content']
    
    return translated_review

# Function for sentiment analysis and emoji
def analyze_sentiment(text):
    # Use TextBlob to determine sentiment
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity  # Range: -1 (negative) to 1 (positive)
    
    # Map the sentiment score to an emoji
    if sentiment_score > 0.2:
        sentiment_emoji = "😊"  # Positive sentiment
    elif sentiment_score < -0.2:
        sentiment_emoji = "😞"  # Negative sentiment
    else:
        sentiment_emoji = "😐"  # Neutral sentiment
    
    return sentiment_score, sentiment_emoji

# Streamlit interface
st.title("Review Vibes Translator")

# Sidebar for user input
st.sidebar.header("Enter Review and Tone")
review_input = st.sidebar.text_area("Enter the Review", "I love this product! It's amazing.")  # Default review
tone_input = st.sidebar.selectbox("Select Tone", ["casual", "sarcastic", "poetic", "formal"])

submit_button = st.sidebar.button("Translate Review")

# Display output when button is pressed
if submit_button:
    if review_input:
        st.write(f"Original Review: {review_input}")
        
        # Translate the review based on selected tone
        translated_review = get_translated_review(review_input, tone_input)
        
        # Display translated review
        st.write(f"Translated Review ({tone_input}): {translated_review}")
        
        # Perform sentiment analysis
        sentiment_score, sentiment_emoji = analyze_sentiment(translated_review)
        
        # Display sentiment with emoji
        st.write(f"Sentiment: {sentiment_score:.2f} {sentiment_emoji}")
    else:
        st.write("Please enter a review to translate.")
