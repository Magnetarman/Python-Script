# Rimozione file non musicali e pulizia cartelle vuote in una directory.
import os
import re
import subprocess
import getpass

# Definisci le estensioni dei file musicali che vuoi preservare
musical_extensions = re.compile(r'\.(flac|opus|mp3|m4a|aac)$', re.IGNORECASE)

def mount_smb_share(unc_path, username=None, password=None):
    """Monta una condivisione SMB usando net use"""
    try:
        # Estrai server e share dal percorso UNC
        # Formato: \\server\share\path
        if not unc_path.startswith('\\\\'):
            return None, "Percorso non UNC valido"

        path_parts = unc_path[2:].split('\\')
        if len(path_parts) < 2:
            return None, "Formato percorso UNC non valido"

        server = path_parts[0]
        share = path_parts[1]

        # Crea il percorso di mount locale (es. Z:)
        drive_letter = "Z:"

        # Comando net use
        cmd = f'net use {drive_letter} \\\\{server}\\{share}'

        if username and password:
            cmd += f' /user:{username} "{password}"'

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            # Restituisci il percorso montato
            mounted_path = f"{drive_letter}\\{'\\'.join(path_parts[2:]) if len(path_parts) > 2 else ''}"
            return mounted_path.rstrip('\\'), None
        else:
            return None, f"Errore nel montare la condivisione: {result.stderr}"

    except Exception as e:
        return None, f"Errore durante il montaggio: {str(e)}"

def unmount_smb_share(drive_letter="Z:"):
    """Smonta una condivisione SMB"""
    try:
        cmd = f'net use {drive_letter} /delete'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def delete_non_music_files(folder_path):
    try:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            # Gestione sicura dei file
            for name in files:
                try:
                    file_path = os.path.join(root, name)
                    # Se il file non ha un'estensione musicale, viene eliminato
                    if not musical_extensions.search(name):
                        print(f"Deleting file: {file_path}")
                        os.remove(file_path)
                except (OSError, PermissionError) as e:
                    print(f"Impossibile eliminare il file {file_path}: {e}")
                    continue

            # Gestione sicura delle directory
            for name in dirs:
                try:
                    dir_path = os.path.join(root, name)
                    # Se la cartella è vuota, viene eliminata
                    if not os.listdir(dir_path):
                        print(f"Deleting empty directory: {dir_path}")
                        os.rmdir(dir_path)
                except (OSError, PermissionError) as e:
                    print(f"Impossibile eliminare la directory {dir_path}: {e}")
                    continue
    except (OSError, PermissionError) as e:
        print(f"Errore durante l'accesso al percorso {folder_path}: {e}")
        return

def is_valid_path(path, use_smb=True):
    """Verifica se un percorso è valido e accessibile"""
    try:
        # Per percorsi UNC, proviamo prima se esiste
        if path.startswith('\\\\') or (len(path) > 1 and path[1] == ':'):
            return os.path.exists(path)
        return False
    except (OSError, PermissionError):
        if use_smb and path.startswith('\\\\'):
            return None  # Indica che potrebbe essere necessario SMB
        return False

def get_smb_credentials():
    """Chiede le credenziali SMB all'utente"""
    print("\nRichieste credenziali per la condivisione di rete:")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    return username, password

def main():
    folder_path = input("Inserisci il percorso della cartella: ").strip()

    # Normalizza il percorso rimuovendo eventuali virgolette
    folder_path = folder_path.strip('"\'')

    mounted_path = None
    drive_letter = None

    # Verifica se il percorso è accessibile direttamente
    path_check = is_valid_path(folder_path, use_smb=False)

    if not path_check and folder_path.startswith('\\\\'):
        print("Il percorso di rete non è accessibile direttamente.")
        print("Tentativo di connessione tramite SMB...")

        # Chiedi credenziali
        username, password = get_smb_credentials()

        # Tenta di montare la condivisione
        mounted_path, error = mount_smb_share(folder_path, username, password)

        if error:
            print(f"Errore durante la connessione: {error}")
            print("Verifica username, password e che la condivisione sia raggiungibile.")
            return

        if mounted_path and os.path.exists(mounted_path):
            print(f"Connessione SMB stabilita. Utilizzando: {mounted_path}")
            # Usa il percorso montato per l'operazione
            work_path = mounted_path
            drive_letter = "Z:"
        else:
            print("Impossibile accedere al percorso anche dopo la connessione SMB.")
            return
    elif path_check:
        # Percorso accessibile direttamente
        work_path = folder_path
    else:
        print("Il percorso inserito non è valido o non è accessibile. Per favore riprova.")
        return

    try:
        delete_non_music_files(work_path)
        print("Pulizia completata.")
    except PermissionError:
        print(f"Errore: Accesso negato al percorso '{work_path}'. Verifica i permessi.")
    except OSError as e:
        print(f"Errore durante la pulizia: {e}")
    except Exception as e:
        print(f"Errore imprevisto: {e}")
    finally:
        # Smonta la condivisione SMB se era stata montata
        if drive_letter:
            print("Disconnessione dalla condivisione di rete...")
            if unmount_smb_share(drive_letter):
                print("Disconnessione completata.")
            else:
                print("Attenzione: impossibile disconnettere automaticamente la condivisione.")

if __name__ == "__main__":
    while True:
        main()
        scelta = input("\nUtilizza di nuovo lo script digitando 1 o premi 0 per ritornare a main.py: ").strip()
        if scelta == '1':
            continue
        elif scelta == '0':
            break
        else:
            print("Scelta non valida. Inserire 1 o 0.")
