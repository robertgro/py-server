@echo off
::call robocopy-remote.cmd
call .\env\Scripts\activate.bat
.\env\Scripts\python.exe -m pip list
.\env\Scripts\python.exe -m pip install --upgrade pip
.\env\Scripts\python.exe -m pip install -r requirements.txt
.\env\Scripts\python.exe -m pip list
::.\env\Scripts\python.exe -m pip freeze > requirements.txt
:: https://stackoverflow.com/questions/14684968/how-to-export-virtualenv