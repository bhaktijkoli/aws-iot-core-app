import time
import traceback
from loguru import logger

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    QOS,
    PublishToIoTCoreRequest,
    SubscribeToIoTCoreRequest,
    IoTCoreMessage,
)


TIMEOUT = 10

ipc_client = None


class StreamHandler(client.SubscribeToIoTCoreStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            topic = event.message.topic_name
            message = str(event.message.payload, "utf-8")
            logger.info("MQTT Stream Recieved Message")
            logger.info(f"Topic: {topic} Message: {message}")
        except:
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        logger.error("MQTT Stream error " + error)
        return True

    def on_stream_closed(self) -> None:
        logger.info("MQTT Stream Closed")


def connect():
    global ipc_client
    ipc_client = awsiot.greengrasscoreipc.connect()


def publish(topic, message, qos=QOS.AT_LEAST_ONCE):
    request = PublishToIoTCoreRequest()
    request.topic_name = topic
    request.payload = bytes(message, "utf-8")
    request.qos = qos
    operation = ipc_client.new_publish_to_iot_core()
    operation.activate(request)
    future_response = operation.get_response()
    future_response.result(TIMEOUT)


def subscribe(topic, qos=QOS.AT_MOST_ONCE):
    request = SubscribeToIoTCoreRequest()
    request.topic_name = topic
    request.qos = qos
    handler = StreamHandler()
    operation = ipc_client.new_subscribe_to_iot_core(handler)
    operation.activate(request)
    future_response = operation.get_response()
    future_response.result(TIMEOUT)
