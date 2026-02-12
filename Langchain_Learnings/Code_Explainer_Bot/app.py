"""
Code Explainer for Developers
A Streamlit + LangChain app that explains code like a senior developer
teaching a junior — with line-by-line breakdowns, use cases, and tips.
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time
import re

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Code Explainer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS — Dark terminal-inspired theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* ── Global ── */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* ── Hero Banner ── */
    .hero {
        background: linear-gradient(145deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
        border: 1px solid #2a2a4a;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(0,212,170,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero h1 {
        color: #e0e0e0;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }
    .hero h1 span {
        background: linear-gradient(135deg, #00d4aa, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        color: #7a7a9a;
        font-size: 1rem;
        margin-top: 0.5rem;
    }

    /* ── Terminal-style code area label ── */
    .terminal-label {
        font-family: 'Fira Code', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #00d4aa;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .terminal-label::before {
        content: '●';
        color: #00d4aa;
        font-size: 0.5rem;
    }

    /* ── Section Cards ── */
    .section-card {
        background: #0d0d14;
        border: 1px solid #1e1e3a;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .section-card h3 {
        color: #e0e0e0;
        font-size: 1.1rem;
        margin-top: 0;
        margin-bottom: 0.75rem;
        font-weight: 700;
    }

    /* ── Language Badge ── */
    .lang-badge {
        display: inline-block;
        background: rgba(0,212,170,0.1);
        border: 1px solid rgba(0,212,170,0.25);
        color: #00d4aa;
        font-family: 'Fira Code', monospace;
        font-size: 0.75rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        margin-bottom: 1rem;
    }

    /* ── Error State ── */
    .error-box {
        background: rgba(255,82,82,0.08);
        border: 1px solid rgba(255,82,82,0.25);
        border-radius: 12px;
        padding: 1.25rem;
        color: #ff5252;
    }

    /* ── Stats Row ── */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .stat-chip {
        background: #0d0d14;
        border: 1px solid #1e1e3a;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-family: 'Fira Code', monospace;
        font-size: 0.8rem;
        color: #7a7a9a;
    }
    .stat-chip strong {
        color: #00d4aa;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: #4a4a6a;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1.5rem 0;
        border-top: 1px solid #1e1e3a;
    }
    .footer a {
        color: #00d4aa;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Prompt Templates (Core Prompt Engineering)
# ──────────────────────────────────────────────
CODE_EXPLAINER_PROMPT = ChatPromptTemplate.from_template(
    """You are a patient, expert senior developer who excels at teaching junior developers.
Your job is to explain code clearly so that anyone can understand it.

Explain the following code:

```
{code}
```

{detail_instruction}

Respond in this EXACT structure using markdown:

## 🔍 What This Code Does
A clear 2-3 sentence summary of the code's purpose and behavior in plain English.

## 📝 Line-by-Line Explanation
Go through EVERY meaningful line or logical block. For each:
- Show the line/block
- Explain what it does in simple language
- Mention any important details (data types, side effects, edge cases)

## 🛠️ When to Use This
Give 2-3 real-world scenarios where this pattern or approach is useful.
Be specific — mention actual use cases like "building a REST API", "processing CSV files", etc.

## ⚡ Key Takeaways
List exactly 3 important things a junior developer should remember about this code.

## ⚠️ Common Pitfalls
Mention 1-2 mistakes beginners often make with this type of code and how to avoid them.

RULES:
- Use simple, jargon-free language. If you must use a technical term, briefly define it.
- Be encouraging — this is a learning moment, not a code review.
- If the input is not valid code, politely explain that and ask for actual code.
- Keep total response under 600 words.
- DO NOT rewrite or improve the code unless there's a critical bug.
"""
)

LANGUAGE_DETECT_PROMPT = ChatPromptTemplate.from_template(
    """Look at this code snippet and identify the programming language.
Respond with ONLY the language name in lowercase (e.g., python, javascript, java, c++, go, rust, sql, html, css, bash, typescript, ruby, php, swift, kotlin, r, scala, dart).
If you cannot identify it, respond with "unknown".

```
{code}
```"""
)


# ──────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────
def get_llm(api_key: str, model_name: str, temperature: float):
    """Create a ChatGroq LLM instance."""
    try:
        llm = ChatGroq(
            model=model_name,
            api_key=api_key,
            temperature=temperature,
            max_tokens=2048,
            request_timeout=45,
        )
        return llm, None
    except Exception as e:
        return None, f"Failed to initialize LLM: {str(e)}"


def detect_language(llm, code: str) -> str:
    """Use LLM to detect the programming language of the code."""
    try:
        chain = LANGUAGE_DETECT_PROMPT | llm | StrOutputParser()
        result = chain.invoke({"code": code})
        lang = result.strip().lower().split("\n")[0].strip("`").strip()
        # Sanitize — only return known languages
        known_langs = {
            "python", "javascript", "typescript", "java", "c", "c++", "c#",
            "go", "rust", "ruby", "php", "swift", "kotlin", "scala", "r",
            "sql", "html", "css", "bash", "shell", "dart", "lua", "perl",
            "haskell", "elixir", "clojure", "matlab", "powershell", "yaml",
            "json", "xml", "dockerfile", "terraform", "unknown",
        }
        return lang if lang in known_langs else "unknown"
    except Exception:
        return "unknown"


def explain_code(llm, code: str, detail_level: str, max_retries: int = 2):
    """Run the code explanation chain with retry logic."""

    # Map detail level to instruction
    detail_map = {
        "Beginner-Friendly": "Explain as if teaching someone who just started coding. Use analogies and avoid jargon entirely.",
        "Standard": "Explain clearly for a junior developer with some basic programming knowledge.",
        "Advanced": "Explain with technical depth. Include mentions of time complexity, design patterns, or best practices where relevant.",
    }
    detail_instruction = detail_map.get(detail_level, detail_map["Standard"])

    chain = CODE_EXPLAINER_PROMPT | llm | StrOutputParser()

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            response = chain.invoke({
                "code": code,
                "detail_instruction": detail_instruction,
            })
            return response, None
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries:
                time.sleep(1.5 * (attempt + 1))
            continue

    return None, f"Failed after {max_retries + 1} attempts. Error: {last_error}"


def validate_code(code: str) -> tuple[bool, str]:
    """Validate the code input."""
    if not code or not code.strip():
        return False, "Please paste some code to explain."
    if len(code.strip()) < 5:
        return False, "Code snippet is too short. Please provide a meaningful code block."
    if len(code.strip()) > 5000:
        return False, "Code is too long (max 5000 chars). Please paste a smaller snippet."
    return True, ""


def count_code_lines(code: str) -> int:
    """Count non-empty lines in the code."""
    return len([line for line in code.strip().split("\n") if line.strip()])


# ──────────────────────────────────────────────
# Sidebar Configuration
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at [console.groq.com](https://console.groq.com)",
    )

    model_name = st.selectbox(
        "Model",
        options=[
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
        ],
        index=0,
        help="Larger models give better explanations but are slower",
    )

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1,
        help="Lower = precise and focused, Higher = more creative explanations",
    )

    detail_level = st.radio(
        "Explanation Depth",
        options=["Beginner-Friendly", "Standard", "Advanced"],
        index=1,
        help="Adjusts how technical the explanation will be",
    )

    st.markdown("---")
    st.markdown("### 🎓 How It Works")
    st.markdown(
        """
    1. Paste any code snippet
    2. Click **Explain This Code**
    3. Get a structured breakdown:
       - What it does
       - Line-by-line walkthrough
       - When to use it
       - Key takeaways
       - Common pitfalls
    """
    )

    st.markdown("---")
    st.markdown(
        """<div style="text-align:center; color:#4a4a6a; font-size:0.75rem;">
        Built with Streamlit + LangChain<br>Powered by Groq LLMs
        </div>""",
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# Hero Header
# ──────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔬 Code <span>Explainer</span></h1>
    <p>Paste any code snippet → Get a clear, structured explanation instantly</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Example Code Snippets
# ──────────────────────────────────────────────
EXAMPLES = {
    "🐍 Python — Loop": """for i in range(5):
    print(i)""",

    "🟨 JavaScript — Fetch API": """fetch('https://api.example.com/data')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));""",

    "☕ Java — ArrayList": """import java.util.ArrayList;

ArrayList<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
for (String name : names) {
    System.out.println("Hello, " + name);
}""",

    "🐍 Python — Dict Comprehension": """scores = {"Alice": 85, "Bob": 92, "Charlie": 78}
passed = {name: score for name, score in scores.items() if score >= 80}
print(passed)""",

    "🟨 JS — Async/Await": """async function getUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error('User not found');
    const user = await response.json();
    return user;
  } catch (error) {
    console.error(error.message);
    return null;
  }
}""",

    "🐍 Python — Decorator": """def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(2)
    return "done"
""",
}

st.markdown('<div class="terminal-label">Quick Examples</div>', unsafe_allow_html=True)
example_cols = st.columns(3)
for idx, (label, code_snippet) in enumerate(EXAMPLES.items()):
    with example_cols[idx % 3]:
        if st.button(label, key=f"ex_{idx}", use_container_width=True):
            st.session_state["prefill_code"] = code_snippet

# ──────────────────────────────────────────────
# Code Input Area
# ──────────────────────────────────────────────
st.markdown('<div class="terminal-label">Paste Your Code</div>', unsafe_allow_html=True)

code_input = st.text_area(
    "code_input",
    value=st.session_state.get("prefill_code", ""),
    height=220,
    placeholder="Paste your code here...\n\nExample:\nfor i in range(5):\n    print(i)",
    max_chars=5000,
    label_visibility="collapsed",
)

# Clear prefill after rendering
if "prefill_code" in st.session_state:
    del st.session_state["prefill_code"]

# Show code stats
if code_input.strip():
    line_count = count_code_lines(code_input)
    char_count = len(code_input.strip())
    st.markdown(
        f"""<div class="stats-row">
            <div class="stat-chip">📏 <strong>{line_count}</strong> lines</div>
            <div class="stat-chip">🔤 <strong>{char_count}</strong> chars</div>
        </div>""",
        unsafe_allow_html=True,
    )

explain_btn = st.button("🔬 Explain This Code", type="primary", use_container_width=True)

# ──────────────────────────────────────────────
# Processing Pipeline
# ──────────────────────────────────────────────
if explain_btn:
    # ── Step 1: Validate API key ──
    if not api_key:
        st.markdown(
            '<div class="error-box">🔑 <strong>API Key Required</strong> — '
            'Enter your Groq API key in the sidebar.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    # ── Step 2: Validate code input ──
    is_valid, msg = validate_code(code_input)
    if not is_valid:
        st.markdown(
            f'<div class="error-box">⚠️ {msg}</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    # ── Step 3: Initialize LLM ──
    llm, llm_error = get_llm(api_key, model_name, temperature)
    if llm_error:
        st.markdown(
            f'<div class="error-box">❌ {llm_error}</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    # ── Step 4: Detect language ──
    with st.spinner("🔎 Detecting language..."):
        detected_lang = detect_language(llm, code_input.strip())

    if detected_lang != "unknown":
        st.markdown(
            f'<span class="lang-badge">Detected: {detected_lang}</span>',
            unsafe_allow_html=True,
        )

    # ── Step 5: Explain the code (with retry) ──
    with st.spinner("🧠 Analyzing code..."):
        explanation, invoke_error = explain_code(
            llm, code_input.strip(), detail_level
        )

    if invoke_error:
        st.markdown(
            f'<div class="error-box">❌ <strong>Error:</strong> {invoke_error}<br>'
            '<em>Check your API key or try a different model.</em></div>',
            unsafe_allow_html=True,
        )
        st.stop()

    # ── Step 6: Display the explanation ──
    st.markdown("---")
    st.markdown(explanation)

    # ── Step 7: Save to history ──
    if "history" not in st.session_state:
        st.session_state["history"] = []
    preview = code_input.strip()[:80] + ("..." if len(code_input.strip()) > 80 else "")
    st.session_state["history"].insert(0, {
        "code_preview": preview,
        "language": detected_lang,
        "explanation": explanation,
        "detail_level": detail_level,
    })


# ──────────────────────────────────────────────
# History Section
# ──────────────────────────────────────────────
if st.session_state.get("history"):
    st.markdown("---")
    with st.expander(f"📜 Explanation History ({len(st.session_state['history'])})"):
        for idx, item in enumerate(st.session_state["history"][:10]):
            lang_tag = f"[{item['language']}]" if item["language"] != "unknown" else ""
            st.markdown(f"**#{idx+1}** {lang_tag} `{item['code_preview']}`")
            st.markdown(item["explanation"])
            st.markdown("---")


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit + LangChain + Groq &nbsp;|&nbsp;
    <a href="https://github.com" target="_blank">⭐ Star on GitHub</a>
</div>
""", unsafe_allow_html=True)
