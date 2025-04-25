import streamlit as st
import openai

# Streamlit interface for custom prompt
st.title("Review Vibes Translator")

st.sidebar.header("Enter Review Details")
review_text = st.sidebar.text_area("Enter the Review Text", "")
tone = st.sidebar.selectbox("Select Tone", ["Casual", "Sarcastic", "Poetic", "Positive", "Negative"])

submit = st.sidebar.button("Submit Query")

# Access the secret key stored in Streamlit Cloud
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_review_translation(review, tone):
    try:
        # Construct the prompt based on tone selection
        prompt = f"Translate this review into a {tone} tone:\n\n{review}"

        # Request to OpenAI GPT model
        response = openai.Completion.create(
            model="gpt-4",  # Use GPT-4 model or the one you prefer
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )

        # Parse the translated review from the API response
        translated_review = response.choices[0].text.strip()

        return translated_review

    except Exception as e:
        return f"Error occurred: {str(e)}"

# Handling the translation when the user submits the form
if submit:
    if review_text:
        # Call the translation function based on the review text and tone
        translated_review = generate_review_translation(review_text, tone)
        
        # Display original review
        st.subheader("Original Review:")
        st.write(review_text)
        
        # Display translated review
        st.subheader(f"Translated Review ({tone} tone):")
        st.write(translated_review)
    else:
        st.write("Please enter a review to translate.")
