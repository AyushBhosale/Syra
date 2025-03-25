import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq

# Streamlit page configuration
st.set_page_config(
    page_title="Ayush",
    page_icon="🤖",
    layout="centered",
)

# Load secrets (local .env or Azure environment variables)
try:
    secrets = dotenv_values(".env")  # For local dev
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
    INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
    INITIAL_MSG = secrets["INITIAL_MSG"]
    CHAT_CONTEXT = secrets["CHAT_CONTEXT"]
except:
    # For Azure deployment (and fallback if .env fails locally)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    INITIAL_RESPONSE = os.getenv("INITIAL_RESPONSE")
    INITIAL_MSG = os.getenv("INITIAL_MSG")
    CHAT_CONTEXT = os.getenv("CHAT_CONTEXT")

# Save the API key to environment variable (required by Groq client)
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Initialize chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE},
    ]

# Page title and caption
st.title("Hey There!")
st.caption("Let's talk developer!...")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar='🤖' if message["role"] == "assistant" else "🗨️"):
        st.markdown(message["content"])

# User input field
user_prompt = st.chat_input("Ask me")

if user_prompt:
    # Display user message
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Prepare messages for the LLM
    messages = [
        {"role": "system", "content": CHAT_CONTEXT},
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    # Display assistant response (non-streaming for F1 compatibility)
    with st.chat_message("assistant", avatar='🤖'):
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            stream=False  # Disable streaming for Azure F1
        )
        response = completion.choices[0].message.content
        st.markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})