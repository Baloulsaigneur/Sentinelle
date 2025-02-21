import subprocess

def sanitize_target(target):
    """
    Nettoie l'URL pour éviter les erreurs :
    - Supprime 'http://' ou 'https://'
    - Supprime '/' à la fin
    """
    target = target.strip().rstrip('/')  # Supprime les espaces et '/' en fin d'URL
    if target.startswith("http://") or target.startswith("https://"):
        target = target.split("://")[1]  # Supprime le protocole
    return target

def run_nmap(target):
    """
    Exécute Nmap pour scanner les ports/services.
    """
    target = sanitize_target(target)  # Nettoie l'URL
    command = ["docker", "run", "--rm", "poc-sentinelle-2-nmap_worker", "-sV", target]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Nmap scan failed: {e.stderr.strip()}"
    except Exception as e:
        return f"Unexpected error during Nmap scan: {str(e)}"

def run_nuclei(target):
    """
    Exécute Nuclei pour détecter les vulnérabilités.
    """
    target = sanitize_target(target)  # Nettoie l'URL
    command = ["docker", "run", "--rm", "poc-sentinelle-2-nuclei_worker", "-u", target, "-no-color"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Nuclei scan failed: {e.stderr.strip()}"
    except Exception as e:
        return f"Unexpected error during Nuclei scan: {str(e)}"

def run_nikto(target):
    """
    Exécute Nikto pour analyser la configuration du serveur web.
    """
    target = sanitize_target(target)  # Nettoie l'URL
    command = ["docker", "run", "--rm", "poc-sentinelle-2-nikto_worker", "-host", target]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Nikto scan failed: {e.stderr.strip()}"
    except Exception as e:
        return f"Unexpected error during Nikto scan: {str(e)}"
