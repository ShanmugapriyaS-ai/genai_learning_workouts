"""
Interview Question Explainer Bot
A Streamlit + LangChain app that helps freshers understand interview questions
with clear explanations, real-world examples, and key takeaways.
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.exceptions import OutputParserException
import os
import time

# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Interview Q&A Explainer",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global */
    .stApp {
        font-family: 'DM Sans', sans-serif;
    }

    /* Header */
    .hero-header {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .hero-header h1 {
        color: #f0f0f0;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-header p {
        color: #a0a0c0;
        font-size: 1rem;
        margin-top: 0.5rem;
    }

    /* Cards */
    .response-card {
        background: #fafbff;
        border: 1px solid #e2e6f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: box-shadow 0.2s;
    }
    .response-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }
    .card-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #6c5ce7;
        margin-bottom: 0.75rem;
        display: block;
    }

    /* Error card */
    .error-card {
        background: #fff5f5;
        border: 1px solid #fed7d7;
        border-radius: 12px;
        padding: 1.5rem;
        color: #c53030;
    }

    /* Example chips */
    .chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #a0a0a0;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem 0;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Prompt Template (Core Prompt Engineering)
# ──────────────────────────────────────────────
EXPLAINER_PROMPT = ChatPromptTemplate.from_template(
    """You are an expert tech interview coach who helps freshers and junior developers 
understand interview questions clearly.

The candidate has asked: "{question}"

Provide a structured, easy-to-understand response in the following format. 
Use markdown formatting.

## 📖 Definition
Explain the concept in simple, plain English. Avoid jargon. 
Imagine explaining to a smart 15-year-old.

## 🌍 Real-World Example
Give ONE concrete, relatable real-world analogy or scenario that makes 
the concept click instantly. Be specific — use a named app, service, or 
everyday situation.

## ⚡ 3 Key Points to Remember
List exactly 3 crisp, memorable bullet points that the candidate should 
remember for interviews. Each point should be 1-2 sentences max.

## 💬 Sample Interview Answer
Write a short (3-4 sentence) model answer the candidate could adapt 
when asked this question in an interview. Keep it confident but natural.

RULES:
- Keep the total response under 400 words.
- Use simple vocabulary — no unnecessary technical jargon.
- Be encouraging and supportive in tone.
- If the question is unclear or not interview-related, politely ask for clarification.
"""
)


# ──────────────────────────────────────────────
# LLM Chain Setup with Error Handling
# ──────────────────────────────────────────────
def get_llm_chain(api_key: str, model_name: str, temperature: float):
    """Create the LangChain chain with error handling."""
    try:
        llm = ChatGroq(
            model=model_name,
            api_key=api_key,
            temperature=temperature,
            max_tokens=1024,
            request_timeout=30,
        )
        # Chain: Prompt → LLM → String Output Parser
        chain = EXPLAINER_PROMPT | llm | StrOutputParser()
        return chain, None
    except Exception as e:
        return None, str(e)


def invoke_chain_with_retry(chain, question: str, max_retries: int = 2):
    """Invoke the chain with retry logic for transient failures."""
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            response = chain.invoke({"question": question})
            return response, None
        except OutputParserException as e:
            return None, f"Failed to parse LLM response: {str(e)}"
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries:
                time.sleep(1 * (attempt + 1))  # backoff
            continue
    return None, f"Failed after {max_retries + 1} attempts. Last error: {last_error}"


def validate_question(question: str) -> tuple[bool, str]:
    """Validate user input before sending to LLM."""
    if not question or not question.strip():
        return False, "Please enter a question."
    if len(question.strip()) < 5:
        return False, "Question is too short. Please provide more detail."
    if len(question.strip()) > 500:
        return False, "Question is too long. Please keep it under 500 characters."
    return True, ""


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free API key at [console.groq.com](https://console.groq.com)",
    )

    model_name = st.selectbox(
        "Model",
        options=[
            "llama-3.1-8b-instant",
            "llama3-8b-8192",
            "llama-3.1-8b-instant",
	        "llama-3.3-70b-versatile",
	        "openai/gpt-oss-20b",
	        "openai/gpt-oss-120b",

        ],
        index=0,
        help="Select the LLM model to use",
    )

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Lower = more focused, Higher = more creative",
    )

    st.markdown("---")
    st.markdown("### 📚 How to Use")
    st.markdown(
        """
    1. Enter your **Groq API key**
    2. Type any interview question
    3. Get a structured explanation!

    **Free API key →** [console.groq.com](https://console.groq.com)
    """
    )

    st.markdown("---")
    st.markdown(
        """
    <div style="text-align:center; color:#888; font-size:0.75rem;">
        Built with Streamlit + LangChain<br>
        Powered by Groq LLMs
    </div>
    """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# Main Content
# ──────────────────────────────────────────────
st.markdown(
    """
<div class="hero-header">
    <h1>🎯 Interview Question Explainer</h1>
    <p>Understand any tech interview question in seconds — with examples & key points</p>
</div>
""",
    unsafe_allow_html=True,
)

# Example questions as quick-select buttons
st.markdown("**Try an example:**")
example_questions = [
    "What is API Gateway?",
    "Explain REST vs GraphQL",
    "What is Docker?",
    "What is CI/CD pipeline?",
    "Explain microservices architecture",
    "What is OAuth 2.0?",
]

cols = st.columns(3)
for i, eq in enumerate(example_questions):
    with cols[i % 3]:
        if st.button(eq, key=f"example_{i}", use_container_width=True):
            st.session_state["prefill_question"] = eq

# Input area
question_input = st.text_area(
    "🔍 Enter your interview question",
    value=st.session_state.get("prefill_question", ""),
    height=80,
    placeholder="e.g., What is API Gateway? / Explain the difference between SQL and NoSQL...",
    max_chars=500,
)

# Clear prefill after use
if "prefill_question" in st.session_state:
    del st.session_state["prefill_question"]

explain_btn = st.button("✨ Explain This!", type="primary", use_container_width=True)

# ──────────────────────────────────────────────
# Processing & Response
# ──────────────────────────────────────────────
if explain_btn:
    # --- Validation Layer ---
    if not api_key:
        st.markdown(
            '<div class="error-card">🔑 <strong>API Key Required</strong> — '
            "Please enter your Groq API key in the sidebar.</div>",
            unsafe_allow_html=True,
        )
        st.stop()

    is_valid, validation_msg = validate_question(question_input)
    if not is_valid:
        st.markdown(
            f'<div class="error-card">⚠️ {validation_msg}</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    # --- Chain Creation ---
    chain, chain_error = get_llm_chain(api_key, model_name, temperature)
    if chain_error:
        st.markdown(
            f'<div class="error-card">❌ <strong>Setup Error:</strong> {chain_error}</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    # --- LLM Invocation with Spinner ---
    with st.spinner("🧠 Thinking..."):
        response, invoke_error = invoke_chain_with_retry(chain, question_input.strip())

    if invoke_error:
        st.markdown(
            f'<div class="error-card">❌ <strong>Error:</strong> {invoke_error}<br>'
            "<em>Check your API key or try again.</em></div>",
            unsafe_allow_html=True,
        )
        st.stop()

    # --- Display Response ---
    st.markdown("---")
    st.markdown(
        f'<span class="card-label">Explaining: {question_input.strip()}</span>',
        unsafe_allow_html=True,
    )
    st.markdown(response)

    # --- Save to History ---
    if "history" not in st.session_state:
        st.session_state["history"] = []
    st.session_state["history"].insert(
        0, {"question": question_input.strip(), "response": response}
    )

# ──────────────────────────────────────────────
# History Section
# ──────────────────────────────────────────────
if st.session_state.get("history"):
    st.markdown("---")
    with st.expander(f"📜 Previous Questions ({len(st.session_state['history'])})"):
        for i, item in enumerate(st.session_state["history"][:10]):
            st.markdown(f"**Q{i+1}: {item['question']}**")
            st.markdown(item["response"])
            st.markdown("---")

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown(
    """
<div class="footer">
    Made with ❤️ using Streamlit + LangChain + Groq | 
    <a href="https://github.com" target="_blank">⭐ Star on GitHub</a>
</div>
""",
    unsafe_allow_html=True,
)
