import openai
import streamlit as st
from textblob import TextBlob  # To analyze sentiment

# Ensure you have set your OpenAI API Key here:
openai.api_key = "OPENAI_API_KEY"  # Replace with your actual API key

# Function to translate the review into Tanglish with tone
def translate_review(review, tone):
    prompt = f"Translate this review to Tanglish with a {tone} tone:\n\n{review}\n\nTanglish translation:"
    
    # Make the API call to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Make sure you're using the correct model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    translated_review = response['choices'][0]['message']['content']
    return translated_review.strip()

# Function to analyze sentiment and add appropriate emoji
def analyze_sentiment(review):
    blob = TextBlob(review)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        sentiment_emoji = "😊"  # Positive sentiment
    elif sentiment_score < 0:
        sentiment_emoji = "😡"  # Negative sentiment
    else:
        sentiment_emoji = "😐"  # Neutral sentiment
    
    return sentiment_emoji

# Streamlit interface
st.title("Review Vibes Translator")

# Sidebar inputs
st.sidebar.header("Enter Review Details")
review_input = st.sidebar.text_area("Enter the Review", "")
tone_input = st.sidebar.selectbox("Select Tone", ["casual", "sarcastic", "poetic", "formal"])

# Button to submit the review
submit_button = st.sidebar.button("Translate Review")

if submit_button:
    if review_input:
        st.write(f"Original Review: {review_input}")
        
        # Translate the review
        translated_review = translate_review(review_input, tone_input)
        
        # Analyze sentiment and get the emoji
        sentiment_emoji = analyze_sentiment(translated_review)
        
        st.write(f"Translated Review: {translated_review} {sentiment_emoji}")
    else:
        st.write("Please enter a review text.")
