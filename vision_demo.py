import streamlit as st
from google import genai
from PIL import Image
import os

# --- CONFIG ---
st.set_page_config(page_title="Architect Vision", layout="centered")
st.title("👁️ AI Architecture Auditor")
with st.expander("💡 About this Demo:"):
    st.markdown("""
    This tool demonstrates **Multimodal AI Analysis**.
    
    Unlike standard LLMs that only read text, this Agent has "Vision." It can look at a raw image—a whiteboard sketch, a cloud dashboard, or a UML diagram—and reason about it like a Senior Architect.
    
    **Capabilities:**
    *   **Component Detection:** Identifies icons and services (AWS/GCP).
    *   **Logic Flow:** Traces how data moves between boxes.
    *   **Risk Auditing:** Spots Single Points of Failure (SPOF) or public-facing databases.
    
    **Your Role:** Implemented the multimodal pipeline connecting **Gemini 2.0 Flash** with Python's image processing libraries to digitize and audit technical assets.
    """)

st.markdown("Upload a **Network Diagram**, **ERD**, or **Whiteboard Sketch**. The AI will audit it.")

# --- SETUP CLIENT ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key missing.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- IMAGE UPLOAD ---
uploaded_file = st.file_uploader("Upload Diagram", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # 1. Display the Image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Design", use_container_width=True)

    # 2. The Auditor Prompt
    prompt = """
    You are a Senior Cloud Architect (AWS/GCP). Audit this technical diagram.
    
    1. **Identify Components:** List the key services seen (e.g., Load Balancers, Databases).
    2. **Flow Analysis:** Briefly explain the data flow.
    3. **Critical Audit:** Identify one Single Point of Failure (SPOF) or Security Risk based on what you see.
    4. **Optimization:** Suggest one modern improvement.
    """

    if st.button("Audit Design"):
        with st.spinner("Analyzing pixels..."):
            try:
                # 3. The Multimodal Call
                # We pass the Text Prompt AND the Image Object together
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[prompt, image]
                )
                
                st.subheader("📋 Architect's Report")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
