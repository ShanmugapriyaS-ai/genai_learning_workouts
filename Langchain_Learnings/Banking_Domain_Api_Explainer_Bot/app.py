"""
Banking Domain API Explainer
Built with Streamlit + LangChain + Groq LLM
Explains banking APIs with business context, technical details, and failure scenarios.
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import time
import json

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Banking API Explainer",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp {
        font-family: 'DM Sans', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #0a1628 0%, #1a365d 50%, #2c5282 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(66, 153, 225, 0.2);
    }
    .main-header h1 {
        color: #e2e8f0;
        font-size: 2rem;
        margin: 0;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #90cdf4;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }

    .result-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s;
    }
    .result-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .result-card h3 {
        color: #1a365d;
        font-size: 1.15rem;
        margin: 0 0 1rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 2px solid #ebf4ff;
        font-weight: 600;
    }

    .api-chip {
        display: inline-block;
        background: #ebf8ff;
        color: #2b6cb0;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 0.2rem;
        border: 1px solid #bee3f8;
    }

    .error-box {
        background: #fff5f5;
        border: 1px solid #fed7d7;
        border-left: 4px solid #e53e3e;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 1rem 0;
    }
    .error-box p {
        color: #c53030;
        margin: 0;
    }

    .sidebar-info {
        background: #f0fff4;
        border: 1px solid #c6f6d5;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        font-size: 0.88rem;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Prompt Templates
# ─────────────────────────────────────────────
BUSINESS_PROMPT = ChatPromptTemplate.from_template(
    """You are a senior banking domain consultant. Explain the "{api_name}" API 
from a BUSINESS perspective in the banking/fintech domain.

Cover:
1. **What it does** — plain English explanation a business stakeholder would understand
2. **Why it's needed** — the real-world banking problem it solves
3. **Business value** — how it impacts revenue, customer experience, or compliance
4. **Who uses it** — teams or systems that depend on this API

Keep it concise (150-200 words), professional, and jargon-free where possible.
Use concrete banking examples (e.g., amounts, scenarios)."""
)

TECHNICAL_PROMPT = ChatPromptTemplate.from_template(
    """You are a senior backend engineer at a large bank. Explain the "{api_name}" API 
from a TECHNICAL perspective.

Cover:
1. **Endpoint design** — typical REST method, path, key request/response fields
2. **How it works internally** — step-by-step flow (e.g., validation → processing → response)
3. **Key technical considerations** — idempotency, rate limiting, auth, timeout handling
4. **Integration pattern** — how downstream systems typically consume this API

Keep it concise (150-200 words). Use realistic field names and HTTP status codes.
Format code snippets with markdown where helpful."""
)

FAILURE_PROMPT = ChatPromptTemplate.from_template(
    """You are a site reliability engineer at a major bank. For the "{api_name}" API, 
explain realistic FAILURE SCENARIOS.

Cover exactly 3 failure cases:

For each failure, provide:
- **Scenario** — what goes wrong (be specific with a realistic example)
- **Root cause** — why this happens technically
- **HTTP status / Error code** — what the caller sees
- **Impact** — what breaks downstream
- **Mitigation** — how to prevent or handle it

Focus on failures that actually occur in production banking systems.
Keep each failure case to 60-80 words. Be specific, not generic."""
)

INTERVIEW_PROMPT = ChatPromptTemplate.from_template(
    """You are a fintech interview coach. For the "{api_name}" API in banking:

Generate 5 likely interview questions that test understanding of this API, ranging from 
basic to advanced. For each question, provide:
- The question
- A brief ideal answer (2-3 sentences)
- What skill it tests (domain knowledge, system design, error handling, etc.)

Focus on questions that combine domain knowledge with technical depth."""
)


# ─────────────────────────────────────────────
# LLM & Chain Setup
# ─────────────────────────────────────────────
def get_llm(api_key: str, temperature: float = 0.3):
    """Initialize Groq LLM with error handling."""
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=api_key,
            temperature=temperature,
            max_tokens=1024,
            request_timeout=30,
        )
        return llm
    except Exception as e:
        raise ConnectionError(f"Failed to initialize LLM: {str(e)}")


def build_chain(llm, prompt_template):
    """Build a LangChain chain with output parsing and error passthrough."""
    chain = prompt_template | llm | StrOutputParser()
    return chain


def invoke_chain_safe(chain, inputs: dict, retries: int = 2):
    """Invoke chain with retry logic and structured error handling."""
    last_error = None
    for attempt in range(retries + 1):
        try:
            result = chain.invoke(inputs)
            return {"success": True, "content": result, "attempts": attempt + 1}
        except Exception as e:
            last_error = e
            error_str = str(e).lower()

            # Classify error
            if "authentication" in error_str or "api key" in error_str or "401" in error_str:
                return {
                    "success": False,
                    "error": "🔑 Invalid API Key. Please check your Groq API key in the sidebar.",
                    "error_type": "auth",
                    "attempts": attempt + 1,
                }
            elif "rate" in error_str or "429" in error_str:
                if attempt < retries:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                return {
                    "success": False,
                    "error": "⏳ Rate limit hit. Please wait a moment and try again.",
                    "error_type": "rate_limit",
                    "attempts": attempt + 1,
                }
            elif "timeout" in error_str:
                if attempt < retries:
                    continue
                return {
                    "success": False,
                    "error": "⌛ Request timed out. The LLM service may be busy — try again.",
                    "error_type": "timeout",
                    "attempts": attempt + 1,
                }
            else:
                if attempt < retries:
                    time.sleep(1)
                    continue

    return {
        "success": False,
        "error": f"❌ Unexpected error after {retries + 1} attempts: {str(last_error)}",
        "error_type": "unknown",
        "attempts": retries + 1,
    }


# ─────────────────────────────────────────────
# Predefined Banking APIs
# ─────────────────────────────────────────────
BANKING_APIS = {
    "Payment Retry API": "Payment Retry API — retries failed payment transactions in banking systems",
    "Account Balance Inquiry API": "Account Balance Inquiry API — fetches real-time account balances",
    "Fund Transfer API": "Fund Transfer API — transfers money between accounts (NEFT/RTGS/IMPS)",
    "KYC Verification API": "KYC Verification API — verifies customer identity documents",
    "Loan Eligibility API": "Loan Eligibility API — checks if a customer qualifies for a loan",
    "Card Tokenization API": "Card Tokenization API — replaces card numbers with secure tokens",
    "Transaction Dispute API": "Transaction Dispute API — handles chargebacks and transaction disputes",
    "Standing Instruction API": "Standing Instruction API — manages recurring/scheduled payments",
    "Fraud Detection API": "Fraud Detection API — real-time fraud scoring for transactions",
    "Account Statement API": "Account Statement API — generates account statements for a date range",
    "Beneficiary Management API": "Beneficiary Management API — add/remove/verify payment beneficiaries",
    "UPI Payment API": "UPI Payment API — processes Unified Payments Interface transactions",
}


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at https://console.groq.com/keys",
    )

    st.markdown("---")
    st.markdown("### 🎛️ Options")

    temperature = st.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Lower = more focused, Higher = more creative",
    )

    sections_to_generate = st.multiselect(
        "Sections to Generate",
        ["Business Explanation", "Technical Explanation", "Failure Scenarios", "Interview Q&A"],
        default=["Business Explanation", "Technical Explanation", "Failure Scenarios"],
    )

    st.markdown("---")
    st.markdown(
        """<div class="sidebar-info">
        <strong>💡 How to use</strong><br>
        1. Enter your Groq API key<br>
        2. Pick a banking API or type your own<br>
        3. Click <b>Explain API</b><br>
        4. Get business + technical breakdowns
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.caption("Built with Streamlit • LangChain • Groq")


# ─────────────────────────────────────────────
# Main Content
# ─────────────────────────────────────────────
st.markdown(
    """<div class="main-header">
        <h1>🏦 Banking Domain API Explainer</h1>
        <p>Powered by GenAI — Get business, technical & failure analysis for any banking API</p>
    </div>""",
    unsafe_allow_html=True,
)

# API Selection
col1, col2 = st.columns([3, 2])

with col1:
    selected_api = st.selectbox(
        "Select a Banking API",
        options=["— Choose a preset —"] + list(BANKING_APIS.keys()) + ["✏️ Custom API (type below)"],
        index=0,
    )

with col2:
    custom_api = st.text_input(
        "Or enter a custom API name",
        placeholder="e.g., Cheque Truncation API",
        disabled=(selected_api != "✏️ Custom API (type below)"),
    )

# Determine final API name
api_name = None
if selected_api and selected_api not in ["— Choose a preset —", "✏️ Custom API (type below)"]:
    api_name = selected_api
elif selected_api == "✏️ Custom API (type below)" and custom_api.strip():
    api_name = custom_api.strip()

# Show selected API chips
if api_name:
    st.markdown(f'<span class="api-chip">🔍 Analyzing: {api_name}</span>', unsafe_allow_html=True)

st.markdown("")

# ─────────────────────────────────────────────
# Generate Button & Results
# ─────────────────────────────────────────────
generate_clicked = st.button("🚀 Explain API", type="primary", use_container_width=True, disabled=(not api_name))

if generate_clicked:
    # Validation
    if not api_key:
        st.markdown(
            '<div class="error-box"><p>🔑 Please enter your Groq API key in the sidebar to continue.</p></div>',
            unsafe_allow_html=True,
        )
        st.stop()

    if not sections_to_generate:
        st.warning("Please select at least one section to generate.")
        st.stop()

    # Initialize LLM
    try:
        llm = get_llm(api_key, temperature)
    except ConnectionError as e:
        st.error(str(e))
        st.stop()

    # Resolve API description for prompt
    api_input = BANKING_APIS.get(api_name, f"{api_name} in banking/fintech context")

    # Section mapping
    section_config = {
        "Business Explanation": ("📊 Business Explanation", BUSINESS_PROMPT),
        "Technical Explanation": ("⚙️ Technical Explanation", TECHNICAL_PROMPT),
        "Failure Scenarios": ("🔴 Failure Scenarios", FAILURE_PROMPT),
        "Interview Q&A": ("🎯 Interview Questions & Answers", INTERVIEW_PROMPT),
    }

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    total = len(sections_to_generate)

    # Store results
    results = {}

    for idx, section_name in enumerate(sections_to_generate):
        title, prompt_template = section_config[section_name]
        status_text.text(f"Generating {title}... ({idx + 1}/{total})")

        chain = build_chain(llm, prompt_template)
        result = invoke_chain_safe(chain, {"api_name": api_input})
        results[section_name] = (title, result)

        progress_bar.progress((idx + 1) / total)

    status_text.empty()
    progress_bar.empty()

    # ─────────────────────────────────────────
    # Display Results
    # ─────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"## 📋 Results: `{api_name}`")

    error_count = 0

    for section_name in sections_to_generate:
        title, result = results[section_name]

        if result["success"]:
            with st.expander(f"{title}", expanded=True):
                st.markdown(result["content"])
                if result["attempts"] > 1:
                    st.caption(f"✅ Succeeded after {result['attempts']} attempt(s)")
        else:
            error_count += 1
            with st.expander(f"❌ {title} — Failed", expanded=True):
                st.markdown(
                    f'<div class="error-box"><p>{result["error"]}</p></div>',
                    unsafe_allow_html=True,
                )
                st.caption(f"Attempted {result['attempts']} time(s) | Error type: {result.get('error_type', 'unknown')}")

    # Summary
    st.markdown("---")
    success_count = total - error_count
    if error_count == 0:
        st.success(f"✅ All {total} sections generated successfully for **{api_name}**.")
    elif error_count < total:
        st.warning(f"⚠️ {success_count}/{total} sections generated. {error_count} had errors — check details above.")
    else:
        st.error("❌ All sections failed. Please check your API key and try again.")

# ─────────────────────────────────────────────
# Footer with Architecture Info
# ─────────────────────────────────────────────
with st.expander("🏗️ Architecture & Flow"):
    st.markdown("""
    ```
    User Input (API Name)
         │
         ▼
    ┌─────────────────────┐
    │  Streamlit Frontend  │
    │  (Selection / Input) │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │  LangChain Chains    │
    │  (4 Prompt Templates)│
    │  Business | Technical │
    │  Failures | Interview │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │  Error Handler       │
    │  - Auth errors       │
    │  - Rate limit retry  │
    │  - Timeout retry     │
    │  - Exponential backoff│
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │  Groq LLM (Llama 3) │
    │  via LangChain       │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │  StrOutputParser     │
    │  → Formatted Output  │
    └─────────────────────┘
    ```
    
    **Key Design Decisions:**
    - **Retry with backoff** — handles transient Groq rate limits gracefully
    - **Error classification** — differentiates auth, rate-limit, timeout, and unknown errors
    - **Modular chains** — each section uses its own optimized prompt template
    - **Streaming progress** — shows real-time generation progress to user
    """)
