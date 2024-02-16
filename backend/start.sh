#!/usr/bin/env bash

# Assuming /venv is the location of your virtual environment
VENV_PATH=".venv"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit

KEY_FILE=".webui_secret_key"

PORT="${PORT:-8080}"
if test -z "$WEBUI_SECRET_KEY" && test -z "$WEBUI_JWT_SECRET_KEY"; then
  echo "No WEBUI_SECRET_KEY provided"

  if ! [ -e "$KEY_FILE" ]; then
    echo "Generating WEBUI_SECRET_KEY"
    # Generate a random value to use as a WEBUI_SECRET_KEY in case the user didn't provide one.
    echo $(head -c 12 /dev/random | base64) > "$KEY_FILE"
  fi

  echo "Loading WEBUI_SECRET_KEY from $KEY_FILE"
  WEBUI_SECRET_KEY=$(cat "$KEY_FILE")
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Set the WEBUI_SECRET_KEY environment variable and execute uvicorn
WEBUI_SECRET_KEY="$WEBUI_SECRET_KEY" exec uvicorn main:app --host 0.0.0.0 --port "$PORT" --forwarded-allow-ips '*'