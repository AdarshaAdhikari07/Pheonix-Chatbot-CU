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
