# Individuazione e rimozione sicura di cartelle vuote in una directory.
import os

def find_empty_directories(folder_path):
    empty_dirs = []
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                empty_dirs.append(dir_path)
    return empty_dirs

def print_and_delete_empty_dirs(empty_dirs):
    print("Cartelle vuote trovate:")
    for dir in empty_dirs:
        print(dir)
    
    print(f"\nNumero totale di cartelle vuote trovate: {len(empty_dirs)}")
    
    if len(empty_dirs) > 0:
        proceed = input("Vuoi procedere con la cancellazione delle cartelle vuote? (y/n): ").strip().lower()
        if proceed == 'y':
            for dir in empty_dirs:
                os.rmdir(dir)
                print(f"Cancellato: {dir}")
        else:
            print("Operazione annullata.")
    else:
        print("Nessuna cartella vuota trovata.")

def main():
    folder_path = input("Inserisci il percorso della cartella: ").strip()
    if os.path.isdir(folder_path):
        empty_dirs = find_empty_directories(folder_path)
        print_and_delete_empty_dirs(empty_dirs)
    else:
        print("Il percorso inserito non è valido. Per favore riprova.")

if __name__ == "__main__":
    main()
