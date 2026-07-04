import streamlit as st
from agent_core import agent

st.title("King Con AI")

if prompt := st.chat_input("Ask me..."):
    response = agent.handle_query(prompt)
    st.write(response["response"])
