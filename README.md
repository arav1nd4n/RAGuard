# 🛡️ RAGuard

> **A command-line AI system for Retrieval-Augmented Generation (RAG) with built-in hallucination detection.**  
> Powered by OpenRouter’s free 🔓 [DeepSeek-R1 70B](https://openrouter.ai/models/deepseek/deepseek-r1) model.

---

## 🚀 What is RAGuard?

RAGuard is a focused, minimalistic AI pipeline that:

1. **Retrieves answers from provided documents** using semantic relevance.
2. **Verifies those answers for hallucinations** using an LLM-based verifier.
3. **Flags unsupported content**, helping you trust what your AI says.

It’s optimized for developers and interviewers who want to see **real-world AI reliability in action**.

---

## 🗂️ Project Structure

```
raguard/
├── guardrag.py           # Main script (RAG + verifier logic)
├── config.py             # Store your OpenRouter API key
├── requirements.sh       # Quick installer
├── requirements.txt      # Python package list
├── sample_input.json     # Sample docs & question
└── README.md             # This file
```

> 🔁 You can rename `guardrag.py` to `raguard.py` if you prefer — same logic, new name.

---

## ⚙️ Setup Instructions

> ✅ Requires **Python 3.7+**

1. **Clone the project**
```bash
git clone https://github.com/yourusername/raguard.git
cd raguard
```

2. **Install dependencies**
```bash
bash requirements.sh
```

3. **Get your OpenRouter API key**  
   - Go to: [https://openrouter.ai](https://openrouter.ai)
   - Sign in, generate a free key
   - Paste it into `config.py`:
```python
# config.py
OPENROUTER_API_KEY = "your-api-key-here"
```

---

## 🧪 How to Use

1. **Prepare input file**
Create or edit `sample_input.json` like this:

```json
{
  "question": "What is the capital of France and what iconic structure is there?",
  "documents": [
    "The capital of France is Paris.",
    "France is a country in Europe known for its history and cuisine."
  ]
}
```

2. **Run the script**
```bash
python guardrag.py sample_input.json
```

---

## 🧠 How RAGuard Works

| Step | What Happens |
|------|--------------|
| 🧲 Retrieval | Uses sentence embeddings to select top relevant documents |
| 💬 RAG Answer | Sends context + question to DeepSeek-R1 |
| 🕵️ Verifier Agent | Sends answer back to DeepSeek and asks it to check for unsupported claims |
| ⚠️ Output | Returns the full answer and flags hallucinations if found |

---

## ✅ Sample Output

```
Original Answer:
The capital of France is Paris. An iconic structure found there is the Eiffel Tower.

⚠️ Hallucinations flagged:
- "Eiffel Tower" is not supported by the provided context.
```

💡 If your documents had mentioned "Eiffel Tower", it would pass cleanly.

---

## 🛠️ Tech Stack

- 🔗 **OpenRouter API** with DeepSeek-R1 (free tier)
- 🧠 **SentenceTransformers** for document similarity
- 🐍 **Python** — no extra framework, pure and fast
- ✅ Runs on CPU — no GPU needed

---

## 📌 Use Cases

- ✅ AI QA systems with hallucination control
- ✅ Prototypes for enterprise RAG flows
- ✅ Technical interviews and portfolio projects

---

## 📎 Future Improvements

- Add CLI options: `--top-k`, `--strict`, `--log-json`
- Integrate with n8n for UI-based chaining
- Add citation-style context markup

---

## 🎯 Why RAGuard Exists

> Built to **solve flaws in Botminds v25’s RAG flow**, RAGuard introduces a simple yet powerful verification layer that catches hallucinations before they cause damage.

If you're building AI systems that make decisions from documents — **you need RAGuard**.

---

## 📄 License

MIT — clone it, fork it, deploy it.

