@echo off
:: ai.bat - Ask a question to Gemini API

if "%~1" == "" (
  echo Usage: ai [your question here]
  echo Example: ai What is the capital of France?
  exit /b 1
)

python "%~dp0ai.py" %*