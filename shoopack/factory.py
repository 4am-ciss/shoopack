from .base import PublisherBase, SubscriberBase, RequesterBase, ResponderBase

def create_publisher(backend: str, **kwargs) -> PublisherBase:
    """

    :param backend:
    :param kwargs:
    :return:
    """
    if backend == "zmq":
        from .impl.zmq.pubsub import ZmqPublisher
        return ZmqPublisher(**kwargs)
    else:
        raise ValueError(f"Unsupported publisher backend: {backend}")

def create_subscriber(backend: str, **kwargs) -> SubscriberBase:
    """

    :param backend:
    :param kwargs:
    :return:
    """
    if backend == "zmq":
        from .impl.zmq.pubsub import ZmqSubscriber
        return ZmqSubscriber(**kwargs)
    else:
        raise ValueError(f"Unsupported subscriber backend: {backend}")

def create_requester(backend: str, **kwargs) -> RequesterBase:
    if backend == "zmq":
        from .impl.zmq.reqres import ZmqRequester
        return ZmqRequester(**kwargs)
    else:
        raise ValueError(f"Unsupported requester backend: {backend}")

def create_responder(backend: str, **kwargs) -> ResponderBase:
    if backend == "zmq":
        from .impl.zmq.reqres import ZmqResponder
        return ZmqResponder(**kwargs)
    else:
        raise ValueError(f"Unsupported responder backend: {backend}")

def create_client(backend: str, **kwargs):
    return create_requester(backend, **kwargs)

def create_server(backend: str, **kwargs):
    return create_responder(backend, **kwargs)