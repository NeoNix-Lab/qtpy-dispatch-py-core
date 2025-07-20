from core.message_envelope import MessageEnvelope


class TradingEnvelopes:
    """Example envelopes mirroring the C# sample."""

    NewOrder = MessageEnvelope.create(
        "NewOrder",
        {
            "OrderId": "ORDER123",
            "Symbol": "AAPL",
            "Side": "BUY",
            "Quantity": 100,
            "Price": 172.35,
        },
        lambda msg: print(
            f"[NewOrder] {msg.data['OrderId']} {msg.data['Side']} {msg.data['Quantity']}x{msg.data['Symbol']}"
        ),
    )

    PriceUpdate = MessageEnvelope.create(
        "PriceUpdate",
        {
            "Symbol": "AAPL",
            "Bid": 172.30,
            "Ask": 172.40,
        },
        lambda msg: print(
            f"[PriceUpdate] {msg.data['Symbol']}: Bid={msg.data['Bid']} Ask={msg.data['Ask']}"
        ),
    )

    AccountBalance = MessageEnvelope.create(
        "AccountBalance",
        {
            "AccountId": "ACC12345",
            "Cash": 25000.50,
            "Positions": {"AAPL": 150, "MSFT": 75},
        },
        lambda msg: print(
            f"[AccountBalance] Cash={msg.data['Cash']} Positions={msg.data['Positions']}"
        ),
    )
