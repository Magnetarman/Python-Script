# Conversione di email .eml in PDF con dettagli del messaggio.
import os
import sys
import pdfkit
from email import message_from_file

# Funzione per convertire il contenuto di un file .eml in HTML
def eml_to_html(eml_file):
    with open(eml_file, 'r', encoding='utf-8') as f:
        msg = message_from_file(f)
        subject = msg["Subject"] or "(No Subject)"
        sender = msg["From"] or "(Unknown Sender)"
        to = msg["To"] or "(Unknown Recipient)"

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

        # Creazione dell'HTML
        html_content = f"""
        <html>
        <head><meta charset='utf-8'><title>{subject}</title></head>
        <body>
            <h1>Subject: {subject}</h1>
            <p><strong>From:</strong> {sender}</p>
            <p><strong>To:</strong> {to}</p>
            <pre>{body}</pre>
        </body>
        </html>
        """
        return html_content

# Funzione per convertire file .eml in PDF
def convert_eml_to_pdf(input_folder):
    output_folder = os.path.join(input_folder, "converted_pdfs")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.eml'):
            eml_path = os.path.join(input_folder, filename)
            html_content = eml_to_html(eml_path)

            pdf_filename = os.path.splitext(filename)[0] + ".pdf"
            pdf_path = os.path.join(output_folder, pdf_filename)

            pdfkit.from_string(html_content, pdf_path)
            print(f"Converted: {filename} -> {pdf_path}")

if __name__ == "__main__":
    # Richiede il percorso della cartella all'utente
    input_folder = input("Inserisci il percorso della cartella contenente i file .eml: ").strip()

    if not os.path.isdir(input_folder):
        print("Errore: Il percorso specificato non è una cartella valida.")
        sys.exit(1)

    convert_eml_to_pdf(input_folder)
    print("Tutti i file .eml sono stati convertiti in PDF nella cartella 'converted_pdfs'.")