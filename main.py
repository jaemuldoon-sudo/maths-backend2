import streamlit as st

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.write("API key loaded:", os.getenv("OPENAI_API_KEY") is not None)



st.set_page_config(page_title="Maths Tutor Test", page_icon="📐")

st.title("📐 Maths Tutor Backend Test")
st.write("If you can see this running on Streamlit, everything is working!")

name = st.text_input("Enter your naaaaaaaaaame:")

if st.button("Say hello"):
    st.success(f"Hello {name}, your backend is working!")
