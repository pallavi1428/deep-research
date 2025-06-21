# 🔍 Deep Research (Python Edition)

Deep Research is a command-line tool that automates recursive web research using SERP queries, scraping, and LLM summarization. It’s built using FastAPI, Python, and integrates with Firecrawl and OpenAI.

---

## 🧠 Features

- Iterative multi-query deep research
- Follow-up question generator
- Async Firecrawl search + markdown extraction
- Works with OpenAI, local endpoints, or Fireworks (DeepSeek R1)
- Outputs: Final answer or long-form report
- API & CLI support

---

## 📦 Requirements

- Python 3.10+
- `.env` file with API keys
- Optional: Docker + docker-compose

---

## ⚙️ Setup

1. **Clone Repo**

```bash
git clone https://github.com/yourname/deep-research.git
cd deep-research
```
2. **Update .env.template**
- Update .env.template to .env with API keys

3. **main.py and main_cli.py**