import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


# Load environment variables
load_dotenv()

# Configure the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Step 1: Read PDF and Extract Text
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text

# Step 2: Split text into manageable chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    return chunks

# Step 3: Create embeddings and store them in Chroma DB
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    vector_store = Chroma.from_texts(text_chunks, embeddings, persist_directory="chroma_store")
    #vector_store.persist()  # Store the vector store locally for later use
    print("Chroma vector store has been updated with the embeddings.")

# Step 4: Load the question-answering chain
def get_conversation_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide the source of the answer.
    If the answer is not in the context, say "I don't know".
    Context: {context}
    Question: {question}
    Answer:
    """
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Step 5: Handle user input and query the Chroma DB
def user_input_handler(user_input):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    new_db = Chroma(persist_directory="chroma_store", embedding_function=embeddings)
    docs = new_db.similarity_search(user_input)

    # Use the QA chain to generate an answer
    chain = get_conversation_chain()
    response = chain.invoke(

        {
            "input_documents": docs,
            "question": user_input,
        },
        return_only_outputs=True,
    )

    print("Answer:", response["output_text"])


# Step 6: Main CLI function
def run_cli():
    print("Welcome to the PDF Question Answering CLI!")
    
    # Step 6.1: Upload PDF and process
    pdf_path = input("Enter the path to your PDF file: ")
    if not os.path.exists(pdf_path):
        print("PDF file not found!")
        return

    # Read and chunk the text from the PDF
    text = get_pdf_text([pdf_path])
    chunks = get_text_chunks(text)
    
    # Step 6.2: Store the embeddings in Chroma DB
    get_vector_store(chunks)
    
    print("PDF processing complete! You can now ask questions based on its content.")

    # Step 6.3: Ask questions based on the processed PDF
    while True:
        user_input = input("Enter your question (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        if user_input:
            user_input_handler(user_input)
        else:
            print("Please enter a question.")

if __name__ == "__main__":
    run_cli()