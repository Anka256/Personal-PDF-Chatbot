import streamlit as st
from rag import load_pdf, split_documents, create_vector_store

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


if users_file is not None:
    with st.spinner("PDF loading..."):
        docs = load_pdf(users_file)
        chunks = split_documents(docs)
        vector_store = create_vector_store(chunks)
        results = vector_store.similarity_search("Skillset", k=3)

    st.success(f"PDF loaded successfully! Total page:{len(docs)}")

    with st.expander("Results"):
        st.write(results)