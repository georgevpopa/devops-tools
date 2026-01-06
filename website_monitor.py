import requests
import datetime

targets = [
    "https://www.google.com",
    "https://www.ericsson.com",
    "https://github.com/georgevpopa"
]

def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"[UP] {url} - {response.elapsed.total_seconds()}s"
        else:
            return f"[DOWN] {url} - Status: {response.status_code}"
    except requests.exceptions.RequestException:
        return f"[ERROR] {url} - Inaccesibil"

print(f"--- Raport {datetime.datetime.now()} ---")
for site in targets:
    print(check_site(site))
