import streamlit as st
import base64
import requests

OLLAMA_URL = "http://localhost:11434/"
MODEL_NAME = "testrigtesting"

st.set_page_config(page_title="Ollama Image Prompt", layout="centered")
st.title("Ollama Image-to-Text Generator")

st.markdown("Upload an image and enter a prompt to interact with your local Ollama model.")

# Input fields
prompt = st.text_input("Enter your prompt:")
file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if st.button("Submit") and file and prompt:
    with st.spinner("Processing..."):
        # Read and encode the image
        image_bytes = file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # Create prompt with image encoded
        full_prompt = f"{prompt}\n[image:base64]\n{image_base64}"

        # Call Ollama API directly
        payload = {
            "model": MODEL_NAME,
            "prompt": full_prompt,
            "stream": False
        }

        OLLAMA_URL = "http://localhost:11434/api/generate"


        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            result = response.json()

            st.success("✅ Response received from Ollama!")
            st.write("📄 **Model Output:**")
            st.json(result)
        except Exception as e:
            st.error(f"❌ Failed to get response: {e}")
