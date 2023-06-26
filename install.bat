
@ECHO OFF
IF /i {%1}=={ECHO} ECHO ON&SHIFT

setlocal

set "env_name=%~1"
if "%env_name%" == "" set "env_name=venv"

set "python_exe=%env_name%\Scripts\python.exe"

if not exist "%python_exe%" (
    python -m venv "%env_name%"
)

call "%env_name%\Scripts\activate.bat"

python -m pip install --upgrade pip

python -m pip install -r ./requirements.txt

pause
endlocal



