import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
import base64

from tts_utils import speak_text
from vectorstore_utils import get_vectorstore_fromurl
from chains_utils import get_responce

load_dotenv()

st.set_page_config(
    page_title="Chat with Websites",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

body {
    background: linear-gradient(120deg, #071a2d, #0b2c4a, #0f3a5f);
}

audio { display: none; }

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255,255,255,0.12);
}

.footer {
    text-align: center;
    color: #bcdcff;
    font-size: 13px;
    margin-top: 18px;
    opacity: 0.9;
}

/* USER RIGHT SIDE */
[data-testid="stChatMessage"]:has(img[alt="👤"]) {
    flex-direction: row-reverse;
}

[data-testid="stChatMessage"]:has(img[alt="👤"]) img {
    margin-left: 10px;
    margin-right: 0;
    animation: userPop 0.25s ease-out;
}

@keyframes userPop {
    0% { transform: scale(0.4); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

/* User Bubble */
[data-testid="stChatMessage"]:has(img[alt="👤"]) .stChatMessageContent {
    background: rgba(80, 150, 255, 0.20) !important;
    border: 1px solid rgba(120, 180, 255, 0.35) !important;
    border-radius: 14px 0 14px 14px !important;
    margin-left: auto;
}

/* AI Bubble */
[data-testid="stChatMessage"]:has(img[alt="🤖"]) .stChatMessageContent {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.20) !important;
    border-radius: 0 14px 14px 14px !important;
}

</style>
""", unsafe_allow_html=True)

st.title("🤖 Chat with Websites")
st.caption("Ask questions directly from any website using AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Paste a website URL and ask your first question.")
    ]

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "current_url" not in st.session_state:
    st.session_state.current_url = None

if "last_audio" not in st.session_state:
    st.session_state.last_audio = None


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <audio autoplay hidden>
            <source src="data:audio/mp3;base64,{b64}">
        </audio>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.subheader("Website Input")
    website_url = st.text_input("Website URL", placeholder="https://example.com")
    parse_btn = st.button("Parse Website")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        clear_chat_btn = st.button("Clear Chat")
    with col2:
        reindex_btn = st.button("Re-Index")

    if clear_chat_btn:
        st.session_state.chat_history = [
            AIMessage(content="Paste a website URL and ask your first question.")
        ]
        st.session_state.last_audio = None
        st.success("Chat cleared")


if parse_btn and website_url:
    with st.spinner("Indexing website..."):
        st.session_state.vector_store = get_vectorstore_fromurl(website_url)
        st.session_state.current_url = website_url
    st.sidebar.success("Website indexed")


user_query = st.chat_input("Ask a question...")

if user_query:
    if st.session_state.vector_store is None:
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(
            AIMessage(content="Please parse a website first.")
        )
    else:
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        with st.spinner("Thinking..."):
            responce = get_responce(user_query)

        with st.spinner("Generating voice..."):
            audio_file = speak_text(responce)

        st.session_state.last_audio = audio_file
        st.session_state.chat_history.append(AIMessage(content=responce))


for idx, message in enumerate(st.session_state.chat_history):
    if isinstance(message, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.write(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("ai", avatar="🤖"):
            st.write(message.content)
            if idx == len(st.session_state.chat_history) - 1 and st.session_state.last_audio:
                autoplay_audio(st.session_state.last_audio)


st.markdown("""
<div class="footer">
Powered by Groq · HuggingFace · LangChain · Chroma · ElevenLabs · Streamlit
</div>
""", unsafe_allow_html=True)
