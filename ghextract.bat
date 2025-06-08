@echo off
:: GitHub Repo Extractor by Rudra Garg
:: Usage: drag and drop a URL or type it after the script

if "%~1"=="" (
    echo Please provide a GitHub repository URL.
    echo Example: ghextract.bat https://github.com/username/repo.git
    exit /b 1
)

python "%~dp0ghextract.py" %*
pause
