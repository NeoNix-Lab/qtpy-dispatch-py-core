
import streamlit as st
import generator as g
from core.socket_client_service import SocketClientService as Client

sta = g.STATE

st.header(f"TEst {sta}")

client = Client("localhost", 8080)

if st.button("Connect"):
    st.write("Connecting to server...")
    client.connect()
    st.write(f"{client.status}")