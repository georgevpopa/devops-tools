# 1. Alegem baza: Un Linux foarte mic care are deja Python instalat
FROM python:3.9-slim

# 2. Setam folderul de lucru in interiorul containerului (ca un 'cd' automat)
WORKDIR /app

# 3. Copiem fișierele din folderul curent (Linux-ul tau) în container (/app)
COPY . /app

# 4. Instalam libraria necesara (in interiorul containerului)
# --no-cache-dir e pentru a tine imaginea mica
RUN pip install --no-cache-dir requests

# 5. Comanda care se executa cand porneste containerul
CMD ["python", "website_monitor.py"]
