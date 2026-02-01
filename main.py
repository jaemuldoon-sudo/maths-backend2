import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.write("API key loaded:", os.getenv("OPENAI_API_KEY") is not None)



st.set_page_config(page_title="Maths Tutor Test", page_icon="📐")

st.title("📐 Maths Tutor Backend Test")
st.write("If you can see this running on Streamlit, everything is working!")

name = st.text_input("Enter your name:")

if st.button("Say hello"):
    st.success(f"Hello {name}, your backend is working!")


def generate_worksheet(topic: str, question: str) -> str:
    prompt = f"""
You are a tutor for Leaving Cert Higher Level Maths in Ireland.

Generate EXACTLY 10 {topic} questions similar in style and difficulty to the following:

"{question}"

STRICT RULES:
- Output ONLY the 10 questions.
- Number them 1 to 10.
- No introductions.
- No explanations.
- No headings.
- No blank lines.
- No solutions.

Example format:
1. ...
2. ...
...
10. ...

Now generate the worksheet:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # ⚡ faster + cheaper for worksheets
        messages=[
            {"role": "system", "content": "You generate exam‑style maths questions only."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
    
    
    
# ---------------------------------------------------------
#  STREAMLIT UI
# ---------------------------------------------------------
st.set_page_config(page_title="Leaving Cert HL Maths Tutor", page_icon="📐")

st.title("📐 Leaving Cert Higher Level Maths Tutor")
st.write("Choose **Full Solution**, **Hints Mode**, or generate a **Worksheet** of similar, harder, or honours-level questions.")

topic = st.selectbox(
    "Choose a topic:",
    ["Probability", "Algebra", "Calculus", "Trigonometry", "The Circle"],
)

question = st.text_area(
    "Enter your question:",
    placeholder="e.g. What is the probability of picking a red ace from a pack of cards?",
    height=150,
)