# shoopack 

### 💨 shoopack — 'Shoo your messages, packed and ready'

## Installation

[//]: # (```bash)

[//]: # (pip install shoopack)

[//]: # (```)

[//]: # (or )
```bash
pip install git+https://github.com/4am-ciss/shoopack
# If you want to install the latest version from the repository, use:
pip install git+https://github.com/4am-ciss/shoopack -U
```

## Usage
### Basic Usage

```python
# Publisher Example
from shoopack import create_publisher
pub = create_publisher('zmq', address='localhost', topic_name='my_topic')
pub.publish('Hello, World!')
```

```python
# Subscriber Example
from shoopack import create_subscriber
sub = create_subscriber('zmq', address='localhost', topic_name='my_topic')
msg = sub.receive()
print(msg)  # Outputs: Hello, World!
```

### Advanced Usage
#### Pairing Publisher and Subscriber
```python
# Pairing Publisher and Subscriber Example (tests/pairing_pubsub.py)
# This example demonstrates how to create a pairing publisher and subscriber
import shoopack
import time
def test_pairing_pubsub():
    a = shoopack.create_pairing_pubsub("zmq",
                                        target_address="localhost",
                                        target_port=5555,
                                        source_address="localhost",
                                        source_port=5556,
                                        source_timeout=500,
                                        protocol="tcp",
                                        topic_name="test_topic")
    b = shoopack.create_pairing_pubsub("zmq",
                                        target_address="localhost",
                                        target_port=5556,
                                        source_address="localhost",
                                        source_port=5555,
                                        source_timeout=500,
                                        protocol="tcp",
                                        topic_name="test_topic")

    a.listen()
    b.listen()
    i = 0
    # await a, b is listened
    while not (a._listen_loop and b._listen_loop):
        print("Waiting for both A and B to start listening...")
        time.sleep(0.1)

    try:
        while True:
            a.publish({"message": f"Hello from A {i}"})
            b.publish({"message": f"Hello from B {i}"})
            i += 1
            print(f"A gets: {a.get()}")
            print(f"B gets: {b.get()}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Test interrupted by user.")
    finally:
        a.close()
        b.close()
        print("Pairing Pub/Sub test completed and resources cleaned up.")

if __name__ == "__main__":
    test_pairing_pubsub()
```
It will create a pairing publisher and subscriber that can communicate with each other. \
The publisher sends messages, and the subscriber receives them.
It looks like this image:

![Paring Pub/Sub Img](./images/pairpubsub.jpg)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
