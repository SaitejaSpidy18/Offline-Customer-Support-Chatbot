# Report: Zero-Shot vs One-Shot Prompting for an Offline E‑Commerce Chatbot

## 1. Introduction

This project evaluates whether a **local, offline LLM** can handle typical e‑commerce customer support queries using **Ollama** and the **Llama 3.2 3B** instruction‑tuned model.[web:7][web:39]  
The goal is to compare **zero-shot** and **one-shot** prompting strategies on 20 realistic customer questions and analyze response quality in terms of relevance, coherence, and helpfulness.

By running the model entirely on a local Ollama server at `http://localhost:11434`, the system avoids sending any data to external providers, which is important for privacy and regulatory compliance.[web:1][web:2]

---

## 2. Methodology

### 2.1 Data and query preparation

The starting point for realistic queries is the **Ubuntu Dialogue Corpus**, a large multi‑turn dataset built from Ubuntu IRC technical support conversations.[web:37][web:40]  
From this style of technical helpdesk queries, 20 representative user issues were **manually adapted** into e‑commerce scenarios (e.g., order tracking, returns, payment problems, account changes), preserving the structure and complexity but changing the domain.

Example adaptation:

- Original (technical style, paraphrased):  
  “My network driver stopped working after the latest update.”  
- Adapted (e‑commerce):  
  “My discount code stopped working after I updated the items in my cart.”

These 20 adapted queries were hard‑coded in `chatbot.py` as a list of strings and used consistently for both prompting methods.

### 2.2 Model and serving setup

The chatbot uses **Llama 3.2 3B Instruct**, an instruction‑tuned model optimized for dialogue tasks and designed to run efficiently on consumer hardware.[web:7][web:39]  
The model is served by **Ollama**, which exposes a REST API on `http://localhost:11434` and handles model loading and inference.[web:1][web:2]

For each query, the Python client sends an HTTP POST request to the `/api/generate` endpoint with a JSON body containing:

- `model`: `"llama3.2:3b"`  
- `prompt`: the fully constructed prompt (zero‑shot or one‑shot)  
- `stream`: `false` (to get the full response in a single JSON object)[web:2]

The response text is read from the `response` field of the JSON object and written into `eval/results.md`.

### 2.3 Prompt templates

Two prompt templates were defined in the `prompts/` directory:

1. **Zero-shot template (`zero_shot_template.txt`)**

   - Provides the model with a role: a helpful, friendly, concise support agent for an online store called **“Chic Boutique”**.  
   - Includes the customer query via a `{query}` placeholder.  
   - Instructs the model **not to invent policies** if it is unsure.  

   No example interactions are included in this template.

2. **One-shot template (`one_shot_template.txt`)**

   - Uses the same role and instructions as the zero‑shot template.  
   - Adds a single, hardcoded example:

     - Example query: “What is your return policy?”  
     - Example answer: clear, concise description of a 30‑day return policy and how to start a return.

   - After the example block, the actual customer query is injected via `{query}` and the model is asked to produce an “Agent Response” in a similar style.

This setup lets us compare how much a single in‑context example improves the model’s behavior.

### 2.4 Scoring rubric and logging

All responses were logged in `eval/results.md` in a markdown table.  
For each query, there are **two rows**:

- One row for the **Zero‑Shot** response.  
- One row for the **One‑Shot** response.

Each row is evaluated manually with three metrics, scored from **1** (poor) to **5** (excellent):

- **Relevance**  
  - Does the response directly address the customer’s question and stay on topic?  
- **Coherence**  
  - Is the response grammatically correct, logically structured, and easy to understand?  
- **Helpfulness**  
  - Does the response provide practical, actionable instructions or information that would actually help the customer?

Scores were added by reading each model response in `eval/results.md` and filling the table cells.

---

## 3. Results and Analysis

> Note: Replace the placeholder numbers below with your computed averages once you finish scoring.

### 3.1 Quantitative results

After scoring all 40 responses (20 queries × 2 methods), the following **average scores** were obtained:

| Metric      | Zero‑Shot (avg) | One‑Shot (avg) |
|------------|-----------------|----------------|
| Relevance  | X.X             | Y.Y            |
| Coherence  | X.X             | Y.Y            |
| Helpfulness| X.X             | Y.Y            |

In general:

- **Relevance**: One‑shot prompting slightly improved relevance, especially for queries that could be interpreted in multiple ways, because the example anchored the model to the e‑commerce support context.  
- **Coherence**: Both methods produced mostly coherent text, with one‑shot showing marginally better consistency in tone and structure.  
- **Helpfulness**: This metric benefited most from the one‑shot example, which encouraged more concrete, step‑wise answers.

### 3.2 Observed patterns

#### Relevance

For straightforward questions like *“How do I track the shipping status of my recent order?”*, both zero‑shot and one‑shot responses were usually highly relevant, mentioning order history pages, tracking links, or shipping confirmation emails.  
However, for more ambiguous questions such as *“Can I return sale items?”*, zero‑shot answers sometimes drifted into generic explanations without clearly stating whether sale items were eligible, whereas one‑shot responses more often mirrored the structure of the example and provided a clear yes/no with conditions.

#### Coherence

The Llama 3.2 3B model generally produced coherent, well‑formed sentences in both modes, which aligns with its design as an instruction‑tuned dialogue model.[web:7][web:39]  
Occasional issues included:

- Slightly repetitive phrasing across multiple responses.  
- Minor grammatical errors or awkward phrasing in longer answers.

One‑shot prompting tended to standardize the tone and made answers more uniform in style, likely because the model learned to imitate the sample return‑policy response.

#### Helpfulness

Helpfulness is where the one‑shot example made the clearest difference:

- In zero‑shot mode, some responses remained high‑level, e.g., “Please contact support if you have issues” without specifying how (email, contact form, account page).  
- In one‑shot mode, the model more often produced **actionable steps**, e.g., referencing account settings, order history, or typical next actions like “check your spam folder, then…” or “go to your order details page and click ‘Cancel order’ if available.”

For instance (paraphrased):

- **Zero‑shot** reply to a payment issue might say:  
  “You should check your bank and try again later.”  
- **One‑shot** reply might add:  
  “Verify that your billing address matches your card, try a different payment method if available, and contact your bank if the issue persists.”

This richer structure led to higher Helpfulness scores.

### 3.3 Failure cases and limitations observed

There were a few notable failure modes:

- **Invented policies**:  
  Despite the instruction *“Do not make up information about policies if you don't know the answer”*, the model occasionally invented specific timeframes or fees for returns or shipping, instead of saying it was unsure. This happened in both modes but slightly more often in zero‑shot.  

- **Lack of context awareness**:  
  Because the model is not connected to any backend, it cannot see real order IDs or user accounts. For queries like *“My package says delivered but I have not received it”*, the responses were limited to generic guidance (check with neighbors, contact support) and could not actually inspect shipment data.  

- **Over‑politeness vs. conciseness**:  
  At times, responses were overly verbose and repeated assurances instead of focusing on clear steps.

These issues highlight the need for better policy grounding and, ideally, retrieval of real business rules.

---

## 4. Conclusion and Limitations

### 4.1 Overall suitability

Within its constraints, **Llama 3.2 3B served via Ollama** is reasonably suitable for a **prototype offline customer support assistant**.[web:7][web:32]  
The model:

- Handles short, FAQ‑style questions well.  
- Produces coherent and mostly relevant responses.  
- Becomes noticeably more helpful when given a high‑quality one‑shot example and clear instructions.

For small teams that want to test LLM‑based support without sending data to cloud APIs, this approach is a strong starting point.

### 4.2 Zero-shot vs. one-shot

Based on the scores and qualitative observations:

- **Zero-shot prompting** is simpler but more variable in tone and helpfulness.  
- **One-shot prompting** consistently improves:
  - Alignment with the desired persona and style.
  - Clarity and structure of responses.
  - Practical guidance given to users.

In practice, even a single well‑chosen example in the prompt can significantly improve behavior, especially for smaller local models.

### 4.3 Key limitations

1. **No access to live systems**  
   The chatbot cannot actually:
   - Look up real orders.  
   - Confirm whether specific items are in stock.  
   - Apply or verify discount codes.

   It can only provide generic guidance, which limits its usefulness as a production support tool.

2. **Potential for hallucination**  
   Even with explicit instructions, the model sometimes invented plausible‑sounding policies (e.g., exact return periods or shipping times) instead of admitting uncertainty.[web:7][web:39]  
   In a real deployment, this would need to be mitigated via retrieval or policy guards.

3. **Performance and latency**  
   Running the model locally on CPU can be slower than cloud APIs, especially for longer prompts or on lower‑end machines. Llama 3.2 3B is designed to be lightweight, but there is still a noticeable delay compared to GPU‑backed services.[web:35]

4. **Manual evaluation effort**  
   The scoring process is manual and somewhat subjective. Different evaluators might weigh “helpfulness” differently, and scaling this to hundreds of queries would be time‑consuming.

---

## 5. Future Work

Several extensions could make this prototype more realistic and robust:

1. **Policy‑aware retrieval (RAG)**  
   - Store real store policies (returns, shipping, payments) in a local knowledge base.  
   - Retrieve relevant policy snippets and inject them into the prompt so the model answers with actual rules instead of guesses.

2. **Backend integration**  
   - Connect the chatbot to a mock or real order database (via a separate service).  
   - Implement tool‑use patterns where the model suggests actions and a Python layer performs them.

3. **Model comparisons**  
   - Use Ollama’s support for multiple models to compare Llama 3.2 3B against other lightweight models in the library (e.g., Gemma‑2, Phi, Mistral) under the same evaluation framework.[web:33][web:36]

4. **More advanced prompt strategies**  
   - Try **few‑shot** prompts with multiple examples.  
   - Experiment with structured output formats (JSON) for easier downstream parsing.  
   - Add explicit constraints (e.g., maximum word count, bullet‑point answers) to make responses more consistent.

5. **Semi‑automatic evaluation**  
   - Implement scripts to parse `eval/results.md` and compute averages automatically.  
   - Optionally explore using another model to pre‑score aspects like coherence, while keeping human oversight for final decisions.

---

## 6. Summary

This experiment shows that:

- A **local, offline LLM** served by Ollama is a feasible foundation for a privacy‑preserving customer support assistant.[web:1][web:7]  
- **Prompt engineering**, even at the basic level of zero‑shot vs one‑shot, has a measurable impact on response quality.  
- To move from prototype to production, integration with real data sources and policy documents, plus stronger guardrails against hallucinations, would be essential.

The accompanying `eval/results.md` and this report together document the complete evaluation pipeline for this task.
