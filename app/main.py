import os
from dotenv import load_dotenv
from loguru import logger
from app.mqtt import connect, publish, subscribe

load_dotenv()


def start():
    logger.info("App Started")

    ipc_socket = os.getenv("AWS_GG_NUCLEUS_DOMAIN_SOCKET_FILEPATH_FOR_COMPONENT")
    authtoken = os.getenv("SVCUID")
    logger.info(f"ipc_socket={ipc_socket}")
    logger.info(f"authtoken={authtoken}")

    connect()

    logger.info("Connected")

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
