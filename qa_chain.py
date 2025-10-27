from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from operator import itemgetter

# Using the model found in your environment
OLLAMA_LLM_MODEL = "llama3.2:latest" 

def format_docs(docs):
    """A helper function to combine retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

def build_qa_chain(retriever):
    """
    Builds the Retrieval-Augmented Generation (RAG) chain using LangChain Runnables.
    """
    
    # 1. Setup the Language Model (LLM)
    llm = OllamaLLM(model=OLLAMA_LLM_MODEL, temperature=0.2) 

    # 2. Setup the Prompt Template
    prompt_template = """
    You are a professional chef and culinary expert.
    Your task is to answer user questions clearly and accurately, based ONLY on the recipes provided below.

    Use the provided recipes to give precise, step-by-step answers.
    If the question is unrelated to cooking or recipes, politely refuse to answer.

    Here are the relevant recipes:
    {context}

    Question:
    {question}

    Provide your answer in a friendly, helpful tone, mentioning the name of the recipe you used.
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # 3. Build the RAG Chain using Runnables
    
    # 3.1. Retrieval Chain: Takes the question, retrieves documents, and formats them
    retrieval_chain = itemgetter("question") | retriever | RunnableLambda(format_docs).with_config(run_name="format_docs")

    # 3.2. Main RAG Chain: Passes the question and the context to the prompt and then to the LLM
    rag_chain = RunnablePassthrough.assign(context=retrieval_chain) | prompt | llm

    # 4. Return the final chain
    return rag_chain