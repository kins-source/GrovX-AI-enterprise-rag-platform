import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "default-dev-key")
BACKEND_URL = "http://localhost:8000"
HEADERS = {"X-API-KEY": API_KEY}

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Enterprise AI Engine", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed" # We collapse default just in case CSS doesn't hide it instantly
)

# ----------------- SESSION STATE -----------------
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "avg_latency" not in st.session_state:
    st.session_state.avg_latency = 0.0

# ----------------- GLOBAL CSS -----------------
st.markdown("""
<style>
    /* SaaS Global Styling */
    .stApp { background-color: #fcfcfc; }
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Completely hide native sidebar and toggle buttons */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Main container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1000px;
    }

    /* Modern Chat Bubble Settings */
    /* AI Message Bubble */
    [data-testid="stChatMessage"] {
        background-color: #f9fafb !important;
        border: 1px solid #eaebec;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    /* User Message Bubble */
    [data-testid="stChatMessage"][data-baseweb="block"]:nth-child(odd) {
        background-color: #e5e7eb !important;
        border: 1px solid #d1d5db;
    }
    /* Force text visibility and contrast */
    [data-testid="stChatMessage"] * {
        color: #111827 !important;
        opacity: 1 !important;
    }
    .stChatInput { border-radius: 20px; }

    /* Custom Sidebar Styling using CSS :has() */
    div[data-testid="stVerticalBlock"]:has(> div.element-container div#my-custom-sidebar) {
        position: fixed !important;
        top: 0;
        left: 0;
        width: 280px;
        height: 100vh;
        background-color: #0f172a;
        z-index: 999999;
        padding: 2rem 1.5rem;
        overflow-y: auto;
        transition: transform 0.3s ease-in-out;
        border-right: 1px solid #1e293b;
        box-shadow: 4px 0 10px rgba(0,0,0,0.1);
    }

    /* Force all text inside custom sidebar to white */
    div[data-testid="stVerticalBlock"]:has(> div.element-container div#my-custom-sidebar) * {
        color: #ffffff !important;
    }

    /* Custom button styling within dark sidebar */
    div[data-testid="stVerticalBlock"]:has(> div.element-container div#my-custom-sidebar) button {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    div[data-testid="stVerticalBlock"]:has(> div.element-container div#my-custom-sidebar) button:hover {
        border: 1px solid #475569 !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR TOGGLE LOGIC -----------------
if st.session_state.sidebar_open:
    st.markdown("""
        <style>
            div[data-testid="stVerticalBlock"]:has(> div.element-container div#my-custom-sidebar) {
                transform: translateX(0);
            }
            .block-container {
                padding-left: 320px !important;
                transition: padding-left 0.3s ease-in-out;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            div[data-testid="stVerticalBlock"]:has(> div.element-container div#my-custom-sidebar) {
                transform: translateX(-100%);
            }
            .block-container {
                padding-left: 3rem !important;
                transition: padding-left 0.3s ease-in-out;
            }
        </style>
    """, unsafe_allow_html=True)

# ----------------- CUSTOM SIDEBAR CONTAINER -----------------
sidebar_container = st.container()
with sidebar_container:
    # Invisible marker to anchor CSS Targeting
    st.markdown('<div id="my-custom-sidebar" style="display:none;"></div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='margin-bottom:0;'>⚡ AI Workspace</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #1e293b; margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    
    # 1. Documents Section
    st.markdown("<h4>📂 Documents</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Data", type=["pdf", "txt"], label_visibility="collapsed")
    if st.button("Upload & Index", use_container_width=True):
        if uploaded_file:
            with st.spinner("Processing..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{BACKEND_URL}/upload", files=files, headers=HEADERS)
                    if response.status_code == 200:
                        st.session_state.uploaded_files.append(uploaded_file.name)
                        st.success("Indexed!")
                    else:
                        st.error("Upload failed.")
                except Exception as e:
                    st.error("Backend Error")
    
    if st.session_state.uploaded_files:
        st.markdown("<p style='font-size: 0.9em; margin-top:1em; margin-bottom:0;'>Indexed Files:</p>", unsafe_allow_html=True)
        for f in set(st.session_state.uploaded_files):
            st.caption(f"📄 {f}")
            
    st.markdown("<hr style='border-color: #1e293b; margin-top: 1.5rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    
    # 2. History Section
    st.markdown("<h4>🕘 Query History</h4>", unsafe_allow_html=True)
    if st.session_state.query_count > 0:
        user_msgs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        for m in reversed(user_msgs[-5:]):
            preview = m[:25] + '...' if len(m) > 25 else m
            st.caption(f"• {preview}")
    else:
        st.caption("No queries run yet.")

    st.markdown("<hr style='border-color: #1e293b; margin-top: 1.5rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    
    # 3. Settings Section
    st.markdown("<h4>⚙️ Settings</h4>", unsafe_allow_html=True)
    st.selectbox("LLM Engine", ["Llama 3.1", "Mistral-7B", "GPT-4"], disabled=True)
    st.caption("Locked by Organization settings.")


# ----------------- MAIN LAYOUT HEADER AND BUTTON -----------------
# ----------------- MAIN LAYOUT HEADER AND BUTTON -----------------
col_btn, col_title = st.columns([0.08, 0.92])

with col_btn:
    # ☰ Hamburger button to toggle the sidebar
    if st.button("☰", key="hamburger", help="Toggle Sidebar"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()

with col_title:
    st.markdown("""
    <h1 style="
        color: #111827;
        font-weight: 700;
        font-size: 40px;
        margin-bottom: 5px;
    ">
    ⚡ Enterprise AI Knowledge Assistant
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#6c757d; font-size:1.1rem; margin-bottom:2rem;'>Securely query organizational metrics, sales records, and compliance requirements.</p>", unsafe_allow_html=True)
# ----------------- DASHBOARD METRICS -----------------
col1, col2, col3 = st.columns(3)
m_col1 = col1.empty()
m_col2 = col2.empty()
m_col3 = col3.empty()

def render_metrics():
    # Render into empty placeholders so they stay at the top
    with m_col1:
        st.metric("Queries Run", st.session_state.query_count)
    with m_col2:
        st.metric("Knowledge Objects", len(set(st.session_state.uploaded_files)))
    with m_col3:
        st.metric("Avg Latency", f"{st.session_state.avg_latency:.2f}s" if st.session_state.query_count > 0 else "0.00s")

render_metrics()
st.markdown("<br>", unsafe_allow_html=True)

# ----------------- EMPTY STATE UI -----------------
prompt = None

if len(st.session_state.messages) == 0:
    st.info("👋 Welcome to the Intelligence Center. Connect to your data to begin.")
    st.markdown("<h4 style='color:#495057; font-size: 1rem; margin-top:20px;'>✨ Try asking:</h4>", unsafe_allow_html=True)
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    if btn_col1.button("What is total revenue?", use_container_width=True):
        prompt = "What is total revenue?"
    if btn_col2.button("Summarize uploaded document", use_container_width=True):
        prompt = "Summarize uploaded document"
    if btn_col3.button("Show compliance insights", use_container_width=True):
        prompt = "Show compliance insights"

# ----------------- CHAT INTERFACE -----------------
# Render History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "latency" in msg:
            st.caption(f"⏱️ {msg['latency']}s | 📚 {len(msg.get('sources', []))} Citations")
            if msg.get("sources"):
                with st.expander("Verify Data Sources"):
                    for s in msg["sources"]:
                        st.write(f"- {s}")

# Handle main chat input bar
if chat_val := st.chat_input("Ask something about your data..."):
    prompt = chat_val

# ----------------- EXECUTION PIPELINE -----------------
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("Analyzing parameters..."):
            try:
                payload = {"query": prompt}
                response = requests.post(f"{BACKEND_URL}/query", json=payload, headers=HEADERS)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer provided.")
                    
                    raw_latency = data.get("latency_seconds", 0)
                    latency = round(raw_latency, 2) if isinstance(raw_latency, (int, float)) else 0.0
                    sources = data.get("sources", [])
                    
                    st.markdown(answer)
                    st.caption(f"⏱️ {latency}s | 📚 {len(sources)} Citations")
                    if sources:
                        with st.expander("Verify Data Sources"):
                            for s in sources:
                                st.write(f"- {s}")
                                
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "latency": latency,
                        "sources": sources
                    })
                    
                    # Update Metrics
                    current_total = st.session_state.avg_latency * st.session_state.query_count
                    st.session_state.query_count += 1
                    st.session_state.avg_latency = (current_total + latency) / st.session_state.query_count
                    
                    # Target metrics immediately
                    render_metrics()
                    
                    if prompt != chat_val:
                        st.rerun()

                else:
                    error_msg = f"API Encountered an Issue: {response.status_code}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except Exception as e:
                error_msg = "Backend Offline. Please confirm the FastAPI server is running."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
