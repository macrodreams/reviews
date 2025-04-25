import openai
import streamlit as st
from textblob import TextBlob

# Set your OpenAI API Key
openai.api_key = "OPENAI_API_KEY"  # Make sure to replace with your actual key

# Simplified OpenAI call for testing
def translate_review(review, tone):
    prompt = f"Translate this review to Tanglish with a {tone} tone:\n\n{review}\n\nTanglish translation:"
    
    try:
        # Using a basic completions call for debugging
        response = openai.Completion.create(
            engine="text-davinci-003",  # Simplified for testing
            prompt=prompt,
            max_tokens=150
        )
        translated_review = response.choices[0].text.strip()
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
