import streamlit as st
import requests

# CRITICAL: st.set_page_config MUST be the very first Streamlit command in the file
st.set_page_config(page_title="Cloud Web AI File Searcher", layout="wide")

# 1. Read the secret password securely from your Streamlit Cloud Dashboard secrets panel
# If it's not typed in the dashboard yet, it safely falls back to a temporary text string
SECRET_PASSWORD = st.secrets.get("access_password", "temporary_admin_password_123")

# 2. Check session state to see if the user is already logged in
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 3. If NOT logged in, show the clean login form block
if not st.session_state["authenticated"]:
    st.title("🔒 Secure AI Workspace Gateway")
    st.write("This portal routes down to a private local data engine. Please authenticate.")
    
    # Password entry field
    user_password = st.text_input("Enter Access Password", type="password")
    
    if st.button("Login"):
        if user_password == SECRET_PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Access Granted! Loading Workspace...")
            st.rerun() # Refresh the page to show the main application interface
        else:
            st.error("Incorrect password. Access denied.")
            
    st.stop() # CRITICAL: Stops execution right here so your underlying layout stays hidden

# =========================================================================
# MAIN APP INTERFACE (Only visible AFTER a successful login)
# =========================================================================
st.title("🌐 Cloud Web AI File Searcher")
st.write("This public web interface routes queries securely down to your home laptop's local RAG data engine.")

st.sidebar.header("🔌 Connection Tunnel Settings")
tunnel_url = st.sidebar.text_input("Enter Laptop Tunnel URL", value="https://2189-2406-7400-45-ac2a-f5bb-9208-e338-d6c5.ngrok-free.app")

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
