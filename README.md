# Offline Customer Support Chatbot with Ollama & Llama 3.2

This project implements an **offline customer support chatbot** for a fictional e‑commerce store called **Chic Boutique**, running entirely on a local machine using **Ollama** and the **Llama 3.2 3B** model.[web:7][web:32]  
It demonstrates how to build and evaluate a privacy‑preserving chatbot without sending any data to external APIs.

The main goal is to compare **zero-shot** and **one-shot** prompt engineering techniques for handling typical customer support queries such as order tracking, returns, discounts, and account issues.

---

## 1. Project Background

Modern e‑commerce platforms receive thousands of customer support tickets about orders, returns, discounts, and account problems. Many teams want to use Large Language Models (LLMs) to automate these interactions but face serious **data privacy** and **cost** concerns when using cloud APIs.

This project shows how to:

- Run a capable LLM **fully offline** using Ollama’s local server.[web:1][web:31]
- Build a simple Python client that talks to the model via HTTP.
- Explore how **prompt design** (zero‑shot vs one‑shot) affects response quality.
- Manually evaluate responses using a structured rubric.

Because everything runs on `http://localhost:11434`, no customer data leaves the machine.[web:1][web:31]

---

## 2. System Architecture

The architecture is intentionally simple:

1. **`chatbot.py` (Python client)**  
   - Reads 20 e‑commerce customer queries (adapted from the Ubuntu Dialogue Corpus).[web:6]  
   - Loads **zero-shot** and **one-shot** prompt templates from `prompts/`.  
   - For each query, builds two prompts and calls the local Ollama server via `/api/generate` with `model = "llama3.2:3b"`.[web:2][web:7]

2. **Ollama server (local)**  
   - Hosts and runs the `llama3.2:3b` model.[web:7][web:32]  
   - Exposes an HTTP API at `http://localhost:11434`.  
   - Receives JSON payloads and returns JSON responses with the generated text.[web:1][web:2][web:31]

3. **Evaluation log (`eval/results.md`)**  
   - For each query and prompting method, stores:
     - Query #
     - Customer query text
     - Prompting method (Zero‑Shot / One‑Shot)
     - Model response
     - Scores for Relevance, Coherence, Helpfulness

The full data flow:

1. `chatbot.py` formats a prompt and sends a POST request to `http://localhost:11434/api/generate` with `{ "model": "llama3.2:3b", "prompt": "...", "stream": false }`.[web:2][web:5]  
2. Ollama runs Llama 3.2 3B locally and generates a response.[web:7][web:32]  
3. The JSON response is parsed by `chatbot.py`.  
4. The script logs the response into `eval/results.md` in a markdown table for later manual scoring.

---

## 3. Project Structure

```text
.
├── prompts/
│   ├── zero_shot_template.txt      # Zero-shot prompt template (no examples)
│   └── one_shot_template.txt       # One-shot prompt template (one example QA)
├── eval/
│   └── results.md                  # Generated responses + manual scores
├── chatbot.py                      # Main script that talks to Ollama
├── setup.md                        # Environment setup & run instructions
├── report.md                       # Final analysis (zero-shot vs one-shot)
└── README.md                       # This file
chatbot.py
Python script that orchestrates everything:

Loads templates.

Iterates over 20 customer queries.

Calls the Ollama /api/generate endpoint.

Writes a markdown table of all responses and (initially blank) scores.

prompts/

zero_shot_template.txt: Only role + query + output instruction.

one_shot_template.txt: Same instructions plus one hardcoded example query‑response pair, then the actual query.

eval/results.md
Final log of all 20 queries × 2 prompting methods (40 rows) with manual scores.

report.md
Contains the analysis of results, average scores, and discussion of patterns.

4. Setup & Installation
For detailed step‑by‑step commands, see setup.md.
Below is the high‑level summary.

4.1 Prerequisites
Python 3.9+

Git

VS Code or any editor

Ollama installed and running on your machine[web:1][web:19]

Internet connection for initial model download

4.2 Install Ollama
Download and install Ollama for your OS using the official instructions.[web:1][web:19]

Verify installation in a terminal:

bash
ollama --version
Pull the Llama 3.2 3B model:

bash
ollama pull llama3.2:3b
This downloads and registers the model with Ollama.[web:7][web:32]

4.3 Clone repo and create virtual environment
bash
git clone <YOUR_PUBLIC_REPO_URL>.git
cd <YOUR_REPO_FOLDER>

python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Linux/macOS
# source venv/bin/activate

pip install requests datasets
requests: for HTTP calls to Ollama’s /api/generate endpoint.[web:2][web:5]

datasets: to work with the Ubuntu Dialogue Corpus when preparing queries (used during data preparation).[web:6]

5. Running the Chatbot Evaluation
Make sure the Ollama app/service is running and the model is pulled.

With your virtual environment active, run:

bash
python chatbot.py
What happens:

The script loads both prompt templates from prompts/.

It iterates through 20 e‑commerce queries adapted from the Ubuntu Dialogue Corpus.[web:6]

For each query:

Builds a zero-shot prompt and calls http://localhost:11434/api/generate.[web:2]

Builds a one-shot prompt and calls the same endpoint.

Logs both responses into eval/results.md as separate rows.

At the end, eval/results.md contains:

A scoring rubric description (Relevance, Coherence, Helpfulness).

A markdown table with 40 rows: 20 zero-shot + 20 one-shot responses.

You then manually fill in the score columns.

6. Prompt Engineering Details
6.1 Zero-shot template
prompts/zero_shot_template.txt defines the role and structure but gives no examples:

text
You are a helpful, friendly, and concise customer support agent for an online store called 'Chic Boutique'. Your goal is to assist customers with their questions. Do not make up information about policies if you don't know the answer.

Customer Query: "{query}"

Agent Response:
For each query, {query} is replaced with the actual customer question.

6.2 One-shot template
prompts/one_shot_template.txt includes one complete example to guide tone and format:

text
You are a helpful, friendly, and concise customer support agent for an online store called 'Chic Boutique'. Your goal is to assist customers with their questions. Do not make up information about policies if you don't know the answer.

--- EXAMPLE START ---
Customer Query: "What is your return policy?"
Agent Response: "We offer a 30-day return policy for all unworn items with tags still attached. You can start a return from your order history page."
--- EXAMPLE END ---

Customer Query: "{query}"

Agent Response:
This helps the model mimic the example’s style in the actual responses.

7. Data Preparation
The 20 customer queries used in this project were manually adapted from the Ubuntu Dialogue Corpus, a large dataset of technical support conversations from Ubuntu’s IRC channels.[web:6]

Example adaptation:

Original (technical):
“My wifi driver is not working after the latest update.”

Adapted (e‑commerce):
“My discount code is not working at checkout.”

This ensures the queries are realistic and diverse while being relevant to an e‑commerce support scenario.

8. Evaluation Methodology
8.1 Scoring rubric
Each response (zero-shot and one-shot) is manually evaluated according to three criteria:

Relevance (1–5)
How well does the response address the customer’s query?

Coherence (1–5)
Is the response grammatically correct and easy to understand?

Helpfulness (1–5)
Does the response provide clear, actionable guidance?

Scores are entered manually for every row in eval/results.md, resulting in 40 × 3 scores.

8.2 Aggregation
After scoring:

Compute average Relevance, Coherence, and Helpfulness for:

Zero-shot responses (20 rows).

One-shot responses (20 rows).

These averages are reported and discussed in report.md.

9. Results Summary (to be filled by you)
In report.md, you will summarize:

Average scores per metric for zero-shot and one-shot.

Observed patterns:

Did one-shot improve relevance and helpfulness?

Did zero-shot ever do surprisingly well?

Any hallucinations or invented policies?

You should provide concrete examples (brief paraphrases) from eval/results.md to support your analysis.

10. Limitations & Future Work
Limitations:

The chatbot cannot access real order databases or live inventory, so it can only simulate support, not perform actual actions.

Llama 3.2 3B, while efficient, is a relatively small model and may sometimes produce incomplete or generic responses.[web:7][web:32]

All scoring is manual and subjective; different evaluators might rate differently.

Possible extensions:

Integrate a retrieval layer (RAG) to pull real policy documents or FAQs into the prompt.

Compare multiple models (e.g., other Ollama models like Gemma, Mistral, Phi) under the same evaluation framework.[web:7][web:5][web:29]

Automate part of the evaluation with heuristics or another model (while keeping human review for final judgment).

11. How to Reproduce
Install Ollama and pull llama3.2:3b.[web:1][web:7]

Clone this repository and create a Python virtual environment.

Install dependencies: pip install requests datasets.

Run python chatbot.py.

Open eval/results.md, review responses, and fill in scores.

Review report.md for the summarized findings, or update it with your own analysis.

12. License & Credits
Model: Llama 3.2 3B served via Ollama.[web:7][web:32]

Dataset inspiration: Ubuntu Dialogue Corpus for realistic support‑style queries.[web:6]

This repo does not ship any proprietary data or secrets.

You are free to fork and extend this project for learning or experimentation.
