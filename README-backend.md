# Proyecto FastAPI

Este proyecto utiliza **FastAPI** y se ejecuta con **uvicorn**. Este README describe cómo levantar el proyecto en **PowerShell** y **Visual Studio 2022**, incluyendo la instalación del entorno virtual y dependencias.

---

## Requisitos Previos

- Python 3.10+ instalado en tu sistema.
- Visual Studio 2022 (con soporte para Python si quieres usar el IDE).
- PowerShell (viene por defecto en Windows).

---

## 1. Clonar el proyecto

```powershell
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>

# 2. Crear entorno virtual

python -m venv venv

# 3. Activar entorno virtual

.\venv\Scripts\Activate.ps1

⚠️ Si recibes un error de ejecución de scripts, ejecuta:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Instalar dependencias

pip install --upgrade pip
pip install -r requirements.txt

# 5. Levantar el servidor con uvicorn
uvicorn app.main:app --reload
