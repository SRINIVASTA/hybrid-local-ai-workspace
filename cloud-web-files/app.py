import streamlit as st
import requests

st.set_page_config(page_title="Cloud Web AI File Searcher", layout="wide")
st.title("🌐 Cloud Web AI File Searcher")
st.write("This public web interface routes queries securely down to your home laptop's local RAG data engine.")

st.sidebar.header("🔌 Connection Tunnel Settings")
tunnel_url = st.sidebar.text_input("Enter Laptop Tunnel URL", value="https://xxxx-xxxx.ngrok-free.app")

# FIXED: We use a direct master engine token string now to bypass login routing
api_key = st.sidebar.text_input("Master Hardware Engine Token", type="password")

st.header("💬 Ask Your Local Documents")
query = st.text_input("What would you like to ask the documents stored on your home machine?")

if query:
    if not api_key or "ngrok" not in tunnel_url:
        st.error("⚠️ Setup incomplete: Please specify a valid tunnel URL and engine token in the sidebar.")
    else:
        with st.spinner("Streaming request down to your laptop..."):
            try:
                base_url = tunnel_url.strip('/')
                
                # Use standard Bearer token mapping straight to the core completion engine
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "gemma2:2b",
                    "messages": [{"role": "user", "content": query}]
                }
                
                # Plural completions endpoint target
                response = requests.post(f"{base_url}/api/chat/completions", headers=headers, json=payload, timeout=60)
                
                if response.status_code == 200:
                    answer = response.json()['choices']['message']['content']
                    st.subheader("💡 Answer from your local documents:")
                    st.write(answer)
                else:
                    st.error(f"❌ Connection Failed. Server returned Status Code: {response.status_code}. Detail: {response.text}")
                        
            except Exception as e:
                st.error(f"🔗 Network Bridge Interrupted. Ensure your laptop's Ngrok tunnel is currently live. Error: {e}")
