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
    # Analyze sentiment using TextBlob
    blob = TextBlob(review)
    sentiment_score = blob.sentiment.polarity
    
    # Select avatar based on sentiment
    if sentiment_score > 0:
        return "./positive-pup.png"  # Relative path to positive sentiment image
    elif sentiment_score < 0:
        return "./negative-pup.png"  # Relative path to negative sentiment image
    else:
        return "./neutral-pup.png"  # Relative path to neutral sentiment image

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
            # Analyze sentiment and get avatar
            sentiment_avatar = analyze_sentiment(translated_review)
            st.write(f"Translated Review: {translated_review}")
            
            # Debugging: print the absolute path to check the image location
            print("Image path:", os.path.abspath(sentiment_avatar))
            
            # Display the avatar image based on sentiment
            st.image(sentiment_avatar)
    else:
        st.write("Please enter a review to translate.")
