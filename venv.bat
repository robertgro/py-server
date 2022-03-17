@echo off
if not exist env\ (
    python -m venv env
)
start /wait /b .\env\Scripts\activate.bat
rem https://ss64.com/nt/start.html