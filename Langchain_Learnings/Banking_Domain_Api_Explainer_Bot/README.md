# 🏦 Banking Domain API Explainer

A GenAI-powered Streamlit application that explains banking APIs with business context, technical details, failure scenarios, and interview prep — built with **LangChain** and **Groq (Llama 3)**.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-Core-green)
![Groq](https://img.shields.io/badge/LLM-Groq%20Llama3-orange)

---

## 🎯 What It Does

Enter any banking API name → get a structured, multi-section explanation:

| Section | What You Get |
|---|---|
| 📊 **Business Explanation** | Plain-English breakdown, business value, who uses it |
| ⚙️ **Technical Explanation** | Endpoint design, internal flow, HTTP codes, integration patterns |
| 🔴 **Failure Scenarios** | 3 realistic production failures with root cause & mitigation |
| 🎯 **Interview Q&A** | 5 graded interview questions with model answers |

### Preset Banking APIs Included

- Payment Retry API
- Fund Transfer API (NEFT/RTGS/IMPS)
- KYC Verification API
- Card Tokenization API
- Fraud Detection API
- UPI Payment API
- ...and 6 more, plus custom input

---

## 🏗️ Architecture

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
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Error Handler       │
│  - Auth check        │
│  - Rate limit retry  │
│  - Timeout retry     │
│  - Exponential backoff│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Groq LLM (Llama 3) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  StrOutputParser →   │
│  Formatted Response  │
└─────────────────────┘
```

**Key design decisions:**
- **Retry with exponential backoff** — handles transient Groq rate limits
- **Error classification** — auth vs rate-limit vs timeout vs unknown
- **Modular prompt chains** — each section has its own optimized prompt
- **Configurable** — temperature slider + section picker

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/<your-username>/banking-api-explainer.git
cd banking-api-explainer
pip install -r requirements.txt
```

### 2. Get a Groq API Key (Free)

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up / log in
3. Create a new API key
4. Copy the key (starts with `gsk_...`)

### 3. Run

```bash
streamlit run app.py
```

Open `http://localhost:8501` → paste your API key in the sidebar → select an API → click **Explain API**.

---

## 📁 Project Structure

```
banking-api-explainer/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## 🛡️ Error Handling

The app handles real-world LLM failures gracefully:

| Error | Detection | Response |
|---|---|---|
| Invalid API key | `401` / `authentication` in error | Immediate stop, clear message |
| Rate limit | `429` / `rate` in error | Retry with exponential backoff (up to 3 attempts) |
| Timeout | `timeout` in error | Retry up to 3 times |
| Unknown | Catch-all | Retry once, then show error details |

---

## 🧠 Tech Stack

- **Frontend**: Streamlit
- **LLM Orchestration**: LangChain Core
- **LLM Provider**: Groq (Llama 3.1 8B Instant)
- **Output Parsing**: LangChain StrOutputParser
- **Error Handling**: Custom retry logic with classification

---

## 📄 License

MIT License — free for personal & commercial use.
