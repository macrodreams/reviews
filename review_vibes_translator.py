import streamlit as st
import openai

# Function to get sentiment emoji based on sentiment analysis
def get_sentiment_emoji(text):
    positive_keywords = ['good', 'great', 'amazing', 'excellent', 'love', 'happy', 'fantastic']
    negative_keywords = ['bad', 'poor', 'horrible', 'terrible', 'hate', 'worst']
    
    # Default sentiment
    sentiment = "neutral"
    
    # Convert to lowercase for simpler keyword matching
    text = text.lower()
    
    # Check for positive or negative keywords in the review text
    if any(keyword in text for keyword in positive_keywords):
        sentiment = "positive"
    elif any(keyword in text for keyword in negative_keywords):
        sentiment = "negative"
    
    # Return emoji based on sentiment
    if sentiment == "positive":
        return "😊"  # Happy emoji for positive sentiment
    elif sentiment == "negative":
        return "😞"  # Sad emoji for negative sentiment
    else:
        return "😐"  # Neutral emoji for neutral sentiment

# Initialize OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI components
st.title("Review Vibes Translator")
st.sidebar.header("Select Tone for Review Translation")
tone = st.sidebar.selectbox("Select Tone", ["Casual", "Sarcastic", "Poetic", "Formal"])

review_input = st.text_area("Enter the Review Text:")

if review_input:
    try:
        # Adjusted for OpenAI API >=1.0.0, using the newer chat completions endpoint
        response = openai.chat.Completion.create(
            model="gpt-3.5-turbo",  # Use the appropriate model version
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Translate the following review into a {tone} tone:\n{review_input}"}
            ],
            max_tokens=150,
            temperature=0.7,
        )

        translated_review = response['choices'][0]['message']['content'].strip()

        # Get sentiment emoji
        sentiment_emoji = get_sentiment_emoji(review_input)

        # Display translated review and sentiment emoji
        st.subheader("Translated Review:")
        st.write(translated_review)
        st.markdown(f"Sentiment: {sentiment_emoji}")

    except Exception as e:
        st.error(f"Error occurred: {e}")

