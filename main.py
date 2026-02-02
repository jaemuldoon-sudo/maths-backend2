import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Maths Tutor – Worksheet with Difficulty Levels")

SUBTOPICS = {
    "Probability": [
        "Combined events",
        "Conditional probability",
        "Expected value",
        "Permutations and combinations",
        "Binomial distribution",
        "Bernoulli Trials",
        "Normal Distribution"
    ],
    "Trigonometry": [
        "Trig identities",
        "Trig equations",
        "Graphs",
        "Radians",
        "Sine rule / Cosine rule"
    ],
    "Algebra": [
        "Quadratics",
        "Functions",
        "Logs",
        "Sequences & series",
        "Inequalities"
    ],
    "Calculus": [
        "Differentiation",
        "Integration",
        "Rates of change",
        "Area under curves",
        "Product/Quotient/Chain rule"
    ]
}




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
def generate_worksheet(topic, subtopics, difficulty):
    chosen = ", ".join(subtopics)

    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Generate exactly 5 unique exam‑style questions. "
        "Every time you are asked, produce a completely different set. "
        f"Difficulty level: {difficulty}. "
        f"Focus ONLY on these subtopics: {chosen}. "
        "Use LaTeX formatting for ALL mathematical expressions, wrapped in $$ ... $$. "
        "Return the questions as a numbered list, one per line, no solutions."
    )

    user_prompt = f"Create a {difficulty} worksheet on {topic} covering: {chosen}"

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


def generate_similar_question(question, topic, difficulty):
    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Generate ONE new question that is similar in style and difficulty "
        "to the given question, but not identical. "
        "Use LaTeX formatting for all mathematical expressions, wrapped in $$ ... $$. "
        f"Match the difficulty level: {difficulty}. "
        "Do not provide a solution."
    )

    user_prompt = f"Topic: {topic}\nDifficulty: {difficulty}\nOriginal question: {question}"

    return call_openai(system_prompt, user_prompt)
    

def generate_balanced_worksheet(topic, subtopics):
    chosen = ", ".join(subtopics)

    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Generate ONE exam‑style question for EACH of the subtopics of the selected topic. "
        "Use LaTeX formatting for all mathematical expressions, wrapped in $$ ... $$. "
        "Ensure each question is unique and non‑repetitive. "
        "Return them as a numbered list, one per line, no solutions."
    )

    user_prompt = f"Topic: {topic}\nSubtopics: {chosen}\nGenerate one question per subtopic."

    text = call_openai(system_prompt, user_prompt)
    questions = [q.strip() for q in text.split("\n") if q.strip()]
    return questions


# ---------------------------------------------------------
# 4. UI
# ---------------------------------------------------------
TOPICS = ["Probability", "Trigonometry", "Algebra", "Calculus"]

topic = st.selectbox("Choose a topic:", TOPICS)
subtopics = st.multiselect(
    "Choose subtopics:",
    SUBTOPICS.get(topic, [])
)


# Initialise session state
if "questions" not in st.session_state:
    st.session_state.questions = []
if "difficulty" not in st.session_state:
    st.session_state.difficulty = None


# Difficulty buttons
# --- Row 1: Easy / Medium / Hard ---
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    if st.button("Easy Worksheet"):
        st.session_state.difficulty = "Easy"
        st.session_state.questions = generate_worksheet(topic, subtopics, "Easy")

with row1_col2:
    if st.button("Medium Worksheet"):
        st.session_state.difficulty = "Medium"
        st.session_state.questions = generate_worksheet(topic, subtopics, "Medium")

with row1_col3:
    if st.button("Hard Worksheet"):
        st.session_state.difficulty = "Hard"
        st.session_state.questions = generate_worksheet(topic, subtopics, "Hard")


# --- Row 2: Random / Balanced ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    if st.button("Random Worksheet"):
        import random
        random_difficulty = random.choice(["Easy", "Medium", "Hard"])
        st.session_state.difficulty = random_difficulty
        st.session_state.questions = generate_worksheet(topic, subtopics, random_difficulty)

with row2_col2:
    if st.button("Balanced Worksheet"):
        st.session_state.difficulty = "Balanced"
        st.session_state.questions = generate_balanced_worksheet(topic, subtopics)



# Display worksheet
if st.session_state.questions:
    difficulty = st.session_state.difficulty
    st.subheader(f"{topic} Worksheet ({difficulty})")

    for i, q in enumerate(st.session_state.questions):
        with st.container():
            st.write(f"### Question {i+1}")
            st.markdown(q)

            # Show Answer button
            if st.button(f"Show Answer to Q{i+1}", key=f"answer_btn_{i}"):
                with st.spinner("Generating answer..."):
                    answer = generate_answer(q, topic, difficulty)
                    st.markdown(answer)

            # More Questions Like This button
            if st.button(f"More Questions Like This (Q{i+1})", key=f"more_like_{i}"):
                with st.spinner("Generating similar question..."):
                    similar = generate_similar_question(q, topic, difficulty)
                    st.markdown(f"**Another question like Q{i+1}:**")
                    st.markdown(similar)

        st.markdown("---")








