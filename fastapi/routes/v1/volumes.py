# volumes.py

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from databricks.sdk import WorkspaceClient
import os

router = APIRouter(tags=["volumes"])
w = WorkspaceClient()


@router.get(
    "/download",
    summary="Stream a Unity Catalog file",
    description=(
        "Streams the content of a file stored in a Unity Catalog volume without "
        "loading the entire file into memory. "
        "Client must call: `/download?file_path=/Volumes/<...>/<filename>`."
    ),
    responses={
        200: {
            "description": "Streaming binary response; the client should receive "
                           "the file as an attachment."
        },
        400: {"description": "Bad request (e.g. missing file_path or Databricks error)"},
        404: {"description": "File not found in Unity Catalog or underlying storage"},
    },
)
async def download_file(
    file_path: str = Query(
        ..., 
        description="Full path to the file inside a Unity Catalog volume, e.g. `/Volumes/main/data/large.csv`"
    )
):
    """
    Streams a large file from Unity Catalog to the HTTP client in chunks.

    - `file_path`: the path inside your Unity Catalog volume.
    - Returns a StreamingResponse so that the API server never holds the full file in RAM.
    """
    if not file_path:
        raise HTTPException(status_code=400, detail="`file_path` is required.")

    try:
        # Begin the download from Databricks; resp.contents is a generator of bytes
        resp = w.files.download(file_path)
    except Exception as e:
        # If Databricks returns an error (e.g. path not found), convert to 400
        raise HTTPException(status_code=400, detail=f"Databricks error: {str(e)}")

    file_name = os.path.basename(file_path)

    def file_iterator(chunk_size: int = 1024 * 1024):
        """
        Read resp.contents in constant‐size chunks (here 1 MB) and yield them
        directly to the StreamingResponse. FastAPI will stream each chunk
        to the client without buffering the whole file.
        """
        with resp.contents as stream:
            for chunk in stream:
                yield chunk

    headers = {
        "Content-Disposition": f'attachment; filename="{file_name}"'
    }

    return StreamingResponse(
        file_iterator(),
        media_type="application/octet-stream",
        headers=headers,
    )