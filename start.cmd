@echo off
setlocal EnableDelayedExpansion


set "path=%cd%"
cd ..
cls

if not exist "%path%\.env" (
    echo Error: .env file not found.
    exit /b 1
)

for /f "usebackq tokens=1,2 delims==" %%A in ("%path%\.env") do set "%%A=%%B"

if not exist "%path%\.venv\Scripts\python.exe" (
    echo Error: Virtual environment not found in %path%\.venv
    exit /b 1
)

echo.
echo Starting DisSafe Shield API
echo.
"%path%\.venv\Scripts\python.exe" "%path%\manage.py" runserver %HOST%:%PORT%
echo.
echo.
