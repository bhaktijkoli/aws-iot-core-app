import os
import pathlib
from dotenv import load_dotenv
from loguru import logger
from app.mqtt import connect, publish, subscribe

load_dotenv()


def start():
    logFilePath = (
        pathlib.Path(__file__).parent.joinpath("..", "logs", "out.log").resolve()
    )
    logger.add(logFilePath)
    logger.info("App Started")

    ipc_socket = os.getenv("AWS_GG_NUCLEUS_DOMAIN_SOCKET_FILEPATH_FOR_COMPONENT")
    authtoken = os.getenv("SVCUID")
    stream_port = os.getenv("STREAM_MANAGER_SERVER_PORT")
    container_authtoken = os.getenv("AWS_CONTAINER_AUTHORIZATION_TOKEN")
    logger.info(f"ipc_socket={ipc_socket}")
    logger.info(f"authtoken={authtoken}")
    logger.info(f"stream_port={stream_port}")
    logger.info(f"container_authtoken={container_authtoken}")

    connect()

    subscribe("test/topic")

    publish("test/topic", "Hello from greengrass")

    try:
        print("Press Ctrl+C to exit")
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Shutting down app")
