@echo off
REM Abre JupyterLab con el entorno del proyecto, parado en la carpeta de cuadernos.
REM Doble clic sobre este archivo. Se abre el navegador solo. Para cerrar: cerrar esta ventana negra.
cd /d "%~dp0"
if not exist ".venv\Scripts\jupyter.exe" (
  echo No se encontro el entorno .venv. Ver README.md para crearlo.
  pause
  exit /b 1
)
".venv\Scripts\jupyter.exe" lab notebooks
