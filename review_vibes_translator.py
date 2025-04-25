import streamlit as st
import openai
from textblob import TextBlob

# Set your OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to translate review into Tanglish with tone and emoji
def translate_review(review, tone):
    # Sentiment analysis using TextBlob
    sentiment = TextBlob(review).sentiment.polarity
    if sentiment > 0.3:
        emoji = "😍"
    elif sentiment < -0.3:
        emoji = "😤"
    else:
        emoji = "😐"

    prompt = (
        f"Convert this English review to Tanglish (Tamil-English mixed) in a {tone} tone. "
        f"End with an emoji matching the tone.\n\nReview: {review}\nTanglish:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        tanglish_review = response.choices[0].message["content"]
        return f"{tanglish_review.strip()} {emoji}"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("🌀 Review Vibes Translator")

st.markdown("Translate boring English reviews into **fun Tanglish** with customizable tone and auto sentiment emojis! 💬✨")

with st.sidebar:
    st.header("Input ✍️")
    review = st.text_area("Enter English Review", placeholder="This EV charger was fast and efficient.")
    tone = st.selectbox("Select Tone", ["casual", "sarcastic", "poetic", "angry", "flirty", "funny"])

if st.button("Translate"):
    if review:
        output = translate_review(review, tone)
        st.subheader("Tanglish Translation 🔄")
        st.write(output)
    else:
        st.warning("Please enter a review to translate.")
