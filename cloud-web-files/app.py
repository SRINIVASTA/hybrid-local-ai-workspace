import streamlit as st
import requests
import pdfplumber  # <-- MAKE SURE THIS LINE IS PRESENT HERE!
from docx import Document
import openpyxl
from pptx import Presentation


# CRITICAL: st.set_page_config MUST be the very first Streamlit command in the file
st.set_page_config(page_title="Cloud Web AI File Searcher", layout="wide")

# 1. Read the password ONLY from your Streamlit Cloud Dashboard secrets panel.
if "access_password" in st.secrets:
    SECRET_PASSWORD = st.secrets["access_password"]
else:
    st.error("🔒 Security Error: Access password not configured in Streamlit Cloud Dashboard.")
    st.stop()

# 2. Check session state to see if the user is already logged in
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 3. Show the login panel if the user is not authenticated
if not st.session_state["authenticated"]:
    st.title("🔒 Secure AI Workspace Gateway")
    st.write("This portal routes down to a private local data engine. Please authenticate.")
    
    user_password = st.text_input("Enter Access Password", type="password")
    
    if st.button("Login"):
        if user_password == SECRET_PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Access Granted! Loading Workspace...")
            st.rerun()
        else:
            st.error("Incorrect password. Access denied.")
    st.stop()

# =========================================================================
# MAIN APP INTERFACE (Only visible AFTER a successful login)
# =========================================================================
st.title("🌐 Cloud Web AI File Searcher")
st.write("Upload documents securely and extract semantic insights using your laptop's local RAG data engine.")

st.sidebar.header("🔌 Connection Tunnel Settings")
# Fetches the local file string configuration value dynamically if available
default_tunnel = st.secrets.get("saved_tunnel_url", "https://ngrok-free.app")

tunnel_url = st.sidebar.text_input("Enter Laptop Tunnel URL", value=default_tunnel)

# HELPER FUNCTIONS TO EXTRACT VERBATIM TEXT FROM DIVERSE USER ASSETS
def extract_text_from_file(uploaded_file):
    name = uploaded_file.name.lower()
    text = ""
    try:
        if name.endswith('.pdf'):
            # Using pdfplumber to extract layout text and handle advanced formatting
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif name.endswith('.docx'):
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif name.endswith('.txt'):
            text = uploaded_file.read().decode("utf-8")
        elif name.endswith('.xlsx'):
            wb = openpyxl.load_workbook(uploaded_file, data_only=True)
            for sheet in wb.sheetnames:
                ws = wb[sheet]
                for row in ws.iter_rows(values_only=True):
                    row_text = " | ".join([str(cell) for cell in row if cell is not None])
                    if row_text:
                        text += row_text + "\n"
        elif name.endswith('.pptx'):
            prs = Presentation(uploaded_file)
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
    except Exception as e:
        st.sidebar.error(f"Error parsing asset {name}: {e}")
    return text

# FILE INGESTION STORAGE CONTAINER
st.header("📂 Document Knowledge Hub")
uploaded_files = st.file_uploader(
    "Drag and drop documents here to contextualize your local AI model context layer:", 
    type=["pdf", "docx", "txt", "xlsx", "pptx"], 
    accept_multiple_files=True
)

# Extract and combine text from all uploaded files
context_accumulator = ""
if uploaded_files:
    for f in uploaded_files:
        context_accumulator += f"\n--- DOCUMENT CONTENT: {f.name} ---\n"
        context_accumulator += extract_text_from_file(f)
    st.success(f"✓ Context layer armed! Extracted roughly {len(context_accumulator)} characters of local data.")

st.header("💬 Ask Your Local Gemma Model")
query = st.text_input("What would you like to search or analyze inside your context files?")

if query:
    if not in tunnel_url:
        st.error("⚠️ Setup incomplete: Please specify a valid tunnel URL in the sidebar.")
    else:
        # Construct the final prompt injecting the parsed local file text strings
        enriched_prompt = query
        if context_accumulator:
            enriched_prompt = f"Use the following referenced document segments to fulfill the user request precisely:\n{context_accumulator}\n\nUser Question: {query}"
            
        with st.spinner("Streaming data down to your local machine context engine..."):
            try:
                base_url = tunnel_url.strip('/')
                endpoint = f"{base_url}/api/generate"
                
                payload = {
                    "model": "gemma2:2b",
                    "prompt": enriched_prompt,
                    "stream": False
                }
                
                response = requests.post(endpoint, json=payload, timeout=90) # Increased timeout for heavy data arrays
                
                if response.status_code == 200:
                    answer = response.json().get('response', '')
                    st.subheader("💡 Answer from your local machine:")
                    st.write(answer)
                else:
                    st.error(f"❌ Failed to reach Ollama. Status Code: {response.status_code}. Details: {response.text}")
            except Exception as e:
                st.error(f"🔗 Network Bridge Interrupted. Ensure your laptop's Ngrok tunnel is live. Error: {e}")
