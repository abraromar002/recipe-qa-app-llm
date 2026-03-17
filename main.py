import streamlit as st
import requests
import base64


st.set_page_config(
    page_title="🍰 Culinary Q&A",
    page_icon="🍪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

BACKGROUND_IMAGE_PATH = "bg.jpg"
base64_img = get_base64_image(BACKGROUND_IMAGE_PATH)


def perform_search(q):
    with st.spinner("⏳ Searching for answer..."):
        try:
            response = requests.get(
                "http://127.0.0.1:8500/ask",
                params={"question": q},
                timeout=60
            )
            if response.status_code == 200:
                answer = response.json().get("answer", "❌ Could not find an answer.")
                st.markdown(f"""
                <div style="background-color: rgba(0,0,0,0.85); border: 2px solid #FFC300; 
                border-radius: 15px; padding: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.5); 
                color: #FFFFFF; font-size:16px;">
                🍴 {answer}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"⚠️ Server Error: {response.status_code}")
        except Exception as e:
            st.error(f"🚫 Connection failed: {e}")


if base64_img:
    css_content = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_img}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0,0,0,0.7);  
        z-index: -1;
    }}
    
    body, .stMarkdown, p, span, label {{
        color: #FFFFFF !important;
        font-family: 'Georgia', serif;
        font-weight: 500;
        text-shadow: 1px 1px 3px #000;
    }}
    h1, h3 {{
        color: #FFC300 !important;
        text-shadow: 2px 2px 5px #000;
    }}
    .stButton>button {{
        background-color: #C70039; color: #FFC300;
        border-radius: 12px; border: 2px solid #FFC300;
        font-weight: bold; width: 100%;
    }}
    </style>
    """
    st.markdown(css_content, unsafe_allow_html=True)

st.title("🍪 Culinary AI Assistant")
st.markdown("<h3>👩‍🍳 Ask About Recipes or Ingredients</h3>", unsafe_allow_html=True)
st.markdown("---")

question = st.text_input("✍️ Type your question here:", placeholder="E.g., How do I make eggless chocolate cake?")

if st.button("🔍 Find Answer", use_container_width=True):
    if not question.strip():
        st.warning("⚠️ Please type a question first.")
    else:
        perform_search(question)


st.markdown("---")
st.markdown("<div style='color:#FFC300; text-align:center; font-size:1.2em;'>💡 Click to ask directly:</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)


if col1.button("🥞 Pancakes"):
    perform_search("What are the ingredients for pancakes?")
if col2.button("🧀 Mac & Cheese"):
    perform_search("How to make the best mac and cheese?")
if col3.button("🧈 Butter vs Oil"):
    perform_search("Difference between vegetable oil and butter in a cake?")