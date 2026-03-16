# Setup Instructions

## 1. Prerequisites

- Python 3.9+ installed.
- Ollama installed and configured on your machine.[web:1]
- VS Code installed.

## 2. Install Ollama and pull model

1. Download and install Ollama from the official website.[web:1]
2. Open a terminal (or VS Code terminal) and run:

```bash
ollama --version
ollama pull llama3.2:3b

3. Clone repo and open in VS Code
git clone <YOUR_REPO_URL>.git
cd <YOUR_REPO_FOLDER>
code .

4. Create and activate virtual environment
In VS Code terminal:
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Linux/macOS
# source venv/bin/activate

Install Python dependencies:
pip install requests datasets

5. Run the chatbot
Ensure the Ollama app/service is running.

In VS Code terminal (with venv active):
python chatbot.py


After completion, check eval/results.md to see the logged responses.

Manually fill in the scoring columns for each row.


## 5. `README.md` – summary for the project

Basic, VS‑Code‑oriented version:

```markdown
# Offline Customer Support Chatbot (Ollama + Llama 3.2 3B)

This project implements an offline customer support chatbot for a fictional e-commerce store **Chic Boutique** using the local Ollama server and the `llama3.2:3b` model.[web:1][web:7]  
It compares **zero-shot** vs **one-shot** prompting on 20 adapted customer queries.

## Features

- Runs entirely on your local machine using Ollama's REST API at `http://localhost:11434`.[web:1]
- Uses `llama3.2:3b`, a small, efficient LLM suitable for consumer hardware.[web:7]
- Evaluates zero-shot vs one-shot prompts with manual scoring for:
  - Relevance
  - Coherence
  - Helpfulness

## Project Structure

```text
.
├── prompts/
│   ├── zero_shot_template.txt
│   └── one_shot_template.txt
├── eval/
│   └── results.md
├── chatbot.py
├── setup.md
├── report.md
└── README.md
└── README.md

How it works
chatbot.py loads the two prompt templates.

It iterates through 20 e-commerce customer queries.

For each query, it:

Builds a zero-shot prompt and calls http://localhost:11434/api/generate with model llama3.2:3b.[web:1][web:17]

Builds a one-shot prompt and calls the same endpoint.

Logs both responses into eval/results.md as a markdown table.

You then manually score each response (Relevance, Coherence, Helpfulness) directly in the table.

For environment setup and running instructions, see setup.md.


***

## 6. `report.md` – skeleton for your analysis

You will fill in actual numbers after scoring.

```markdown
# Report: Zero-Shot vs One-Shot Prompting

## 1. Introduction

This project evaluates the feasibility of using a local LLM (Llama 3.2 3B via Ollama) to handle e-commerce customer support queries offline.[web:1][web:7]  
We compare zero-shot and one-shot prompting using 20 adapted customer queries.

## 2. Methodology

- **Queries**: 20 queries adapted from realistic technical support conversations (Ubuntu Dialogue Corpus) into e-commerce scenarios.[web:16]
- **Model**: `llama3.2:3b` served locally by Ollama's `/api/generate` endpoint.[web:1][web:17]
- **Prompting methods**:
  - Zero-shot: role + query only.
  - One-shot: role + one example QA + query.
- **Scoring rubric** (1–5 each):
  - Relevance
  - Coherence
  - Helpfulness

All responses and scores are logged in `eval/results.md`.

## 3. Results & Analysis

### 3.1 Average scores

Summarize average scores after you score:

- Zero-shot:
  - Relevance: X.X
  - Coherence: X.X
  - Helpfulness: X.X
- One-shot:
  - Relevance: Y.Y
  - Coherence: Y.Y
  - Helpfulness: Y.Y

### 3.2 Observations

Describe patterns you observed, e.g.:

- One-shot often produced more structured, policy-like answers.
- Zero-shot sometimes missed context or gave generic replies.
- Any cases where zero-shot did better or where both struggled.

Include a few brief examples (paraphrased) from `eval/results.md` to support your points.

## 4. Conclusion & Limitations

- **Suitability**: Llama 3.2 3B is usable for a simple FAQ-style support assistant, especially with a one-shot example.[web:7]
- **Limitations**:
  - No real back-end integration (no actual order lookup).
  - Occasional hallucinations or overconfident statements.
  - CPU latency for larger prompts.
- **Future work**:
  - Add retrieval from real policy docs.
  - Experiment with more examples or other models supported by Ollama.[web:11][web:13]


7. Running from VS Code (step‑by‑step)
Open VS Code → File > Open Folder → select your project folder.

Open the built‑in terminal: Ctrl+`.

Create/activate venv and install deps:
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# Linux/macOS
# source venv/bin/activate

pip install requests datasets


Make sure Ollama is running and the model is pulled:
ollama pull llama3.2:3b


Run the script:
python chatbot.py

-------------------------END-------------------------------------------------------------