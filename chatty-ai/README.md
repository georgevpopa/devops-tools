# 🤖 Chatty - Your Local DevOps Command Center

Chatty is a private AI assistant designed for SysAdmins to automate VMware infrastructure management. It bridges the gap between technical documentation (RAG) and live execution (Ansible/Docker).

---

## 🛠️ Step-by-Step Installation

### 1. System Requirements
- OS: Linux (Ubuntu/Debian recommended)
- Tools: Python 3.10+, Docker, Ansible
- AI Engine: Ollama (Run `ollama run llama3` to download the model)

### 2. Environment Setup
- Enter the project folder: `cd ~/Desktop/chatty-project`
- Create and activate virtual environment: `python3 -m venv venv && source venv/bin/activate`
- Install required libraries: `pip install streamlit chromadb requests`

### 3. Infrastructure Config
- inventory.ini: Add your VMware server IPs (control-node and workers).
- SSH Access: Ensure the control machine has SSH key access to all nodes (`ssh-copy-id administrator@IP`).

### 4. Launching the App
- Step A: Train the brain (RAG): `python3 train_force.py`
- Step B: Start the dashboard: `streamlit run chatty_real.py`

---

## 🧠 Method of Procedure (MOP) - Command Table

| Task / Intent | Chat Trigger Keywords | Backend Execution | Expected Result |
| :--- | :--- | :--- | :--- |
| **Connectivity Test** | "ping", "reachable", "ssh" | `ansible all -m ping` | "SUCCESS" for all nodes |
| **Fleet Health** | "health", "fleet", "ansible" | `ansible-playbook check_health.yml` | Resource usage report (RAM/Disk) |
| **Log Investigation** | "logs", "show logs", "tail" | `docker logs --tail 20 [target]` | Last 20 lines of service logs |
| **Service Recovery** | - | `docker restart [container]` | Status icon turns 🟢 in Sidebar |

---

## 🏗️ Technical Architecture



1. Interface: Streamlit (Business Blue Theme).
2. Memory: ChromaDB (Vector Database) - stores your procedures from docs_firma/.
3. Brain: Ollama (Llama3) - 100% local and private.
4. Arms: Ansible (for remote fleet) and Docker (for local services).

---

## 🔧 Troubleshooting

- **Red Status in Sidebar:** Check if the local container was stopped. Use the **Fix** button.
- **Action Button Missing:** Ensure you are in "IT Support (RAG)" mode and use keywords from the MOP table above.
- **Ansible Errors:** If a server is UNREACHABLE, verify SSH manually: `ssh administrator@IP`.

---
*Created for the transition from SysAdmin to DevOps.*