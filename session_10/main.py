from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings , OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


llm_embedding = OllamaEmbeddings(model="llama3.2:3b")
llm = OllamaLLM(model="llama3.2:3b")

loader = WebBaseLoader(web_path ="https://en.wikipedia.org/wiki/Fungal_infection")
# loader = PyPDFLoader("lorem.pdf")


documents = loader.lazy_load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap= 200
    )

chunks = text_splitter.split_documents(documents=documents)

vector_store =  Chroma.from_documents(
    documents= chunks,
    embedding=llm_embedding,
    collection_name="web_db",
    
)

retriever = vector_store.as_retriever(search_kwargs={'k': 6})

template = "answer the following question based on the given context:\nContext: {context}\nQuestion: {question}"
prompt = ChatPromptTemplate.from_template(template)

chain = {"context":retriever  , "question":RunnablePassthrough()} | prompt | llm

response = chain.invoke("What is the most dangerous fungal infection?")

print(response)

