# shoopack 

### 💨 shoopack — 'Shoo your messages, packed and ready'

## Installation

```bash
pip install shoopack
```
or 
```bash
pip install git+https://github.com/4am-ciss/shoopack
```

## Usage

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

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
