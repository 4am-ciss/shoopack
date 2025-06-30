from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

class Publisher(ABC):
    """
    Abstract base class for publishers.
    """

    @abstractmethod
    def publish(self, message: Union[str, Dict[str, Any]]) -> None:
        """
        Publish a message to the publisher.

        Args:
            message (Union[str, Dict[str, Any]]): The message to be published.
        """
        pass


class Subscriber(ABC):
    """
    Abstract base class for subscribers.
    """

    @abstractmethod
    def subscribe(self, topic: str) -> None:
        """
        Subscribe to a topic.

        Args:
            topic (str): The topic to subscribe to.
        """
        pass

    @abstractmethod
    def receive(self) -> List[Union[str, Dict[str, Any]]]:
        """
        Receive messages from the subscribed topics.

        Returns:
            List[Union[str, Dict[str, Any]]]: A list of received messages.
        """
        pass
