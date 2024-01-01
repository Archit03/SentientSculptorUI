from flask import Flask, request, Response, jsonify
from flask_cors import CORS


import requests
import json


from apps.web.models.users import Users
from constants import ERROR_MESSAGES
from utils.utils import decode_token
from config import OLLAMA_API_BASE_URL, WEBUI_AUTH

app = Flask(__name__)
CORS(
    app
)  # Enable Cross-Origin Resource Sharing (CORS) to allow requests from different domains

# Define the target server URL
TARGET_SERVER_URL = OLLAMA_API_BASE_URL


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
    # Combine the base URL of the target server with the requested path
    target_url = f"{TARGET_SERVER_URL}/{path}"
    print(target_url)

    # Get data from the original request
    data = request.get_data()
    headers = dict(request.headers)

    # Basic RBAC support
    if WEBUI_AUTH:
        if "Authorization" in headers:
            _, credentials = headers["Authorization"].split()
            token_data = decode_token(credentials)
            if token_data is None or "email" not in token_data:
                return jsonify({"detail": ERROR_MESSAGES.UNAUTHORIZED}), 401

            user = Users.get_user_by_email(token_data["email"])
            if user:
                # Only user and admin roles can access
                if user.role in ["user", "admin"]:
                    if path in ["pull", "delete", "push", "copy", "create"]:
                        # Only admin role can perform actions above
                        if user.role == "admin":
                            pass
                        else:
                            return (
                                jsonify({"detail": ERROR_MESSAGES.ACCESS_PROHIBITED}),
                                401,
                            )
                    else:
                        pass
                else:
                    return jsonify({"detail": ERROR_MESSAGES.ACCESS_PROHIBITED}), 401
            else:
                return jsonify({"detail": ERROR_MESSAGES.UNAUTHORIZED}), 401
        else:
            return jsonify({"detail": ERROR_MESSAGES.UNAUTHORIZED}), 401
    else:
        pass

    r = None

    headers.pop("Host", None)
    headers.pop("Authorization", None)
    headers.pop("Origin", None)
    headers.pop("Referer", None)

    try:
        # Make a request to the target server
        r = requests.request(
            method=request.method,
            url=target_url,
            data=data,
            headers=headers,
            stream=True,  # Enable streaming for server-sent events
        )

        r.raise_for_status()

        # Proxy the target server's response to the client
        def generate():
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk

        response = Response(generate(), status=r.status_code)

        # Copy headers from the target server's response to the client's response
        for key, value in r.headers.items():
            response.headers[key] = value

        return response
    except Exception as e:
        print(e)
        error_detail = "Ollama WebUI: Server Connection Error"
        if r != None:
            print(r.text)
            res = r.json()
            if "error" in res:
                error_detail = f"Ollama: {res['error']}"
            print(res)

        return (
            jsonify(
                {
                    "detail": error_detail,
                    "message": str(e),
                }
            ),
            400,
        )


if __name__ == "__main__":
    app.run(debug=True)
