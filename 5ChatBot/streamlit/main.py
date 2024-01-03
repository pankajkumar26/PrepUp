from dataclasses import dataclass
from typing import Literal
import streamlit as st

from chatbot import (
    get_completion,
    display_and_store_response,
    text_to_speech,
    speech_to_text,
    get_question,
    request_bard,
)

# from langchain import OpenAI
# from langchain.callbacks import get_openai_callback
# from langchain.chains import ConversationChain
# from langchain.chains.conversation.memory import ConversationSummaryMemory

import streamlit.components.v1 as components


@dataclass
class Message:
    """Class for keeping track of a chat message."""

    origin: Literal["human", "ai"]
    message: str


def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)


def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
#     # if "conversation" not in st.session_state:
#     #     llm = OpenAI(
#     #         temperature=0,
#     #         openai_api_key=st.secrets["openai_api_key"],
#     #         model_name="text-davinci-003"
#     #     )
#     #     st.session_state.conversation = ConversationChain(
#     #         llm=llm,
#     #         memory=ConversationSummaryMemory(llm=llm),
#     #     )


def on_click_callback():
    human_prompt = st.session_state.human_prompt
    llm_response = st.session_state.conversation.run(
        human_prompt
    )
    st.session_state.history.append(Message("human", human_prompt))
    st.session_state.history.append(Message("ai", llm_response))


load_css()
# initialize_session_state()

title = f"<h1 class=center> Interview Assistant 🤖 </h1>"
st.markdown(title, unsafe_allow_html=True)

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")

with chat_placeholder:
    for chat in st.session_state.history:
        div = f"""
<div class="chat-row 
    {'' if chat.origin == 'ai' else 'row-reverse'}">
    <img class="chat-icon" src="app/static/{
        'ai_icon.png' if chat.origin == 'ai' 
                      else 'user_icon.png'}"
         width=28 height=28>
    <div class="chat-bubble
    {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
        &#8203;{chat.message}
    </div>
</div>
        """
        st.markdown(div, unsafe_allow_html=True)

    for _ in range(3):
        st.markdown("")

with prompt_placeholder:
    st.markdown("**Chat**")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "Chat",
        value="Hello ",
        label_visibility="collapsed",
        key="human_prompt",
    )
    cols[1].form_submit_button(
        "Submit",
        type="primary",
        on_click=on_click_callback,
    )


components.html(
    """
<script>
const streamlitDoc = window.parent.document;

const buttons = Array.from(
    streamlitDoc.querySelectorAll('.stButton > button')
);
const submitButton = buttons.find(
    el => el.innerText === 'Submit'
);

streamlitDoc.addEventListener('keydown', function(e) {
    switch (e.key) {
        case 'Enter':
            submitButton.click();
            break;
    }
});
</script>
""",
    height=0,
    width=0,
)