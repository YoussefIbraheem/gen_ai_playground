from langchain_ollama import ChatOllama
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
import streamlit as strmlt
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
strmlt.set_page_config(layout ="wide")
strmlt.title("Welcome to Langchain Chat App! 🦜")

with strmlt.sidebar:
    prompt_template = strmlt.text_area(label="Prompt Template",value="You are a smart assistant named 'Dan'")
    max_tokens = strmlt.slider("Max Tokens",min_value=0.0,max_value=1000.0)
    temprature = strmlt.slider("Temprature",min_value=0.0,max_value=1.0)
    

llm = ChatOllama(model="llama3.2:3b",temperature=temprature,max_tokens=max_tokens)

prompt = ChatPromptTemplate.from_messages([
    ("ai",prompt_template),
    ("placeholder", "{history}"),
    ("human","{input}")
])

memory = StreamlitChatMessageHistory(key="history")

chain = prompt | llm

if not memory.messages:
    memory.add_ai_message("Hey There! How can I be of help?")

chain_w_memory = RunnableWithMessageHistory(
    chain,
    lambda session_id: memory,
    history_messages_key="history"    
)

if prompt_text := strmlt.chat_input("Type your message here..."):
       with strmlt.container():
           strmlt.chat_message("human").write(prompt_text)
           response_placeholder = strmlt.empty()
           full_response = ""
           with strmlt.spinner("Thinking..."):
             for chunk in chain_w_memory.stream(
                 { "input":prompt_text },
                 config={ "configurable":{"session_id":"conv"} }):
                    full_response += chunk.content
                    response_placeholder.markdown(full_response)
            
           response_placeholder.markdown(full_response)     
               
       
                     
            