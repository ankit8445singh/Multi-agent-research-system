# Multi-agent-research-system

# ResearchMind

<p align="center">
  <img src="https://images.unsplash.com/photo-1526379095098-d400fd0bf935?auto=format&fit=crop&w=1200&q=80" alt="AI product experience" width="100%" />
</p>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C5C?logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Models-412991?logo=openai&logoColor=white)](https://openai.com/)
[![Tavily](https://img.shields.io/badge/Tavily-Search-00C7B7)](https://tavily.com/)

ResearchMind is a multi-agent AI research platform that turns a single user query into a structured, high-quality research report. It combines web search, document extraction, content synthesis, and quality review in one streamlined workflow.

Instead of manually browsing sources and building notes from scratch, users can ask a topic and let the system find, read, and summarize the most relevant information automatically.

## Product vision

We believe research workflows should feel fast, intelligent, and collaborative. ResearchMind helps users move from raw topic input to actionable insight in a single flow.

## How it works

```text
Topic Input
  ↓
Search Agent
  ↓
Reader Agent
  ↓
Writer Agent
  ↓
Critic Agent
```

Each step has a distinct role:

- Search Agent: discovers recent and relevant web sources
- Reader Agent: scrapes and condenses key source content
- Writer Agent: builds a clear and structured research report
- Critic Agent: reviews the report, scores it, and flags gaps

## Features

- Multi-agent research pipeline
- Real-time web search integration
- Content extraction from relevant URLs
- Dynamic report generation with structured sections
- AI review and scoring layer
- Streamlit-based user experience
- Modular architecture for future expansion

## Product benefits

- Reduces time spent on manual information gathering
- Makes research more structured and repeatable
- Speeds up early-stage analysis and synthesis
- Creates a compelling demo of AI workflow orchestration
- Demonstrates how LLM-powered systems can work with real tools

## Stack

- Python
- LangChain
- OpenAI API
- Tavily
- Streamlit
- BeautifulSoup
- Requests

## Architecture

```text
User topic
   ↓
Search tool
   ↓
AI agent
   ↓
Scraper
   ↓
Writer model
   ↓
Critic model
```

## Project structure

```text
researchmind/
├── agents.py
├── app.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── .gitignore
├── README.md
```

## Getting started

### Install

```bash
git clone https://github.com/AkarshVyas/Multi-agent-research-system.git
cd Multi-agent-research-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure API keys

```bash
touch .env
```

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Run app

```bash
streamlit run app.py
```

## Example workflow

```text
User: "What are the key trends in generative AI adoption in 2025?"
```

System flow:
- search relevant sources
- extract the most useful information
- summarize findings
- generate a structured report
- critique the final output

## Limitations

- Needs internet connectivity
- Requires valid API keys
- Best suited for research assistance, not final fact verification
- Web scraping effectiveness depends on source formatting

## Roadmap

- improve source ranking and filtering
- add citation support
- add document export options
- add session memory and history
- expand into broader research workflows

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with improvements.

## License

This project is licensed under the MIT License.

---

Built to showcase how AI workflows can move from raw information to polished output with human-like reasoning and structured execution.
