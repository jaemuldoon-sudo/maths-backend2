import streamlit as st

st.set_page_config(page_title="Maths Tutor Test", page_icon="📐")

st.title("📐 Maths Tutor Backend Test")
st.write("If you can see this running on Streamlit, everything is working!")

name = st.text_input("Enter your name:")

if st.button("Say hello"):
    st.success(f"Hello {name}, your backend is working!")
