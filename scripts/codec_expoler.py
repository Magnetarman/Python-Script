# Analizza i file video identifica codec H264 o H265, ne mostra i dettagli e consente l’esportazione
import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

h264_list = []
h265_list = []

def get_video_info(file_path):
    try:
        # ffprobe per codec, risoluzione e durata
        cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name,width,height',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            file_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.strip().split('\n')

        if len(output) < 4:
            return None

        codec, width, height, duration_str = output
        duration = float(duration_str)
        size_bytes = os.path.getsize(file_path)

        bitrate_bps = (size_bytes * 8) / duration
        bitrate_kbps = int(bitrate_bps / 1000)

        return {
            'Nome File': os.path.basename(file_path),
            'Percorso': file_path,
            'Codec': codec,
            'Risoluzione': f"{width}x{height}",
            'Bitrate (kbps)': bitrate_kbps,
            'Dimensione (GB)': round(size_bytes / (1024 ** 3), 3)
        }
    except Exception as e:
        print(f"Errore durante l'analisi: {e}")
        return None

def scan_videos(folder):
    global h264_list, h265_list
    h264_list.clear()
    h265_list.clear()

    for root, _, files in os.walk(folder):
        for name in files:
            if name.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv')):
                path = os.path.join(root, name)
                info = get_video_info(path)
                if info:
                    if info['Codec'] == 'h264':
                        h264_list.append(info)
                        root_window.after(0, lambda i=info: add_to_tree(tree_h264, i))
                    elif info['Codec'] in ('h265', 'hevc'):
                        h265_list.append(info)
                        root_window.after(0, lambda i=info: add_to_tree(tree_h265, i))

def add_to_tree(tree, data):
    tree.insert('', tk.END, values=[
        data['Nome File'],
        data['Codec'],
        data['Risoluzione'],
        data['Bitrate (kbps)'],
        f"{data['Dimensione (GB)']} GB"
    ])

def start_threaded_scan():
    folder = filedialog.askdirectory(title="Seleziona la cartella da analizzare")
    if not folder:
        return

    for t in [tree_h264, tree_h265]:
        for i in t.get_children():
            t.delete(i)

    threading.Thread(target=lambda: run_scan(folder), daemon=True).start()

def run_scan(folder):
    scan_videos(folder)
    if not h264_list and not h265_list:
        messagebox.showinfo("Risultato", "Nessun file video H264 o H265 trovato.")
    else:
        messagebox.showinfo("Risultato", "Analisi completata.")

def export_data():
    if not h264_list and not h265_list:
        messagebox.showwarning("Attenzione", "Prima analizza una cartella.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel file", "*.xlsx"), ("CSV file", "*.csv")],
        title="Salva il file come..."
    )
    if not file_path:
        return

    try:
        df_h264 = pd.DataFrame(h264_list)
        df_h265 = pd.DataFrame(h265_list)

        if file_path.endswith('.xlsx'):
            with pd.ExcelWriter(file_path) as writer:
                df_h264.to_excel(writer, sheet_name="H264", index=False)
                df_h265.to_excel(writer, sheet_name="H265", index=False)
        else:
            df_h264.to_csv(file_path.replace(".csv", "_h264.csv"), index=False)
            df_h265.to_csv(file_path.replace(".csv", "_h265.csv"), index=False)

        messagebox.showinfo("Esportazione", "Esportazione completata con successo.")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante l'esportazione:\n{str(e)}")

# GUI Setup
root_window = tk.Tk()
root_window.title("Analizzatore Codec Video")
root_window.geometry("850x550")

btn = tk.Button(root_window, text="Seleziona cartella e analizza", command=start_threaded_scan)
btn.pack(pady=10)

tabs = ttk.Notebook(root_window)
tabs.pack(fill='both', expand=True)

def create_tree_tab(label):
    frame = ttk.Frame(tabs)
    columns = ("Nome File", "Codec", "Risoluzione", "Bitrate (kbps)", "Dimensione")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=160)
    tree.pack(fill='both', expand=True)
    tabs.add(frame, text=label)
    return tree

tree_h264 = create_tree_tab("Video H264")
tree_h265 = create_tree_tab("Video H265")

export_btn = tk.Button(root_window, text="Esporta in Excel o CSV", command=export_data)
export_btn.pack(pady=10)

root_window.mainloop()
