# Quirofano oftalmologia (Htal Rossi)

Programa de consola para pegar una tabla (copiada desde Excel), limpiar datos, editar en Excel, generar un PDF y (opcionalmente) enviarlo por Gmail.

## Uso en Windows (recomendado: EXE)

1. En GitHub, ir a **Actions** -> workflow **Build Windows EXE**.
2. Abrir el último run y descargar el artefacto **app-windows**.
3. Descomprimir. Dentro vas a ver una carpeta `dist/main/`.
4. Ejecutar `dist/main/main.exe`.

Archivos que genera el programa:
- `plantilla_quirofano.pdf` (en la misma carpeta del EXE si es escribible; si no, en una carpeta `Quirofano_oftalmologia_rossi` dentro del home del usuario).
- `data/excel.xlsx` (para editar antes de crear el PDF).
- `credentials/email_token.json` (se crea la primera vez que se envía un mail).

Notas para el envío por email:
- La primera vez que se usa “Enviar PDF a email”, se abre el navegador para autenticar Gmail (OAuth).
- El `credentials/email_credentials.json` va incluido dentro del ejecutable.

Nota de dependencias:
- El build de Windows usa `requirements-app.txt` (mínimo y portable). El `requirements.txt` actual está “inflado” con paquetes del sistema y no es portable a Windows.

## Uso en Linux (desde código)

Crear un venv e instalar dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
