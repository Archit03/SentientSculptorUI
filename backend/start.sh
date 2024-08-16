#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit

KEY_FILE=.Falcor_secret_key

PORT="${PORT:-8080}"
HOST="${HOST:-0.0.0.0}"
if test "$Falcor_SECRET_KEY $Falcor_JWT_SECRET_KEY" = " "; then
  echo "Loading Falcor_SECRET_KEY from file, not provided as an environment variable."

  if ! [ -e "$KEY_FILE" ]; then
    echo "Generating Falcor_SECRET_KEY"
    # Generate a random value to use as a Falcor_SECRET_KEY in case the user didn't provide one.
    echo $(head -c 12 /dev/random | base64) > "$KEY_FILE"
  fi

  echo "Loading Falcor_SECRET_KEY from $KEY_FILE"
  Falcor_SECRET_KEY=$(cat "$KEY_FILE")
fi

if [[ "${USE_OLLAMA_DOCKER,,}" == "true" ]]; then
    echo "USE_OLLAMA is set to true, starting ollama serve."
    ollama serve &
fi

if [[ "${USE_CUDA_DOCKER,,}" == "true" ]]; then
  echo "CUDA is enabled, appending LD_LIBRARY_PATH to include torch/cudnn & cublas libraries."
  export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib/python3.11/site-packages/torch/lib:/usr/local/lib/python3.11/site-packages/nvidia/cudnn/lib"
fi

# Check if SPACE_ID is set, if so, configure for space
if [ -n "$SPACE_ID" ]; then
  echo "Configuring for HuggingFace Space deployment"
  if [ -n "$ADMIN_USER_EMAIL" ] && [ -n "$ADMIN_USER_PASSWORD" ]; then
    echo "Admin user configured, creating"
    Falcor_SECRET_KEY="$Falcor_SECRET_KEY" uvicorn main:app --host "$HOST" --port "$PORT" --forwarded-allow-ips '*' &
    Falcor_pid=$!
    echo "Waiting for Falcor to start..."
    while ! curl -s http://localhost:8080/health > /dev/null; do
      sleep 1
    done
    echo "Creating admin user..."
    curl \
      -X POST "http://localhost:8080/api/v1/auths/signup" \
      -H "accept: application/json" \
      -H "Content-Type: application/json" \
      -d "{ \"email\": \"${ADMIN_USER_EMAIL}\", \"password\": \"${ADMIN_USER_PASSWORD}\", \"name\": \"Admin\" }"
    echo "Shutting down Falcor..."
    kill $Falcor_pid
  fi

  export Falcor_URL=${SPACE_HOST}
fi

Falcor_SECRET_KEY="$Falcor_SECRET_KEY" exec uvicorn main:app --host "$HOST" --port "$PORT" --forwarded-allow-ips '*'
