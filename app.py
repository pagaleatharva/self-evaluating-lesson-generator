
import streamlit as st
from html import escape
from workflow.graph import run_workflow

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="LessonAI | Intelligent Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background: #0b1020;
    color: #f1f5f9;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

header {
    visibility: hidden;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.subtitle {
    color: #94a3b8;
    font-size: 16px;
    margin-bottom: 30px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 25px;
    margin-bottom: 15px;
}

.hero {
    background: linear-gradient(120deg, #172554, #312e81, #581c87);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #4338ca;
    margin-bottom: 28px;
}

.hero h2 {
    color: white;
    font-size: 26px;
    margin-bottom: 8px;
}

.hero p {
    color: #dbeafe;
    font-size: 15px;
    margin-bottom: 0;
}

.stTextInput input {
    background-color: #151d32;
    color: white;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 14px;
}

.stTextInput label {
    color: #e2e8f0 !important;
    font-weight: 600;
}

.stButton button {
    background: linear-gradient(90deg, #6366f1, #9333ea);
    color: white;
    border: none;
    border-radius: 10px;
    height: 48px;
    font-weight: 700;
    width: 100%;
    transition: 0.3s;
}

.stButton button:hover {
    border: 1px solid #a78bfa;
    color: white;
    background: linear-gradient(90deg, #4f46e5, #7e22ce);
}

.metric-card {
    background: #151d32;
    border: 1px solid #29354d;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    margin-bottom: 15px;
}

.metric-label {
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 8px;
}

.metric-value {
    color: #ffffff;
    font-size: 29px;
    font-weight: 800;
}

.check-card {
    background: #151d32;
    border: 1px solid #29354d;
    border-radius: 12px;
    padding: 17px;
    margin-bottom: 12px;
}

.check-name {
    color: #f8fafc;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 10px;
}

.pass {
    color: #4ade80;
    font-weight: 700;
}

.fail {
    color: #f87171;
    font-weight: 700;
}

.check-reason {
    color: #cbd5e1;
    font-size: 14px;
    margin-top: 8px;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    padding-top: 35px;
}

hr {
    border-color: #29354d;
}

[data-testid="stExpander"] {
    background: #151d32;
    border: 1px solid #29354d;
    border-radius: 10px;
}

.stMarkdown {
    color: #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
<div class="main-title">📚 LessonAI</div>
<div class="subtitle">
    Self-Evaluating AI Lesson Generator
</div>

<div class="hero">
    <h2>Learn Smarter with AI</h2>
    <p>
        Generate beginner-friendly lessons, evaluate their quality,
        and automatically improve them using an AI-powered workflow.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- TOPIC INPUT ----------------

st.markdown(
    '<div class="section-title">Generate Your Lesson</div>',
    unsafe_allow_html=True
)

topic = st.text_input(
    "Enter your learning topic",
    placeholder="e.g. Introduction to RAG"
)

generate_button = st.button(
    "✨ Generate & Evaluate Lesson",
    type="primary",
    use_container_width=True
)


# ---------------- RUN WORKFLOW ----------------

if generate_button:

    if not topic.strip():
        st.warning("Please enter a learning topic.")

    else:
        try:
            with st.spinner(
                "AI is generating and evaluating your lesson..."
            ):
                result = run_workflow(topic.strip())

                st.session_state["result"] = result
                st.session_state["topic"] = topic.strip()

        except Exception as error:
            st.error(f"Something went wrong: {error}")


# ---------------- DISPLAY RESULTS ----------------

if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()

    st.markdown(
        '<div class="section-title">Workflow Overview</div>',
        unsafe_allow_html=True
    )

    # Status
    if result["status"] == "PASS":
        st.success("✓ Lesson Approved — All six quality checks passed.")
    else:
        st.error("✕ Lesson Rejected — Quality requirements not satisfied.")

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">WORKFLOW STATUS</div>
            <div class="metric-value">
                {"PASS" if result["status"] == "PASS" else "FAIL"}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL ATTEMPTS</div>
            <div class="metric-value">
                {result["retry_count"] + 1}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">REGENERATIONS</div>
            <div class="metric-value">
                {result["retry_count"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Evaluation
    st.markdown(
        '<div class="section-title">Quality Evaluation</div>',
        unsafe_allow_html=True
    )

    checks = list(result["evaluation"].items())

    for start in range(0, len(checks), 2):

        columns = st.columns(2)

        for column, (name, check) in zip(
            columns,
            checks[start:start + 2]
        ):

            status = check["status"]
            status_class = "pass" if status == "PASS" else "fail"
            symbol = "✓" if status == "PASS" else "✕"

            with column:
                st.markdown(f"""
                <div class="check-card">
                    <div class="check-name">
                        {escape(name.replace("_", " ").title())}
                    </div>
                    <div class="{status_class}">
                        {symbol} {escape(status)}
                    </div>
                    <div class="check-reason">
                        {escape(check["reason"])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if check["improvement"]:
                    with st.expander("Suggested Improvement"):
                        st.write(check["improvement"])

    # Rejection log
    st.markdown(
        '<div class="section-title">Rejection History</div>',
        unsafe_allow_html=True
    )

    if result["rejection_log"]:

        for log in result["rejection_log"]:

            with st.expander(f"Attempt {log['attempt']} — Rejected"):

                for failure in log["failed_checks"]:
                    st.write(f"• {failure}")

    else:
        st.success("No rejections. The lesson passed on its first attempt.")

    # Final lesson
    st.markdown(
        '<div class="section-title">Final Generated Lesson</div>',
        unsafe_allow_html=True
    )

    if result["status"] == "PASS":
        st.success("This lesson successfully passed the evaluation.")
    else:
        st.warning("This lesson did not pass the evaluation.")

    st.markdown(result["lesson"])

    # Footer
    st.markdown("""
    <div class="footer">
        LessonAI | Built with Python, LangChain, LangGraph,
        Groq AI and Streamlit
    </div>
    """, unsafe_allow_html=True)


else:

    st.markdown("""
    <div class="footer">
        Enter a topic above to start generating your AI-powered lesson.
    </div>
    """, unsafe_allow_html=True)
