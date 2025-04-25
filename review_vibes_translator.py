import openai
import streamlit as st

# Make sure to set your OpenAI API key securely
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

# Streamlit app logic
st.title("Review Vibes Translator")

# Input for user review
review_input = st.text_area("Enter a review", "This place is awesome!")

# Button to submit the review for translation
if st.button("Translate Review"):
    if review_input:
        # Get the translated review (you can customize the prompt further)
        translated_review = get_openai_response(f"Translate this review into Tanglish: {review_input}")
        st.write(f"Translated Review: {translated_review}")
