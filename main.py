import streamlit as st

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
        "Sine rule / Cosine rule",
        "Unit Circle"
    ],
    "Algebra": [
        "Quadratics",
        "Functions",
        "Logs",
        "Sequences & series",
        "Inequalities"
    ],
    
    "Circle": [
        "Center (0,0) and radius r",
        "Center (h,k) and radius r",
        "Equations of the form x^2 +y^2 + 2gx + 2gy + c = 0",
        "Points outside, inside or on the Circle",
        "Intersection of a line and circle"
    ],
    
    "Calculus": [
        "Differentiation",
        "Integration",
        "Rates of change",
        "Area under curves",
        "Product/Quotient/Chain rule"
    ]
}


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="LC Maths Tutor",
    layout="centered",
)

# -----------------------------
# BRAND HEADER
# -----------------------------
st.markdown(
    """
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <h1 style="margin-bottom:0;">📘 LC Maths Tutor</h1>
        <p style="color:#4a4a4a; font-size:18px; margin-top:5px;">
            Adaptive, exam‑style practice — built for students.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# TOPIC + SUBTOPICS
# -----------------------------
st.markdown("### Choose Your Topic")
topic = st.selectbox("", topics)

st.markdown("### Choose Subtopics")
subtopics = st.multiselect(
    "",
    SUBTOPICS.get(topic, []),
    placeholder="Pick 1–5 subtopics"
)

st.markdown("---")

# -----------------------------
# WORKSHEET BUTTONS (MOBILE‑FIRST)
# -----------------------------
st.markdown("### Generate Worksheet")

# Row 1 — Difficulty
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Easy", use_container_width=True):
        st.session_state.difficulty = "Easy"
        st.session_state.questions = generate_worksheet(topic, subtopics, "Easy")

with c2:
    if st.button("Medium", use_container_width=True):
        st.session_state.difficulty = "Medium"
        st.session_state.questions = generate_worksheet(topic, subtopics, "Medium")

with c3:
    if st.button("Hard", use_container_width=True):
        st.session_state.difficulty = "Hard"
        st.session_state.questions = generate_worksheet(topic, subtopics, "Hard")

# Row 2 — Modes
c4, c5 = st.columns(2)

with c4:
    if st.button("Random", use_container_width=True):
        import random
        diff = random.choice(["Easy", "Medium", "Hard"])
        st.session_state.difficulty = diff
        st.session_state.questions = generate_worksheet(topic, subtopics, diff)

with c5:
    if st.button("Balanced", use_container_width=True):
        st.session_state.difficulty = "Balanced"
        st.session_state.questions = generate_balanced_worksheet(topic, subtopics)

st.markdown("---")

# -----------------------------
# DISPLAY WORKSHEET
# -----------------------------
questions = st.session_state.get("questions", [])
difficulty = st.session_state.get("difficulty", None)

if questions:
    st.markdown(
        f"""
        <h2 style="margin-bottom:0;">{topic} Worksheet</h2>
        <p style="color:#6a6a6a; margin-top:0;">
            Mode: <strong>{difficulty}</strong>
        </p>
        """,
        unsafe_allow_html=True
    )

    if subtopics:
        st.caption("Subtopics: " + ", ".join(subtopics))

    for i, q in enumerate(questions):
        st.markdown(
            f"""
            <div style="
                background:#f7f9fc;
                padding:18px;
                border-radius:10px;
                margin-bottom:15px;
                border:1px solid #e3e6eb;
            ">
                <h4 style="margin-top:0;">Question {i+1}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(q)

        b1, b2 = st.columns(2)

        with b1:
            if st.button(f"Show Answer", key=f"ans_{i}", use_container_width=True):
                ans = generate_answer(q, topic, difficulty)
                st.markdown(ans)

        with b2:
            if st.button(f"More Like This", key=f"more_{i}", use_container_width=True):
                sim = generate_similar_question(q, topic, difficulty)
                st.markdown("**Another question like this:**")
                st.markdown(sim)

else:
    st.info("Choose a topic, pick subtopics, and select a worksheet mode to begin.")
