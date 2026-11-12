@echo off

set "VENV_PATH=%~dp0..\..\.venv"

if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found.
    echo Expected location:
    echo %VENV_PATH%
    echo.
    echo Run create_venv.bat first.
    exit /b 1
)

call "%VENV_PATH%\Scripts\activate.bat"

cd /d "%~dp0..\.."

call make html
pause