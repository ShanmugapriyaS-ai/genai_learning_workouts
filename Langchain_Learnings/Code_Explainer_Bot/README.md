# 🔬 Code Explainer for Developers

A **Streamlit + LangChain** application that explains any code snippet like a senior developer teaching a junior — with line-by-line breakdowns, real-world use cases, and common pitfalls.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-green)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)

---

## 🚀 What It Does

Paste any code snippet and get a **structured explanation**:

| Section | What You Get |
|---------|-------------|
| 🔍 **What This Code Does** | Plain-English summary of the code's purpose |
| 📝 **Line-by-Line Explanation** | Every meaningful line broken down |
| 🛠️ **When to Use This** | Real-world scenarios where this pattern applies |
| ⚡ **Key Takeaways** | 3 important things to remember |
| ⚠️ **Common Pitfalls** | Mistakes beginners make + how to avoid them |

### Example

**Input:**
```python
for i in range(5):
    print(i)
```

**Output:** A full structured breakdown covering what loops do, how `range()` works, when to use this pattern, and what to watch out for.

---

## 🏗️ Architecture

```
Code Input → Validation → Language Detection (LLM) → Explanation Prompt → LLM → Output Parser → Structured Response
                ↓                                                           ↓
          Error Message                                              Retry (2x with backoff)
```

### Key Design Patterns

| Pattern | Implementation |
|---------|---------------|
| **Prompt Engineering** | Role-based prompt with structured output format and rules |
| **Dual LLM Chains** | Chain 1: Language detection, Chain 2: Code explanation |
| **LCEL Pipeline** | `ChatPromptTemplate \| ChatGroq \| StrOutputParser` |
| **3-Layer Error Handling** | Input validation → LLM init errors → Invocation retry with backoff |
| **Dynamic Prompts** | Detail level (Beginner/Standard/Advanced) modifies prompt instructions |
| **Session History** | Past explanations stored via `st.session_state` |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (custom dark terminal-themed CSS)
- **LLM Orchestration**: LangChain Core + LangChain Groq
- **LLM Provider**: Groq (free tier available)
- **Models**: Llama 3.1 8B, Llama 3.3 70B, GPT-OSS 20B, GPT-OSS 120B

---

## 📦 Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/code-explainer-bot.git
cd code-explainer-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a Groq API Key (free)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / log in
3. Create an API key

### 4. Run the app

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`. Enter your API key in the sidebar and paste any code!

---

## 📁 Project Structure

```
code-explainer-bot/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
└── README.md            # Documentation
```

---

## ✨ Features

- **Multi-Language Support** — Auto-detects Python, JavaScript, Java, Go, Rust, SQL, and 20+ languages
- **3 Detail Levels** — Beginner-Friendly, Standard, and Advanced explanations
- **6 Quick Examples** — One-click code samples to try instantly
- **Code Stats** — Shows line count and character count before submitting
- **Explanation History** — Browse your last 10 explanations
- **Retry with Backoff** — Handles transient API failures gracefully
- **Dark Terminal Theme** — Custom CSS for a developer-focused aesthetic

---

## 🔑 Skills Demonstrated

| Skill | Where |
|-------|-------|
| Prompt Engineering | Structured prompt with role, format, rules, and dynamic detail levels |
| LLM Reasoning | Line-by-line code analysis + use case identification |
| Chain Composition | Two separate LCEL chains (detect + explain) |
| Error Handling | Input validation → init check → retry with exponential backoff |
| Developer Productivity | Paste code → get instant structured knowledge |

---

## 🧪 Code Snippets to Try

```python
# Python — List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]
```

```javascript
// JavaScript — Debounce function
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}
```

```sql
-- SQL — Window function
SELECT name, salary,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

> Built with ❤️ using Streamlit + LangChain + Groq
