import streamlit as st
from datetime import datetime
from agent_core import agent
from data_store import db

st.set_page_config(
    page_title="King Con Accessories - AI Agent",
    page_icon="🛻",
    layout="wide"
)

# Custom CSS for King Con branding
st.markdown("""
    <style>
    .main { background-color: #f5f0e8; }
    .stChatMessage { background-color: white; border-radius: 10px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
col1, col2, col3 = st.columns([2,1,1])
with col1:
    st.title("🛻 King Con Accessories")
    st.caption("Premium Rubber Mats for Bakkies | Premium Rubber Matte vir Bakkies")
with col2:
    st.metric("🌍 Active Languages", "3 (AF, EN, ZU)")
with col3:
    st.metric("🟢 Online", "2 Producers")

# --- Sidebar ---
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/2d5a27/white?text=KING+CON", use_column_width=True)
    st.divider()
    
    st.subheader("📊 Live Stats")
    st.metric("Open Tickets", len(db.get_open_tickets()))
    st.metric("Today's Bookings", len(db.appointments))
    
    st.divider()
    st.subheader("👥 Producers")
    for p in db.producers:
        st.success(f"🟢 {p}")
    
    st.divider()
    st.subheader("🌍 Language Support")
    st.info("🇿🇦 Afrikaans | 🇬🇧 English | 🇿🇺 Zulu")
    st.caption("Auto-detects your language!")
    
    st.divider()
    st.subheader("📚 Quick FAQ")
    for key in list(db.faqs.keys())[:3]:
        with st.expander(key.capitalize()):
            st.write(db.faqs[key]["en"])

# --- Main Chat ---
st.subheader("💬 Customer Service")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Welcome message in 3 languages
    welcome = """👋 Welcome to King Con Accessories!
    
🇬🇧 How can I help with your bakkie mats?
🇿🇦 Hoe kan ek help met jou bakkie matte?
🇿🇺 Ngingakusiza kanjani ngamath e-bakkie akho?"""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("ticket_id"):
            st.info(f"🎫 Ticket #{msg['ticket_id']}")

# Chat input
if prompt := st.chat_input("Ask about rubber mats | Vra oor rubber matte | Buza ngamath e-rubber..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Process with agent
    response = agent.handle_query(prompt)
    
    # Show response
    with st.chat_message("assistant"):
        st.write(response["response"])
        
        # Show language detected
        lang_names = {"af": "🇿🇦 Afrikaans", "en": "🇬🇧 English", "zu": "🇿🇺 Zulu"}
        st.caption(f"Responding in: {lang_names.get(response.get('language', 'en'), 'English')}")
        
        if response.get("ticket_id"):
            st.warning(f"🔔 Ticket #{response['ticket_id']} created - Producer notified")
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["response"],
        "ticket_id": response.get("ticket_id")
    })

# --- Booking Section ---
if any("book" in msg["content"].lower() for msg in st.session_state.messages[-3:]):
    with st.expander("📅 Book Installation", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("Date | Datum | Usuku")
        with col2:
            time = st.time_input("Time | Tyd | Isikhathi")
        with col3:
            vehicle = st.selectbox("Vehicle | Voertuig | Imoto", 
                                  ["Toyota Hilux", "Ford Ranger", "Isuzu D-Max", "Nissan Navara", "Other"])
        
        if st.button("✅ Confirm Booking | Bevestig | Qinisekisa", type="primary"):
            result = agent.confirm_booking(str(date), str(time), vehicle, "Customer")
            st.success(result)
            st.balloons()

# --- Producer Dashboard ---
with st.expander("👨‍💼 Producer Control Panel", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🆕 Open Tickets")
        tickets = db.get_open_tickets()
        if tickets:
            for t in tickets:
                with st.container():
                    lang_emoji = {"af": "🇿🇦", "en": "🇬🇧", "zu": "🇿🇺"}
                    st.warning(f"{lang_emoji.get(t.get('language', 'en'), '🌍')} #{t['id']} | {t['query'][:60]}...")
                    st.caption(f"Assigned: {t.get('assigned_to', 'Unassigned')}")
                    if st.button(f"Resolve #{t['id']}", key=f"resolve_{t['id']}"):
                        t["resolved"] = True
                        st.rerun()
        else:
            st.success("🎉 No open tickets!")
    
    with col2:
        st.subheader("📋 Today's Bookings")
        if db.appointments:
            for a in db.appointments:
                st.info(f"🛻 {a['vehicle']} | {a['client']} | {a['date']}")
        else:
            st.write("No bookings yet today")

# --- Footer ---
st.divider()
st.caption("🏢 King Con Accessories | 123 Main Street, Johannesburg | 011 234 5678")
