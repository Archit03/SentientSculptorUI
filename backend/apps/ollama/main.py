import json
import uuid

import requests
from config import ENABLE_OLLAMA, OLLAMA_API_BASE_URL
from constants import ERROR_MESSAGES
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from utils.utils import get_current_user, get_admin_user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.ENABLE_OLLAMA = ENABLE_OLLAMA
app.state.OLLAMA_API_BASE_URL = OLLAMA_API_BASE_URL

# TARGET_SERVER_URL = OLLAMA_API_BASE_URL


REQUEST_POOL = []


class EnabledUpdateForm(BaseModel):
    enabled: bool


@app.get("/enabled")
async def get_ollama_enablement(user=Depends(get_admin_user)):
    return {"ENABLE_OLLAMA": app.state.ENABLE_OLLAMA}


@app.post("/enabled/update")
async def update_ollama_enablement(form_data: EnabledUpdateForm, user=Depends(get_admin_user)):
    app.state.ENABLE_OLLAMA = form_data.enabled
    return {"ENABLE_OLLAMA": app.state.ENABLE_OLLAMA}


@app.get("/url")
async def get_ollama_api_url(user=Depends(get_admin_user)):
    return {"OLLAMA_API_BASE_URL": app.state.OLLAMA_API_BASE_URL}


class UrlUpdateForm(BaseModel):
    url: str


@app.post("/url/update")
async def update_ollama_api_url(form_data: UrlUpdateForm, user=Depends(get_admin_user)):
    app.state.OLLAMA_API_BASE_URL = form_data.url
    return {"OLLAMA_API_BASE_URL": app.state.OLLAMA_API_BASE_URL}


@app.get("/cancel/{request_id}")
async def cancel_ollama_request(request_id: str, user=Depends(get_current_user)):
    if user:
        if request_id in REQUEST_POOL:
            REQUEST_POOL.remove(request_id)
        return True
    else:
        raise HTTPException(status_code=401, detail=ERROR_MESSAGES.ACCESS_PROHIBITED)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(path: str, request: Request, user=Depends(get_current_user)):
    target_url = f"{app.state.OLLAMA_API_BASE_URL}/{path}"

    body = await request.body()
    headers = dict(request.headers)

    if user.role in ["user", "admin"]:
        if path in ["pull", "delete", "push", "copy", "create"]:
            if user.role != "admin":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )

    headers.pop("host", None)
    headers.pop("authorization", None)
    headers.pop("origin", None)
    headers.pop("referer", None)

    r = None

    def get_request():
        nonlocal r

        request_id = str(uuid.uuid4())
        try:
            REQUEST_POOL.append(request_id)

            def stream_content():
                try:
                    if path in ["chat"]:
                        yield json.dumps({"id": request_id, "done": False}) + "\n"

                    for chunk in r.iter_content(chunk_size=8192):
                        if request_id in REQUEST_POOL:
                            yield chunk
                        else:
                            print("User: canceled request")
                            break
                finally:
                    if hasattr(r, "close"):
                        r.close()
                        REQUEST_POOL.remove(request_id)

            r = requests.request(
                method=request.method,
                url=target_url,
                data=body,
                headers=headers,
                stream=True,
            )

            r.raise_for_status()

            # r.close()

            return StreamingResponse(
                stream_content(),
                status_code=r.status_code,
                headers=dict(r.headers),
            )
        except Exception as e:
            raise e

    try:
        return await run_in_threadpool(get_request)
    except Exception as e:
        error_detail = "Open WebUI: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )
