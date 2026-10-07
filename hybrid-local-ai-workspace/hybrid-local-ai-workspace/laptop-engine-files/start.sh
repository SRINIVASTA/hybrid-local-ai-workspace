#!/bin/bash
echo "⚙️ Creating data directories..."
mkdir -p data/webui data/ollama

echo "🐳 Running Ollama & Open WebUI on your laptop..."
docker compose up -d

echo "⏳ Waiting for Ollama to stabilize..."
until docker exec -it ollama-engine ollama list >/dev/null 2>&1; do
  sleep 2
done

echo "🤖 Downloading Gemma 2 (2B) model onto your hard drive..."
docker exec -it ollama-engine ollama pull gemma2:2b

echo "=========================================================="
echo "🎉 DOWNLOAD COMPLETE & LOCAL SERVER RUNNING!"
echo "🌐 Go to: http://localhost:3000 to upload documents."
echo "✨ Next, open a new terminal and run: ngrok http 3000"
echo "=========================================================="
