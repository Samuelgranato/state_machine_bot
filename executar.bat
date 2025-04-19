@echo off
:: Caminho absoluto para o Python da venv (baseado na localização do próprio .bat)
set PYTHON=%~dp0.venv\Scripts\python.exe

:: Executa com o Python correto
"%PYTHON%" "%~dp0menu.py"
pause
