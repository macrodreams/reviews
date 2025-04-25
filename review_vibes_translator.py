import openai
import streamlit as st
from textblob import TextBlob
import os

# Set the API key using environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure that the API key is set as an environment variable

# Function to translate review using GPT-4 (ChatCompletion)
def translate_review(review, tone):
    prompt = f"Translate this review to Tanglish with a {tone} tone:\n\n{review}\n\nTanglish translation:"
    
    try:
        # Using GPT-4 Chat Completion
        response = openai.ChatCompletion.create(
            model="gpt-4",  # GPT-4 model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        translated_review = response['choices'][0]['message']['content'].strip()
        return translated_review
    except Exception as e:
        st.error(f"Error in OpenAI API call: {e}")
        return None

# Sentiment analysis function
def analyze_sentiment(review):
    blob = TextBlob(review)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return "😊"  # Positive sentiment
    elif sentiment_score < 0:
        return "😡"  # Negative sentiment
    else:
        return "😐"  # Neutral sentiment

# Streamlit UI setup
st.title("Review Vibes Translator")

# Sidebar input
review_input = st.sidebar.text_area("Enter Review", "")
tone_input = st.sidebar.selectbox("Select Tone", ["casual", "sarcastic", "poetic", "formal"])
submit_button = st.sidebar.button("Translate Review")

if submit_button:
    if review_input:
        st.write(f"Original Review: {review_input}")
        
        # Get translated review
        translated_review = translate_review(review_input, tone_input)
        
        if translated_review:
            # Analyze sentiment and add emoji
            sentiment_emoji = analyze_sentiment(translated_review)
            st.write(f"Translated Review: {translated_review} {sentiment_emoji}")
    else:
        st.write("Please enter a review to translate.")
