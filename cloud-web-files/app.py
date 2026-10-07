import streamlit as st
import requests

st.set_page_config(page_title="Cloud Web AI File Searcher", layout="wide")
st.title("🌐 Cloud Web AI File Searcher")
st.write("This public web interface routes queries securely down to your home laptop's local RAG data engine.")

st.sidebar.header("🔌 Connection Tunnel Settings")
tunnel_url = st.sidebar.text_input("Enter Laptop Tunnel URL", value="https://xxxx-xxxx.ngrok-free.app")

# CHANGED: Use your normal login credentials instead of looking for hidden keys!
st.sidebar.subheader("🔒 Open WebUI Credentials")
email = st.sidebar.text_input("Email Address", value="")
password = st.sidebar.text_input("Password", type="password")

st.header("💬 Ask Your Local Documents")
query = st.text_input("What would you like to ask the documents stored on your home machine?")

if query:
    if not email or not password or "ngrok" not in tunnel_url:
        st.error("⚠️ Setup incomplete: Please specify your tunnel URL, Email, and Password in the sidebar.")
    else:
        with st.spinner("Logging into your laptop and streaming request..."):
            try:
                base_url = tunnel_url.strip('/')
                
                # 1. Automatically request a fresh JWT Token using your sign-in details
                login_payload = {"email": email, "password": password}
                login_res = requests.post(f"{base_url}/api/v1/auths/signin", json=login_payload, timeout=15)
                
                if login_res.status_code != 200:
                    st.error(f"❌ Login Failed: Unable to authenticate with Open WebUI. Check your email/password. Status: {login_res.status_code}")
                else:
                    # Extract the bearer token provided by your machine
                    jwt_token = login_res.json().get("token")
                    
                    # 2. Use the token to pass your query down to gemma2:2b
                    headers = {
                        "Authorization": f"Bearer {jwt_token}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": "gemma2:2b",
                        "messages": [{"role": "user", "content": query}]
                    }
                    
                    response = requests.post(f"{base_url}/api/chat/completions", headers=headers, json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        answer = response.json()['choices']['message']['content']
                        st.subheader("💡 Answer from your local documents:")
                        st.write(answer)
                    else:
                        st.error(f"❌ Failed to query model. Status Code: {response.status_code}. Details: {response.text}")
                        
            except Exception as e:
                st.error(f"🔗 Network Bridge Interrupted. Ensure your laptop's Ngrok tunnel is currently live. Error: {e}")
