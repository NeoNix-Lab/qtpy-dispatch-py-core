# QtPy Dispatch Core

Utilities for sending and receiving length-prefixed JSON messages and routing
them to Python callbacks.

## Features
- Dynamic message dataclass with JSON serialization
- Message envelopes with optional callbacks
- In-memory dispatcher for routing messages
- Socket helpers for length-prefixed communication
- High-level hub facade that combines sockets and dispatching

## Basic Usage

```python
from pydantic import BaseModel
from core.message_envelope import MessageEnvelope
from hub import connect, register, send_dispatcher, disconnect

class Greeting(BaseModel):
    title: str = "greeting"
    name: str

def on_greeting(msg: Greeting) -> None:
    print(f"Hello {msg.name}!")

envelope = MessageEnvelope(Greeting(name="Alice"), on_greeting)
connect("localhost", 9000)
register(envelope)
send_dispatcher(envelope)
disconnect()
```

## License

This project is licensed under the terms of the MIT license. See
[LICENSE](LICENSE) for details.
