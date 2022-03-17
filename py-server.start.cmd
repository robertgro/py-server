@echo off
::cd %~dp0
::start python main.py 127.0.0.1 8000
powershell -NoLogo -ExecutionPolicy Unrestricted -File .\py-server.start.ps1