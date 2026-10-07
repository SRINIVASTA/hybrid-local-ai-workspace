@echo off
echo ⚙️ Creating data directories...
mkdir data\webui 2>nul
mkdir data\ollama 2>nul

echo 🐳 Running Ollama ^& Open WebUI on your laptop...
docker compose up -d

echo ⏳ Waiting for Ollama to stabilize...
:loop
docker exec -it ollama-engine ollama list >nul 2>&1
if %errorlevel% neq 0 (
    timeout /t 2 /nobreak >nul
    goto loop
)

echo 🤖 Downloading Gemma 2 (2B) model onto your hard drive...
docker exec -it ollama-engine ollama pull gemma2:2b

echo ==========================================================
echo 🎉 DOWNLOAD COMPLETE ^& LOCAL SERVER RUNNING!
echo 🌐 Go to: http://localhost:3000 to upload documents.
echo ✨ Next, open a new command prompt and run: ngrok http 3000
echo ==========================================================
pause
