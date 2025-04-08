import os
import subprocess
import sys

def check_python_installed():
    """Verifica se Python è installato."""
    try:
        subprocess.run(['python', '--version'], check=True, stdout=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        print("Python non è installato. Installalo prima di procedere.")
        return False

def check_python_version(min_version):
    """Verifica se la versione di Python è compatibile."""
    current_version = sys.version_info
    min_required = tuple(map(int, min_version.split('.')))
    
    if current_version >= min_required:
        return True
    else:
        print(f"Richiesta versione Python {min_version} o superiore. Versione attuale: {sys.version}")
        return False

def sync_libraries():
    """Sincronizza le librerie con requirements.txt."""
    requirements_file = 'requirements.txt'
    if os.path.exists(requirements_file):
        try:
            subprocess.run(['pip', 'install', '-r', requirements_file], check=True)
            print("Librerie sincronizzate con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'installazione delle librerie: {e}")
    else:
        print("File requirements.txt non trovato.")

def list_scripts(directory):
    """Elenca tutti gli script Python nella directory specificata."""
    return [f for f in os.listdir(directory) if f.endswith('.py') and f != 'main.py']

def main():
    # Controlla la versione di Python richiesta (modifica '3.8' se necessario)
    if not check_python_version('3.10'):
        sys.exit(1)

    # Controlla se Python è installato
    if not check_python_installed():
        sys.exit(1)

    # Sincronizza le librerie con requirements.txt
    sync_libraries()

    # Specifica la directory contenente gli script
    scripts_dir = './scripts'  # Cambia il percorso se necessario

    # Elenca gli script disponibili
    scripts = list_scripts(scripts_dir)
    if not scripts:
        print("Nessuno script trovato nella directory.")
        return

    print("Seleziona uno script da eseguire:")
    for i, script in enumerate(scripts, start=1):
        print(f"{i}. {script}")

    try:
        choice = int(input("Inserisci il numero dello script: "))
        if 1 <= choice <= len(scripts):
            selected_script = scripts[choice - 1]
            subprocess.run(['python', os.path.join(scripts_dir, selected_script)])
        else:
            print("Scelta non valida.")
    except ValueError:
        print("Inserisci un numero valido.")

if __name__ == '__main__':
    main()
