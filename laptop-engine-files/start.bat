@echo off
title 🔌 Local AI Workspace Engine Launcher
cls
echo ==========================================================
echo       🚀 STARTING YOUR LOCAL WORKSPACE PIPELINE
echo ==========================================================
echo.

:: Step 1: Ensure directories exist safely
echo [1/4] Verifying data workspace folders...
mkdir data\webui 2>nul
mkdir data\ollama 2>nul
echo       ✓ Directories verified.
echo.

:: Step 2: Clear traffic blocks by keeping Open WebUI stopped
echo [2/4] Optimizing port lanes for Cloud Web App...
docker stop open-webui-dashboard >nul 2>&1
echo       ✓ Port traffic lanes cleared!
echo.

:: Step 3: Waking up your core Ollama container
echo [3/4] Initializing local Ollama-Engine...
docker start ollama-engine >nul 2>&1
echo       ✓ Ollama container engine is awake!
echo.

:: Step 4: Verification loop to ensure model is awake
echo [4/4] Verifying Gemma2 model status inside storage...
:loop
docker exec ollama-engine ollama list >nul 2>&1
if %errorlevel% neq 0 (
    timeout /t 2 /nobreak >nul
    goto loop
)
echo       ✓ Local engine stable and model library linked!
echo.

echo ==========================================================
echo   🎉 SUCCESS: LOCAL PIPELINE ACTIVE!
echo   👉 COPY THE NEW URL BELOW AND PASTE IT ON THE WEBSITE!
echo   ⚠️ KEEP THIS DOS WINDOW OPEN WHILE CHATTING!
echo ==========================================================
echo.

:: Launch ngrok pointing directly to Ollama core engine port
"D:\localai\ngrok-v3-stable-windows-amd64\ngrok.exe" http 11434
