import os
import shutil
from tkinter import Tk, filedialog

# Funzione per selezionare la directory
def select_directory():
    root = Tk()
    root.withdraw()  # Nascondi la finestra principale di Tkinter
    directory = filedialog.askdirectory(title="Seleziona la cartella")
    return directory

# Chiedi all'utente di inserire la parola (o set di caratteri)
search_term = input("Inserisci il set di caratteri che vuoi cercare alla fine dei nomi dei file: ")

# Permetti all'utente di selezionare la directory
directory = select_directory()

if directory:
    # Crea la cartella "duplicati" nella stessa directory in cui si trova lo script
    duplicati_folder = os.path.join(directory, "duplicati")
    os.makedirs(duplicati_folder, exist_ok=True)

    # Cerca tutti i file nella directory specificata e nelle sottocartelle
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            # Ottieni il nome del file senza estensione
            name_without_ext, ext = os.path.splitext(file_name)
            # Controlla se il nome del file (senza estensione) termina con il set di caratteri specificato
            if name_without_ext.endswith(search_term):
                # Ottieni il percorso completo del file
                file_path = os.path.join(root, file_name)
                # Sposta il file nella cartella "duplicati"
                shutil.move(file_path, duplicati_folder)
                print(f"File spostato in 'duplicati': {file_path}")

    print("Operazione completata!")
else:
    print("Nessuna cartella selezionata.")
