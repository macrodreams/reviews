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
    # Check if the review length is sufficient for sentiment analysis
    if len(review.strip()) == 0:
        st.write("Review is too short or empty. Please provide more details.")
        return None
    
    # Analyze sentiment using TextBlob
    blob = TextBlob(review)
    sentiment_score = blob.sentiment.polarity
    
    # Debugging: print the sentiment score to see if it's working
    st.write(f"Sentiment Score: {sentiment_score}")
    
    # Use raw GitHub URLs for images based on sentiment
    if sentiment_score > 0:
        return "https://raw.githubusercontent.com/macrodreams/reviews/main/positive-pup.png"
    elif sentiment_score < 0:
        return "https://raw.githubusercontent.com/macrodreams/reviews/main/negative-pup.png"
    else:
        return "https://raw.githubusercontent.com/macrodreams/reviews/main/neutral-pup.png"

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
            # Analyze sentiment and get avatar URL
            sentiment_avatar_url = analyze_sentiment(translated_review)
            if sentiment_avatar_url:
                st.write(f"Translated Review: {translated_review}")
                st.image(sentiment_avatar_url)  # Display the image from the GitHub raw URL
    else:
        st.write("Please enter a review to translate.")
