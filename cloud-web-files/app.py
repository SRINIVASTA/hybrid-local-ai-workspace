import streamlit as st
import requests

st.set_page_config(page_title="Cloud Web AI File Searcher", layout="wide")
st.title("🌐 Cloud Web AI File Searcher")
st.write("This public web interface routes queries securely down to your home laptop's local RAG data engine.")

st.sidebar.header("🔌 Connection Tunnel Settings")
tunnel_url = st.sidebar.text_input("Enter Laptop Tunnel URL", value="https://xxxx-xxxx.ngrok-free.app")
api_key = st.sidebar.text_input("Open WebUI API Key (JWT Token)", type="password")

st.header("💬 Ask Your Local Documents")
query = st.text_input("What would you like to ask the documents stored on your home machine?")

if query:
    if not api_key or "ngrok" not in tunnel_url:
        st.error("⚠️ Setup incomplete: Please specify a valid tunnel URL and API key in the sidebar.")
    else:
        with st.spinner("Streaming request down to your 8GB RAM laptop..."):
            try:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "gemma2:2b",
                    "messages": [{"role": "user", "content": query}]
                }
                
                response = requests.post(f"{tunnel_url.strip('/')}/api/chat/completions", headers=headers, json=payload)
                
                if response.status_code == 200:
                    answer = response.json()['choices']['message']['content']
                    st.subheader("💡 Answer from your local documents:")
                    st.write(answer)
                else:
                    st.error(f"❌ Failed to reach local machine. Status Code: {response.status_code}")
            except Exception as e:
                st.error(f"🔗 Network Bridge Interrupted. Ensure your laptop's Ngrok tunnel is currently live. Error: {e}")
