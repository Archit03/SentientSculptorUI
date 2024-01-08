docker build -t ollama-webui .
docker stop ollama-webui || true
docker rm ollama-webui || true
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v ollama-webui:/app/backend/data --name ollama-webui --restart always ollama-webui
docker image prune -f