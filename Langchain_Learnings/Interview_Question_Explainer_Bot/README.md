# 🎯 Interview Question Explainer Bot

A **Streamlit + LangChain** app that helps freshers and junior developers understand tech interview questions with clear explanations, real-world examples, and key takeaways.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-green)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)

---

## 🚀 What It Does

Enter any interview question like **"What is API Gateway?"** and get:

| Section | Description |
|---------|-------------|
| 📖 **Definition** | Simple, jargon-free explanation |
| 🌍 **Real-World Example** | Concrete analogy that makes it click |
| ⚡ **3 Key Points** | Crisp, memorable interview-ready bullets |
| 💬 **Sample Answer** | A model answer to adapt in interviews |

---

## 🏗️ Architecture

```
User Question → Input Validation → Prompt Template → LLM (Groq) → Output Parser → Structured Response
                     ↓                                    ↓
               Error Message                     Retry (up to 2x)
```

### Key Design Patterns

- **Prompt Engineering** — Structured prompt with role, format, and rules for consistent output
- **LangChain Chain** — `Prompt | LLM | StrOutputParser` pipeline using LCEL
- **Error Handling** — Input validation → chain creation errors → LLM invocation with retry + backoff
- **Session State** — Question history preserved across interactions

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (custom CSS theming)
- **LLM Orchestration**: LangChain Core + LangChain Groq
- **LLM Provider**: Groq (free tier available)
- **Models Supported**: Llama 3.1, Llama 3, Gemma 2, Mixtral

---

## 📦 Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/interview-explainer-bot.git
cd interview-explainer-bot
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

The app opens at `http://localhost:8501`. Enter your API key in the sidebar and start asking questions!

---

## 📁 Project Structure

```
interview-explainer-bot/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

---

## 🔑 Features Demonstrated

| Concept | Implementation |
|---------|---------------|
| **Prompt Engineering** | Structured prompt with role, format rules, and constraints |
| **LCEL Chain** | `ChatPromptTemplate \| ChatGroq \| StrOutputParser` |
| **Error Handling** | 3-layer: input validation → setup errors → invocation retry |
| **Structured Output** | Consistent markdown sections via prompt instructions |
| **Teaching AI Behavior** | System role as "interview coach" with tone/length rules |
| **Session Management** | Question history with `st.session_state` |
| **UI/UX** | Custom CSS, example chips, sidebar config |

---

## 🧪 Example Questions to Try

- What is API Gateway?
- Explain REST vs GraphQL
- What is Docker?
- What is CI/CD pipeline?
- Explain microservices architecture
- What is OAuth 2.0?
- What is the difference between SQL and NoSQL?
- Explain event-driven architecture

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
