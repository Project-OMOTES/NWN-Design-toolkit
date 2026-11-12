@echo off
setlocal

cd /d "%~dp0..\.."

if not exist pyproject.toml (
    echo ERROR: pyproject.toml not found in %CD%
    exit /b 1
)

echo Creating/synchronizing virtual environment in:
echo %CD%

uv sync

if errorlevel 1 (
    echo ERROR: uv sync failed.
    exit /b 1
)

echo.
echo Virtual environment ready:
echo %CD%\.venv