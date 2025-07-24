import streamlit as st
import base64  
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "testrigtesting"

st.set_page_config(page_title="Ollama Prompt", layout="centered")
st.title("Ollama Prompt Interface")

st.markdown("Optionally upload an image and enter a prompt to interact with your local Ollama model.")

# Input fields
prompt = st.text_input("Enter your prompt:")
file = st.file_uploader("Choose an image (optional)", type=["png", "jpg", "jpeg"])

if st.button("Submit") and prompt:
    with st.spinner("Processing..."):
        full_prompt = prompt

        if file:
            image_bytes = file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            # Append image to the prompt if file is present
            full_prompt += f"\n[image:base64]\n{image_base64}"

        payload = {
            "model": MODEL_NAME,
            "prompt": full_prompt,
            "stream": False
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            result = response.json()

            st.success("✅ Response received from Ollama!")
            st.write("📄 **Model Output:**")
            st.json(result)
        except Exception as e:
            st.error(f"❌ Failed to get response: {e}")
