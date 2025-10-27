import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os

# اسم المجلد الذي سيتم حفظ قاعدة البيانات فيه
DB_DIR = "./recipes_chroma_db"
# اسم نموذج Ollama لـ Embeddings
OLLAMA_EMBEDDING_MODEL = "mxbai-embed-large" 

def parse_r_list(r_string):
    if pd.isna(r_string) or r_string.strip() == "":
        return []
    r_string = r_string.strip()
    if r_string.startswith('c(') and r_string.endswith(')'):
        r_string = r_string[2:-1]
    items = []
    for part in r_string.split(','):
        part = part.strip().strip('"').strip("'")
        if part:
            items.append(part)
    return items

def load_and_process_data():
    """تحميل البيانات من CSV وتحويلها إلى مستندات LangChain."""
    print("... جاري تحميل ومعالجة البيانات من recipes.csv")
    
    # تحميل الأعمدة المطلوبة
    df = pd.read_csv("recipes.csv", usecols=[
        "RecipeId", "Name", "Description", "RecipeIngredientParts", "RecipeInstructions"
    ])
    
    documents = []
    for index, row in df.iterrows():
        ingredients = ", ".join(parse_r_list(row["RecipeIngredientParts"]))
        content = f"وصفة: {row['Name']}\nالمكونات: {ingredients}\nالوصف: {row['Description']}\nالتعليمات: {row['RecipeInstructions']}"
        
        document = Document(
            page_content=content,
            metadata={"source": "recipes.csv", "recipe_id": row["RecipeId"], "name": row["Name"]}
        )
        documents.append(document)
    
    print(f"... تم معالجة {len(documents)} وصفة.")
    return documents

def get_retriever():
    """إنشاء أو تحميل قاعدة البيانات المتجهة Chroma وإرجاع المسترجع."""
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL)
    
    if not os.path.exists(DB_DIR):
        print(f"... قاعدة البيانات غير موجودة. جاري بناء قاعدة بيانات جديدة وحفظها في {DB_DIR}")
        documents = load_and_process_data()
        
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=DB_DIR
        )
        vectorstore.persist()
        print("... تم بناء وحفظ قاعدة البيانات بنجاح.")
    else:
        print(f"... جاري تحميل قاعدة البيانات المتجهة من {DB_DIR}")
        vectorstore = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings
        )
        print("... تم تحميل قاعدة البيانات بنجاح.")

    return vectorstore.as_retriever(search_kwargs={"k": 5})

retriever = get_retriever()
