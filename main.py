#!/usr/bin/env python3
import os
import sys
import subprocess

def install_python_3_10():
    """
    Verifica se Python 3.10 è installato e, se non lo è, lo installa tramite winget.
    """
    try:
        # Verifica se Python 3.10 è già installato
        result = subprocess.run(["python3.10", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Python 3.10 non trovato. Installazione in corso...")
            subprocess.run(["winget", "install", "Python.Python.3.10"], check=True)
            print("Python 3.10 installato con successo.")
        else:
            print("Python 3.10 già installato.")
    except FileNotFoundError:
        print("Python 3.10 non trovato. Installazione in corso...")
        subprocess.run(["winget", "install", "Python.Python.3.10"], check=True)
        print("Python 3.10 installato con successo.")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'installazione di Python 3.10: {e}")

def install_requirements():
    """
    Installa le dipendenze presenti nel file requirements.txt.
    Se il file non esiste, stampa un messaggio di avviso.
    """
    requirements_file = 'requirements.txt'
    
    if os.path.isfile(requirements_file):
        print("Trovato requirements.txt. Installazione delle dipendenze...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)
            print("Dipendenze installate con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'installazione delle dipendenze: {e}")
    else:
        print("requirements.txt non trovato. Nessuna dipendenza da installare.")

def get_scripts(directory):
    """
    Restituisce una lista di file .py presenti in 'directory', 
    escludendo questo script principale (main.py).
    La lista viene ordinata alfabeticamente.
    """
    scripts = []
    for file in os.listdir(directory):
        if file.endswith('.py') and file != 'main.py':
            scripts.append(file)
    return sorted(scripts)

def get_description(filepath):
    """
    Estrae una breve descrizione dallo script in 'filepath'.
    La funzione cerca il primo commento (linea che inizia con "#") o docstring che non sia uno shebang.
    Se non viene trovata una descrizione, restituisce un messaggio generico.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignora shebang e linee vuote
                if line.startswith("#!") or not line:
                    continue
                # Se è un commento, lo considera descrizione
                if line.startswith("#"):
                    return line.lstrip("#").strip()
                # Se è l'inizio di una docstring in formato triple quotes
                if line.startswith('"""') or line.startswith("'''"):
                    # Rimuove i delimitatori se presenti sulla stessa linea
                    desc = line.strip('"""').strip("'''").strip()
                    if desc:  # Se contiene del testo, lo restituisce
                        return desc
                    # Altrimenti, continua a leggere le righe successive fino a chiudere la docstring
                    description_lines = []
                    for next_line in f:
                        next_line = next_line.strip()
                        if next_line.endswith('"""') or next_line.endswith("'''"):
                            description_lines.append(next_line.rstrip('"""').rstrip("'''").strip())
                            break
                        description_lines.append(next_line)
                    return " ".join(description_lines).strip()
        return "Nessuna descrizione disponibile."
    except Exception:
        return "Nessuna descrizione disponibile."

def main():
    # Installa Python 3.10 se non è già installato
    install_python_3_10()

    # Installa le dipendenze da requirements.txt (se presente)
    install_requirements()

    # Se esiste una cartella "scripts", usiamola, altrimenti la directory corrente
    base_dir = os.getcwd()
    scripts_dir = os.path.join(base_dir, "scripts")
    if os.path.isdir(scripts_dir):
        directory = scripts_dir
    else:
        directory = base_dir

    scripts = get_scripts(directory)
    if not scripts:
        print("Nessuno script disponibile da eseguire.")
        return

    # Stampa il menu di selezione in ordine alfabetico
    print("Seleziona lo script da eseguire:\n")
    for idx, script in enumerate(scripts, start=1):
        desc = get_description(os.path.join(directory, script))
        print(f"{idx}. {script} - {desc}")

    print("\n0. Esci")

    try:
        choice = int(input("\nInserisci il numero corrispondente alla tua scelta: "))
    except ValueError:
        print("Scelta non valida. Inserire un numero.")
        return

    if choice == 0:
        print("Uscita.")
        return

    if 1 <= choice <= len(scripts):
        selected_script = os.path.join(directory, scripts[choice - 1])
        print(f"Esecuzione di {scripts[choice - 1]}...\n")
        # Avvia lo script selezionato usando l'interprete Python
        subprocess.run([sys.executable, selected_script])
    else:
        print("Scelta non valida.")

if __name__ == '__main__':
    main()
