from abc import ABC, abstractmethod
from typing import Callable, Any


# ===== Pub/Sub Interface =====

class PublisherBase(ABC):
    @abstractmethod
    def publish(self, message: Any) -> None:
        """Send a message to subscribers."""
        raise NotImplementedError


class SubscriberBase(ABC):
    @abstractmethod
    def listen(self, callback: Callable[[Any], None]) -> None:
        """Listen for messages and handle them via the callback."""
        raise NotImplementedError

    @abstractmethod
    def receive(self) -> Any:
        """Receive a message from the publisher."""
        raise NotImplementedError


# ===== Req/Res Interface =====

class RequesterBase(ABC):
    @abstractmethod
    def send(self, message: Any) -> Any:
        """Send a request and return the response."""
        raise NotImplementedError


class ResponderBase(ABC):
    @abstractmethod
    def listen(self, callback: Callable[[Any], Any]) -> None:
        """Listen for requests and respond using the callback result."""
        raise NotImplementedError

    @abstractmethod
    def receive(self) -> None:
        """"""
        raise NotImplementedError

    @abstractmethod
    def send(self, message):
        raise NotImplementedError