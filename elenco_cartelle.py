import os

def list_folders_in_path():
    # Chiede all'utente il percorso
    path = input("Inserisci il percorso: ").strip()
    
    # Verifica che il percorso esista e sia una directory
    if not os.path.isdir(path):
        print(f"Errore: Il percorso '{path}' non è valido o non è una directory.")
        return
    
    # Elenca tutte le cartelle di primo livello
    folders = [os.path.join(path, folder) for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    
    # Percorso del file di output
    output_file = os.path.join(path, "cartelle_primo_livello.txt")
    
    try:
        # Salva i risultati nel file
        with open(output_file, "w") as f:
            f.write("Cartelle di primo livello:\n")
            for folder in folders:
                f.write(f"{folder}\n")
        print(f"Risultati salvati in: {output_file}")
    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")

if __name__ == "__main__":
    list_folders_in_path()
