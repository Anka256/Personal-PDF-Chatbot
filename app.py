from typing import cast
import streamlit as st
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from rag import load_pdf, split_documents, create_vector_store
import os
from dotenv import load_dotenv

load_dotenv()

st.html(
    """
    <style>
    .stApp{
        background-color: #FFFFE7;
    }
    </style>
    """
)

st.title("Personal PDF Chatbot", text_alignment="center")

st.divider()

with st.columns([3, 2, 3])[1]:
    users_file = st.file_uploader(
        label="PDF Uploader",
        type="pdf",
    )

if users_file is not None and "vector_store" not in st.session_state:
    with st.spinner("PDF işleniyor..."):
        docs = load_pdf(users_file)
        chunks = split_documents(docs)
        st.session_state.vector_store = create_vector_store(chunks)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        context = ""
        if "vector_store" in st.session_state:
            top_chunks = st.session_state.vector_store.similarity_search(prompt, k=3)
            context = "\n\n".join(doc.page_content for doc in top_chunks)

        system_msg = {
            "role": "system",
            "content": f"Answer the question using the PDF content below:\n\n{context}",
        }

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=cast(
                list[ChatCompletionMessageParam],
                [system_msg]
                + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            ),
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
