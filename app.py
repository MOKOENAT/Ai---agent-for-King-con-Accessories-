import streamlit as st
import os

# ========== DATA STORE ==========
class DataStore:
    def __init__(self):
        self.faqs = {
            "rubber mats": {
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
        afrikaans_words = ["ek", "jy", "my", "ons", "hulle", "is", "het", "was", "baie", "goed", "ja", "wat", "hoe", "vir", "met"]
        zulu_words = ["ngi", "si", "ni", "ba", "ku", "lo", "le", "la", "kulo", "ngoba", "wena", "mina", "yami", "yakho"]
        
        text_lower = text.lower()
        af_score = sum(1 for word in afrikaans_words if word in text_lower)
        zu_score = sum(1 for word in zulu_words if word in text_lower)
        
        if af_score > zu_score:
            return "af"
        elif zu_score > af_score:
            return "zu"
        return "en"
    
    def get_faq_response(self, query, lang="en"):
        query_lower = query.lower()
        for key, translations in self.faqs.items():
            if key in query_lower:
                return translations.get(lang, translations["en"])
        return None

db = DataStore()

# ========== AGENT CORE ==========
class AgentCore:
    def __init__(self):
        self.faqs = db.faqs
    
    def handle_query(self, user_input):
        # Detect language
        lang = db.detect_language(user_input)
        
        # Check FAQ
        faq_response = db.get_faq_response(user_input, lang)
        if faq_response:
            return {
                "response": faq_response,
                "language": lang
            }
        
        # Booking intent
        if any(word in user_input.lower() for word in ["book", "appointment", "install", "afspraak", "bhuka"]):
            responses = {
                "af": "Ek kan jou help om 'n afspraak te maak! Watter datum en tyd pas vir jou?",
                "zu": "Ngingakusiza ukuthi ubhuke isikhathi! Yiluphi usuku nesikhathi okuhambelana nawe?",
                "en": "I can help you book an appointment! What date and time works for you?"
            }
            return {
                "response": responses.get(lang, responses["en"]),
                "language": lang
            }
        
        # Fallback responses
        responses = {
            "af": f"Dankie vir jou boodskap! Ek is die King Con Accessories assistent. Ons spesialiseer in premium rubber matte vir bakkies. Kan ek jou help met pryse, installasie, of 'n afspraak maak?",
            "zu": f"Ngiyabonga ngomlayezo wakho! Ngingumsizi we-King Con Accessories. Sigxile kumath e-rubber e-premium e-bakkies. Ngingakusiza ngamanani, ukufaka, noma ukubhuka isikhathi?",
            "en": f"Thank you for your message! I'm the King Con Accessories assistant. We specialize in premium rubber mats for bakkies. Can I help you with pricing, installation, or booking an appointment?"
        }
        return {
            "response": responses.get(lang, responses["en"]),
            "language": lang
        }

agent = AgentCore()

# ========== STREAMLIT APP ==========
st.set_page_config(
    page_title="King Con Accessories",
    page_icon="🛻",
    layout="wide"
)

# Header
st.title("🛻 King Con Accessories")
st.markdown("### Premium Rubber Mats for Bakkies")
st.caption("Afrikaans | English | Zulu")

# Sidebar
with st.sidebar:
    st.subheader("📚 Quick FAQ")
    for key in list(db.faqs.keys())[:3]:
        with st.expander(key.capitalize()):
            st.write(db.faqs[key]["en"])
    
    st.divider()
    st.info("💡 Try typing in Afrikaans, English, or Zulu!")
    
    st.divider()
    st.subheader("👥 Our Team")
    for p in db.producers:
        st.success(f"🟢 {p}")

# Main chat
st.subheader("💬 Ask about rubber mats for your bakkie!")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = """👋 Welcome to King Con Accessories!
    
💬 Ask me about:
• Rubber mats for your bakkie
• Prices and installation
• Booking appointments

I understand: Afrikaans, English, and Zulu!"""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input - THIS IS THE KEY PART!
prompt = st.chat_input("Ask about rubber mats...")
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get response
    response = agent.handle_query(prompt)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response["response"]})
    
    # Rerun to show messages
    st.rerun()
