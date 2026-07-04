import streamlit as st
import os

# ========== DATA STORE ==========
class DataStore:
    def __init__(self):
        # Better FAQ with multiple keywords
        self.faqs = [
            {
                "keywords": ["mat", "matt", "rubber", "fit", "bakkie", "hilux", "ranger", "d-max", "navara"],
                "en": "We have custom-fit rubber mats for Toyota Hilux, Ford Ranger, Isuzu D-Max, and Nissan Navara. Full set: R1,499.",
                "af": "Ons het pasgemaakte rubbermatte vir Toyota Hilux, Ford Ranger, Isuzu D-Max, en Nissan Navara. Volle stel: R1,499.",
                "zu": "Sinamath e-rubber afanele i-Toyota Hilux, Ford Ranger, Isuzu D-Max, ne-Nissan Navara. Isethi ephelele: R1,499."
            },
            {
                "keywords": ["price", "cost", "how much", "what is the price", "expensive", "cheap", "prys", "kos", "kubiza", "malini"],
                "en": "Full set (front + back): R1,499. Single cab: R899. Installation: R250. We also offer payment plans.",
                "af": "Volle stel (voor + agter): R1,499. Enkel kajuit: R899. Installasie: R250. Ons bied ook betaalplanne.",
                "zu": "Isethi ephelele (ngaphambili + ngemuva): R1,499. I-cab eyodwa: R899. Ukufaka: R250. Sinazo nezinhlelo zokukhokha."
            },
            {
                "keywords": ["install", "fitting", "fitment", "place", "put on", "installasie", "ukufaka"],
                "en": "Installation takes 30-45 minutes. Walk-ins welcome at our workshop, or book an appointment.",
                "af": "Installasie neem 30-45 minute. Loslopers welkom by ons werkswinkel, of maak 'n afspraak.",
                "zu": "Ukufaka kuthatha imizuzu engama-30-45. Siyamukela abangazimisile emsebenzini wethu, noma bhuka isikhathi."
            },
            {
                "keywords": ["warranty", "guarantee", "return", "defect", "waarborg", "iwaranti"],
                "en": "2-year warranty against defects. Our mats are heat-resistant, non-slip, and durable.",
                "af": "2-jaar waarborg teen defekte. Ons matte is hittebestand, glyvry, en duursaam.",
                "zu": "Iwaranti yeminyaka emi-2 ngokumelene namaphutha. Amathe ethu awashisi, awasheleli, futhi ahlala isikhathi eside."
            },
            {
                "keywords": ["delivery", "shipping", "courier", "post", "send", "lewer", "ukuhambisa"],
                "en": "We deliver nationwide. 2-3 days in Gauteng, 3-5 days other provinces. Delivery cost: R150.",
                "af": "Ons lewer landwyd. 2-3 dae in Gauteng, 3-5 dae ander provinsies. Afleweringskoste: R150.",
                "zu": "Sihambisa ezweni lonke. Izinsuku 2-3 eGauteng, izinsuku 3-5 kwezinye izifundazwe. Izindleko zokuhambisa: R150."
            },
            {
                "keywords": ["book", "appointment", "schedule", "afspraak", "bhuka", "isikhathi"],
                "en": "I can help you book an appointment! Please tell me your preferred date and time.",
                "af": "Ek kan jou help om 'n afspraak te maak! Sê vir my jou voorkeurdatum en -tyd.",
                "zu": "Ngingakusiza ukuthi ubhuke isikhathi! Ngicela ungitshele usuku nesikhathi okukhethayo."
            },
            {
                "keywords": ["payment", "pay", "eft", "cash", "snapscan", "zapper", "credit", "card", "betaal", "ikhokhe"],
                "en": "We accept Cash, EFT, SnapScan, Zapper, and Credit Cards. We also offer buy-now-pay-later options.",
                "af": "Ons aanvaar Kontant, EFT, SnapScan, Zapper, en Kredietkaarte. Ons bied ook koop-nou-betaal-later opsies.",
                "zu": "Siyamukela Imali, EFT, SnapScan, Zapper, namakhadi esikweletu. Sinazo nezinhlelo zokuthenga-manje-khokha-kamuva."
            },
            {
                "keywords": ["hello", "hi", "hey", "good day", "hallo", "sawubona", "morning", "afternoon"],
                "en": "Hello! 👋 Welcome to King Con Accessories. How can I help you with rubber mats for your bakkie today?",
                "af": "Hallo! 👋 Welkom by King Con Accessories. Hoe kan ek jou vandag help met rubber matte vir jou bakkie?",
                "zu": "Sawubona! 👋 Siyakwemukela e-King Con Accessories. Ngingakusiza kanjani namuhla ngamath e-rubber e-bakkie yakho?"
            }
        ]
        
        self.producers = [
            "Pieter (Sales - Afrikaans)",
            "Johan (Installation - English/Afrikaans)",
            "Thabo (Support - Zulu/English)"
        ]
    
    def detect_language(self, text):
        afrikaans_words = ["ek", "jy", "my", "ons", "hulle", "is", "het", "was", "baie", "goed", "ja", "wat", "hoe", "vir", "met", "nie", "ook", "maar"]
        zulu_words = ["ngi", "si", "ni", "ba", "ku", "lo", "le", "la", "kulo", "ngoba", "wena", "mina", "yami", "yakho", "ukuthi", "ngiy"]
        
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
        
        # Check each FAQ entry
        for faq in self.faqs:
            # Check if ANY keyword matches
            for keyword in faq["keywords"]:
                if keyword in query_lower:
                    return faq.get(lang, faq["en"])
        
        return None

db = DataStore()

# ========== AGENT CORE ==========
class AgentCore:
    def __init__(self):
        self.faqs = db.faqs
    
    def handle_query(self, user_input):
        # Detect language
        lang = db.detect_language(user_input)
        
        # Check FAQ with smart matching
        faq_response = db.get_faq_response(user_input, lang)
        if faq_response:
            return {
                "response": faq_response,
                "language": lang,
                "type": "faq"
            }
        
        # If no FAQ matches, give a helpful response
        responses = {
            "af": f"Dankie vir jou vraag! Ek is die King Con Accessories assistent. Ek kan jou help met:\n• Rubber matte vir bakkies (Toyota, Ford, Isuzu, Nissan)\n• Pryse (vanaf R899)\n• Installasie (30-45 minute)\n• Afsprake en aflewering\n\nWat sal jy graag wil weet?",
            "zu": f"Ngiyabonga ngombuzo wakho! Ngingumsizi we-King Con Accessories. Ngingakusiza nge:\n• Amath e-rubber e-bakkies (Toyota, Ford, Isuzu, Nissan)\n• Amanani (kusuka R899)\n• Ukufaka (imizuzu 30-45)\n• Ukubhuka nokuhambisa\n\nYini ongathanda ukuyazi?",
            "en": f"Thank you for your question! I'm the King Con Accessories assistant. I can help you with:\n• Rubber mats for bakkies (Toyota, Ford, Isuzu, Nissan)\n• Pricing (from R899)\n• Installation (30-45 minutes)\n• Bookings and delivery\n\nWhat would you like to know?"
        }
        return {
            "response": responses.get(lang, responses["en"]),
            "language": lang,
            "type": "fallback"
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
st.caption("🌍 Afrikaans | English | Zulu")

# Sidebar
with st.sidebar:
    st.subheader("📚 Quick FAQ")
    st.write("Try asking about:")
    for faq in db.faqs[:5]:
        st.write(f"• {faq['keywords'][0].capitalize()}")
    
    st.divider()
    st.info("💡 Type in Afrikaans, English, or Zulu!")
    
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
• Bookings and delivery

🌍 I understand: Afrikaans, English, and Zulu!

Try asking:
• "How much is the mat?"
• "What fits my Hilux?"
• "I want to book installation"
• "Do you deliver?" """
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
prompt = st.chat_input("Ask about rubber mats...")
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get response
    with st.spinner("Thinking..."):
        response = agent.handle_query(prompt)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response["response"]})
    
    # Show language detected
    lang_names = {"af": "🇿🇦 Afrikaans", "en": "🇬🇧 English", "zu": "🇿🇺 Zulu"}
    st.caption(f"Detected: {lang_names.get(response.get('language', 'en'), 'English')}")
    
    # Rerun to show messages
    st.rerun()
