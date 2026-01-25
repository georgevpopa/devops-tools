import chromadb
import json
import os

# 1. Configurare: Unde salvăm memoria pe disk?
# Se va crea automat un folder 'chroma_data' în proiectul tău
db_path = "./chroma_data"
client = chromadb.PersistentClient(path=db_path)

# 2. Creăm colecția (tabelul) 'knowledge_base'
# Ștergem versiunea veche dacă există, ca să nu duplicăm datele când rulăm scriptul de mai multe ori
try:
    client.delete_collection(name="knowledge_base")
    print("🗑️  Memoria veche ștearsă. Creăm una nouă...")
except:
    pass

collection = client.create_collection(name="knowledge_base")

# 3. Citim fișierul JSON creat de tine
with open('tickets_db.json', 'r') as f:
    tickets = json.load(f)

print(f"🔄 Încep antrenarea cu {len(tickets)} tichete...")

# 4. Pregătim listele pentru ChromaDB
ids = []
documents = []
metadatas = []

for ticket in tickets:
    # ID-ul unic
    ids.append(ticket["ticket_id"])
    
    # DOCUMENTUL: Ce va citi AI-ul. Combinăm Problema + Descrierea.
    text_de_invatat = f"PROBLEM: {ticket['issue']}. DETAILS: {ticket['description']}"
    documents.append(text_de_invatat)
    
    # METADATA: Informații extra pe care le vrem înapoi (Soluția)
    metadatas.append({
        "resolution": ticket["resolution"],
        "category": ticket["category"]
    })

# 5. Inserarea datelor (Aici se întâmplă transformarea în vectori)
collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)

print("\n✅ SUCCES! Memoria a fost creată.")
print(f"📂 Datele sunt salvate în folderul: {os.path.abspath(db_path)}")
print("🤖 Acum poți rula Chatty, iar el va ști aceste rezolvări.")