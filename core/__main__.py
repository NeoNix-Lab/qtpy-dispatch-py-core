from .message_dispatcher import MessageDispatcher
from trading_envelopes import TradingEnvelopes
from socket_manager import SocketManager


if __name__ == "__main__":
    manager = SocketManager.connect("localhost", 9000)
    dispatcher = MessageDispatcher()
    dispatcher.register(TradingEnvelopes.NewOrder)
    dispatcher.register(TradingEnvelopes.PriceUpdate)
    dispatcher.register(TradingEnvelopes.AccountBalance)

    manager.send(TradingEnvelopes.NewOrder.to_json())

    try:
        while True:
            incoming = manager.receive()
            dispatcher.dispatch(incoming)
    finally:
        manager.close()
