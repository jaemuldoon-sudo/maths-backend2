import streamlit as st
import os
from openai import OpenAI


st.markdown("""
<style>
/* Make the whole page responsive */
.main {
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Improve button spacing on mobile */
.stButton>button {
    width: 100%;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    padding: 0.8rem 1rem;
    font-size: 1.1rem;
}

/* Improve selectbox and text input sizing */
.stSelectbox, .stTextInput {
    font-size: 1.1rem;
}

/* Prevent horizontal scrolling */
.block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
</style>
""", unsafe_allow_html=True)






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
    response.choices[0].message.content



# -----------------------------
# 2. Action functions
# -----------------------------
def generate_worksheet(topic):
    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Generate exactly 5 exam‑style questions on the topic. "
        "Return them as a numbered list, one question per line, no solutions."
    )

    user_prompt = f"Create a worksheet on: {topic}"

    text = call_openai(client, system_prompt, user_prompt)

    # Split into individual questions
    questions = [q.strip() for q in text.split("\n") if q.strip()]

    return questions


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

def generate_answer(question, topic):
    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Provide a full step‑by‑step worked solution to the question."
    )

    user_prompt = f"Topic: {topic}\nQuestion: {question}\nProvide the full solution."

    return call_openai(client, system_prompt, user_prompt)


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

    if st.button("Generate Worksheet"):
        questions = generate_worksheet(topic)

        st.subheader(f"{topic} Worksheet")

        for i, q in enumerate(questions):
            with st.container():
                st.write(q)

                if st.button(f"Show Answer to Q{i+1}"):
                    answer = generate_answer(q, topic)
                    st.write(answer)


