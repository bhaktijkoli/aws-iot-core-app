import pathlib
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

from loguru import logger
from app.mqtt import connect, publish, subscribe

load_dotenv()

app = FastAPI()


@app.middleware("http")
async def request_info(request: Request, call_next):
    start_time = datetime.now()
    response: Response = await call_next(request)
    process_time = int((datetime.now() - start_time).total_seconds() * 1000)
    logger.info(
        f"{request.method} {request.url} {response.status_code} - {str(process_time)}ms"
    )
    return response


@app.on_event("startup")
def startup_event():
    logFilePath = (
        pathlib.Path(__file__).parent.joinpath("..", "logs", "out.log").resolve()
    )
    logger.add(logFilePath)
    logger.info("App Started")

    connect()

    subscribe("test/topic")

    publish("test/topic", "Hello from greengrass")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down App")


@app.get("/ping")
async def ping():
    return "OK"
