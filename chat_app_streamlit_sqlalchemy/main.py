import streamlit as strmlt
from db import get_conversations , get_session
strmlt.set_page_config(layout ="wide")
strmlt.title("Welcome to Langchain Chat App :rainbow[Smarter Version]! 🦜🔗🧠",help="It will remeber your past conversastions!")

session = get_session()

conversations = get_conversations(session=session)

conversations_titles = [conv.title for conv in conversations]
conversations_id = [conv.id for conv in conversations]

with strmlt.sidebar:
    selected_conv = strmlt.radio("Select a Conversation",options=["New Conversation"] + conversations_titles)
    if selected_conv == "New Conversation":
        strmlt.session_state.selected_conv_id = None
    elif selected_conv in conversations_titles:
        idx = conversations_titles.index(selected_conv)
        strmlt.session_state.selected_conv_id = conversations_id[idx]     