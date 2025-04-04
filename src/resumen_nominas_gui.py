import os
import re
import csv
import shutil
import pdfplumber
from tkinter import Tk, filedialog, messagebox, Label, Entry, Button
from fpdf import FPDF
from fpdf.enums import XPos, YPos

def procesar_nominas(carpeta, mes):
    carpeta_mes = os.path.join(carpeta, mes.replace(" ", "_"))
    os.makedirs(carpeta_mes, exist_ok=True)

    salida_csv = os.path.join(carpeta_mes, "resumen_nominas.csv")
    salida_pdf = os.path.join(carpeta_mes, "resumen_final.pdf")

    with open(salida_csv, "w", newline="", encoding='utf-8') as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(["Trabajador", "Liquido", "Deduccion", "OtrasDeducciones"])

        for archivo in os.listdir(carpeta):
            if archivo.lower().endswith(".pdf") and not archivo.startswith("resumen"):
                ruta_pdf = os.path.join(carpeta, archivo)

                nombre_trabajador = os.path.splitext(archivo)[0]
                nombre_trabajador = re.sub(r"n[oó]mina.*", "", nombre_trabajador, flags=re.IGNORECASE).strip()

                with pdfplumber.open(ruta_pdf) as pdf:
                    texto = ""
                    lineas = []
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            texto += page_text + "\n"
                            lineas += page_text.splitlines()

                texto = texto.replace(",", ".").replace("€", "")

                match_liquido = re.search(r"L[ií]quido total a percibir.*?(\d+\.\d{2})", texto)
                liquido = match_liquido.group(1) if match_liquido else "0.00"

                match_deduccion = re.search(r"Total a deducir.*?(\d+\.\d{2})", texto)
                deduccion = match_deduccion.group(1) if match_deduccion else ""

                otras_deducciones = ""
                for linea in lineas:
                    if "5. otras deducciones" in linea.lower():
                        limpia = "".join(c for c in linea if c.isdigit() or c in ",. ")
                        numeros = re.findall(r"\d+[.,]\d{2}", limpia)
                        if numeros:
                            otras_deducciones = numeros[-1].replace(",", ".")
                        break

                writer.writerow([nombre_trabajador, liquido, deduccion, otras_deducciones])

                nuevo_nombre = f"{nombre_trabajador} - {mes}.pdf"
                nuevo_ruta = os.path.join(carpeta_mes, nuevo_nombre)
                shutil.copy2(ruta_pdf, nuevo_ruta)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 10, text=f"Resumen de Nóminas - {mes}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    with open(salida_csv, newline='', encoding='utf-8') as f_csv:
        reader = csv.DictReader(f_csv)
        for fila in reader:
            linea = f"{fila['Trabajador']} - Líquido: {fila['Liquido']} euros | Deducción: {fila['Deduccion']} euros"
            if fila['OtrasDeducciones']:
                linea += f" | Otras deducciones: {fila['OtrasDeducciones']} euros"
            pdf.cell(200, 10, text=linea, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(salida_pdf)
    return salida_csv, salida_pdf

def lanzar_interfaz():
    def seleccionar_carpeta():
        carpeta = filedialog.askdirectory()
        if carpeta:
            carpeta_entry.delete(0, "end")
            carpeta_entry.insert(0, carpeta)

    def ejecutar():
        carpeta = carpeta_entry.get()
        mes = mes_entry.get()
        if not carpeta or not mes:
            messagebox.showerror("Error", "Debes seleccionar la carpeta y escribir el mes.")
            return
        try:
            csv_path, pdf_path = procesar_nominas(carpeta, mes)
            messagebox.showinfo("Éxito", f"Resumen generado correctamente.\nCSV: {csv_path}\nPDF: {pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana = Tk()
    ventana.title("Resumen de Nóminas")
    ventana.geometry("450x180")

    Label(ventana, text="Carpeta con PDFs:").pack(pady=(10, 0))
    carpeta_entry = Entry(ventana, width=50)
    carpeta_entry.pack()
    Button(ventana, text="Seleccionar carpeta", command=seleccionar_carpeta).pack(pady=5)

    Label(ventana, text="Mes (ej: Abril 2025):").pack()
    mes_entry = Entry(ventana, width=30)
    mes_entry.pack()

    Button(ventana, text="Generar Resumen", command=ejecutar).pack(pady=10)
    ventana.mainloop()

if __name__ == "__main__":
    lanzar_interfaz()
