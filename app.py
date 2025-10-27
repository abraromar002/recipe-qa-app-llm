

from fastapi import FastAPI
from qa_chain import build_qa_chain
from vector import retriever
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI(title="Recipe Q&A API", version="1.0.0")

# Build the RAG chain
qa_chain = build_qa_chain(retriever)

# Response model
class Answer(BaseModel):
    answer: str

@app.get("/ask", response_model=Answer)
def ask(question: str):
    """
    Endpoint for answering questions using the RAG Chain.
    """
    try:
        # Using "question" as the key to match the custom RAG chain (qa_chain.py)
        result = qa_chain.invoke({"question": question}) 
        
        # Since we are using Runnables, the result is the answer string directly
        answer = result 
        
        return {"answer": answer}
    except Exception as e:
        # Log the error for debugging
        print(f"Error during RAG invocation: {e}")
        return {"answer": f"An internal error occurred while processing the question: {e}"}

