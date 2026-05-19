# 🔍 ReAct Web Search Agent

A conversational AI agent that thinks step-by-step before answering — powered by **Gemini** and **LangChain's ReAct pattern**.

```
You: What is the current gold price in euros?

Thought: I need to search for the gold price and EUR exchange rate.
Action: web_search
Action Input: gold price per ounce USD today
Observation: Gold is trading at $2,340/oz...

Thought: Now I need the USD to EUR rate.
Action: web_search
Action Input: USD to EUR exchange rate today
Observation: 1 USD = 0.92 EUR

Thought: I can calculate: 2340 × 0.92
Action: calculator
Action Input: 2340 * 0.92
Observation: 2152.8

Final Answer: Gold is currently ~€2,153 per troy ounce.
```

---

## Tools

| Tool | Description |
|---|---|
| `web_search` | Search the web via DuckDuckGo — no API key needed |
| `calculator` | Safely evaluate math expressions |
| `get_current_date` | Returns today's date |

---

## Quickstart

```bash
git clone https://github.com/yourname/react-agent.git
cd react-agent
pip install -r requirements.txt
```

Add your Google API key to a `.env` file:

```
GOOGLE_API_KEY=your_key_here
```

Run:

```bash
python agent.py
```

---

## Requirements

```
langchain
langchain-google-genai
langchain-community
duckduckgo-search
python-dotenv
```

---

## Project structure

```
├── agent.py      # ReAct loop and entry point
├── tools.py      # Tool definitions
├── prompt.py     # System prompt template
└── .env          # API key (not committed)
```

---

## License

MIT