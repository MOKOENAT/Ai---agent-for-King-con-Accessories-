import streamlit as st
import os
from openai import OpenAI

# ============================================
# ALL CODE IN ONE FILE - NO IMPORTS NEEDED!
# ============================================

# ========== DATA STORE ==========
class DataStore:
    def __init__(self):
        self.faqs = {
            "what rubber mats fit my bakkie": {
                "en": "We have custom-fit rubber mats for Toyota Hilux, Ford Ranger, Isuzu D-Max, and Nissan Navara.",
                "af": "Ons het pasgemaakte rubbermatte vir Toyota Hilux, Ford Ranger, Isuzu D-Max, en Nissan Navara.",
                "zu": "Sinamath e-rubber afanele i-Toyota Hilux, Ford Ranger, Isuzu D-Max, ne-Nissan Navara."
            },
            "price": {
                "en": "Full set (front + back): R1,499. Single cab: R899. Installation: R250.",
                "af": "Volle stel (voor + agter): R1,499. Enkel kajuit: R899. Installasie: R250.",
                "zu": "Isethi ephelele (ngaphambili + ngemuva): R1,499. I-cab eyodwa: R899. Ukufaka: R250."
            },
            "installation": {
                "en": "Installation takes 30-45 minutes. Walk-ins welcome or book appointment.",
                "af": "Installasie neem 30-45 minute. Loslopers welkom of maak 'n afspraak.",
                "zu": "Ukufaka kuthatha imizuzu engama-30-45. Siyamukela abangazimisile noma bhuka isikhathi."
            },
            "warranty": {
                "en": "2-year warranty against defects. Heat-resistant and non-slip.",
                "af": "2-jaar waarborg teen defekte. Hittebestand en glyvry.",
                "zu": "Iwaranti yeminyaka emi-2 ngokumelene namaphutha. Awashisi futhi awasheleli."
            },
            "delivery": {
                "en": "We deliver nationwide. 2-3 days in Gauteng, 3-5 days other provinces.",
                "af": "Ons lewer landwyd. 2-3 dae in Gauteng, 3-5 dae ander provinsies.",
                "zu": "Sihambisa ezweni lonke. Izinsuku 2-3 eGauteng, izinsuku 3-5 kwezinye izifundazwe."
            }
        }
        
        self.producers = [
            "Pieter (Sales - Afrikaans)",
            "Johan (Installation - English/Afrikaans)",
            "Thabo (Support - Zulu/English)"
        ]
    
    def detect_language(self, text):
        """Simple language detection"""
        afrikaans_words = ["ek", "jy", "my", "ons", "hulle", "is", "het", "was", "baie", "goed", "ja", "wat", "hoe"]
        zulu_words = ["ngi", "si", "ni", "ba", "ku", "lo", "le", "la", "kulo", "ngoba", "wena", "mina"]
        
        text_lower = text.lower()
        af_score = sum(1 for word in afrikaans_words if word in text_lower)
        zu_score = sum(1 for word in zulu_words if word in text_lower)
        
        if af_score > zu_score:
            return "af"
        elif zu_score > af_score:
            return "zu"
        return "en"
    
    def get_faq_response(self, query, lang="en"):
        """Get FAQ in detected language"""
        for key, translations in self.faqs.items():
            if key in query.lower() or any(word in query.lower() for word in key.split()):
                return translations.get(lang, translations["en"])
        return None

db = DataStore()

# ========== AGENT CORE ==========
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AgentCore:
    def __init__(self):
        self.faqs = db.faqs
    
    def handle_query(self, user_input, user_name="Guest"):
        # Detect language
        lang = db.detect_language(user_input)
        
        # 1. Check FAQ
        faq_response = db.get_faq_response(user_input, lang)
        if faq_response:
            return {
                "type": "faq",
                "response": faq_response,
                "language": lang
            }
        
        # 2. Booking intent
        if any(word in user_input.lower() for word in ["book", "appointment", "install", "afspraak", "bhuka"]):
            return {
                "type": "booking",
                "response": self._get_booking_response(lang),
                "language": lang
            }
        
        # 3. AI fallback with language context
        try:
            system_prompt = f"""You're a helpful assistant for King Con Accessories - we sell rubber mats for bakkies/pickups.
            Respond in {lang} language. Be friendly and professional.
            If asked about price, mention R1,499 for full set.
            If asked about fitment, say we fit Toyota Hilux, Ford Ranger, Isuzu D-Max, Nissan Navara."""
            
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=200
            )
            return {
                "type": "ai_response",
                "response": completion.choices[0].message.content,
                "language": lang
            }
        except Exception as e:
            return {
                "type": "error",
                "response": f"Sorry, I'm having trouble. Please try again or contact us directly. Error: {str(e)[:100]}",
                "language": lang
            }
    
    def _get_booking_response(self, lang):
        responses = {
            "af": "Ek kan jou help om 'n afspraak te maak! Watter datum (YYYY-MM-DD) en tyd (HH:MM) pas vir jou?",
            "zu": "Ngingakusiza ukuthi ubhuke isikhathi! Yiluphi usuku (YYYY-MM-DD) nesikhathi (HH:MM) okuhambelana nawe?",
            "en": "I can help you book an appointment! What date (YYYY-MM-DD) and time (HH:MM) works for you?"
        }
        return responses.get(lang, responses["en"])

agent = AgentCore()

# ========== STREAMLIT APP ==========
st.set_page_config(
    page_title="King Con Accessories - AI Agent",
    page_icon="🛻",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f5f0e8; }
    .stChatMessage { background-color: white; border-radius: 10px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([2,1])
with col1:
    st.title("🛻 King Con Accessories")
    st.caption("Premium Rubber Mats for Bakkies | Premium Rubber Matte vir Bakkies")
with col2:
    st.metric("🌍 Languages", "🇿🇦🇬🇧🇿🇺")

# Sidebar
with st.sidebar:
    st.subheader("📚 Quick FAQ")
    for key in list(db.faqs.keys())[:3]:
        with st.expander(key.capitalize()):
            st.write(db.faqs[key]["en"])
    
    st.divider()
    st.subheader("👥 Producers")
    for p in db.producers:
        st.success(f"🟢 {p}")

# Main Chat
st.subheader("💬 Ask about rubber mats for your bakkie!")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = """👋 Welcome to King Con Accessories!
    
🇬🇧 How can I help with your bakkie mats?
🇿🇦 Hoe kan ek help met jou bakkie matte?
🇿🇺 Ngingakusiza kanjani ngamath e-bakkie akho?"""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if prompt := st.chat_input("Ask about rubber mats | Vra oor rubber matte | Buza ngamath e-rubber..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    response = agent.handle_query(prompt)
    with st.chat_message("assistant"):
        st.write(response["response"])
        lang_names = {"af": "🇿🇦 Afrikaans", "en": "🇬🇧 English", "zu": "🇿🇺 Zulu"}
        st.caption(f"Responding in: {lang_names.get(response.get('language', 'en'), 'English')}")
    
    st.session_state.messages.append({"role": "assistant", "content": response["response"]})
