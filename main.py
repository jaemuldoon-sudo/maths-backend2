import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Maths Tutor – Worksheet with Difficulty Levels")


# ---------------------------------------------------------
# 1. Shared OpenAI call
# ---------------------------------------------------------
def call_openai(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


# ---------------------------------------------------------
# 2. Generate worksheet (returns list of questions)
# ---------------------------------------------------------
def generate_worksheet(topic, difficulty):
    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Generate exactly 5 unique exam‑style questions. "
        "Every time you are asked, produce a completely different set. "
        f"Difficulty level: {difficulty}. "
        "Use LaTeX formatting for ALL mathematical expressions. "
        "Wrap every LaTeX expression in double dollar signs $$ ... $$. "
        "Do NOT output plain text maths like x^2 or 1/6. "
        "Return the questions as a numbered list, one per line, no solutions."
    )

    user_prompt = f"Create a {difficulty} worksheet on: {topic}"

    text = call_openai(system_prompt, user_prompt)
    questions = [q.strip() for q in text.split('\n') if q.strip()]
    return questions



# ---------------------------------------------------------
# 3. Generate answer for a single question
# ---------------------------------------------------------
def generate_answer(question, topic, difficulty):
    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Provide a full step-by-step worked solution. "
        "Use LaTeX formatting for all mathematical expressions. "
        "Wrap all LaTeX in double dollar signs $$ ... $$ so Streamlit renders it. "
        f"Match the difficulty level: {difficulty}."
    )

    user_prompt = f"Topic: {topic}\nDifficulty: {difficulty}\nQuestion: {question}"

    return call_openai(system_prompt, user_prompt)



# ---------------------------------------------------------
# 4. UI
# ---------------------------------------------------------
TOPICS = ["Probability", "Trigonometry", "Algebra", "Calculus"]

topic = st.selectbox("Choose a topic:", TOPICS)

# Initialise session state
if "questions" not in st.session_state:
    st.session_state.questions = []
if "difficulty" not in st.session_state:
    st.session_state.difficulty = None


# Difficulty buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Easy Worksheet"):
        st.session_state.difficulty = "Easy"
        st.session_state.questions = generate_worksheet(topic, "Easy")

with col2:
    if st.button("Medium Worksheet"):
        st.session_state.difficulty = "Medium"
        st.session_state.questions = generate_worksheet(topic, "Medium")

with col3:
    if st.button("Hard Worksheet"):
        st.session_state.difficulty = "Hard"
        st.session_state.questions = generate_worksheet(topic, "Hard")


# Display worksheet
if st.session_state.questions:
    difficulty = st.session_state.difficulty
    st.subheader(f"{topic} Worksheet ({difficulty})")

    for i, q in enumerate(st.session_state.questions):
        with st.container():
            st.write(f"### Question {i+1}")
            st.write(q)

            if st.button(f"Show Answer to Q{i+1}", key=f"answer_btn_{i}"):
                with st.spinner("Generating answer..."):
                    answer = generate_answer(q, topic, difficulty)
                    st.markdown(answer)

        st.markdown("---")







