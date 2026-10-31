@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" backend\ide_launcher.py
if errorlevel 1 pause
