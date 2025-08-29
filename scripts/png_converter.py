# Conversione ricorsiva di tutte le immagini PNG in JPEG all'interno di una cartella specificata, gestendo la trasparenza e rimuovendo i file PNG originali.
import os
from PIL import Image

def convert_png_to_jpeg(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(".png"):
                png_path = os.path.join(dirpath, filename)
                jpg_filename = os.path.splitext(filename)[0] + ".jpg"
                jpg_path = os.path.join(dirpath, jpg_filename)

                try:
                    with Image.open(png_path) as img:
                        if img.mode in ("RGBA", "LA"):
                            # Sfondo bianco per immagini con trasparenza
                            background = Image.new("RGB", img.size, (255, 255, 255))
                            background.paste(img, mask=img.split()[-1])  # Usa l'alpha come maschera
                            background.save(jpg_path, "JPEG")
                        else:
                            # Nessuna trasparenza, conversione diretta
                            img.convert("RGB").save(jpg_path, "JPEG")

                    os.remove(png_path)
                    print(f"[✔] Convertito: {png_path} → {jpg_path}")
                except Exception as e:
                    print(f"[!] Errore con il file {png_path}: {e}")

def main():
    folder = input("Inserisci il percorso della cartella da analizzare: ").strip()
    if not os.path.isdir(folder):
        print("Percorso non valido. Uscita.")
        return

    convert_png_to_jpeg(folder)
    print("Operazione completata.")

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
