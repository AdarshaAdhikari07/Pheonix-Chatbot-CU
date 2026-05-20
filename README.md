# 🦅 Phoenix: AI Student Ambassador for Coventry University

Phoenix is an enterprise-grade B2B SaaS Retrieval-Augmented Generation (RAG) agent designed to automate prospective student onboarding, instant query resolution, and lead generation. Built specifically as a proof-of-concept targeting higher education institutions like Coventry University, Phoenix serves as a highly scalable, 24/7 digital twin of student ambassadors, positioning itself as an automated replacement for peer-to-peer chat architectures like Unibuddy.

---

## 🚀 Core Architectural Features

* **Semantic RAG Framework**: Integrated with **ChromaDB** vector space and local text embeddings, allowing the agent to perform conceptual intent mapping and resolve severe student typos (e.g., matching "viza guidelines" to verified compliance records).
* **Zero-Hallucination Guardrails**: Features a strict validation architecture. If a critical university policy or visa regulation is missing from the local knowledge base, the agent smoothly degrades to verified fallback endpoints instead of inventing compliance parameters.
* **CRM Lead Capture Interface**: Optimized for institutional ROI. Converts anonymous prospective web traffic into high-intent student leads via an embedded sidebar CRM widget that tracks enrollment intent.
* **State-Gated Request Loop**: Runs on the state-of-the-art **Gemini 2.5 Flash** engine utilizing custom session-state gating flags (`st.session_state.run_generation`) to enforce ultra-low latency while completely protecting API quotas from infinite background refresh cycles.

---

## 🛠️ The Tech Stack

* **Frontend UI**: Streamlit (Compiled with customized corporate styling matching Coventry University's official brand identity)
* **Orchestration SDK**: `google-genai` (The modern, official Google GenAI Client SDK)
* **LLM Core Engine**: Gemini 2.5 Flash (Configured with a low temperature of `0.3` for high-fidelity compliance reasoning)
* **Vector Datastore**: ChromaDB (In-Memory execution layer for zero-config deployments)
* **Embedding Pipeline**: Sentence Transformers (Local open-source mathematical vector token matching)

---

## 📁 Repository Structure

```text
├── .streamlit/
│   └── secrets.toml      # Local encrypted secrets (Bypassed in version control)
├── app.py                # Main application engine and state pipeline
├── requirements.txt      # Pinned container dependencies
└── README.md             # Project documentation and B2B architecture brief

## 📈 Business Value & Institutional ROI



* **Cost Optimization**: Drastically reduces the operational hourly overhead spent on human student ambassador shifts for basic, repetitive FAQ management.
* **Conversion Optimization**: Captures international lead traffic in real-time across opposing time zones, dropping engagement friction to absolute zero and minimizing applicant drop-offs.
* **Admissions Relief**: Intercepts high-volume, low-complexity questions regarding application platforms (`Aula`, `SOLAR`, `Nova`) before they hit the ticketing queues of human admissions officers.

---

## 🔒 Security, Compliance & Data Privacy

Universities operate under strict UK data compliance regulations. Phoenix handles governance gracefully:

* **UK GDPR Compliance**: Form structures cleanly isolate user input logs. Student lead capture emails are processed sequentially and are never stored or transmitted to external entities for model-training purposes.
* **Isolated RAG Scope**: By locking down data retrieval to an internal `ChromaDB` vector framework with a strict low-temperature ceiling, the model is mathematically insulated from reading or referencing unauthorized external websites.
* **Safeguarding Gating**: The system's underlying fallback layer safely detects sensitive prompts and shifts administrative control to authorized personnel channels via standard support helpdesks.

---

## 🎭 Interactive Evaluation Demo Script

To demonstrate the robust semantic matching capabilities of the underlying RAG system during a live pitch or code review, try using these sample user query types:

| Test Scenario | Sample User Input | Expected Engine Behavior |
| :--- | :--- | :--- |
| **The Typo Test** | *"how can i get a viza"* | Correctly ignores the misspelling and prints the embedded CAS and UKVI guide text. |
| **The Concept Test** | *"where do I look up my classes?"* | Semantically maps the word "classes" to the internal documentation regarding the `Aula` platform. |
| **The Out-of-Bounds Test** | *"what is the deadline for the chemistry scholarship?"* | Automatically detects a context mismatch and safely paths the user to `ukadmissions@coventry.ac.uk`. |

---

## 🤝 Contributing & Extension Paths

This repository serves as an extensible base framework. Future development milestones include:
1. Migrating the local in-memory `ChromaDB` layer to an enterprise cloud instance (e.g., Pinecone or permanent AWS hosted storage).
2. Setting up direct webhook triggers to pipe captured lead data into university CRM systems like Salesforce or Slate.
3. Adding voice-to-text inference widgets for automated multilingual audio support.

---

## ⚖️ Compliance & Governance Disclaimer

*This application is an independent software demo built as a minimum viable product proof-of-concept for university recruitment evaluation. It is strictly grounded on public-facing curriculum frameworks and operating parameters.*
