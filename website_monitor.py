from flask import Flask
import requests
import socket

app = Flask(__name__)

targets = [
    "https://www.google.com",
    "https://www.ericsson.com",
    "https://github.com/georgevpopa"
]

def check_site(url):
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return f'<div style="color:green;">[UP] {url} - {response.elapsed.total_seconds()}s</div>'
        else:
            return f'<div style="color:red;">[DOWN] {url} - {response.status_code}</div>'
    except:
        return f'<div style="color:red;">[ERROR] {url}</div>'

@app.route('/')
def home():
    # Aflam pe ce Worker suntem (Hostname-ul containerului)
    worker_name = socket.gethostname()
    
    html_content = f"<h1>Monitorizare Site-uri - AUTOMATIZAT CU GITHUB ACTIONS</h1>"
    html_content += f"<h3>Raport generat de: {worker_name}</h3><hr>"
    
    for site in targets:
        html_content += check_site(site)
        
    return html_content

if __name__ == '__main__':
    # Pornim serverul web pe portul 5000
    app.run(host='0.0.0.0', port=5000)
