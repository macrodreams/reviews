import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Title
st.title("Review Vibes Translator")
st.write("Convert boring reviews into *Tanglish* with vibes!")

# Text input
review_text = st.text_area("Paste the English Review")

# Tone options
tone = st.selectbox("Choose a Vibe", ["Casual", "Sarcastic", "Poetic", "Emotional", "Flirty", "Gossip"])

# Translate button
if st.button("Translate to Tanglish"):
    if not review_text.strip():
        st.warning("Paste some review text first!")
    else:
        # Prompt for the LLM
        prompt = f"""
        You're Anika, a fun South Indian bestie who speaks in Tanglish.
        Translate this English review into {tone} Tanglish.
        Be expressive but keep the meaning clear.
        
        Review: {review_text}
        
        Tanglish ({tone} style):
        """

        # Call GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )

        tanglish_output = response['choices'][0]['message']['content']
        st.subheader("Translated Tanglish Review")
        st.write(tanglish_output)
