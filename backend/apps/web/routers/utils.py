from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from fastapi import Depends, HTTPException, status
from starlette.responses import StreamingResponse

from pydantic import BaseModel

import requests
import os
import aiohttp
import json


from utils.misc import calculate_sha256

from config import OLLAMA_API_BASE_URL


router = APIRouter()


class UploadBlobForm(BaseModel):
    filename: str


from urllib.parse import urlparse


def parse_huggingface_url(hf_url):
    try:
        # Parse the URL
        parsed_url = urlparse(hf_url)

        # Get the path and split it into components
        path_components = parsed_url.path.split("/")

        # Extract the desired output
        user_repo = "/".join(path_components[1:3])
        model_file = path_components[-1]

        return model_file
    except ValueError:
        return None


async def download_file_stream(url, file_path, file_name, chunk_size=1024 * 1024):
    done = False

    if os.path.exists(file_path):
        current_size = os.path.getsize(file_path)
    else:
        current_size = 0

    headers = {"Range": f"bytes={current_size}-"} if current_size > 0 else {}

    timeout = aiohttp.ClientTimeout(total=600)  # Set the timeout

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers) as response:
            total_size = int(response.headers.get("content-length", 0)) + current_size

            with open(file_path, "ab+") as file:
                async for data in response.content.iter_chunked(chunk_size):
                    current_size += len(data)
                    file.write(data)

                    done = current_size == total_size
                    progress = round((current_size / total_size) * 100, 2)
                    yield f'data: {{"progress": {progress}, "completed": {current_size}, "total": {total_size}}}\n\n'

                if done:
                    file.seek(0)
                    hashed = calculate_sha256(file)
                    file.seek(0)

                    url = f"{OLLAMA_API_BASE_URL}/blobs/sha256:{hashed}"
                    response = requests.post(url, data=file)

                    if response.ok:
                        res = {
                            "done": done,
                            "blob": f"sha256:{hashed}",
                            "name": file_name,
                        }
                        os.remove(file_path)

                        yield f"data: {json.dumps(res)}\n\n"
                    else:
                        raise "Ollama: Could not create blob, Please try again."


@router.get("/download")
async def download(
    url: str,
):
    # url = "https://huggingface.co/TheBloke/stablelm-zephyr-3b-GGUF/resolve/main/stablelm-zephyr-3b.Q2_K.gguf"
    file_name = parse_huggingface_url(url)

    if file_name:
        os.makedirs("./uploads", exist_ok=True)
        file_path = os.path.join("./uploads", f"{file_name}")

        return StreamingResponse(
            download_file_stream(url, file_path, file_name),
            media_type="text/event-stream",
        )
    else:
        return None


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    os.makedirs("./uploads", exist_ok=True)
    file_path = os.path.join("./uploads", file.filename)

    async def file_write_stream():
        total = 0
        total_size = file.size
        chunk_size = 1024 * 1024

        done = False
        try:
            with open(file_path, "wb+") as f:
                while True:
                    chunk = file.file.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    total += len(chunk)
                    done = total_size == total
                    progress = round((total / total_size) * 100, 2)

                    res = {
                        "progress": progress,
                        "total": total_size,
                        "completed": total,
                    }

                    yield f"data: {json.dumps(res)}\n\n"

                if done:
                    f.seek(0)
                    hashed = calculate_sha256(f)
                    f.seek(0)

                    url = f"{OLLAMA_API_BASE_URL}/blobs/sha256:{hashed}"
                    response = requests.post(url, data=f)

                    if response.ok:
                        res = {
                            "done": done,
                            "blob": f"sha256:{hashed}",
                            "name": file.filename,
                        }
                        os.remove(file_path)

                        yield f"data: {json.dumps(res)}\n\n"
                    else:
                        raise "Ollama: Could not create blob, Please try again."

        except Exception as e:
            res = {"error": str(e)}
            yield f"data: {json.dumps(res)}\n\n"

    return StreamingResponse(file_write_stream(), media_type="text/event-stream")
