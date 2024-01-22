@echo off
setlocal enabledelayedexpansion

echo this is a work in progress...

:: Set the working directory
set "WORKING_DIR=%CD%"
set "VENV_PATH="
:: Check if Git is installed and in PATH
where git >nul 2>&1
if errorlevel 1 (
    echo Git is not installed or not in PATH.
    exit /b 1
)

:: Clone the repository using Git
echo Cloning facefusion repository...
git clone https://github.com/facefusion/facefusion

:: Define Python version
set "PYTHON_VERSION=3.10.11"

:: Initialize PYTHON_DIR variable
set "PYTHON_DIR="

:: Find Python 3.10 location in LOCALAPPDATA
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set "PYTHON_DIR=%LOCALAPPDATA%\Programs\Python\Python310"
    goto FoundPython
)

:: Find Python 3.10 location in ProgramData
if exist "C:\ProgramData\Python310\python.exe" (
    set "PYTHON_DIR=C:\ProgramData\Python310"
    goto FoundPython
)


:: If Python is not found, download and extract it
if not defined PYTHON_DIR (
    echo Python 3.10 not found. Attempting to download...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip' -OutFile 'python-%PYTHON_VERSION%-embed-amd64.zip'"
    echo Extracting Python...
    powershell -Command "Expand-Archive -LiteralPath 'python-%PYTHON_VERSION%-embed-amd64.zip' -DestinationPath '.\py'"
    set "PYTHON_DIR=%CD%\py"
)

:FoundPython
:: Set PYTHON_EXE variable based on the identified PYTHON_DIR
set "PYTHON_EXE=!PYTHON_DIR!\python.exe"
echo Found Python in %PYTHON_DIR%
echo Executable is %PYTHON_EXE%

set "VENV_PATH=%CD%\venv\Scripts\activate.bat"
set "PYPATH=%CD%\venv\Scripts\python.exe"

@echo on
:: Create virtual environment using located or downloaded Python
echo Creating a virtual environment...
call "%PYTHON_EXE%" -m venv venv

:: Activate the virtual environment
echo Activating the virtual environment...
call "%VENV_PATH%"

:: Install your python package with desired options
echo Installing packages...
call "%PYPATH%" install.py --torch cuda --onnxruntime cuda

:: Download content_analyser.py and copy to /facefusion/facefusion/
echo Downloading content_analyser.py...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/samfisherirl/facefusion-unleashed-one-click-installer/master/facefusion/content_analyser.py' -OutFile '.\facefusion\facefusion\content_analyser.py'"

:: Run the program
echo Running the program...
python run.py --torch cuda --onnxruntime cuda

:: Deactivate virtual environment
:: "%WORKING_DIR%\venv\Scripts\deactivate.bat"

echo Script completed.
endlocal
