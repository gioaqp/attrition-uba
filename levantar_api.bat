@echo off
REM Levanta la API y abre la pantalla de demostracion en el navegador.
REM Doble clic sobre este archivo. Para apagarla: cerrar esta ventana negra.
cd /d "%~dp0"
if not exist ".venv\Scripts\uvicorn.exe" (
  echo No se encontro el entorno .venv. Ver README.md para crearlo.
  pause
  exit /b 1
)
start "" /min cmd /c "timeout /t 4 >nul & start "" http://127.0.0.1:8000/docs"
".venv\Scripts\uvicorn.exe" api.app:app
pause
