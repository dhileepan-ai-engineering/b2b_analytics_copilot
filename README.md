# B2B Analytics Copilot 🚀

An enterprise-grade, asynchronous **Agentic AI Copilot** engineered to ingest unstructured B2B retail queries, automatically resolve domain-specific terminology constraints locally, and intelligently execute dynamic multi-agent workflows.

Built using **Python 3.13**, the **OpenAI Python SDK Wrapper**, and **Groq's Llama-3-powered inference cloud**, this project demonstrates how to bridge production software engineering practices (asynchronous loops, modular design, deterministic testing) with modern Generative AI orchestration patterns.

---

## 🏗️ System Architecture & Workflow

The framework is built around a non-linear pipeline designed to optimize latency, context accuracy, and system observability:

```text
  [Raw User Query]
         │
         ▼
 ┌──────────────────────────────┐
 │  Semantic Glossary Pipeline  │ ──> (Scans config/glossary.json & inflates 
 └──────────────────────────────┘      acronyms like MDF & VCM locally)
         │
         ▼
 ┌──────────────────────────────┐
 │   Intent Router Agent Node   │ ──> (Analyzes intent using llama-3.3-70b-versatile)
 └──────────────────────────────┘
         │
         ├─────── Validated As: STRATEGIC_ANALYTICS ──────┐
         │                                                ▼
         │                                 ┌──────────────────────────────┐
         │                                 │   Analytics Execution Agent  │
         │                                 └──────────────────────────────┘
         │                                                │
         └─────── Validated As: DATA_TUTOR ────────┐      │
                                                   ▼      ▼
                                   ┌──────────────────────────────┐
                                   │  Data Tutor Execution Agent  │
                                   └──────────────────────────────┘
                                                   │
                                                   ▼
                                      [Structured Console Output]
                                      [JSON Telemetry Audit Logs]
