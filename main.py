import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Maths Tutor – Worksheet with Answers")


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
def generate_worksheet(topic):
    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Generate exactly 5 exam‑style questions on the topic. "
        "Return them as a numbered list, one question per line, no solutions."
    )

    user_prompt = f"Create a worksheet on: {topic}"

    text = call_openai(system_prompt, user_prompt)

    # Split into individual questions
    questions = [q.strip() for q in text.split("\n") if q.strip()]

    return questions


# ---------------------------------------------------------
# 3. Generate answer for a single question
# ---------------------------------------------------------
def generate_answer(question, topic):
    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Provide a full step‑by‑step worked solution to the question."
    )

    user_prompt = f"Topic: {topic}\nQuestion: {question}\nProvide the full solution."

    return call_openai(system_prompt, user_prompt)


# ---------------------------------------------------------
# 4. UI
# ---------------------------------------------------------
TOPICS = ["Probability", "Trigonometry", "Algebra", "Calculus"]

topic = st.selectbox("Choose a topic:", TOPICS)

# Generate worksheet button
if st.button("Generate Worksheet", key="generate_ws"):
    questions = generate_worksheet(topic)

    st.subheader(f"{topic} Worksheet")

    # Display each question with its own Show Answer button
    for i, q in enumerate(questions):
        st.write(f"### Question {i+1}")
        st.write(q)

        # Unique key for each answer button
        if st.button(f"Show Answer to Q{i+1}", key=f"answer_btn_{i}"):
            with st.spinner("Generating answer..."):
                answer = generate_answer(q, topic)
                st.write(answer)

        st.markdown("---")




