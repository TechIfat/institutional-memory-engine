# Institutional Memory Engine (Raw SDK Orchestrator)
**Status:** Completed  
**Architect:** Ifat Noreen, Principal Agentic AI Architect (ShiftAi Systems Ltd)  

## 🏢 The Initiative
Banks do not suffer from a lack of data; they suffer from AI amnesia and compliance hallucinations. If a junior underwriter drafts a £20M commercial facility agreement but misses a strict internal risk covenant, the resulting operational waste and compliance risk is massive.

This repository demonstrates the **Evaluator-Optimiser Pattern** built entirely from scratch using the **Raw Anthropic Python SDK** (bypassing third-party frameworks like LangGraph or CrewAI). It forces two AI agents to argue in an adversarial, self-correcting loop until a drafted contract is 100% compliant with historical institutional memory.

Built specifically to demonstrate mastery of Raw API Primitives, Prompt Caching, and Forced Structured Outputs for the **Claude Certified Architect (CCA)** exam.

---

## 🏗️ Architectural Highlights

### 1. Raw API State Management (No Black Boxes)
By bypassing abstraction frameworks, this architecture utilizes a deterministic Python `while` loop to manually manage the conversation history (`messages` array). This provides complete auditability of the AI's memory state and eliminates the hidden latency/token-bloat often introduced by third-party wrappers.

### 2. FinOps via Anthropic Prompt Caching
To simulate deep "Institutional Memory," historical banking precedents are loaded into the system prompt using Anthropic's `cache_control: {"type": "ephemeral"}` directive. 
- **The Result:** The Evaluator hits the cached memory on every subsequent iteration of the review loop, dropping API context-read costs by **90%** and massively reducing Time-To-First-Token (TTFT).

### 3. The Adversarial "Maker-Checker" Loop
- **The Underwriter (Generator):** Drafts the initial loan term sheet.
- **The Evaluator (Reviewer):** Audits the draft against the cached institutional memory. If it detects a policy breach (e.g., a DSCR of 1.20x when bank policy strictly mandates 1.25x for the Retail sector), it forcefully rejects the draft and injects strict redlines back into the Underwriter's context.

### 4. Forced JSON Tool Calling (`tool_choice`)
The Evaluator is mathematically bound to a strict Pydantic JSON schema using the native `tool_choice` parameter. This entirely strips the LLM of its conversational output layer, ensuring that the Python orchestration loop receives deterministic boolean triggers (`is_compliant: false`) to manage the circuit breakers.

---

## 🚀 How to Run 

This project uses `uv` for lightning-fast dependency management.

**1. Clone and Sync**
```bash
uv sync
```

**2. Configure Environment**
Create a .env.local file in the root directory:
```Env
ANTHROPIC_API_KEY="sk-ant-your-key-here"
```
**3. Run the Orchestrator**
The script will intentionally request an under-priced retail loan to trigger the adversarial loop.
```Bash
uv run python src/orchestrator.py
```

Watch the terminal as the Evaluator catches the DSCR policy breach, rejects Draft v1, and forces the Underwriter to generate a fully compliant Draft v2 utilising the cached institutional memory.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact & Consulting

**Ifat Noreen**
*Principal Agentic AI Architect | Founder, ShiftAi Systems Ltd*

* **LinkedIn:**[linkedin.com/in/ifat-noreen](https://www.linkedin.com/in/ifat-noreen)
* **GitHub:** [@TechIfat](https://github.com/TechIfat)

