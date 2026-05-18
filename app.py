import streamlit as st
from google import genai
from google.genai import types
import os

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ─────────────────────────────────────────
# Page config
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Phoenix | Coventry University AI",
    page_icon="🦅",
    layout="centered"
)

# Refined branding colors to closely match Coventry University's visual identity
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
    .hero h1 { color: white; font-size: 2rem; margin: 0; }
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
</style>

<div class="hero">
    <h1>🦅 Phoenix</h1>
    <p>Your Official AI Student Ambassador at Coventry University</p>
    <span class="badge">⭐ Rated Gold for Student Experience · TEF 2023</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/e/e3/Coventry_University_logo.svg/320px-Coventry_University_logo.svg.png", width=180)
    st.markdown("### ⚙️ Settings")

    default_key = os.getenv("GEMINI_API_KEY", "")
    if not default_key and hasattr(st, "secrets"):
        default_key = st.secrets.get("GEMINI_API_KEY", "")

    if default_key:
        api_key = default_key
        st.success("✅ Connected to Campus Node")
    else:
        api_key = st.text_input("Gemini API Key", type="password", placeholder="AIza...")
        st.markdown("[Get a FREE key](https://aistudio.google.com/app/apikey)")

    st.divider()
    st.markdown("**Ask me about:**")
    st.markdown("""
- 🎓 Courses & campuses  
- 🌍 International student visas  
- 🏠 Accommodation & halls  
- 💻 Aula, SOLAR & Nova platforms  
- 📞 Contacts & admissions  
- 🏆 Rankings & student life  
""")
    st.divider()
    st.markdown("📧 ukadmissions@coventry.ac.uk")
    st.markdown("📞 +44 (0)24 7765 6565")

    if st.button("🗑️ Clear chat history"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────
# Coventry Knowledge Base Tool
# ─────────────────────────────────────────
def tool_coventry_knowledge_base(query: str) -> str:
    coventry_data = {
        "visa": (
            "International students must get a Confirmation of Acceptance for Studies (CAS), "
            "pay their tuition deposit, apply for a Student Visa, and set up a UKVI e-Visa account."
        ),
        "platforms": (
            "Coventry University uses 'Aula' for online learning and course modules, "
            "'SOLAR' for checking exam results and records, and 'Nova' for tracking attendance."
        ),
        "contacts": (
            "UK Admissions: ukadmissions@coventry.ac.uk | "
            "General Phone: +44 (0)24 7765 6565 | "
            "Protection Services (Emergency): +44 (0)24 7765 7363."
        ),
        "rankings": (
            "Coventry University is Rated Gold for Student Experience (TEF 2023) and is voted "
            "a Top 10 Student City in England for Affordability (QS Best Student Cities Index 2026)."
        ),
        "halls": (
            "Popular accommodation options include Singer Hall, Cycle Works, and Godiva Place, "
            "all located within walking distance of the main city campus."
        ),
        "campus": (
            "Coventry University has three campuses: Main Campus in Coventry city centre, "
            "CU London in Dagenham, and CU Scarborough on the Yorkshire coast."
        ),
        "scholarship": (
            "For the latest scholarship deadlines and eligibility, please check the official portal "
            "at coventry.ac.uk/study-at-coventry/fees-and-funding/scholarships/ or email "
            "ukadmissions@coventry.ac.uk as deadlines change each academic year."
        ),
        "aula": (
            "Aula is Coventry University's online learning platform where you access course materials, "
            "submit assignments, join discussions, and communicate with lecturers."
        ),
        "solar": (
            "SOLAR is the student records system at Coventry University. Use it to check your exam "
            "results, view your timetable, and manage your student record."
        ),
        "nova": (
            "Nova is the attendance tracking system at Coventry University. "
            "Students and staff use it to record and monitor lecture attendance."
        ),
    }

    query_lower = query.lower()
    matched = []
    for key, text in coventry_data.items():
        if key in query_lower:
            matched.append(text)

    if matched:
        return " | ".join(matched)
    return (
        "No explicit keyword match found in primary handbook data. Rely on system fallback instructions."
    )

# ─────────────────────────────────────────
# System prompt
# ─────────────────────────────────────────
SYSTEM_PROMPT = """You are 'Phoenix', an official AI Student Ambassador for Coventry University.
Your goal is to help prospective and current students learn about life at Coventry,
our campuses (Main Campus, London, Scarborough), and application steps.

Tone Rules:
- Be enthusiastic, welcoming, and proud to be part of the Coventry community.
- Always mention we are Rated Gold for Student Experience (TEF 2023) when relevant.
- Guide international students on CAS deposits, accommodation, and the UKVI e-Visa process.
- Refer to university systems accurately: 'Aula' for learning, 'SOLAR' for records, 'Nova' for attendance.
- If the [COVENTRY DATA CONTEXT] explicitly says no keyword match is found AND you don't know an exact policy or deadline from your training data, NEVER make it up. Direct them to ukadmissions@coventry.ac.uk or +44 (0)24 7765 6565.

Format Rules:
- Always use markdown with headers, bullet points, and relevant emojis.
- Keep responses friendly, clear, and well-structured.
- End responses with an encouraging line or offer to help further.

Context Rule:
You will receive a [COVENTRY DATA CONTEXT] block containing verified university data facts for the current turn.
Rely on this data to answer accurately before attempting to extrapolate from general knowledge."""

# ─────────────────────────────────────────
# Chat state
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Welcome to Coventry University!** I'm **Phoenix**, your AI Student Ambassador.\n\n"
                "I'm here to help you with:\n"
                "- 🎓 Courses, campuses & student life\n"
                "- 🌍 International visa & CAS guidance\n"
                "- 🏠 Accommodation options\n"
                "- 💻 University platforms (Aula, SOLAR, Nova)\n"
                "- 📞 Contacts & admissions info\n\n"
                "What would you like to know? 😊"
            )
        }
    ]

# Render chat history cleanly
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🦅" if msg["role"] == "assistant" else None):
        st.markdown(msg["content"])

# ─────────────────────────────────────────
# Chat input
# ─────────────────────────────────────────
user_input = st.chat_input("Ask Phoenix anything about Coventry University...")

if user_input:
    if not api_key:
        st.warning("Please enter your Gemini API key in the sidebar.")
        st.stop()

    # Append and display clean user query to keep session state UI pristine
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Retrieve fresh knowledge base context
    facts = tool_coventry_knowledge_base(user_input)

    # Reconstruct the historical log for Gemini's API without contaminating past turns
    contents = []
    # Skip the welcome introduction message index 0 to save tokens and avoid baseline noise
    for m in st.session_state.messages[1:-1]:
        role = "user" if m["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))

    # Package the current user turn with its specific context block safely isolated
    augmented_query = f"[COVENTRY DATA CONTEXT]: {facts}\n\nUser Question: {user_input}"
    contents.append(types.Content(role="user", parts=[types.Part(text=augmented_query)]))

    with st.chat_message("assistant", avatar="🦅"):
        with st.spinner("Phoenix is reviewing campus records..."):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",  # Upgraded to the modern production flash standard
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.4, # Lowered slightly from 0.7 to enforce higher fidelity to your KB context
                    )
                )
                final_text = response.text
                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})

            except Exception as e:
                st.error(f"Sorry, I encountered an error connecting to the system: {e}")
