import subprocess

def ruleaza_comanda():
    print("Execut comanda Ansible...")
    rezultat = subprocess.run(
        ["ansible", "all", "-a", "free -h", "-i", "inventory.ini"], 
        capture_output=True, 
        text=True
    )
    print("--- REZULTAT DE LA SERVERES ---")
    print(rezultat.stdout)

ruleaza_comanda()
