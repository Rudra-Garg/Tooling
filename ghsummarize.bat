@echo off
:: summarize_repos.bat — GitHub → Gemini auto‑summaries
if "%~1" neq "" (
  echo This script doesn’t take args; just make sure GITHUB_TOKEN and GEMINI_API_KEY are set.
  pause
  exit /b
)
python "%~dp0ghsummarize.py"
pause