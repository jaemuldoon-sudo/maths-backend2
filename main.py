import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.write("API key loaded:", os.getenv("OPENAI_API_KEY") is not None)





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


# ---------------------------------------------------------
#  BUTTONS
# ---------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    full_solution_btn = st.button("Full Solution")

with col2:
    hints_btn = st.button("Hints Mode")

with col3:
    worksheet_btn = st.button("Generate Worksheet")

with col4:
    hard_worksheet_btn = st.button("Harder Questions")

with col5:
    honours_worksheet_btn = st.button("Honours Questions")
    
    
    
# ---------------------------------------------------------
#  PROCESS FULL SOLUTION / HINTS
# ---------------------------------------------------------
if (full_solution_btn or hints_btn) and question.strip():

    with st.spinner("Thinking..."):
        answer = call_llm(f"Topic: {topic}\nQuestion: {question}")

    st.session_state["full_answer"] = answer
    steps = [s.strip() for s in answer.split("STEP") if s.strip()]
    st.session_state["steps"] = steps
    st.session_state["current_step"] = 0


# ---------------------------------------------------------
#  FULL SOLUTION MODE
# ---------------------------------------------------------
if full_solution_btn and "full_answer" in st.session_state:
    st.markdown("### Full Solution")
    st.markdown(st.session_state["full_answer"])


# ---------------------------------------------------------
#  HINTS MODE
# ---------------------------------------------------------
if hints_btn and "steps" in st.session_state:
    st.markdown("### Step-by-step Hints")
    st.markdown("STEP " + st.session_state["steps"][0])
    st.session_state["current_step"] = 1


# ---------------------------------------------------------
#  SHOW NEXT HINT BUTTON
# ---------------------------------------------------------
if "steps" in st.session_state and st.session_state["current_step"] > 0:

    if st.session_state["current_step"] < len(st.session_state["steps"]):
        if st.button("Show next hint"):
            st.markdown("STEP " + st.session_state["steps"][st.session_state["current_step"]])
            st.session_state["current_step"] += 1
    else:
        st.success("You've reached the final answer.")


# ---------------------------------------------------------
#  NORMAL WORKSHEET
# ---------------------------------------------------------
if worksheet_btn and question.strip():
    with st.spinner("Generating worksheet..."):
        worksheet = generate_worksheet(topic, question)

    questions = re.findall(r"\d+\.\s.*", worksheet)
    st.session_state["worksheet_questions"] = questions
    st.markdown("## 📄 Worksheet: Similar Questions")


# ---------------------------------------------------------
#  HARD WORKSHEET
# ---------------------------------------------------------
if hard_worksheet_btn and question.strip():
    with st.spinner("Generating harder questions..."):
        worksheet = generate_harder_worksheet(topic, question)

    questions = re.findall(r"\d+\.\s.*", worksheet)
    st.session_state["worksheet_questions"] = questions
    st.markdown("## 🔥 Harder Worksheet: Advanced Questions")


# ---------------------------------------------------------
#  HONOURS WORKSHEET (OPTION B)
# ---------------------------------------------------------
if honours_worksheet_btn and question.strip():
    with st.spinner("Generating honours-level questions..."):
        worksheet = generate_honours_worksheet(topic, question)

    questions = re.findall(r"\d+\.\s.*", worksheet)
    st.session_state["worksheet_questions"] = questions
    st.markdown("## 🏅 Honours-Level Worksheet: Exam-Style Difficulty")


# ---------------------------------------------------------
#  DISPLAY WORKSHEET + ANSWER BUTTONS
# ---------------------------------------------------------
if "worksheet_questions" in st.session_state:

    for i, q in enumerate(st.session_state["worksheet_questions"]):
        st.markdown(f"### Question {i+1}")
        st.markdown(q)

        if st.button(f"Show Answer to Q{i+1}"):
            with st.spinner("Solving..."):
                answer = solve_single_question(q)
            st.markdown(f"**Answer to Question {i+1}:**")
            st.markdown(answer)
