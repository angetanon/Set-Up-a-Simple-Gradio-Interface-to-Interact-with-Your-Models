from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.chains import RetrievalQA

import gradio as gr

load_dotenv(Path(__file__).with_name(".env"))

if not os.environ.get("OPENAI_API_KEY", "").strip():
    raise RuntimeError("Set OPENAI_API_KEY in the .env file before starting the app.")

## LLM
def get_llm():
    llm = ChatOpenAI(
    model="gpt-4o-mini",
    max_tokens=256, # Limit the maximum number of tokens in the response
    temperature=0.5, # Control the randomness of the response (0.0 = deterministic, 1.0 = very random)
)
    return llm

## Document loader
def document_loader(file):
    loader = PyPDFLoader(file)
    loaded_document = loader.load()
    return loaded_document

## Text splitter
def text_splitter(data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        length_function=len,
    )
    chunks = text_splitter.split_documents(data)
    return chunks

## Embedding model
def openai_embedding():
    return OpenAIEmbeddings()

## Vector db
def vector_database(chunks):
    embedding_model = openai_embedding()
    vectordb = Chroma.from_documents(chunks, embedding_model)
    return vectordb


## Retriever
def retriever(file):
    splits = document_loader(file)
    chunks = text_splitter(splits)
    vectordb = vector_database(chunks)
    retriever = vectordb.as_retriever()
    return retriever

## QA Chain
def retriever_qa(file, query):
    llm = get_llm()
    retriever_obj = retriever(file)
    qa = RetrievalQA.from_chain_type(llm=llm, 
                                    chain_type="stuff", 
                                    retriever=retriever_obj, 
                                    return_source_documents=False)
    response = qa.invoke(query)
    return response['result']

# Create Gradio interface
rag_application = gr.Interface(
    fn=retriever_qa,
    flagging_mode="never",
    inputs=[
        gr.File(label="Upload PDF File", file_count="single", file_types=['.pdf'], type="filepath"),  # Drag and drop file upload
        gr.Textbox(label="Input Query", lines=2, placeholder="Type your question here...")
    ],
    outputs=gr.Textbox(label="Output"),
    title="RAG Chatbot",
    description="Upload a PDF document and ask any question. The chatbot will try to answer using the provided document."
)

# Launch the app
if __name__ == "__main__":
    rag_application.launch(server_name="0.0.0.0", server_port=7860, share=True)
