import os
from openai import OpenAI
from data_store import db

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AgentCore:
    def __init__(self):
        self.faqs = db.faqs
        
    def translate_prompt(self, text, target_lang):
        """Translate customer query to English for processing"""
        if target_lang == "en":
            return text
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Translate this to English: {text}"}
                ],
                temperature=0.3,
                max_tokens=100
            )
            return completion.choices[0].message.content
        except:
            return text  # fallback
    
    def handle_query(self, user_input, user_name="Guest"):
        # Detect language
        lang = db.detect_language(user_input)
        
        # 1. Check FAQ in detected language
        faq_response = db.get_faq_response(user_input, lang)
        if faq_response:
            return {
                "type": "faq",
                "response": faq_response,
                "language": lang,
                "ticket_id": None
            }
        
        # 2. Booking intent
        if any(word in user_input.lower() for word in ["book", "appointment", "install", "fit", "afspraak", "bhuka"]):
            return {
                "type": "booking",
                "response": self._get_booking_response(lang),
                "language": lang,
                "ticket_id": None
            }
        
        # 3. Escalation to producer
        if any(word in user_input.lower() for word in ["complaint", "refund", "problem", "manager", "klagte", "isikhalo"]):
            ticket = db.create_ticket(user_input, lang)
            return {
                "type": "producer_escalation",
                "response": self._get_escalation_response(lang, ticket["assigned_to"], ticket["id"]),
                "language": lang,
                "ticket_id": ticket["id"]
            }
        
        # 4. AI fallback with language context
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
            "language": lang,
            "ticket_id": None
        }
    
    def _get_booking_response(self, lang):
        responses = {
            "af": "Ek kan jou help om 'n afspraak te maak! Watter datum (YYYY-MM-DD) en tyd (HH:MM) pas vir jou?",
            "zu": "Ngingakusiza ukuthi ubhuke isikhathi! Yiluphi usuku (YYYY-MM-DD) nesikhathi (HH:MM) okuhambelana nawe?",
            "en": "I can help you book an appointment! What date (YYYY-MM-DD) and time (HH:MM) works for you?"
        }
        return responses.get(lang, responses["en"])
    
    def _get_escalation_response(self, lang, producer, ticket_id):
        responses = {
            "af": f"Ek verbind jou nou met {producer}. Hulle sal binne 5 minute kontak maak. Verwysingsnommer: #{ticket_id}",
            "zu": f"Ngikuxhumanisa no-{producer} manje. Bazokuthinta kungakapheli imizuzu emi-5. Inombolo yereferensi: #{ticket_id}",
            "en": f"I'm connecting you to {producer} right now. They'll reach out within 5 minutes. Reference: #{ticket_id}"
        }
        return responses.get(lang, responses["en"])
    
    def confirm_booking(self, date, time, vehicle_type="", user_name="Guest"):
        appt = db.book_appointment(user_name, date, time, vehicle_type)
        return f"✅ Booked for {user_name} on {date} at {time}. Confirmation #{appt['id']}"

agent = AgentCore()
