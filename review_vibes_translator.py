import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Review Vibes Translator", layout="centered")
st.title("🌀 Review Vibes Translator")
st.markdown("Translate reviews into **Tanglish** with a chosen tone and vibe ✨")

review_text = st.text_area("Paste your English review here:", height=150)

tone = st.selectbox(
    "Choose the tone:",
    ["Casual", "Sarcastic", "Poetic", "Wholesome", "Comedic", "Filmy", "Rant"]
)

submit = st.button("Translate to Tanglish 🪄")

if submit and review_text:
    with st.spinner("Translating with Anika's AI magic ✨"):
        prompt = f"""Convert this English review into {tone} Tanglish and also detect sentiment as Positive, Negative or Neutral. 
Give output in this format:
Tanglish: <converted_text>
Sentiment: <Positive/Negative/Neutral>

Review: \"{review_text}\"""        

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cool Tamil-English translator who understands tone and emotion."},
                    {"role": "user", "content": prompt}
                ]
            )

            output = response.choices[0].message.content

            if "Tanglish:" in output and "Sentiment:" in output:
                lines = output.split("\n")
                tanglish = lines[0].replace("Tanglish:", "").strip()
                sentiment = lines[1].replace("Sentiment:", "").strip()

                emoji_map = {
                    "Positive": "😍✨💯",
                    "Negative": "😤💔👎",
                    "Neutral": "😐🤔🙃"
                }
                vibe = emoji_map.get(sentiment, "")

                st.subheader(f"🌟 Translated Review in Tanglish {vibe}")
                st.success(tanglish)
            else:
                st.warning("Hmm... Couldn't understand the format. Please try again.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

elif submit:
    st.warning("Please paste a review to translate.")
