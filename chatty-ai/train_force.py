import os
import shutil
import sys

print("--- 🚀 START PROCEDURA DE FORTA ---")

# 1. VERIFICARE LIBRARII
try:
    import chromadb
    import pypdf
    import docx
    import pandas
    print("✅ Librariile sunt instalate corect.")
except ImportError as e:
    print(f"❌ EROARE CRITICA: Lipseste ceva! {e}")
    sys.exit(1)

# 2. CONFIGURARE & CURATENIE
DB_PATH = "./chroma_data"
DOCS_PATH = "./docs_firma"

# Stergem baza de date veche sa fim siguri
if os.path.exists(DB_PATH):
    try:
        shutil.rmtree(DB_PATH)
        print("🧹 Am sters baza de date veche (Reset).")
    except:
        pass

# Asiguram folderul de documente
if not os.path.exists(DOCS_PATH):
    os.makedirs(DOCS_PATH)
    print(f"📂 Am creat folderul '{DOCS_PATH}'.")

# 3. GENERARE FISIER TEST (SECRETUL!)
# Scriem fortat un fisier ca sa fim SIGURI ca exista ceva de citit
fisier_test = os.path.join(DOCS_PATH, "test_automat.txt")
with open(fisier_test, "w", encoding="utf-8") as f:
    f.write("Aceasta este o procedura de urgenta. Daca serverul ia foc, folositi extinctorul. Nu aruncati cu apa!")
print(f"📝 Am creat AUTOMAT fisierul de test: {fisier_test}")

# 4. INGESTIE (CITIRE)
print("🔌 Conectare la ChromaDB...")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("knowledge_base")

print("👀 Citesc folderul...")
fisiere = os.listdir(DOCS_PATH)
print(f"   Am gasit fisierele: {fisiere}")

count = 0
for nume_fisier in fisiere:
    cale_completa = os.path.join(DOCS_PATH, nume_fisier)
    
    # Citim doar TXT pentru acest test simplu si sigur
    if nume_fisier.endswith(".txt"):
        print(f"   Processing: {nume_fisier}...")
        with open(cale_completa, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Introducere in DB
        if text:
            collection.add(
                ids=[nume_fisier],
                documents=[text],
                metadatas=[{"source": "Test Automat"}]
            )
            count += 1
            print("   ✅ Adaugat in baza de date!")

# 5. VERIFICARE FINALA
print("-" * 30)
if count > 0:
    print(f"🎉 VICTORIE! Avem {count} documente in memorie.")
    print("Acum poti rula: streamlit run chatty_real.py")
else:
    print("❌ CEVA E FOARTE GRESIT. Nu s-a adaugat nimic.")
print("-" * 30)
