@echo off
REM Levanta la API y abre la pantalla de demostracion en el navegador.
REM Doble clic sobre este archivo. Para apagarla: cerrar esta ventana negra.
cd /d "%~dp0"
if not exist ".venv\Scripts\uvicorn.exe" (
  echo No se encontro el entorno .venv. Ver README.md para crearlo.
  pause
  exit /b 1
)
echo Levantando el servicio. El navegador se abre solo cuando este listo.
start "" /min powershell -NoProfile -Command "for($i=0;$i -lt 90;$i++){try{$null=Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8000/health' -TimeoutSec 2; Start-Process 'http://127.0.0.1:8000/docs'; break}catch{Start-Sleep -Seconds 1}}"
".venv\Scripts\uvicorn.exe" api.app:app
pause
