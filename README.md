# Resumen de Nóminas 📄💼

**Aplicación profesional de escritorio desarrollada por Jesús Ramos Mejías para automatizar la gestión de nóminas en su entorno de trabajo.**

## 🧠 ¿Qué hace esta app?

- Lee archivos PDF de nóminas.
- Extrae el nombre del trabajador, líquido total a percibir, deducciones y otras deducciones.
- Renombra cada PDF con formato estándar (`Nombre Apellido - Mes Año.pdf`).
- Genera un resumen en formato CSV y PDF.
- Organiza todos los documentos en una carpeta por mes.
- Proporciona una interfaz gráfica fácil de usar con `tkinter`.

## 🧰 Tecnologías utilizadas

- `Python 3.10+`
- `pdfplumber`
- `fpdf`
- `tkinter`
- `PyInstaller` (para crear ejecutables)

## 🚀 Uso

### Ejecutar desde código:

```bash
pip install -r requirements.txt
python src/resumen_nominas_gui.py
```

### Compilar ejecutable (Windows):

```bash
pyinstaller ResumenNominas.spec
```

O simplemente haz doble clic en:

```bat
compilar_ejecutable.bat
```

### Ejecutable portable

Disponible en la carpeta `/build/ResumenNominas.exe`.

## 🧪 Casos de uso reales

Esta app ha sido usada en entornos reales para:

- Procesar mensual y automáticamente decenas de nóminas.
- Crear informes claros y exportables.
- Ahorro de tiempo administrativo.

## 🧩 Personalización

Puedes adaptar la lógica del script para otras estructuras de nómina en PDF o añadir exportación a Excel, resumen mensual, etc.

## 🪪 Licencia

MIT License. Puedes usarla, adaptarla y compartirla libremente.
