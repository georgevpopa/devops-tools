import streamlit as st
import chromadb
import requests
import subprocess
import time
import os

# --- 1. MEMORY SETUP (ChromaDB) ---
try:
    client = chromadb.PersistentClient(path="./chroma_data")
    collection = client.get_or_create_collection("knowledge_base")
except Exception as e:
    st.error(f"ChromaDB Connection Error: {e}")
    st.stop()

# --- 2. PAGE CONFIG & DESIGN ---
st.set_page_config(page_title="Chatty AI DevOps", page_icon="🔒", layout="wide")

# CSS - Business Blue Design with High-Contrast Header
st.markdown("""
<style>
    .stApp, [data-testid="stSidebar"] { background-color: #E3F2FD; }
    [data-testid="stSidebar"] { border-right: 1px solid #90CAF9; }
    h1, h2, h3, p, span, div, li, label { color: #0D47A1; }
    
    .stChatMessage { 
        background-color: #FFFFFF; 
        border: 1px solid #BBDEFB; 
        border-radius: 12px; 
        padding: 1.2rem; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
    }
    
    .stMain .stButton > button { 
        background-color: #1976D2 !important; 
        color: white !important; 
        font-weight: bold; 
        border-radius: 8px;
    }
    
    .stCode { background-color: #263238 !important; color: #EEFFFF !important; }

    .main-header {
        background: linear-gradient(90deg, #0D47A1 0%, #1565C0 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        color: #FFFFFF !important;
        margin: 0;
        font-weight: 800;
    }
    
    .main-header p {
        color: #E3F2FD !important;
        margin-top: 0.5rem;
        font-size: 1.1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE FUNCTIONS ---

def get_context(question):
    try:
        results = collection.query(query_texts=[question], n_results=2)
        if results['documents'] and results['documents'][0]:
            return {"source": "🏢 INTERNAL KNOWLEDGE", "text": "\n".join(results['documents'][0])}
    except: pass
    return None

def ask_ollama(prompt, context_db, model):
    system_instruction = (
        "You are Chatty, a Senior DevOps Engineer. "
        "STRICT RULE: Always prioritize technical data from [CONTEXT]. "
        "Explain procedures in English clearly."
    )
    ctx_text = f"[CONTEXT]:\n{context_db['text']}" if context_db else "[CONTEXT]: No internal records found."
    full_p = f"{system_instruction}\n\n{ctx_text}\n\nUSER QUESTION: {prompt}"
    
    try:
        response = requests.post("http://localhost:11434/api/generate", 
                                 json={"model": model, "prompt": full_p, "stream": False})
        return response.json()['response'], (context_db['source'] if context_db else "🧠 General Knowledge")
    except: return "Ollama connection error", "Error"

def run_action(action_type, target):
    path = os.path.dirname(os.path.abspath(__file__))
    try:
        if action_type == "docker_restart":
            subprocess.run(["docker", "restart", target], check=True)
            return f"✅ Successfully restarted local container: {target}"
        elif action_type == "docker_logs":
            res = subprocess.run(["docker", "logs", "--tail", "20", target], capture_output=True, text=True)
            return res.stdout if res.stdout else "No logs found."
        elif action_type == "ansible_health":
            res = subprocess.run(["ansible-playbook", "-i", "inventory.ini", "check_health.yml"], 
                                 capture_output=True, text=True, cwd=path)
            return res.stdout if res.stdout else res.stderr
        elif action_type == "ansible_ping":
            res = subprocess.run(["ansible", "all", "-m", "ping", "-i", "inventory.ini"], 
                                 capture_output=True, text=True, cwd=path)
            return res.stdout if res.stdout else res.stderr
    except Exception as e: return f"Execution Error: {str(e)}"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎛️ Control Panel")
    mod_active = st.radio("Mode:", ("🛠️ IT Support (RAG)", "🧠 General Chat"))
    model_choice = st.selectbox("Model:", ("llama3", "mistral"))
    
    st.markdown("---")
    st.markdown("### 🐳 Infrastructure Status")
    for srv in ["server-web-01", "server-db-01"]:
        col_st, col_btn = st.columns([2, 1])
        try:
            check = subprocess.run(["docker", "ps", "-q", "-f", f"name={srv}"], capture_output=True, text=True)
            status = "🟢" if check.stdout.strip() else "🔴"
        except: status = "⏳"
        
        col_st.write(f"**{status} {srv}**")
        if col_btn.button("Fix", key=f"fix_{srv}"):
            run_action("docker_restart", srv)
            st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.session_state.last_output = None
        st.rerun()

# --- 5. MAIN UI ---
st.markdown('<div class="main-header"><h1>🤖 Chatty DevOps Dashboard</h1><p>Infrastructure Monitoring & Automated Support</p></div>', unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if "last_output" not in st.session_state: st.session_state.last_output = None

# Show Message History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Show Output (Ansible/Logs)
if st.session_state.last_output:
    with st.chat_message("assistant"):
        st.success("📝 Command Output:")
        st.code(st.session_state.last_output, language="text")

prompt = st.chat_input("Ask: 'Check fleet health' or 'Are servers reachable?'...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.last_output = None
    st.rerun()

# Processing (after rerun for instant feedback)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_p = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing infrastructure..."):
            context = get_context(last_p) if "IT Support" in mod_active else None
            ans, src = ask_ollama(last_p, context, model_choice)
            st.markdown(ans)
            st.caption(f"🔍 Source: {src}")
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.rerun()

# --- 6. ACTION TRIGGERS ---
if st.session_state.messages and "IT Support" in mod_active:
    # Use context from the last 2 messages for better intent detection
    combined_context = ""
    for m in st.session_state.messages[-2:]:
        combined_context += m["content"].lower()
    
    if combined_context:
        st.divider()
        st.subheader("🛠️ Available Actions")
        cols = st.columns(3)
        
        # 1. Connectivity Test
        if any(x in combined_context for x in ["reachable", "ping", "ssh", "connect"]):
            if cols[0].button("📡 TEST CONNECTIVITY (PING)", key="btn_ping"):
                with st.spinner("Pinging fleet..."):
                    st.session_state.last_output = run_action("ansible_ping", None)
                    st.rerun()

        # 2. Health Check
        if any(x in combined_context for x in ["health", "fleet", "ansible", "run"]):
            if cols[1].button("🚀 RUN FLEET HEALTH CHECK", key="btn_ansible"):
                with st.spinner("Executing Playbook..."):
                    st.session_state.last_output = run_action("ansible_health", None)
                    st.rerun()

        # 3. Logs
        if "log" in combined_context:
            target = "server-db-01" if "db" in combined_context else "server-web-01"
            if cols[2].button(f"👁️ FETCH LOGS: {target.upper()}", key="btn_logs"):
                with st.spinner("Fetching logs..."):
                    st.session_state.last_output = run_action("docker_logs", target)
                    st.rerun()
