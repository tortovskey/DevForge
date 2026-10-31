@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" backend\desktop_launcher.py
) else if exist "release\DevForge\DevForge.exe" (
    "release\DevForge\DevForge.exe"
) else (
    echo Python environment not found. Please run setup.bat first.
    pause
)
if errorlevel 1 pause
