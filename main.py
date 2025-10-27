import streamlit as st
import requests
import base64


def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

BACKGROUND_IMAGE_PATH = "pexels-ella-olsson-572949-1640774.jpg"
base64_img = get_base64_image(BACKGROUND_IMAGE_PATH)

if base64_img:
    css_content = f"""
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_img}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.55);  /* overlay */
        z-index: -1;
    }}
    body, .stMarkdown, .stText, .stTextInput label, .stHeader, .stTitle, .stSubheader {{
        color: #FFFFFF !important;
        font-family: 'Georgia', serif;
    }}
    .st-emotion-cache-10trblm.e1nzilvr1, h1 {{
        color: #FFC300 !important;
        text-shadow: 2px 2px 4px #000;
    }}
    .stButton>button {{
        background-color: #C70039;
        color: #FFC300;
        border-radius: 12px;
        border: 2px solid #FFC300;
        font-weight: bold;
        font-size: 1.1em;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #900C3F;
        color: #FFFFFF;
        transform: scale(1.05);
    }}
    .stTextInput>div>div>input {{
        border: 2px solid #FFC300;
        border-radius: 10px;
        padding: 12px;
        background-color: rgba(255,255,255,0.15);
        color: #FFFFFF;
    }}
    """
else:
    css_content = """
    .stApp { background-color: #1A1A1A; }
    """

st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

st.set_page_config(
    page_title="🍰 Culinary Q&A",
    page_icon="🍪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- 2️⃣ عنوان الواجهة ---
st.title("🍪 Culinary AI Assistant")
st.markdown("<h3 style='color:#FFC300;'>👩‍🍳 Ask About Recipes or Ingredients</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- 3️⃣ مربع السؤال ---
question = st.text_input("✍️ Type your question here:", placeholder="E.g., How do I make eggless chocolate cake?")

if st.button("🔍 Find Answer", use_container_width=True):
    if not question.strip():
        st.warning("⚠️ Please type a question first.")
    else:
        with st.spinner("⏳ Searching for answer..."):
            try:
                response = requests.get(
                    "http://127.0.0.1:8500/ask",
                    params={"question": question},
                    timeout=60
                )
                if response.status_code == 200:
                    answer = response.json().get("answer", "❌ Could not find an answer.")

                    
                    st.markdown(f"""
                    <div style="
                        background-color: rgba(0,0,0,0.85);
                        border: 2px solid #FFC300;
                        border-radius: 15px;
                        padding: 20px;
                        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
                        color: #FFFFFF;
                        font-size:16px;
                    ">
                    🍴 {answer}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"⚠️ Server Error (Status Code: {response.status_code})")

            except requests.exceptions.ConnectionError:
                st.error("🚫 Connection failed. Make sure the FastAPI server is running on port 8500.")
            except requests.exceptions.Timeout:
                st.error("⌛ Connection timed out. Please try again.")
            except Exception as e:
                st.error(f"❗ An unexpected error occurred: {e}")

# --- 4️⃣ اقتراحات أسئلة ---
st.markdown("---")
st.markdown("<div style='color:#FFC300; text-align:center; font-size:1.2em;'>💡 Try questions like:</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.info("🥞 Ingredients for pancakes?")
with col2:
    st.info("🧀 How to make mac and cheese?")
with col3:
    st.info("🧈 Difference between vegetable oil and butter in a cake?")

