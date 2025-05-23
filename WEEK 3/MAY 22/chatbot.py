
import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


import chromadb
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

import re


# Load environment variables
load_dotenv()

chroma_client = chromadb.PersistentClient(path="./faq_db")
embedding_function = GoogleGenerativeAiEmbeddingFunction(
    api_key=os.getenv("API_KEY"), model_name="models/embedding-001"
)

faq_collection = chroma_client.get_or_create_collection(
    name="faq_data", embedding_function=embedding_function
)

# Sample FAQ data — only populate if not already present
if faq_collection.count() == 0:
    faq_items = [
        {"id": "1", "question": "What is your return policy?", "answer": "Returns are accepted within 30 days."},
        {"id": "2", "question": "How can I track my order?", "answer": "Use the tracking number sent to your email."},
        {"id": "3", "question": "Do you offer international shipping?", "answer": "Yes, to over 50 countries worldwide."}
    ]
    faq_collection.add(
        documents=[item["question"] for item in faq_items],
        metadatas=[{"answer": item["answer"]} for item in faq_items],
        ids=[item["id"] for item in faq_items]
    )


async def main():
    # Create the model client
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=os.getenv("API_KEY"),
    )

    def retrieve_faq_answer(question: str) -> str:
        # Clean and preprocess the question using regex
        question = question.strip().lower()
        
        # Remove common stop phrases (e.g., "please", "can you", etc.)
        question = re.sub(r"\b(please|can you|could you|would you|explain|tell me|what is|how does)\b", "", question)
        
        # Remove extra whitespace
        question = re.sub(r"\s+", " ", question).strip()

        # Run ChromaDB similarity search
        results = faq_collection.query(query_texts=[question], n_results=1)

        if results["documents"]:
            # Return the most relevant document found
            return results["documents"][0][0]
        else:
            return "No relevant FAQ found."

# Agent 1: Query Handler
    query_handler = AssistantAgent(
        name="query_handler",
        model_client=model_client,
        description="Receives a user's question and decides if RAG retrieval is needed.",
        system_message=(
            "You are an assistant that receives user queries for FAQ support. "
            "If information is required, delegate retrieval to the RAG retriever. "
            "After receiving the result, explain it clearly to the user."
        )
    )

# Agent 2: RAG Retriever with access to ChromaDB tool
    rag_retriever = AssistantAgent(
        name="rag_retriever",
        model_client=model_client,
        description="Performs FAQ retrieval using a ChromaDB-based tool.",
        system_message=(
            "You are an assistant that retrieves relevant answers using the retrieve_faq_answer tool "
            "and passes them back to the Query Handler."
        ),
        tools=[retrieve_faq_answer]
    )
    # Set up termination condition
    termination = TextMentionTermination("TERMINATE")

# Team setup
    group_chat = RoundRobinGroupChat(
        [query_handler, rag_retriever],termination_condition=termination
    )

# Start task
    await Console(group_chat.run_stream(task="What is Retrieval-Augmented Generation?"))

    # Cleanup
    await model_client.close()

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())







