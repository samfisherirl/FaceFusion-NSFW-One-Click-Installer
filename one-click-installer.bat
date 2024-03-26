@echo off
SET venv_dir=venv

REM Check if the virtual environment directory exists
IF EXIST "%venv_dir%\Scripts\activate.bat" (
    ECHO Virtual environment found. Activating...
) ELSE (
    ECHO Creating virtual environment...
    python -m venv %venv_dir%
)

REM Activate the virtual environment
CALL %venv_dir%\Scripts\activate.bat

REM Upgrade pip and install requirements if needed
IF NOT EXIST "%venv_dir%\Scripts\pip.exe" (
    ECHO Installing dependencies...
    python -m pip install --upgrade pip
    python -m pip install --upgrade -r requirements.txt
)

REM Run the Python script
python -m pip install --upgrade -r requirements.txt 
python main.py

REM close this window on completion

REM Pause the command window
pause