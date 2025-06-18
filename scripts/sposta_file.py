# Spostamento file in directory principale e rimozione cartelle vuote.
import os
import shutil

def move_files_to_main_directory(main_directory):
    # Verifica se la directory principale esiste
    if not os.path.isdir(main_directory):
        print(f"Errore: La directory '{main_directory}' non esiste.")
        return

    print(f"Directory principale: {main_directory}")

    # Conta il numero di file da spostare
    total_files = 0
    for root, dirs, files in os.walk(main_directory):
        if root == main_directory:
            continue
        total_files += len(files)
    
    if total_files == 0:
        print("Nessun file trovato nelle sottocartelle.")
        return
    else:
        print(f"Trovati {total_files} file da spostare.")

    files_moved = 0

    # Cammina attraverso tutte le sottocartelle
    for root, dirs, files in os.walk(main_directory):
        # Salta la directory principale
        if root == main_directory:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            new_location = os.path.join(main_directory, file)

            # Controlla se esiste già un file con lo stesso nome nella directory principale
            if os.path.exists(new_location):
                print(f"Attenzione: Il file '{file}' esiste già nella directory principale. Saltando.")
                continue
            
            # Sposta il file alla directory principale
            print(f"Spostando '{file_path}' a '{new_location}'")
            shutil.move(file_path, new_location)
            files_moved += 1

    print(f"{files_moved} file sono stati spostati alla directory principale.")

    # Rimuove le sottocartelle vuote
    empty_dirs_removed = 0
    for root, dirs, files in os.walk(main_directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # Controlla se la directory è vuota
                print(f"Rimuovendo directory vuota '{dir_path}'")
                os.rmdir(dir_path)
                empty_dirs_removed += 1

    print(f"{empty_dirs_removed} sottocartelle vuote sono state rimosse.")
    print("Operazione completata.")

# Chiede all'utente di inserire il percorso della directory principale
main_directory = input("Inserisci il percorso della directory principale: ").strip()

# Esegui la funzione
move_files_to_main_directory(main_directory)
