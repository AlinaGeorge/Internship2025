import chromadb

myclient=chromadb.Client()      #creating an instance of chromadb i.e, a database client

collection=myclient.create_collection(name="AgenticRAG")  #creating a collection in the database

#adding documents to the collection
collection.add(
    documents=["Agentic RAG stands for Agentic Retrieval-Augmented Generation.",
                "It combines LLMs, information retrieval and autonomous decision making.",
                "Agentic RAG is more interactive and capable of solving complex problems."],
    ids=["line1", "line2", "line3"],
)  

coll=collection.get() #getting the collection
print(coll)  #printing the collection