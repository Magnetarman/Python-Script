# Download immagini da una pagina web, inclusi contenuti Base64.
import os
import requests
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from PIL import Image
import io

def download_images(url):
    # Creare la cartella export se non esiste
    folder = "export"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Scaricare il contenuto della pagina
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Errore nel caricamento della pagina: {e}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Ottenere tutti i tag img
    img_tags = soup.find_all("img")
    
    for index, img in enumerate(img_tags):
        img_url = img.get("src") or img.get("data-src")  # Considera anche lazy loading
        if not img_url:
            continue
        
        if img_url.startswith("data:image"):  # Gestire immagini Base64
            try:
                header, encoded = img_url.split(",", 1)
                img_data = base64.b64decode(encoded)
                ext = header.split("/")[1].split(";")[0]  # Estrai l'estensione dell'immagine
                
                if ext == "svg+xml":
                    ext = "png"  # Convertire SVG in PNG
                    img_name = os.path.join(folder, f"base64_image_{index}.{ext}")
                    
                    with open(img_name, "wb") as img_file:
                        img_file.write(img_data)
                    
                    print(f"Scaricata immagine Base64 convertita in PNG: {img_name}")
                else:
                    img_name = os.path.join(folder, f"base64_image_{index}.{ext}")
                    
                    with open(img_name, "wb") as img_file:
                        img_file.write(img_data)
                    
                    print(f"Scaricata immagine Base64: {img_name}")
            except Exception as e:
                print(f"Errore nella conversione Base64: {e}")
            continue
        
        # Convertire URL relativi in assoluti
        img_url = urljoin(url, img_url)
        img_url = unquote(img_url.split('?')[0])  # Rimuovere parametri dall'URL
        
        try:
            img_response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
            img_response.raise_for_status()
            
            img_name = os.path.join(folder, os.path.basename(urlparse(img_url).path))
            
            # Salvare l'immagine
            with open(img_name, "wb") as img_file:
                img_file.write(img_response.content)
            
            print(f"Scaricata: {img_name}")
        except requests.exceptions.RequestException as e:
            print(f"Errore nel download di {img_url}: {e}")

if __name__ == "__main__":
    url = input("Inserisci l'URL della pagina web: ")
    download_images(url)