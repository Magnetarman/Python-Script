# Genera PDF da immagini Jpeg.
"""
Script per l'elaborazione di documenti scansionati
Versione: 1.5
Autore: MagnetarMan + Claude AI
Data: 2025

Questo script fornisce un'interfaccia grafica per processare immagini di documenti scansionati
e convertirle in un PDF ottimizzato.
"""

import os
import sys
import cv2
import numpy as np
from datetime import datetime
from PIL import Image, ImageFilter, ImageEnhance
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
import io

class DocumentProcessor:
    def __init__(self):
        self.processed_images = []
        self.original_folder = None
        
    def analyze_image(self, image_path):
        """
        Analizza l'immagine per identificare il contenuto del documento
        """
        try:
            # Carica l'immagine con OpenCV
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Impossibile caricare l'immagine: {image_path}")
            
            # Converti in RGB per PIL
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return image_rgb
        except Exception as e:
            print(f"Errore nell'analisi dell'immagine {image_path}: {e}")
            return None
    
    def enhance_sharpness(self, image):
        """
        Aumenta la nitidezza dell'immagine (funzione rimossa per problemi di leggibilità)
        """
        # Funzione disabilitata: l'aumento della nitidezza rendeva la pagina illegibile
        # Ritorna l'immagine senza modifiche
        return image
    
    def detect_and_correct_orientation(self, image):
        """
        Rileva e corregge l'orientamento della pagina usando metodi più robusti
        """
        # Converte in scala di grigi per l'analisi
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Applica blur per ridurre il rumore
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Applica soglia per evidenziare il testo
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Prova diversi metodi per rilevare l'orientamento
        
        # Metodo 1: Analisi delle linee usando Hough Transform
        edges = cv2.Canny(binary, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        
        angles = []
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                angle = np.degrees(theta) - 90
                angles.append(angle)
        
        # Metodo 2: Analisi dei contorni di testo
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtra e analizza i contorni più significativi
        text_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:  # Filtra contorni troppo piccoli
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h
                # Considera solo contorni che potrebbero essere testo
                if 0.1 < aspect_ratio < 10 and w > 10 and h > 5:
                    text_contours.append(contour)
        
        # Calcola angoli dai contorni di testo
        for contour in text_contours:
            if cv2.contourArea(contour) > 100:
                rect = cv2.minAreaRect(contour)
                angle = rect[2]
                if rect[1][0] < rect[1][1]:  # width < height
                    angle = angle + 90
                angles.append(angle)
        
        # Metodo 3: Analisi della distribuzione dei pixel
        # Calcola le proiezioni orizzontali e verticali
        h_projection = np.sum(binary, axis=1)
        v_projection = np.sum(binary, axis=0)
        
        # Calcola la varianza delle proiezioni per diversi angoli
        test_angles = [-90, -45, 0, 45, 90]
        variances = []
        
        for test_angle in test_angles:
            if test_angle != 0:
                center = (image.shape[1] // 2, image.shape[0] // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, test_angle, 1.0)
                rotated_binary = cv2.warpAffine(binary, rotation_matrix, (binary.shape[1], binary.shape[0]))
                h_proj = np.sum(rotated_binary, axis=1)
            else:
                h_proj = h_projection
            
            # Calcola la varianza della proiezione orizzontale
            variance = np.var(h_proj)
            variances.append(variance)
        
        # L'angolo con la varianza maggiore dovrebbe essere quello corretto
        if variances:
            best_angle_idx = np.argmax(variances)
            best_angle = test_angles[best_angle_idx]
            angles.append(best_angle)
        
        # Determina l'angolo finale
        if angles:
            # Raggruppa angoli simili
            angle_groups = {}
            for angle in angles:
                # Normalizza l'angolo
                normalized = angle % 90
                if normalized > 45:
                    normalized = normalized - 90
                
                # Raggruppa per intervalli di 10 gradi
                group_key = round(normalized / 10) * 10
                if group_key not in angle_groups:
                    angle_groups[group_key] = []
                angle_groups[group_key].append(angle)
            
            # Trova il gruppo con più angoli
            if angle_groups:
                best_group = max(angle_groups.items(), key=lambda x: len(x[1]))
                rotation_angle = np.median(best_group[1])
                
                # Determina la rotazione da applicare
                if rotation_angle > 60:
                    final_rotation = 90
                elif rotation_angle > 30:
                    final_rotation = 45
                elif rotation_angle < -60:
                    final_rotation = -90
                elif rotation_angle < -30:
                    final_rotation = -45
                elif abs(rotation_angle) < 5:
                    final_rotation = 0
                else:
                    final_rotation = rotation_angle
                
                # Applica la rotazione se necessaria
                if abs(final_rotation) > 2:  # Soglia minima per evitare rotazioni inutili
                    center = (image.shape[1] // 2, image.shape[0] // 2)
                    rotation_matrix = cv2.getRotationMatrix2D(center, final_rotation, 1.0)
                    
                    # Calcola le nuove dimensioni per evitare di tagliare l'immagine
                    cos_angle = abs(rotation_matrix[0, 0])
                    sin_angle = abs(rotation_matrix[0, 1])
                    new_width = int((image.shape[0] * sin_angle) + (image.shape[1] * cos_angle))
                    new_height = int((image.shape[0] * cos_angle) + (image.shape[1] * sin_angle))
                    
                    # Aggiusta la matrice di rotazione per centrare l'immagine
                    rotation_matrix[0, 2] += (new_width / 2) - (image.shape[1] / 2)
                    rotation_matrix[1, 2] += (new_height / 2) - (image.shape[0] / 2)
                    
                    # Applica la rotazione
                    rotated = cv2.warpAffine(image, rotation_matrix, (new_width, new_height), 
                                           borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
                    
                    print(f"Immagine ruotata di {final_rotation} gradi")
                    return rotated
        
        return image
    
    def convert_to_bw(self, image):
        """
        Converte l'immagine in bianco e nero puro
        """
        # Converte in scala di grigi
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Applica soglia adattiva per un migliore risultato
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Converte in RGB per mantenere compatibilità
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    
    def clean_noise(self, image):
        """
        Applica filtri di pulizia del rumore mantenendo i testi nitidi
        """
        # Converte in scala di grigi per l'elaborazione
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # 1. Filtro mediano per rimuovere il rumore salt-and-pepper
        # Usa un kernel piccolo per non danneggiare i dettagli del testo
        denoised = cv2.medianBlur(gray, 3)
        
        # 2. Morfologia: apertura per rimuovere piccoli punti di rumore
        # Crea un kernel molto piccolo per preservare i caratteri
        kernel_opening = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        opened = cv2.morphologyEx(denoised, cv2.MORPH_OPEN, kernel_opening)
        
        # 3. Morfologia: chiusura per riempire piccoli buchi nei caratteri
        kernel_closing = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_closing)
        
        # 4. Filtro bilaterale per ridurre ulteriormente il rumore preservando i bordi
        # Usa parametri conservativi per mantenere la nitidezza del testo
        bilateral = cv2.bilateralFilter(closed, 5, 80, 80)
        
        # 5. Riapplica una soglia per assicurare il bianco e nero puro
        _, clean_binary = cv2.threshold(bilateral, 127, 255, cv2.THRESH_BINARY)
        
        # 6. Operazione finale di pulizia: rimuove componenti connesse troppo piccole
        # Trova tutte le componenti connesse
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            255 - clean_binary, connectivity=8, ltype=cv2.CV_32S)
        
        # Crea una maschera per le componenti da mantenere
        min_area = 10  # Rimuove componenti più piccole di 10 pixel
        mask = np.zeros_like(clean_binary)
        
        for i in range(1, num_labels):  # Salta il background (label 0)
            if stats[i, cv2.CC_STAT_AREA] >= min_area:
                mask[labels == i] = 255
        
        # Applica la maschera
        result = clean_binary.copy()
        result[mask == 255] = 0  # Rende neri i pixel del testo
        
        # Converte in RGB per mantenere compatibilità
        return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    
    def enhance_contrast(self, image):
        """
        Enfatizza leggermente il contrasto dell'immagine (funzione rimossa per problemi di leggibilità)
        """
        # Funzione disabilitata: il contrasto eccessivo rendeva la pagina illegibile
        # Ritorna l'immagine senza modifiche
        return image
    
    def remove_borders(self, image):
        """
        Rimuove i bordi esterni identificando automaticamente il foglio
        """
        # Converte in scala di grigi per l'analisi
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Applica blur per ridurre il rumore
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Applica soglia per separare il foglio dallo sfondo
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Trova i contorni
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Trova il contorno più grande (presumibilmente il foglio)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Calcola il rettangolo di delimitazione
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Aggiungi un piccolo margine per sicurezza
            margin = 10
            x = max(0, x - margin)
            y = max(0, y - margin)
            w = min(image.shape[1] - x, w + 2 * margin)
            h = min(image.shape[0] - y, h + 2 * margin)
            
            # Ritaglia l'immagine
            cropped = image[y:y+h, x:x+w]
            
            # Verifica che il ritaglio sia ragionevole
            if cropped.shape[0] > image.shape[0] * 0.3 and cropped.shape[1] > image.shape[1] * 0.3:
                return cropped
        
        # Se non riesce a trovare un contorno valido, ritorna l'immagine originale
        return image
    
    def process_single_image(self, image_path, progress_callback=None):
        """
        Processa una singola immagine attraverso tutte le fasi
        """
        try:
            if progress_callback:
                progress_callback("Analisi immagine...")
            
            # 1. Analisi iniziale
            image = self.analyze_image(image_path)
            if image is None:
                return None
            
            if progress_callback:
                progress_callback("Aumento nitidezza...")
            
            # 2. Aumento della nitidezza (disabilitato)
            # image = self.enhance_sharpness(image)
            
            if progress_callback:
                progress_callback("Correzione orientamento...")
            
            # 3. Correzione dell'orientamento
            image = self.detect_and_correct_orientation(image)
            
            if progress_callback:
                progress_callback("Conversione in bianco e nero...")
            
            # 4. Conversione in bianco e nero
            image = self.convert_to_bw(image)
            
            if progress_callback:
                progress_callback("Pulizia del rumore...")
            
            # 5. Pulizia del rumore (nuovo passaggio)
            image = self.clean_noise(image)
            
            if progress_callback:
                progress_callback("Enfatizzazione contrasto...")
            
            # 5. Enfatizzazione del contrasto (disabilitata)
            # image = self.enhance_contrast(image)
            
            if progress_callback:
                progress_callback("Rimozione bordi...")
            
            # 6. Eliminazione dei bordi
            image = self.remove_borders(image)
            
            return image
            
        except Exception as e:
            print(f"Errore nel processamento dell'immagine {image_path}: {e}")
            return None
    
    def create_pdf(self, processed_images, output_path):
        """
        Crea un PDF dalle immagini processate
        """
        try:
            # Crea il canvas PDF
            c = canvas.Canvas(output_path, pagesize=A4)
            
            for i, image_array in enumerate(processed_images):
                # Converte l'array numpy in PIL Image
                pil_image = Image.fromarray(image_array)
                
                # Crea un buffer in memoria per l'immagine
                img_buffer = io.BytesIO()
                pil_image.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                # Dimensioni della pagina A4
                page_width, page_height = A4
                
                # Calcola le dimensioni dell'immagine mantenendo le proporzioni
                img_width, img_height = pil_image.size
                aspect_ratio = img_width / img_height
                
                if aspect_ratio > page_width / page_height:
                    # L'immagine è più larga, adatta alla larghezza
                    new_width = page_width
                    new_height = page_width / aspect_ratio
                else:
                    # L'immagine è più alta, adatta all'altezza
                    new_height = page_height
                    new_width = page_height * aspect_ratio
                
                # Centro l'immagine nella pagina
                x = (page_width - new_width) / 2
                y = (page_height - new_height) / 2
                
                # Disegna l'immagine sul PDF
                c.drawImage(ImageReader(img_buffer), x, y, width=new_width, height=new_height)
                
                # Aggiungi una nuova pagina se non è l'ultima immagine
                if i < len(processed_images) - 1:
                    c.showPage()
            
            # Salva il PDF
            c.save()
            return True
            
        except Exception as e:
            print(f"Errore nella creazione del PDF: {e}")
            return False

class DocumentScannerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Elaboratore Documenti Scansionati")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.processor = DocumentProcessor()
        self.image_paths = []
        self.is_processing = False
        
        self.setup_gui()
    
    def setup_gui(self):
        """
        Configura l'interfaccia grafica
        """
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configura il ridimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Titolo
        title_label = ttk.Label(main_frame, text="Elaboratore Documenti Scansionati", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sezione selezione file
        ttk.Label(main_frame, text="Seleziona Immagini:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.file_listbox = tk.Listbox(main_frame, height=8)
        self.file_listbox.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Scrollbar per la listbox
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S), pady=5)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Pulsanti per gestire i file
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Aggiungi Immagini", 
                  command=self.add_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Rimuovi Selezionata", 
                  command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Svuota Lista", 
                  command=self.clear_list).pack(side=tk.LEFT, padx=5)
        
        # Pulsante elaborazione
        self.process_button = ttk.Button(main_frame, text="Elabora Documenti", 
                                        command=self.start_processing, style="Accent.TButton")
        self.process_button.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Barra di progresso
        self.progress_var = tk.StringVar()
        self.progress_var.set("Pronto per l'elaborazione")
        
        ttk.Label(main_frame, text="Stato:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.status_label = ttk.Label(main_frame, textvariable=self.progress_var)
        self.status_label.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Informazioni aggiuntive
        info_frame = ttk.LabelFrame(main_frame, text="Informazioni", padding="10")
        info_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        info_text = """Operazioni eseguite su ogni immagine:
1. Analisi e caricamento dell'immagine
2. Correzione automatica dell'orientamento (migliorata)
3. Conversione in bianco e nero
4. Pulizia del rumore (nuovo - rimuove effetto fotocopiatrice)
5. Rimozione automatica dei bordi

Il PDF finale sarà salvato nella stessa cartella delle immagini.
Nota: Le funzioni di aumento nitidezza e contrasto sono state rimosse per migliorare la leggibilità."""
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)
    
    def add_images(self):
        """
        Aggiunge immagini alla lista
        """
        file_paths = filedialog.askopenfilenames(
            title="Seleziona immagini",
            filetypes=[("Immagini JPEG", "*.jpg *.jpeg"), ("Tutte le immagini", "*.jpg *.jpeg *.png")]
        )
        
        for file_path in file_paths:
            if file_path not in self.image_paths:
                self.image_paths.append(file_path)
                self.file_listbox.insert(tk.END, os.path.basename(file_path))
        
        self.update_ui_state()
    
    def remove_selected(self):
        """
        Rimuove l'immagine selezionata dalla lista
        """
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            self.file_listbox.delete(index)
            del self.image_paths[index]
            self.update_ui_state()
    
    def clear_list(self):
        """
        Svuota la lista delle immagini
        """
        self.file_listbox.delete(0, tk.END)
        self.image_paths.clear()
        self.update_ui_state()
    
    def update_ui_state(self):
        """
        Aggiorna lo stato dell'interfaccia
        """
        has_images = len(self.image_paths) > 0
        self.process_button.configure(state=tk.NORMAL if has_images and not self.is_processing else tk.DISABLED)
        
        if has_images:
            self.progress_var.set(f"Pronto per elaborare {len(self.image_paths)} immagini")
        else:
            self.progress_var.set("Pronto per l'elaborazione")
    
    def start_processing(self):
        """
        Avvia il processo di elaborazione in un thread separato
        """
        if not self.image_paths:
            messagebox.showwarning("Attenzione", "Seleziona almeno un'immagine da elaborare.")
            return
        
        self.is_processing = True
        self.progress_bar.start()
        self.update_ui_state()
        
        # Avvia il thread di elaborazione
        thread = threading.Thread(target=self.process_images)
        thread.daemon = True
        thread.start()
    
    def process_images(self):
        """
        Processa tutte le immagini e crea il PDF
        """
        try:
            processed_images = []
            total_images = len(self.image_paths)
            
            # Determina la cartella di output
            if self.image_paths:
                output_folder = os.path.dirname(self.image_paths[0])
            else:
                output_folder = os.path.expanduser("~")
            
            # Processa ogni immagine
            for i, image_path in enumerate(self.image_paths):
                def update_progress(message):
                    self.root.after(0, lambda: self.progress_var.set(f"Immagine {i+1}/{total_images}: {message}"))
                
                processed_image = self.processor.process_single_image(image_path, update_progress)
                
                if processed_image is not None:
                    processed_images.append(processed_image)
                else:
                    self.root.after(0, lambda: messagebox.showerror("Errore", f"Impossibile processare l'immagine: {os.path.basename(image_path)}"))
            
            if processed_images:
                # Crea il nome del file PDF
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                pdf_filename = f"Documenti_Scansionati_{timestamp}.pdf"
                pdf_path = os.path.join(output_folder, pdf_filename)
                
                # Aggiorna il progresso
                self.root.after(0, lambda: self.progress_var.set("Creazione PDF..."))
                
                # Crea il PDF
                if self.processor.create_pdf(processed_images, pdf_path):
                    self.root.after(0, lambda: self.show_success_message(pdf_path))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Errore", "Errore nella creazione del PDF"))
            else:
                self.root.after(0, lambda: messagebox.showerror("Errore", "Nessuna immagine è stata processata con successo"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Errore", f"Errore durante l'elaborazione: {str(e)}"))
        finally:
            # Ripristina l'interfaccia
            self.root.after(0, self.processing_complete)
    
    def show_success_message(self, pdf_path):
        """
        Mostra il messaggio di successo
        """
        messagebox.showinfo("Successo", f"Elaborazione completata!\nIl PDF è stato salvato in:\n{pdf_path}")
    
    def processing_complete(self):
        """
        Ripristina l'interfaccia dopo l'elaborazione
        """
        self.is_processing = False
        self.progress_bar.stop()
        self.progress_var.set("Elaborazione completata")
        self.update_ui_state()
    
    def run(self):
        """
        Avvia l'applicazione
        """
        self.root.mainloop()

def main():
    """
    Funzione principale
    """
    try:
        app = DocumentScannerGUI()
        app.run()
    except Exception as e:
        print(f"Errore nell'avvio dell'applicazione: {e}")
        messagebox.showerror("Errore", f"Errore nell'avvio dell'applicazione: {e}")

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