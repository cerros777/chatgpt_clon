# streamlit_chatgpt_app.py
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit app title
st.set_page_config(page_title="ChatGPT Chatbot")
st.title("ChatGPT Chatbot")

# Initialize session state for storing conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to interact with OpenAI API
def query_openai(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me something..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from OpenAI
    with st.chat_message("assistant"):
        response = query_openai(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
