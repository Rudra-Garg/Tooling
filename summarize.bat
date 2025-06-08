@echo off
:: summarize.bat — Local Git Repository to Gemini auto-summaries
if "%~1" == "" (
  echo Usage: summarize.bat [repository_path]
  echo Example: summarize.bat C:\Projects\my-repo
  pause
  exit /b
)

echo Summarizing repository: %~1
python "%~dp0summarize.py" "%~1"
pause