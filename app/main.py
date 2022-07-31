import os
import pathlib
from datetime import datetime
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, Response, UploadFile, HTTPException
from fastapi.responses import FileResponse

from loguru import logger
from app.mqtt import connect, publish, subscribe

load_dotenv()

app = FastAPI()

# Start Event
@app.middleware("http")
async def request_info(request: Request, call_next):
    start_time = datetime.now()
    response: Response = await call_next(request)
    process_time = int((datetime.now() - start_time).total_seconds() * 1000)
    logger.info(
        f"{request.method} {request.url} {response.status_code} - {str(process_time)}ms"
    )
    return response


# Shutdown Event
@app.on_event("startup")
def startup_event():
    # Log File
    logFilePath = (
        pathlib.Path(__file__).parent.joinpath("..", "logs", "out.log").resolve()
    )
    logger.add(logFilePath)
    # Uploads Folder
    uploadsDir = pathlib.Path(__file__).parent.joinpath("..", "uploads").resolve()
    if os.path.exists(uploadsDir) == False:
        os.mkdir(uploadsDir)

    logger.info("App Started")

    connect()

    subscribe("test/topic")

    publish("test/topic", "Hello from greengrass")


# Shutdown Event
@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down App")


# Ping
@app.get("/ping")
async def ping():
    return "OK"


# Upload File API
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_name = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        file_location = (
            pathlib.Path(__file__).parent.joinpath("..", "uploads", file_name).resolve()
        )
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
            logger.info(f"Uploaded file saved at {file_location}")
        return {"success": True, "file": file_name}
    except Exception as e:
        logger.error(e)
        raise e


# Get Upload File API
@app.get("/uploads/{file_id}")
async def read_item(file_id):
    file_location = (
        pathlib.Path(__file__).parent.joinpath("..", "uploads", file_id).resolve()
    )
    if os.path.exists(file_location):
        return FileResponse(file_location)
    else:
        raise HTTPException(status_code=404, detail="File not found")
