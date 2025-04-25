import openai
import streamlit as st
from textblob import TextBlob  # To analyze sentiment

# Ensure you have stored your OpenAI API key in Streamlit's secret management
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define function to get the response from OpenAI's chat model
def get_openai_response(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]

# Define a function to analyze sentiment and return emoji
def analyze_sentiment(review_text):
    # Use TextBlob to analyze the sentiment
    blob = TextBlob(review_text)
    sentiment_score = blob.sentiment.polarity  # Range from -1 (negative) to 1 (positive)
    
    if sentiment_score > 0.2:
        return "🙂"  # Positive sentiment
    elif sentiment_score < -0.2:
        return "😡"  # Negative sentiment
    else:
        return "😐"  # Neutral sentiment

# Streamlit app logic
st.title("Review Vibes Translator")

# Input for user review
review_input = st.text_area("Enter a review", "This place is awesome!")

# Button to submit the review for translation
if st.button("Translate Review"):
    if review_input:
        # Get the translated review (you can customize the prompt further)
        translated_review = get_openai_response(f"Translate this review into Tanglish: {review_input}")
        
        # Analyze sentiment
        sentiment_emoji = analyze_sentiment(translated_review)
        
        # Display translated review with sentiment emoji
        st.write(f"Translated Review: {translated_review} {sentiment_emoji}")
    else:
        st.error("Please enter a review!")
