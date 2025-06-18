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


## ⚙️ Setup

### 1. Clone Repo

```bash
git clone https://github.com/yourname/deep-research.git
cd deep-research
````

### 2. Configure Environment

A **`.env` template is already provided.**

Update the following keys in `.env` with your actual API credentials:

* `OPENAI_KEY`
* `FIRECRAWL_KEY`

> ✅ Note: The `.env` file is already listed in not listed in `.gitignore`. Add it to keep API keys safe and prevent accidental commits.

---

## ⚙️ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install openai httpx pydantic fastapi python-dotenv
```

---

## 🧪 Run the CLI

```bash
python main.py
```

---

## 📄 License

MIT License. Free for personal and commercial use.

```

