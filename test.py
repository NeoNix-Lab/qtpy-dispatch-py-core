
import streamlit as st
import generator as g
#from core.socket_client_service import SocketClientService as Client
from core.socket_manager import SocketManager as Client
from generated_models import OrderReqDto
import random
import uuid
import json



def random_order_req_dto() -> OrderReqDto:
    """
    Ritorna un OrderReqDto con valori generati casualmente.
    """
    return OrderReqDto(
        SymbolId=str(uuid.uuid4()),
        AccountId=str(uuid.uuid4()),
        IsLong=random.choice([True, False]),
        OrderTypeId=random.choice([None, "market", "limit", "stop", "stop_limit"]),
        Quantity=round(random.uniform(1.0, 1000.0), 4),
        Price=round(random.uniform(10.0, 500.0), 2),
        TriggerPrice=round(random.uniform(10.0, 500.0), 2),
        TrailOffset=round(random.uniform(0.1, 10.0), 3),
        PositionId=str(uuid.uuid4()) if random.random() < 0.5 else None,
        StopLoss=round(random.uniform(0.0, 50.0), 2),
        TakeProfit=round(random.uniform(0.0, 50.0), 2),
        Comment=random.choice([None, "ordine di test", "verifica"]),
        Title=random.choice([None, "DemoOrder", "TestOrder"])
    )

sta = g.STATE

st.header(f"TEst {sta}")



if "Connected" not in st.session_state:

    if st.button("Connect"):
        st.write("Connecting to server...")
        client = Client.connect("127.0.0.1", 8080)

        if "Client" not in st.session_state:
            st.session_state.Client = client
        st.write("Merda")
        st.session_state.Connected = "True"

else:
    st.write("Merda")
    if st.button("Send Data"):
        msg = {
            "Command": "OrderReqDto",   # deve combaciare col .Name registrato
            "Payload":random_order_req_dto().model_dump(mode="json", exclude_none=True)
        }

        raw = json.dumps(random_order_req_dto().model_dump(mode="json", exclude_none=True), separators=(",", ":"))

        st.session_state.Client.send(raw)
        st.write("Random instance sent")

