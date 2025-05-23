import streamlit as strmlt , requests 
from db import (
    create_conversation,
    get_conversations,
    get_conversation,
    get_session,
    get_messages,
    create_message,
    RoleEnum,
)
from ai import get_chain_w_history
from langchain.memory import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import random

strmlt.set_page_config(layout="wide")
strmlt.title(
    "Welcome to Langchain Chat App :rainbow[Smarter Version]! 🦜🔗🧠",
    help="It will remeber your past conversastions!",
)

session = get_session()

conversations = get_conversations(session=session)

conversations_titles = [conv.title for conv in conversations]
conversations_id = [conv.id for conv in conversations]


with strmlt.sidebar:
    selected_conv = strmlt.radio(
        "Select a Conversation", options=["New Conversation"] + conversations_titles
    )
    if selected_conv == "New Conversation":
        strmlt.session_state.active_conv_id = None
    elif selected_conv in conversations_titles:
        idx = conversations_titles.index(selected_conv)
        strmlt.session_state.active_conv_id = conversations_id[idx]


if strmlt.session_state.active_conv_id is not None:
    active_conv_id = strmlt.session_state.active_conv_id
    conv_messages = get_messages(session, active_conv_id)
    conv_title = f"Conversation-{random.randint(0,999)}"


msgs = StreamlitChatMessageHistory(key="history")

chain_w_history = get_chain_w_history(msgs)

conversation = None
messages = None

if strmlt.session_state.active_conv_id is not None:
    conversation = get_conversation(session, strmlt.session_state.active_conv_id)
    messages = get_messages(session, conversation.id)

current_container_key = f"conv-{conversation.id}" if conversation is not None else None

with strmlt.container(key=current_container_key):
    if messages is not None:
        for message in messages:
            strmlt.chat_message(message.role.value).write(message.body)
    
if prompt_text := strmlt.chat_input("Type your message here..."):
        if conversation == None:
            new_conv_title = prompt_text[0:3]
            conversation = create_conversation(session,new_conv_title)
        create_message(session,prompt_text,conversation.id,RoleEnum("human"))
        strmlt.chat_message("human").write(prompt_text)
        response_placeholder = strmlt.chat_message("ai").empty()
        full_response = ""
        with strmlt.spinner("Thinking..."):
            for chunk in chain_w_history.stream(
                { "input":prompt_text },
                config={ "configurable":{"session_id":"conv"} }):
                   full_response += chunk.content
                   response_placeholder.markdown(full_response)
            
        response_placeholder.markdown(full_response)
        create_message(session,full_response,conversation.id,RoleEnum("ai"))
    






    #    with strmlt.container():
    #        strmlt.chat_message("human").write(prompt_text)
    #        response_placeholder = strmlt.empty()
    #        full_response = ""
    #        with strmlt.spinner("Thinking..."):
    #          for chunk in chain_w_memory.stream(
    #              { "input":prompt_text },
    #              config={ "configurable":{"session_id":"conv"} }):
    #                 full_response += chunk.content
    #                 response_placeholder.markdown(full_response)
            
    #        response_placeholder.markdown(full_response)   
# # else:
# #     conversation = create_conversation(session, f"Conversation-{random.randint(0,999)}")
# #     messages = get_messages(session, conversation.id)
# #     strmlt.session_state.active_conv_id = conversation.id

# with strmlt.container():
#     for message in messages:
#         strmlt.chat_message(message.role.value).write(message.body)
#     response_placeholder = strmlt.chat_message("ai").empty()
#     full_response = ""
#     # with strmlt.spinner("Thinking..."):
#     #     for chunk in chain_w_history.stream(
#     #         {"input": prompt_text},
#     #         config={"configurable": {"session_id": f"{conversation.id}"}},
#     #     ):
#     #         full_response += chunk.content
#     #         response_placeholder.write(full_response)
#     #     create_message(session, full_response, conversation.id, role=RoleEnum("ai"))
