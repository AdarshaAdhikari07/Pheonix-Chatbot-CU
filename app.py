import streamlit as st
from google import genai
from google.genai import types
import os
import chromadb
from chromadb.utils import embedding_functions

# ─────────────────────────────────────────
# Page Configuration & UI Branding
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Phoenix | Coventry University AI",
    page_icon="🦅",
    layout="centered"
)

# Custom CSS to match Coventry University's exact corporate identity (Deep Navy & Gold)
st.markdown("""
<style>
    .stChatMessage { border-radius: 12px; }
    .hero {
        background: linear-gradient(135deg, #0A1C3A 0%, #16305B 100%);
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
        border-bottom: 4px solid #EAAA00;
    }
    .hero h1 { color: white; font-size: 2rem; margin: 0; padding-bottom: 5px; }
    .hero p  { color: rgba(255,255,255,0.85); margin: 0.4rem 0 0; font-size: 0.95rem; }
    .badge {
        display: inline-block;
        background: #EAAA00;
        color: #0A1C3A;
        border-radius: 50px;
        padding: 0.2rem 0.8rem;
        font-size: 0.78rem;
        margin-top: 0.6rem;
        font-weight: bold;
    }
    .crm-box {
        background-color: #f0f4f8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #16305B;
        margin-bottom: 1rem;
    }
    div[data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
</style>

<div class="hero">
    <h1>🦅 Phoenix</h1>
    <p>Your Official AI Student Ambassador at Coventry University</p>
    <span class="badge">⭐ Rated Gold for Student Experience · TEF 2023</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Vector Database Initialization (ChromaDB)
# ─────────────────────────────────────────
@st.cache_resource
def init_vector_db():
    """Initializes a local in-memory vector store for robust semantic context lookup."""
    chroma_client = chromadb.Client() 
    emb_fn = embedding_functions.DefaultEmbeddingFunction()
    
    collection = chroma_client.get_or_create_collection(
        name="coventry_handbook", 
        embedding_function=emb_fn
    )
    
    # Core Ground Truth Knowledge Base
    coventry_data = {
        "doc1": "International students must get a Confirmation of Acceptance for Studies (CAS), pay their tuition deposit, apply for a Student Visa, and set up a UKVI e-Visa account.",
        "doc2": "Coventry University uses 'Aula' for online learning and course modules, 'SOLAR' for checking exam results and records, and 'Nova' for tracking attendance.",
        "doc3": "UK Admissions contact information: email ukadmissions@coventry.ac.uk | General Phone: +44 (0)24 7765 6565 | Protection Services (Emergency): +44 (0)24 7765 7363.",
        "doc4": "Coventry University is Rated Gold for Student Experience (TEF 2023) and is voted a Top 10 Student City in England for Affordability (QS Best Student Cities Index 2026).",
        "doc5": "Popular accommodation options include Singer Hall, Cycle Works, and Godiva Place, all located within short walking distance of the main city campus.",
        "doc6": "Coventry University has three main operating locations: Main Campus in Coventry city centre, CU London in Dagenham, and CU Scarborough on the Yorkshire coast.",
        "doc7": "For the latest scholarship deadlines, terms, and eligibility, students must check the official portal at coventry.ac.uk/study-at-coventry/fees-and-funding/scholarships/."
    }
    
    # Build vector keys if initializing fresh
    if collection.count() == 0:
        collection.add(
            ids=list(coventry_data.keys()),
            documents=list(coventry_data.values())
        )
    return collection

vector_collection = init_vector_db()

# ─────────────────────────────────────────
# Sidebar & Lead Capture Framework
# ─────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/e/e3/Coventry_University_logo.svg/320px-Coventry_University_logo.svg.png", width=180)
    
    # Enterprise B2B Feature: Lead Capture Form
    st.markdown("### 🎓 Connect with Admissions")
    with st.container():
        st.markdown("<div class='crm-box'><b>Want an official advisor to follow up with your application?</b></div>", unsafe_allow_html=True)
        lead_email = st.text_input("Enter your email address", placeholder="student@example.com")
        lead_intent = st.selectbox("I am interested in:", ["Undergraduate", "Postgraduate", "International Onboarding"])
        if st.button("Connect Me"):
            if lead_email and "@" in lead_email:
                # In production, this can pipe data straight to Salesforce, Slate, or a webhook
                st.success("🎉 Details saved! An admissions officer will contact you shortly.")
            else:
                st.error("Please enter a valid email address.")
                
    st.divider()
    st.markdown("### ⚙️ System Status")
    
    # API Key Hydration from Environment or Manual Input
    default_key = os.getenv("GEMINI_API_KEY", "")
    if not default_key and hasattr(st, "secrets"):
        default_key = st.secrets.get("GEMINI_API_KEY", "")

    if default_key:
        api_key = default_key
        st.success("✅ Connected to Campus Node")
    else:
        api_key = st.text_input("Gemini API Key", type="password", placeholder="AIza...")
        st.markdown("[Get a FREE key](https://aistudio.google.com/app/apikey)")

    if st.button("🗑️ Clear chat history"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────
# Core System Prompts
# ─────────────────────────────────────────
SYSTEM_PROMPT = """You are 'Phoenix', an official AI Student Ambassador for Coventry University.
Your goal is to help prospective and current students learn about life at Coventry, our campuses, and application steps.

Tone Rules:
- Be enthusiastic, welcoming, and proud to be part of the Coventry community.
- Mention we are Rated Gold for Student Experience (TEF 2023) when relevant.
- Refer to university software systems accurately: 'Aula' for virtual learning, 'SOLAR' for student records, and 'Nova' for checking attendance logs.
- If the contextual reference block doesn't contain explicit parameters to answer a question safely, NEVER hallucinate deadlines or policies. Instruct them to email ukadmissions@coventry.ac.uk or call +44 (0)24 7765 6565.

Format Rules:
- Always use clean markdown structures with headers, bullet points, and relevant emojis.
- Keep responses friendly, clear, and well-structured.

Context Rule:
You will receive a [COVENTRY DATA CONTEXT] block containing verified university data facts for the current turn.
You must strictly base your facts on this block to avoid hallucinating external compliance policies."""

# ─────────────────────────────────────────
# Chat Interface and Execution Logic
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Welcome to Coventry University!** I'm **Phoenix**, your AI Student Ambassador.\n\n"
                "I can assist you with:\n"
                "- 🎓 Courses, campuses & university rankings\n"
                "- 🌍 International student visa & CAS deposit pathways\n"
                "- 🏠 Local accommodation options\n"
                "- 💻 Navigating campus portals (Aula, SOLAR, Nova)\n"
                "- 📞 Official admissions helpdesk paths\n\n"
                "What would you like to explore today? 😊"
            )
        }
    ]

# Render persistent conversation stream UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🦅" if msg["role"] == "assistant" else None):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask Phoenix anything about Coventry University...")

if user_input:
    if not api_key:
        st.warning("Please enter your Gemini API key in the sidebar configuration to begin.")
        st.stop()

    # Append and render the raw user query safely in the UI history state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Execute Semantic Retrieval via ChromaDB Vector Space
    # Pulls the top 2 matching document strings relative to the user query
    results = vector_collection.query(query_texts=[user_input], n_results=2)
    retrieved_facts = " | ".join(results['documents'][0]) if results['documents'] and results['documents'][0] else "No close matching context found."

    # Parse and package chat logging history for the official GenAI API structure
    contents = []
    # Skip the generic first welcoming message index to keep context focused
    for m in st.session_state.messages[1:-1]:
        role = "user" if m["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))

    # Append current isolated turn containing context augmentation injection
    augmented_query = f"[COVENTRY DATA CONTEXT]: {retrieved_facts}\n\nUser Question: {user_input}"
    contents.append(types.Content(role="user", parts=[types.Part(text=augmented_query)]))

    # Execute Inference Pipeline
    with st.chat_message("assistant", avatar="🦅"):
        with st.spinner("Phoenix is searching campus database..."):
            try:
                # Initialize standard Google GenAI Client
                client = genai.Client(api_key=api_key)
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",  
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.3, # Highly deterministic to prevent hallucinated compliance metrics
                    )
                )
                
                final_text = response.text
                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})

            except Exception as e:
                st.error(f"System Link Interrupted: {e}")
