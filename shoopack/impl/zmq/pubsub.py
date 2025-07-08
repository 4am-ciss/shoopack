from ...base import PublisherBase, SubscriberBase
from ...validator import network_validation
import zmq
import re
import json

from typing import Any, Union

class ZmqPublisher(PublisherBase):

    def __init__(
        self,
        address: str,
        port: int = 5555,
        protocol: str = "tcp",
        topic_name: str = "default_topic",
        connect: bool = False,
        chunk_size: int = 1024,
        delimiter: str = " ",
        message_type: Any = None
    ):
        self.socket_addr = f"{protocol}://{address}:{port}"
        self.topic_name = topic_name
        self.chunk_size = chunk_size
        self.delimiter = delimiter
        self.connect = connect

        # Validate address and port
        network_validation(address, port, protocol)

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)

        if connect:
            self.socket.connect(self.socket_addr)
        else:
            self.socket.bind(self.socket_addr)

        self.message_type = message_type

    def __repr__(self):
        s = "ZmqPublisher(socket_addr={}, topic_name={}, connect={}, chunk_size={}, delimiter=`{}`)".format(
           self.socket_addr,  self.topic_name, self.connect, self.chunk_size, self.delimiter
        )
        return s

    def __str__(self):
        return str(self.__repr__())


    def _pub_str(self, message: str) -> None:
        """
        Publish a string message with the topic prefix.
        """
        self.socket.send_string(f"{self.topic_name}{self.delimiter}{message}")

    def _pub_json(self, message: (dict|list)) -> None:
        """
        Publish a JSON-serializable message with the topic prefix.
        """
        self.socket.send_string(f"{self.topic_name}{self.delimiter}{json.dumps(message)}")

    def _pub_audio_chunk(self, audio_chunk: bytes) -> None:
        """
        Publish an audio chunk with the topic prefix.
        """
        chunks = []
        for i in range(0, len(audio_chunk), self.chunk_size):
            chunk = audio_chunk[i:i + self.chunk_size]
            chunks.append(chunk)

        mp_msg = [f"{self.topic_name}{self.delimiter}{chunk}" for chunk in chunks]
        self.socket.send_multipart(mp_msg)

    def publish(self, message: Any):
        """
        Publish a message with the appropriate method based on its type.
        """
        self.message_type = type(message)
        if isinstance(message, str):
            self._pub_str(message)
        elif isinstance(message, (dict, list)):
            self._pub_json(message)
        elif isinstance(message, bytes):
            self._pub_audio_chunk(message)
        else:
            raise TypeError("Unsupported message type. Must be str, dict, list, or bytes.")



class ZmqSubscriber(SubscriberBase):
    def __init__(
        self,
        address: str,
        port: int = 5555,
        protocol: str = "tcp",
        topic_name: str = "default_topic",
        connect: bool = True,
        chunk_size: int = 1024,
        message_type: type(str | bytes | dict | list) = str,
        delimiter: str = " ",
    ):
        self.socket_addr = f"{protocol}://{address}:{port}"
        self.topic_name = topic_name
        self.chunk_size = chunk_size
        self.delimiter = delimiter
        self.message_type = message_type
        self.connect = connect

        # Validate address and port
        network_validation(address, port, protocol)

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        if connect:
            self.socket.connect(self.socket_addr)
        else:
            self.socket.bind(self.socket_addr)

        self.socket.setsockopt_string(zmq.SUBSCRIBE, f"{self.topic_name}{self.delimiter}")

    def __repr__(self):
        s = "ZmqSubscriber(socket_addr={}, topic_name={}, connect={}, chunk_size={}, delimiter=`{}`)".format(
           self.socket_addr,  self.topic_name, self.connect, self.chunk_size, self.delimiter
        )
        return s

    def __str__(self):
        return str(self.__repr__())


    def receive(self):
        """
        Receive a message from the socket.
        Returns:
            str, bytes, dict, or list: The received message.
        """
        if self.message_type == str:
            msg = self.socket.recv_string()
            return msg[len(self.topic_name) + len(self.delimiter):]
        elif self.message_type == bytes:
            msg = self.socket.recv_multipart()
            return b''.join(msg[len(self.topic_name) + len(self.delimiter):])
        elif self.message_type in (dict, list):
            msg = self.socket.recv_string()
            return json.loads(msg.split(self.delimiter, 1)[1])
        else:
            raise TypeError("Unsupported message type. Must be str, bytes, dict, or list.")


    def listen(self, callback):
        """
        Listen for incoming messages and call the provided callback function.
        :param callback: Function to call with the received message.
        """
        while True:
            message = self.receive()
            callback(message)
