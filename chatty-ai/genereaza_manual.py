from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Font Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Titlu
        self.cell(0, 10, 'Documentatie Proiect: Chatty AI DevOps', 0, 1, 'C')
        # Linie de separare
        self.ln(5)

    def footer(self):
        # Pozitie la 1.5 cm de jos
        self.set_y(-15)
        # Font Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Numarul paginii
        self.cell(0, 10, 'Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, num, label):
        # Font Arial 12
        self.set_font('Arial', 'B', 12)
        # Culoare fundal (gri deschis)
        self.set_fill_color(200, 220, 255)
        # Titlu capitol
        self.cell(0, 6, f'Capitolul {num} : {label}', 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        # Font normal
        self.set_font('Arial', '', 11)
        # Text
        self.multi_cell(0, 5, body)
        self.ln()

    def code_block(self, code):
        # Font Monospaced (Courier) pentru cod
        self.set_font('Courier', '', 9)
        self.set_fill_color(240, 240, 240) # Gri foarte deschis
        self.multi_cell(0, 4, code, 0, 'L', True)
        self.ln()

# Instantiere PDF
pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()

# --- INTRODUCERE ---
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Manual de Instalare si Utilizare', 0, 1, 'L')
pdf.ln(5)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, "Acest document contine toti pasii necesari pentru a recrea proiectul Chatty AI (RAG + DevOps Local) de la zero. Sistemul este complet izolat (offline) si securizat.")
pdf.ln(10)

# --- CAPITOLUL 1 ---
pdf.chapter_title(1, 'Pregatirea Mediului (Terminal)')
pdf.chapter_body("Ruleaza urmatoarele comenzi in terminal pentru a pregati folderul si librariile:")
pdf.code_block("""mkdir ~/Desktop/chatty-project
cd ~/Desktop/chatty-project
python3 -m venv venv
source venv/bin/activate
pip install streamlit chromadb requests fpdf""")

# --- CAPITOLUL 2 ---
pdf.chapter_title(2, 'Pasul 1: Baza de Date (tickets_db.json)')
pdf.chapter_body("Creeaza fisierul tickets_db.json care contine 'memoria' firmei:")
pdf.code_block("""[
    {
        "id": "INC001",
        "problem": "Serverul web nu raspunde, da eroare 502.",
        "resolution": "Solutie: docker restart server-web-01"
    },
    {
        "id": "INC002",
        "problem": "Baza de date este blocata.",
        "resolution": "Solutie: docker restart server-db-01"
    }
]""")

# --- CAPITOLUL 3 ---
pdf.chapter_title(3, 'Pasul 2: Antrenarea (train_memory.py)')
pdf.chapter_body("Scriptul care introduce datele in ChromaDB vector store:")
pdf.code_block("""import json
import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="knowledge_base")

with open("tickets_db.json", "r") as f:
    tickets = json.load(f)

ids = [t["id"] for t in tickets]
docs = [t["problem"] for t in tickets]
metas = [{"resolution": t["resolution"]} for t in tickets]

collection.add(ids=ids, documents=docs, metadatas=metas)
print("Memorie antrenata!")""")

# --- CAPITOLUL 4 ---
pdf.chapter_title(4, 'Pasul 3: Infrastructura (docker-compose.yml)')
pdf.chapter_body("Definirea containerelor Docker simulate:")
pdf.code_block("""version: '3'
services:
  server-web-01:
    image: nginx:latest
    container_name: server-web-01
  server-db-01:
    image: redis:latest
    container_name: server-db-01""")

# --- CAPITOLUL 5 ---
pdf.chapter_title(5, 'Pasul 4: Aplicatia Principala (chatty_real.py)')
pdf.chapter_body("Codul complet pentru interfata Streamlit este prea lung pentru a fi afisat aici integral, dar include:\n\n1. Interfata 'Business Blue'\n2. Selector Mod (IT vs General)\n3. Fallback inteligent ('Vrei sa caut in cunostinte generale?')\n4. Monitorizare Docker live.")

# --- CAPITOLUL 6 ---
pdf.chapter_title(6, 'Lansare si Utilizare')
pdf.chapter_body("Pentru a porni aplicatia, asigura-te ca mediul virtual este activ si ruleaza:")
pdf.code_block("streamlit run chatty_real.py")
pdf.chapter_body("Functionalitati cheie:\n- Modul IT: Cauta strict in tichete.\n- Modul General: Discutii libere (Offline).\n- Buton Restart: Apare doar cand AI-ul recomanda o actiune pe infrastructura.")

# Salvare fisier
pdf.output('Manual_Chatty_AI.pdf')
print("✅ PDF Generat cu succes: Manual_Chatty_AI.pdf")
