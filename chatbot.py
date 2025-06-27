import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq


st.set_page_config(
    page_title="Syra",
    page_icon="🤖",
    layout="centered",
)


try:
    secrets = dotenv_values(".env") 
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
    INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
    INITIAL_MSG = secrets["INITIAL_MSG"]
    CHAT_CONTEXT = secrets["CHAT_CONTEXT"]
except:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    INITIAL_RESPONSE = os.getenv("INITIAL_RESPONSE")
    INITIAL_MSG = os.getenv("INITIAL_MSG")
    CHAT_CONTEXT = os.getenv("CHAT_CONTEXT")


os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE},
    ]


st.title("Hey There!")
st.caption("Let's talk developer!...")


for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar='🤖' if message["role"] == "assistant" else "🗨️"):
        st.markdown(message["content"])


user_prompt = st.chat_input("Ask me")

if user_prompt:
    
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    
    messages = [
        {"role": "system", "content": CHAT_CONTEXT},
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    
    with st.chat_message("assistant", avatar='🤖'):
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            stream=False 
        )
        response = completion.choices[0].message.content
        st.markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
