# 🧩 System Design Simplifier

A GenAI-powered Streamlit app that breaks down complex system design concepts into **simple explanations**, **real-world analogies**, **pros/cons**, **architecture diagrams**, **interview Q&A**, and **tradeoff analysis** — built with **LangChain + Groq (Llama 3.1)**.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-Core-green)
![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.1-orange)

---

## 🎯 What It Does

Select any system design topic → get a multi-section breakdown:

| Section | What You Get |
|---|---|
| 📖 **Simple Explanation** | Plain-English breakdown with concrete examples |
| 🌍 **Real-World Analogy** | Memorable everyday analogy (restaurant, airport, etc.) |
| ⚖️ **Pros & Cons** | 4 pros + 4 cons with specific context |
| 🏗️ **Architecture Diagram** | ASCII whiteboard diagram with component labels |
| 🎯 **Interview Q&A** | 5 questions (basic→advanced) with strong answers & red flags |
| 📊 **Tradeoff Analysis** | Comparison table vs alternatives with real-world examples |

---

## 📚 20+ Preset Topics Across 4 Categories

| Architecture Patterns | Scalability & Performance | Data & Storage | Reliability |
|---|---|---|---|
| Microservices | Load Balancing | SQL vs NoSQL | Circuit Breaker |
| Monolithic | Database Sharding | CAP Theorem | API Gateway |
| Event-Driven | Caching Strategies | Message Queues | Distributed Consensus |
| Serverless | Horizontal vs Vertical Scaling | DB Replication | Idempotency |
| SOA | Rate Limiting | CQRS Pattern | CDN |

Plus **custom topic input** — type anything like "GraphQL vs REST" or "Event Sourcing".

---

## 🏗️ Architecture & LangChain Flow

```
User selects topic + sections
         │
         ▼
┌──────────────────────────┐
│     Streamlit Frontend    │
│  Topic picker + Settings  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   LangChain Chain Builder │
│                            │
│  ChatPromptTemplate (x6)   │
│  → ChatGroq (Llama 3.1)   │
│  → StrOutputParser         │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Error Handler            │
│   invoke_with_retry()      │
│                            │
│  Auth error → STOP         │
│  Rate limit → Backoff 2^n  │
│  Timeout → Retry (1s)      │
│  Service down → Retry (2s) │
│  Unknown → Retry once      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Structured Result         │
│  {success, content, type}  │
└──────────────────────────┘
```

### Error Handling Logic

| Error Type | Detection | Retryable? | Strategy |
|---|---|---|---|
| Auth (401) | `api key`, `401` keywords | ❌ No | Stop immediately, show fix |
| Rate Limit (429) | `rate`, `429` keywords | ✅ Yes | Exponential backoff (2s, 4s) |
| Timeout | `timeout` keyword | ✅ Yes | Retry after 1s (max 2) |
| Service Down | `503`, `502` keywords | ✅ Yes | Retry after 2s |
| Unknown | Catch-all | ✅ Once | Retry once then fail gracefully |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/<your-username>/system-design-simplifier.git
cd system-design-simplifier
pip install -r requirements.txt
```

### 2. Get a Free Groq API Key

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up / log in
3. Create a new API key (starts with `gsk_...`)

### 3. Run

```bash
streamlit run app.py
```

Open `http://localhost:8501` → paste API key in sidebar → pick a topic → click **Simplify This Topic**.

---

## 📁 Project Structure

```
system-design-simplifier/
├── app.py               # Main Streamlit + LangChain application
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
└── README.md            # Documentation
```

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit (custom CSS theme) |
| **LLM Orchestration** | LangChain Core (prompts, chains, parsers) |
| **LLM Provider** | Groq — Llama 3.1 8B Instant |
| **Error Handling** | Custom retry with exponential backoff |
| **Output Parsing** | LangChain StrOutputParser |

---

## 🎓 Why This Matters for Interviews

- **Senior dev rounds** → Use "Simple Explanation" + "Pros/Cons" to structure your answer
- **Architecture rounds** → Use "Architecture Diagram" + "Tradeoff Analysis" for whiteboard prep
- **Behavioral/depth** → Use "Interview Q&A" to practice common follow-ups

---

## 📄 License

MIT License — free for personal & commercial use.
