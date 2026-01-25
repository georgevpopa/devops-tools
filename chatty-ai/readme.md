# 📘 MANUAL COMPLET: PROIECT CHATTY (AI SysAdmin)

Acesta este documentul central care explică arhitectura sistemului, cum a fost instalat și cum se operează zilnic.

---

## 🏛️ 1. CUM A FOST CONSTRUIT (PAȘII DE INSTALARE)
Aceștia sunt pașii tehnici parcurși pentru a crea sistemul de la zero.

**Pasul 1: Fundația (Sistem de Operare & Docker)**
1. Am asigurat un mediu Linux (Ubuntu/Debian).
2. Am instalat Docker pentru a putea rula servere izolate.
3. Am configurat permisiunile pentru ca utilizatorul curent să nu aibă nevoie de parolă la comenzi Docker:
   `sudo usermod -aG docker $USER`

**Pasul 2: Inteligența (Ollama)**
1. Am instalat Ollama (motorul AI local).
2. Am descărcat modelul Llama 3:
   `ollama pull llama3`

**Pasul 3: Codul (Python & Streamlit)**
1. Am creat un mediu virtual Python (`venv`) pentru a izola librăriile.
2. Am instalat librăriile esențiale:
   `pip install streamlit chromadb ollama pypdf`
3. Am scris scriptul `chatty_real.py` care integrează interfața web cu logica din spate.
4. Am scris scriptul `train_force.py` pentru gestionarea memoriei.

---

## 🏗️ 2. ARHITECTURA SISTEMULUI
Componentele active care fac sistemul să funcționeze:

1.  **🧠 Creierul (Ollama + Llama 3)**
    * Procesează limbajul natural local pe portul `11434`.
2.  **📚 Memoria (ChromaDB)**
    * Baza de date unde sunt indexate procedurile și incidentele firmei.
3.  **💪 Mușchii (Docker)**
    * Infrastructura simulată: `server-web-01` și `server-db-01`.
4.  **💻 Interfața (Streamlit)**
    * Pagina web prin care utilizatorul controlează totul.

---

## 🚀 3. CHEAT SHEET: OPERARE ZILNICĂ

### A. Pornirea Sistemului (Start-up)
Ordinea exactă de pornire după ce deschizi laptopul:

    # 1. Mergi în folderul proiectului
    cd ~/Desktop/chatty-project

    # 2. Pornește infrastructura
    docker compose up -d

    # 3. Activează mediul Python
    source venv/bin/activate

    # 4. Lansează Chatty
    streamlit run chatty_real.py

*(Aplicația se va deschide automat în browser la http://localhost:8501)*

### B. Actualizarea Memoriei (Antrenare)
Când adaugi proceduri noi:

1.  Pune fișierele (`.pdf`, `.txt`) în folderul `~/Desktop/chatty-project/docs_firma/`.
    *(Atenție: Ce este în acest folder reprezintă toată memoria curentă).*
2.  Rulează antrenarea forțată:
    
    python3 train_force.py

3.  Dă **Refresh** la pagina web Chatty.

---

## 🔧 4. TROUBLESHOOTING & COMENZI UTILE

| Acțiune | Comandă Terminal | Explicație |
| :--- | :--- | :--- |
| **Status Servere** | `docker ps` | Verifică dacă containerele sunt "Up". |
| **Restart Web** | `docker restart server-web-01` | Restart manual server web. |
| **Restart DB** | `docker restart server-db-01` | Restart manual bază de date. |
| **Loguri** | `docker logs server-web-01` | Vezi erorile interne. |
| **Oprire Totală** | `docker compose down` | Oprește containerele. |
| **Listare Docs** | `ls -lh docs_firma/` | Vezi fișierele din memorie. |

---

## 📂 5. STRUCTURA FIȘIERELOR
* `chatty_real.py` → Aplicația principală (Interfața).
* `train_force.py` → Scriptul de învățare (Memoria).
* `docker-compose.yml` → Configurația serverelor.
* `docs_firma/` → Folderul cu documente sursă.
* `chroma_data/` → Folderul bazei de date (Nu modifica manual).
