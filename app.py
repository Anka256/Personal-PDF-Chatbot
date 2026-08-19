from numpy.char import center
import streamlit as st

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

