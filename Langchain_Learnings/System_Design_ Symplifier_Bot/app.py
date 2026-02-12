"""
System Design Simplifier
Built with Streamlit + LangChain + Groq LLM
Breaks down complex system design concepts into simple explanations,
real-world analogies, pros/cons, and interview-ready answers.
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="System Design Simplifier",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS — Dark editorial theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    .stApp {
        font-family: 'Space Grotesk', sans-serif;
    }

    .hero-banner {
        background: linear-gradient(160deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        border: 1px solid rgba(130, 120, 255, 0.15);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(130,120,255,0.12) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-banner h1 {
        color: #e8e6ff;
        font-size: 2.1rem;
        margin: 0;
        font-weight: 700;
        letter-spacing: -0.8px;
    }
    .hero-banner p {
        color: #a5b4fc;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }

    .section-card {
        background: #fafafa;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.8rem 2rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
        transition: transform 0.15s, box-shadow 0.15s;
    }
    .section-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    }
    .section-card.simple     { border-left-color: #6366f1; }
    .section-card.analogy    { border-left-color: #f59e0b; }
    .section-card.proscons   { border-left-color: #10b981; }
    .section-card.diagram    { border-left-color: #8b5cf6; }
    .section-card.interview  { border-left-color: #ef4444; }
    .section-card.tradeoff   { border-left-color: #0ea5e9; }

    .section-card h3 {
        margin: 0 0 0.8rem 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
    }

    .topic-chip {
        display: inline-block;
        background: #eef2ff;
        color: #4338ca;
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 0.15rem 0.2rem;
        border: 1px solid #c7d2fe;
        cursor: default;
    }

    .error-banner {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        margin: 0.8rem 0;
    }
    .error-banner p { color: #b91c1c; margin: 0; font-size: 0.95rem; }

    .success-banner {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #22c55e;
        border-radius: 10px;
        padding: 1rem 1.4rem;
        margin: 1rem 0;
    }
    .success-banner p { color: #166534; margin: 0; }

    .sidebar-tip {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        font-size: 0.85rem;
        color: #1e40af;
    }

    .difficulty-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    .difficulty-badge.beginner { background: #dcfce7; color: #166534; }
    .difficulty-badge.intermediate { background: #fef3c7; color: #92400e; }
    .difficulty-badge.advanced { background: #fce7f3; color: #9d174d; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# System Design Topics Library
# ─────────────────────────────────────────────
TOPICS = {
    "Architecture Patterns": {
        "Microservices Architecture": {
            "desc": "Breaking a monolith into independent, deployable services",
            "difficulty": "intermediate",
            "tags": ["distributed", "scalability", "deployment"],
        },
        "Monolithic Architecture": {
            "desc": "Single unified codebase deployed as one unit",
            "difficulty": "beginner",
            "tags": ["simplicity", "deployment", "coupling"],
        },
        "Event-Driven Architecture": {
            "desc": "Systems communicating through asynchronous events",
            "difficulty": "advanced",
            "tags": ["async", "decoupling", "messaging"],
        },
        "Serverless Architecture": {
            "desc": "Cloud functions that scale automatically without managing servers",
            "difficulty": "intermediate",
            "tags": ["cloud", "scaling", "cost"],
        },
        "Service-Oriented Architecture (SOA)": {
            "desc": "Enterprise integration pattern using reusable service contracts",
            "difficulty": "intermediate",
            "tags": ["enterprise", "integration", "SOAP"],
        },
    },
    "Scalability & Performance": {
        "Load Balancing": {
            "desc": "Distributing traffic across multiple servers",
            "difficulty": "beginner",
            "tags": ["traffic", "availability", "scaling"],
        },
        "Database Sharding": {
            "desc": "Splitting a database across multiple machines horizontally",
            "difficulty": "advanced",
            "tags": ["database", "horizontal-scaling", "partitioning"],
        },
        "Caching Strategies": {
            "desc": "Storing frequently accessed data closer to the consumer",
            "difficulty": "intermediate",
            "tags": ["redis", "CDN", "performance"],
        },
        "Horizontal vs Vertical Scaling": {
            "desc": "Adding more machines vs upgrading existing ones",
            "difficulty": "beginner",
            "tags": ["scaling", "infrastructure", "cost"],
        },
        "Rate Limiting & Throttling": {
            "desc": "Controlling how many requests a client can make",
            "difficulty": "intermediate",
            "tags": ["API", "protection", "fairness"],
        },
    },
    "Data & Storage": {
        "SQL vs NoSQL Databases": {
            "desc": "Relational tables vs flexible document/key-value stores",
            "difficulty": "beginner",
            "tags": ["database", "schema", "flexibility"],
        },
        "CAP Theorem": {
            "desc": "Consistency, Availability, Partition Tolerance — pick two",
            "difficulty": "advanced",
            "tags": ["distributed", "theory", "tradeoffs"],
        },
        "Message Queues (Kafka, RabbitMQ)": {
            "desc": "Asynchronous communication between services via queues",
            "difficulty": "intermediate",
            "tags": ["async", "decoupling", "streaming"],
        },
        "Database Replication": {
            "desc": "Keeping copies of data across multiple database nodes",
            "difficulty": "intermediate",
            "tags": ["availability", "consistency", "failover"],
        },
        "CQRS Pattern": {
            "desc": "Separating read and write models for better performance",
            "difficulty": "advanced",
            "tags": ["pattern", "performance", "event-sourcing"],
        },
    },
    "Reliability & Resiltic": {
        "Circuit Breaker Pattern": {
            "desc": "Preventing cascading failures by stopping calls to failing services",
            "difficulty": "intermediate",
            "tags": ["resilience", "fault-tolerance", "pattern"],
        },
        "API Gateway": {
            "desc": "Single entry point that routes, authenticates, and rate-limits API calls",
            "difficulty": "beginner",
            "tags": ["routing", "auth", "microservices"],
        },
        "Distributed Consensus (Raft/Paxos)": {
            "desc": "How distributed nodes agree on a single value",
            "difficulty": "advanced",
            "tags": ["consensus", "leader-election", "theory"],
        },
        "Idempotency in APIs": {
            "desc": "Ensuring repeated API calls produce the same result",
            "difficulty": "intermediate",
            "tags": ["API", "safety", "retry"],
        },
        "CDN (Content Delivery Network)": {
            "desc": "Serving static content from geographically distributed edge servers",
            "difficulty": "beginner",
            "tags": ["performance", "latency", "caching"],
        },
    },
}


# ─────────────────────────────────────────────
# Prompt Templates (specialized per section)
# ─────────────────────────────────────────────
SIMPLE_EXPLANATION_PROMPT = ChatPromptTemplate.from_template(
    """You are a world-class system design instructor known for making complex topics crystal clear.

Explain "{topic}" in SIMPLE terms.

Rules:
- Start with a one-line definition (bold it)
- Then explain HOW it works in 3-4 short paragraphs
- Use simple language — a junior developer should understand
- Include a concrete example (e.g., "When Netflix serves a movie...")
- End with: "In one sentence: ..." summary

Keep it under 200 words. No bullet points — use flowing prose."""
)

ANALOGY_PROMPT = ChatPromptTemplate.from_template(
    """You are a creative tech educator who explains system design using everyday analogies.

Create a REAL-WORLD ANALOGY for "{topic}".

Rules:
- Pick a relatable scenario (restaurant, hospital, postal service, airport, etc.)
- Map EACH technical component to something in the analogy
- Show how the analogy breaks down or has limits (1 sentence)
- Make it memorable — something an interviewer would smile at

Format:
🎯 **The Analogy**: [One-line hook]
Then 3-4 paragraphs explaining the mapping.
⚠️ **Where it breaks down**: [One sentence]

Keep it under 180 words."""
)

PROS_CONS_PROMPT = ChatPromptTemplate.from_template(
    """You are a senior architect evaluating "{topic}" for a real production system.

Give a balanced PROS and CONS analysis.

For PROS (give exactly 4):
- Each pro should be specific, not generic
- Include WHEN this pro matters most

For CONS (give exactly 4):
- Each con should be a real pain point teams face
- Include what goes wrong if you ignore it

Then add:
**Bottom Line**: One sentence on when to use it vs when NOT to.

Use this exact format:
✅ **Pros**
1. ...
2. ...
3. ...
4. ...

❌ **Cons**
1. ...
2. ...
3. ...
4. ...

**🎯 Bottom Line**: ...

Keep each point to 1-2 sentences. Total under 250 words."""
)

DIAGRAM_PROMPT = ChatPromptTemplate.from_template(
    """You are a system design visual thinker. Create an ASCII ARCHITECTURE DIAGRAM for "{topic}".

Rules:
- Use boxes (┌─┐│└─┘), arrows (→ ← ↓ ↑), and labels
- Show the KEY components and how data/requests flow
- Keep it readable (max 20 lines wide, 15 lines tall)
- Add a 2-3 line caption explaining the flow below the diagram
- Use a monospace-friendly layout

Then below the diagram, add:
**Key Components**:
- Component 1: what it does (1 sentence)
- Component 2: what it does (1 sentence)
- (list 3-5 components)

This should look like something you'd whiteboard in an interview."""
)

INTERVIEW_PROMPT = ChatPromptTemplate.from_template(
    """You are a FAANG system design interviewer. Generate interview content for "{topic}".

Generate exactly 5 interview questions, progressing from basic → advanced:

For each question provide:
- **Q**: The question
- **What they're testing**: (1 line — what skill this evaluates)
- **Strong answer**: (3-4 sentences — what a great candidate would say)
- **Red flag**: (1 sentence — what a weak answer sounds like)

Questions should cover:
1. Basic understanding
2. Real-world application
3. Tradeoffs and alternatives
4. Failure handling
5. Scale / production concerns

Keep total under 400 words."""
)

TRADEOFF_PROMPT = ChatPromptTemplate.from_template(
    """You are a principal engineer making architecture decisions. For "{topic}":

Provide a TRADEOFF ANALYSIS comparing it against its main alternatives.

Format:
**"{topic}" vs [Alternative 1]**
| Dimension | {topic_short} | Alternative |
|---|---|---|
| (5-6 rows covering: complexity, scalability, cost, team size, latency, consistency) |

**When to choose "{topic}"**: (2-3 specific scenarios)
**When to AVOID it**: (2-3 specific scenarios)
**Real-world examples**:
- Companies using {topic}: (name 2-3)
- Companies using alternative: (name 2-3)

Keep it under 250 words. Be opinionated — don't sit on the fence."""
)


# ─────────────────────────────────────────────
# LLM & Chain Utilities
# ─────────────────────────────────────────────
def init_llm(api_key: str, temperature: float = 0.4):
    """Initialize Groq LLM with validation."""
    if not api_key or not api_key.strip().startswith("gsk_"):
        raise ValueError("Invalid API key format. Groq keys start with 'gsk_'.")
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=api_key.strip(),
        temperature=temperature,
        max_tokens=1200,
        request_timeout=30,
    )


def build_chain(llm, prompt):
    """Create a LangChain chain: Prompt → LLM → String Output."""
    return prompt | llm | StrOutputParser()


def invoke_with_retry(chain, inputs: dict, max_retries: int = 2) -> dict:
    """
    Invoke a LangChain chain with retry logic and error classification.

    Error handling flow:
      1. Try invoking the chain
      2. On failure, classify the error (auth / rate-limit / timeout / unknown)
      3. For retryable errors, wait with exponential backoff and retry
      4. Return structured result with success/failure info

    Returns:
        dict with keys: success, content/error, error_type, attempts
    """
    for attempt in range(max_retries + 1):
        try:
            result = chain.invoke(inputs)
            return {"success": True, "content": result, "attempts": attempt + 1}

        except Exception as e:
            err = str(e).lower()

            # ── Auth Error (non-retryable) ──
            if any(kw in err for kw in ["authentication", "api key", "401", "invalid_api_key", "unauthorized"]):
                return {
                    "success": False,
                    "error": "🔑 **Authentication Failed** — Your Groq API key is invalid or expired. "
                             "Please check it in the sidebar.",
                    "error_type": "auth",
                    "attempts": attempt + 1,
                }

            # ── Rate Limit (retryable) ──
            if any(kw in err for kw in ["rate", "429", "too many"]):
                if attempt < max_retries:
                    time.sleep(2 ** (attempt + 1))  # 2s, 4s backoff
                    continue
                return {
                    "success": False,
                    "error": "⏳ **Rate Limited** — Too many requests. Wait 30 seconds and try again.",
                    "error_type": "rate_limit",
                    "attempts": attempt + 1,
                }

            # ── Timeout (retryable) ──
            if any(kw in err for kw in ["timeout", "timed out", "deadline"]):
                if attempt < max_retries:
                    time.sleep(1)
                    continue
                return {
                    "success": False,
                    "error": "⌛ **Timeout** — The LLM took too long. Try a simpler topic or retry.",
                    "error_type": "timeout",
                    "attempts": attempt + 1,
                }

            # ── Model/Service Error (retryable once) ──
            if any(kw in err for kw in ["model", "503", "502", "service", "unavailable"]):
                if attempt < max_retries:
                    time.sleep(2)
                    continue
                return {
                    "success": False,
                    "error": "🔧 **Service Unavailable** — Groq's servers may be down. Try again in a minute.",
                    "error_type": "service",
                    "attempts": attempt + 1,
                }

            # ── Unknown Error (retry once) ──
            if attempt < max_retries:
                time.sleep(1)
                continue

            return {
                "success": False,
                "error": f"❌ **Unexpected Error** — `{str(e)[:200]}`",
                "error_type": "unknown",
                "attempts": attempt + 1,
            }

    # Should never reach here, but safety net
    return {"success": False, "error": "❌ All retries exhausted.", "error_type": "exhausted", "attempts": max_retries + 1}


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Free key → https://console.groq.com/keys",
    )

    st.markdown("---")
    st.markdown("### 🎛️ Settings")

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.1,
        help="Lower = precise & consistent, Higher = creative & varied",
    )

    sections = st.multiselect(
        "Sections to Generate",
        [
            "Simple Explanation",
            "Real-World Analogy",
            "Pros & Cons",
            "Architecture Diagram",
            "Interview Q&A",
            "Tradeoff Analysis",
        ],
        default=[
            "Simple Explanation",
            "Real-World Analogy",
            "Pros & Cons",
        ],
        help="Pick which sections the LLM should generate",
    )

    st.markdown("---")
    st.markdown("### 📊 Topic Stats")
    total_topics = sum(len(v) for v in TOPICS.values())
    st.metric("Preset Topics", total_topics)
    st.metric("Categories", len(TOPICS))

    st.markdown(
        """<div class="sidebar-tip">
        <strong>💡 Interview Tip</strong><br>
        Select <b>all 6 sections</b> to get a complete study sheet 
        you can review before your system design round.
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.caption("Built with Streamlit • LangChain • Groq (Llama 3.1)")


# ─────────────────────────────────────────────
# Hero Banner
# ─────────────────────────────────────────────
st.markdown(
    """<div class="hero-banner">
        <h1>🧩 System Design Simplifier</h1>
        <p>Break down complex architectures into simple explanations, analogies & interview-ready answers</p>
    </div>""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Topic Selection
# ─────────────────────────────────────────────
col_select, col_custom = st.columns([3, 2])

with col_select:
    # Flatten topics for dropdown
    all_topics_flat = {}
    for category, items in TOPICS.items():
        for name, info in items.items():
            all_topics_flat[f"{name}"] = {"category": category, **info}

    topic_options = ["— Select a topic —"] + list(all_topics_flat.keys()) + ["✏️ Custom topic"]
    selected = st.selectbox("Choose a System Design Topic", topic_options)

with col_custom:
    custom_topic = st.text_input(
        "Or type a custom topic",
        placeholder="e.g., GraphQL vs REST, Event Sourcing...",
        disabled=(selected != "✏️ Custom topic"),
    )

# Resolve final topic
topic_name = None
if selected and selected not in ["— Select a topic —", "✏️ Custom topic"]:
    topic_name = selected
elif selected == "✏️ Custom topic" and custom_topic.strip():
    topic_name = custom_topic.strip()

# Show topic info if preset
if topic_name and topic_name in all_topics_flat:
    info = all_topics_flat[topic_name]
    diff = info["difficulty"]
    badge_class = diff  # beginner/intermediate/advanced
    tags_html = " ".join(f'<span class="topic-chip">{t}</span>' for t in info["tags"])

    st.markdown(
        f"""<div style="margin: 0.8rem 0;">
            <span class="topic-chip" style="background:#f0f0ff; font-weight:600;">
                📂 {info['category']}
            </span>
            <span class="difficulty-badge {badge_class}">{diff.upper()}</span>
            <br><br>
            {tags_html}
            <p style="color:#6b7280; margin-top:0.6rem; font-size:0.92rem;">{info['desc']}</p>
        </div>""",
        unsafe_allow_html=True,
    )
elif topic_name:
    st.markdown(
        f'<span class="topic-chip" style="font-weight:600;">🔍 Custom: {topic_name}</span>',
        unsafe_allow_html=True,
    )

st.markdown("")

# ─────────────────────────────────────────────
# Browse All Topics (expandable)
# ─────────────────────────────────────────────
with st.expander("📚 Browse All Topics by Category"):
    for category, items in TOPICS.items():
        st.markdown(f"**{category}**")
        cols = st.columns(len(items))
        for i, (name, info) in enumerate(items.items()):
            diff = info["difficulty"]
            emoji = {"beginner": "🟢", "intermediate": "🟡", "advanced": "🔴"}[diff]
            cols[i].markdown(f"{emoji} {name}")
        st.markdown("---")


# ─────────────────────────────────────────────
# Generate Button
# ─────────────────────────────────────────────
generate = st.button(
    "⚡ Simplify This Topic",
    type="primary",
    use_container_width=True,
    disabled=(not topic_name),
)

if generate:
    # ── Validation ──
    if not api_key:
        st.markdown(
            '<div class="error-banner"><p>🔑 Enter your Groq API key in the sidebar to continue.</p></div>',
            unsafe_allow_html=True,
        )
        st.stop()

    if not sections:
        st.warning("Select at least one section to generate.")
        st.stop()

    # ── Init LLM ──
    try:
        llm = init_llm(api_key, temperature)
    except ValueError as e:
        st.markdown(
            f'<div class="error-banner"><p>{str(e)}</p></div>',
            unsafe_allow_html=True,
        )
        st.stop()

    # ── Section Config ──
    section_map = {
        "Simple Explanation":   ("📖 Simple Explanation",   SIMPLE_EXPLANATION_PROMPT,  "simple"),
        "Real-World Analogy":   ("🌍 Real-World Analogy",   ANALOGY_PROMPT,             "analogy"),
        "Pros & Cons":          ("⚖️ Pros & Cons",          PROS_CONS_PROMPT,           "proscons"),
        "Architecture Diagram": ("🏗️ Architecture Diagram", DIAGRAM_PROMPT,             "diagram"),
        "Interview Q&A":        ("🎯 Interview Q&A",        INTERVIEW_PROMPT,           "interview"),
        "Tradeoff Analysis":    ("📊 Tradeoff Analysis",    TRADEOFF_PROMPT,            "tradeoff"),
    }

    # ── Progress ──
    progress = st.progress(0)
    status = st.empty()
    total = len(sections)
    results = {}

    for idx, section_name in enumerate(sections):
        title, prompt_tmpl, css_class = section_map[section_name]
        status.text(f"⏳ Generating {title}... ({idx + 1}/{total})")

        chain = build_chain(llm, prompt_tmpl)
        result = invoke_with_retry(chain, {"topic": topic_name})
        results[section_name] = (title, css_class, result)

        progress.progress((idx + 1) / total)

    progress.empty()
    status.empty()

    # ─────────────────────────────────────────
    # Display Results
    # ─────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"## 📋 `{topic_name}` — Simplified")

    errors = 0

    for section_name in sections:
        title, css_class, result = results[section_name]

        if result["success"]:
            st.markdown(
                f'<div class="section-card {css_class}"><h3>{title}</h3></div>',
                unsafe_allow_html=True,
            )
            st.markdown(result["content"])
            if result["attempts"] > 1:
                st.caption(f"✅ Succeeded after {result['attempts']} retries")
            st.markdown("")
        else:
            errors += 1
            st.markdown(
                f'<div class="section-card {css_class}"><h3>❌ {title} — Failed</h3></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="error-banner"><p>{result["error"]}</p></div>',
                unsafe_allow_html=True,
            )
            st.caption(f"Tried {result['attempts']} time(s) · Error: {result.get('error_type', 'unknown')}")

    # ── Summary ──
    st.markdown("---")
    ok = total - errors
    if errors == 0:
        st.markdown(
            f'<div class="success-banner"><p>✅ All {total} sections generated successfully for '
            f'<strong>{topic_name}</strong>.</p></div>',
            unsafe_allow_html=True,
        )
    elif errors < total:
        st.warning(f"⚠️ {ok}/{total} sections succeeded. {errors} failed — see details above.")
    else:
        st.error("❌ All sections failed. Check your API key and internet connection.")


# ─────────────────────────────────────────────
# Architecture / Flow Diagram
# ─────────────────────────────────────────────
with st.expander("🏗️ App Architecture & Error Handling Flow"):
    st.markdown("""
    ```
    ┌─────────────────────────────────────────────────────┐
    │                   STREAMLIT UI                       │
    │  Topic Selection → Section Picker → Generate Button  │
    └──────────────────────┬──────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │              LANGCHAIN CHAIN BUILDER                  │
    │                                                       │
    │   ChatPromptTemplate  →  ChatGroq LLM  →  StrOutput  │
    │   (6 specialized         (Llama 3.1)     Parser       │
    │    prompts)                                            │
    └──────────────────────┬──────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │              ERROR HANDLER (invoke_with_retry)        │
    │                                                       │
    │   ┌──────────┐    ┌──────────┐    ┌──────────┐       │
    │   │  Auth     │    │  Rate    │    │ Timeout  │       │
    │   │  Error    │    │  Limit   │    │  Error   │       │
    │   │  401     │    │  429     │    │  30s     │       │
    │   │ STOP ✋   │    │ RETRY ↻  │    │ RETRY ↻  │       │
    │   │          │    │ backoff  │    │ 1s wait  │       │
    │   └──────────┘    └──────────┘    └──────────┘       │
    │                                                       │
    │   Max retries: 2  │  Backoff: 2^n seconds            │
    └──────────────────────┬──────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │              STRUCTURED RESPONSE                      │
    │   {success: bool, content/error, attempts, type}     │
    └─────────────────────────────────────────────────────┘
    ```

    **Error Classification Logic:**
    | Error Type | Detection Keywords | Retryable? | Strategy |
    |---|---|---|---|
    | Auth (401) | `authentication`, `api key`, `401` | ❌ No | Stop immediately |
    | Rate Limit (429) | `rate`, `429`, `too many` | ✅ Yes | Exponential backoff |
    | Timeout | `timeout`, `timed out` | ✅ Yes | Retry after 1s |
    | Service Down | `503`, `502`, `unavailable` | ✅ Yes | Retry after 2s |
    | Unknown | Catch-all | ✅ Once | Retry once, then fail |
    """)
