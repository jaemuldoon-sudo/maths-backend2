import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Maths Tutor")

# -----------------------------
# 1. Shared OpenAI call
# -----------------------------
def call_openai(client, system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message["content"]


# -----------------------------
# 2. Action functions
# -----------------------------
def generate_worksheet(topic):
    return call_openai(
        client,
        "You are a Leaving Cert Higher Level Maths tutor. Generate a worksheet with 5 exam‑style questions. No solutions.",
        f"Create a worksheet on: {topic}"
    )

def generate_exam_questions(topic):
    return call_openai(
        client,
        "You are a Leaving Cert Higher Level Maths tutor. Generate 5 challenging exam‑style questions. No solutions.",
        f"Create exam questions on: {topic}"
    )

def generate_hint(topic):
    return call_openai(
        client,
        "You are a Leaving Cert Higher Level Maths tutor. Provide a helpful hint for solving a typical question in this topic.",
        f"Give a hint for a common problem in: {topic}"
    )

def generate_solution(topic):
    return call_openai(
        client,
        "You are a Leaving Cert Higher Level Maths tutor. Provide a step‑by‑step worked solution to a typical question in this topic.",
        f"Give a worked solution for a typical {topic} question."
    )


# -----------------------------
# 3. Topics + Actions
# -----------------------------
TOPICS = ["Probability", "Trigonometry", "Algebra", "Calculus"]

ACTIONS = {
    "Worksheet": generate_worksheet,
    "Exam Questions": generate_exam_questions,
    "Hint": generate_hint,
    "Solution": generate_solution
}


# -----------------------------
# 4. UI: auto‑generate buttons
# -----------------------------
topic = st.selectbox("Choose a topic:", TOPICS)

st.subheader(f"Actions for {topic}")

for action_label, action_function in ACTIONS.items():
    if st.button(action_label):
        with st.spinner(f"Generating {action_label.lower()}..."):
            output = action_function(topic)
            st.write(output)
