import streamlit as st 
from PyPDF2 import PdfReader 
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv



load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
    chunks=text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    persist_directory = "chroma_index"           #creating folder storing vector(not readable)

    vector_store = Chroma.from_texts(
        texts=text_chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    # Now persist it using .persist()
    vector_store.persist()

def get_conversational_chain():
    prompt_template="""
    Answer the question as detailed as possible from the provided context,
      make sure to provide all the details,
    If the answer is not in the provided context, just say "Answer is not available in the context.",
    don't provide the wrong answer.
    Context:\n {context}?\n
    Question: \n {question}?\n
    
    Answer:
    """


    model=ChatGoogleGenerativeAI(model="models/gemini-2.0-flash",temperature=0.3)

    prompt=PromptTemplate(template=prompt_template, input_variables=["context","question"])
   
    chain=load_qa_chain(model,chain_type="stuff",prompt=prompt)
    return chain



def user_input(user_input):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = Chroma(persist_directory="chroma_index",embedding_function= embeddings)
    docs= new_db.similarity_search(user_input)
    chain = get_conversational_chain()

    response=chain(
        {
            "input_documents": docs,
            "question": user_input
        },return_only_outputs=True)
    print(response)
    st.write("Answer: ", response["output_text"])


def main():
    st.set_page_config("Chat With Muliple PDF")
    st.header("Chat with Multiple PDF using Gemini")

    user_question = st.text_input("Ask a question about your document:")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        st.subheader("Upload your documents here")
        pdf_docs = st.file_uploader("Upload PDFs and Click On Process", type=["pdf"], accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("PDF Processed and Vector Store Created")

if __name__ == "__main__":
    main()