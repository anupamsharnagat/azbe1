from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from rag_backend.services.llm_provider import get_llm, get_embeddings
import os

# using fiss as it faster not croma this tym
VECTOR_DB_PATH = "local_faiss_index"

def create_and_save_vector_store(documents):
    
    # keeping it simple with RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    
    # Embedding Connection
    embeddings = get_embeddings()
    
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(VECTOR_DB_PATH)
    
    return len(chunks)

def answer_query(user_query: str) -> str:
    
    # Check if Vector Store exists
    if not os.path.exists(VECTOR_DB_PATH):
        return "Error: Document has not been uploaded or processed yet. Please upload a PDF first."
    
    embeddings = get_embeddings() 
    # to load local pickle files. Since we created it, it's safe.
    vector_store = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    
    #fetches the top 4 most similar chunks
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    
    llm = get_llm()
    
    # system prompt
    system_prompt = (
        "You are an expert financial and data analyst assistant. "
        "Use the following pieces of retrieved context containing text and tables "
        "from an annual report to answer the user's question.\n\n"
        "If you don't know the answer or the context doesn't contain the information, "
        "just say that you don't know. Do not try to make up an answer.\n\n"
        "{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Create the Chains
    # 'Stuff' chain to stuffretrieved documents into the prompt Context.
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    # vec db +prompt 
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # Execute
    response = rag_chain.invoke({"input": user_query})
    
    # final response
    return response["answer"]
