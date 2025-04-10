# Legal Assistant for the Uneducated (Prototype)
# Streamlit + Groq + OCR + Whisper (for later)

import streamlit as st
from PIL import Image
import pytesseract
from googletrans import Translator
import requests
import os

# Set your Groq API Key
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "mixtral-8x7b-32768"  # Or use llama2-70b, gemma-7b-it, etc.

def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"⚠️ Error from Groq API: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Legal Assistant Bot", page_icon="⚖️")
st.title("⚖️ Legal Assistant for Everyone")
st.markdown("Helping you understand legal documents in simple language and local tongue.")

translator = Translator()

# Upload document
uploaded_file = st.file_uploader("Upload a legal document image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Document', use_column_width=True)

    # OCR
    extracted_text = pytesseract.image_to_string(image)
    st.subheader("📄 Extracted Text")
    st.text(extracted_text)

    # Simplify the legal text
    if st.button("🧠 Simplify & Translate"):
        prompt = f"Simplify this legal document in easy Urdu for a common man: {extracted_text}"
        simplified_text = ask_groq(prompt)
        urdu_translation = translator.translate(simplified_text, dest='ur').text

        st.subheader("🗣️ Simplified Explanation")
        st.write(urdu_translation)

# Ask a legal question
st.markdown("---")
st.subheader("💬 Ask a Legal Question")
user_question = st.text_area("Write your question here (in any language):")

if st.button("Get Answer") and user_question:
    translated_q = translator.translate(user_question, dest='en').text
    prompt = f"Answer this legal question in simple Urdu: {translated_q}"
    answer = ask_groq(prompt)
    urdu_answer = translator.translate(answer, dest='ur').text

    st.subheader("📘 Answer in Urdu")
    st.write(urdu_answer)

st.caption("This tool does not replace professional legal advice. Always consult a lawyer when needed.")
