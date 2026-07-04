from datetime import datetime, timedelta
import uuid

class DataStore:
    def __init__(self):
        self.tickets = []
        self.appointments = []
        self.orders = []
        
        # King Con specific FAQs (Afrikaans/English/Zulu)
        self.faqs = {
            "what rubber mats fit my bakkie": {
                "en": "We have custom-fit rubber mats for Toyota Hilux, Ford Ranger, Isuzu D-Max, and Nissan Navara.",
                "af": "Ons het pasgemaakte rubbermatte vir Toyota Hilux, Ford Ranger, Isuzu D-Max, en Nissan Navara.",
                "zu": "Sinamath e-rubber afanele i-Toyota Hilux, Ford Ranger, Isuzu D-Max, ne-Nissan Navara."
            },
            "price of rubber mats": {
                "en": "Full set (front + back): R1,499. Single cab: R899. Installation available at R250.",
                "af": "Volle stel (voor + agter): R1,499. Enkel kajuit: R899. Installasie beskikbaar teen R250.",
                "zu": "Isethi ephelele (ngaphambili + ngemuva): R1,499. I-cab eyodwa: R899. Ukufaka kuyatholakala nge-R250."
            },
            "installation time": {
                "en": "Installation takes 30-45 minutes. Walk-ins welcome or book appointment.",
                "af": "Installasie neem 30-45 minute. Loslopers welkom of maak 'n afspraak.",
                "zu": "Ukufaka kuthatha imizuzu engama-30-45. Siyamukela abangazimisile noma bhuka isikhathi."
            },
            "warranty": {
                "en": "2-year warranty against defects. Our mats are heat-resistant and non-slip.",
                "af": "2-jaar waarborg teen defekte. Ons matte is hittebestand en glyvry.",
                "zu": "Iwaranti yeminyaka emi-2 ngokumelene namaphutha. Amathe ethu awashisi futhi awasheleli."
            },
            "delivery": {
                "en": "We deliver nationwide. 2-3 days in Gauteng, 3-5 days other provinces.",
                "af": "Ons lewer landwyd. 2-3 dae in Gauteng, 3-5 dae ander provinsies.",
                "zu": "Sihambisa ezweni lonke. Izinsuku 2-3 eGauteng, izinsuku 3-5 kwezinye izifundazwe."
            },
            "payment methods": {
                "en": "Cash, EFT, SnapScan, Zapper. We also accept buy-now-pay-later options.",
                "af": "Kontant, EFT, SnapScan, Zapper. Ons aanvaar ook koop-nou-betaal-later opsies.",
                "zu": "Imali, EFT, SnapScan, Zapper. Siyamukela nokuthenga-manje-khokha-kamuva."
            }
        }
        
        self.producers = [
            "Pieter (Sales - Afrikaans)",
            "Johan (Installation - English/Afrikaans)", 
            "Thabo (Support - Zulu/English)"
        ]
        
    def detect_language(self, text):
        """Simple language detection"""
        afrikaans_words = ["ek", "jy", "my", "ons", "hulle", "is", "het", "was", "baie", "goed", "ja"]
        zulu_words = ["ngi", "si", "ni", "ba", "ku", "lo", "le", "la", "kulo", "ngoba"]
        
        text_lower = text.lower()
        af_score = sum(1 for word in afrikaans_words if word in text_lower)
        zu_score = sum(1 for word in zulu_words if word in text_lower)
        
        if af_score > zu_score:
            return "af"
        elif zu_score > af_score:
            return "zu"
        return "en"  # default English
    
    def get_faq_response(self, query, lang="en"):
        """Get FAQ in detected language"""
        for key, translations in self.faqs.items():
            if key in query.lower() or any(word in query.lower() for word in key.split()):
                return translations.get(lang, translations["en"])
        return None
    
    def create_ticket(self, query, language="en"):
        ticket = {
            "id": str(uuid.uuid4())[:8],
            "query": query,
            "language": language,
            "status": "new",
            "priority": "medium",
            "assigned_to": None,
            "created_at": datetime.now(),
            "resolved": False,
        }
        
        # Route to appropriate producer based on language
        if language == "af":
            ticket["assigned_to"] = self.producers[0]  # Pieter
        elif language == "zu":
            ticket["assigned_to"] = self.producers[2]  # Thabo
        else:
            ticket["assigned_to"] = self.producers[1]  # Johan
            
        self.tickets.append(ticket)
        return ticket
    
    def get_open_tickets(self):
        return [t for t in self.tickets if not t["resolved"]]
    
    def book_appointment(self, client_name, date_str, time_str, vehicle_type=""):
        appt = {
            "id": str(uuid.uuid4())[:8],
            "client": client_name,
            "vehicle": vehicle_type,
            "date": f"{date_str} {time_str}",
            "status": "confirmed",
            "service": "Rubber mat installation"
        }
        self.appointments.append(appt)
        return appt

db = DataStore()
