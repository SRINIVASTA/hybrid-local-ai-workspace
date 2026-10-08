import streamlit as st
import requests

st.set_page_config(page_title="Cloud Web AI File Searcher", layout="wide")
st.title("🌐 Cloud Web AI File Searcher")
st.write("This public web interface routes queries securely down to your home laptop's local RAG data engine.")

st.sidebar.header("🔌 Connection Tunnel Settings")
tunnel_url = st.text_input("Enter Laptop Tunnel URL", value="https://2189-2406-7400-45-ac2a-f5bb-9208-e338-d6c5.ngrok-free.app")

st.header("💬 Ask Your Local Gemma Model")
query = st.text_input("What would you like to ask the Gemma model running on your home machine?")

if query:
    if "ngrok" not in tunnel_url:
        st.error("⚠️ Setup incomplete: Please specify a valid tunnel URL in the sidebar.")
    else:
        with st.spinner("Streaming request down to your 8GB RAM laptop..."):
            try:
                base_url = tunnel_url.strip('/')
                
                # Point directly to Ollama's core generation endpoint
                endpoint = f"{base_url}/api/generate"
                
                payload = {
                    "model": "gemma2:2b",
                    "prompt": query,
                    "stream": False
                }
                
                response = requests.post(endpoint, json=payload, timeout=60)
                
                if response.status_code == 200:
                    answer = response.json().get('response', '')
                    st.subheader("💡 Answer from your local machine:")
                    st.write(answer)
                else:
                    st.error(f"❌ Failed to reach Ollama. Status Code: {response.status_code}. Details: {response.text}")
            except Exception as e:
                st.error(f"🔗 Network Bridge Interrupted. Ensure your laptop's Ngrok tunnel is currently live. Error: {e}")
