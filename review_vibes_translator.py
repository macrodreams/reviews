import streamlit as st
from openai import OpenAI
import os

# Set your OpenAI API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit UI
st.set_page_config(page_title="Review Vibes Translator 💬", layout="centered")
st.title("✨ Review Vibes Translator")
st.write("Convert English reviews into Tanglish with a vibe!")

# Input section
review_text = st.text_area("Enter your review here 👇", height=150)

tone_options = ["Casual", "Sarcastic", "Poetic", "Emotional", "Chill"]
tone = st.selectbox("Choose a tone 🎭", tone_options)

submit = st.button("Translate Vibe")

# Prompt templates
TONE_PROMPTS = {
    "Casual": "Convert this English review into friendly casual Tanglish",
    "Sarcastic": "Convert this English review into sarcastic Tanglish with local flavour",
    "Poetic": "Rewrite this review as a Tanglish poem using rhymes and similes",
    "Emotional": "Express this review in emotional Tanglish with feeling",
    "Chill": "Chill mode! Convert this review into laid-back, relaxed Tanglish"
}

if submit and review_text:
    with st.spinner("Translating... hold tight da! 🎨"):
        prompt = f"{TONE_PROMPTS[tone]}:\n\n\"{review_text}\""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Tanglish tone converter who adapts reviews into the selected tone."},
                    {"role": "user", "content": prompt}
                ]
            )
            output = response.choices[0].message.content
            st.subheader("🌟 Translated Review in Tanglish")
            st.success(output)

        except Exception as e:
            st.error("Oops! Something went wrong.")
            st.exception(e)

# Optional footer
st.markdown("---")
st.caption("Made with ❤️ by Anika & you.")
