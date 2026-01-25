print("--- START DIAGNOSTIC ---")
print("1. Python functioneaza.")

try:
    import chromadb
    print("2. ChromaDB este instalat: OK")
except ImportError:
    print("❌ EROARE: Lipsește 'chromadb'.")

try:
    import pypdf
    print("3. PyPDF este instalat: OK")
except ImportError:
    print("❌ EROARE: Lipsește 'pypdf'.")

try:
    import pandas
    print("4. Pandas este instalat: OK")
except ImportError:
    print("❌ EROARE: Lipsește 'pandas'.")

import os
if os.path.exists("docs_firma"):
    print(f"5. Folderul 'docs_firma' exista si contine {len(os.listdir('docs_firma'))} fisiere.")
else:
    print("❌ EROARE: Nu gasesc folderul 'docs_firma'.")

print("--- DIAGNOSTIC FINALIZAT ---")
