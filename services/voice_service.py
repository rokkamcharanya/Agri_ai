class VoiceAgronomistService:
    """
    Multilingual AI Agronomist and Voice Assistant service.
    Generates intelligent responses in English, Telugu (te), and Hindi (hi)
    using current crop, health score, weather, disease, and risk telemetry.
    """

    @staticmethod
    def answer_query(query, lang="en", context=None):
        query_lower = (query or "").lower().strip()
        ctx = context or {}
        crop = ctx.get('crop_name', 'Paddy')
        health = ctx.get('health_score', 86)
        condition = ctx.get('condition', 'Healthy')
        disease = ctx.get('disease', 'No Significant Disease Detected')
        temp = ctx.get('temperature', 32)
        rain_prob = ctx.get('rain_probability', 60)
        location = ctx.get('location', 'Vijayawada')

        # Multi-language dictionary templates
        if lang == 'te':  # Telugu
            if any(k in query_lower for k in ["పరిస్థితి", "బాగుందా", "health", "condition", "status", "పంట"]):
                ans = f"మీ {crop} పంట ప్రస్తుతం {condition} గా ఉంది. ఆరోగ్య స్కోరు {health} శాతం. క్రమంగా నీటి పారుదల మరియు పరిశీలన కొనసాగించండి."
            elif any(k in query_lower for k in ["వర్షం", "వాన", "rain", "weather", "వాతావరణం"]):
                ans = f"{location} లో రేపు వర్షం పడే అవకాశం {rain_prob} శాతం ఉంది. ఉష్ణోగ్రత {temp} డిగ్రీల సెల్సియస్. పొలంలో నీటి పారుదల కాలువలు సిద్ధంగా ఉంచుకోండి."
            elif any(k in query_lower for k in ["వ్యాధి", "తెగులు", "disease", "yellow", "పసుపు", "మచ్చలు"]):
                ans = f"మీ పంటలో నమోదైన వ్యాధి గమనింపు: {disease}. ఆకుల వెనుక భాగంలో మచ్చలు ఉన్నాయో లేదో గమనించి, వేప నూనె పిచికారీ చేయండి."
            elif any(k in query_lower for k in ["మార్కెట్", "ధర", "ప్రాప్తి", "price", "market"]):
                ans = f"{crop} యొక్క ప్రస్తుత మార్కెట్ ధర క్వింటాలుకు ₹2,350 గా ఉంది. ట్రెండ్ సానుకూలంగా ఉంది."
            else:
                ans = f"మీ {crop} పంట ఆరోగ్య స్కోరు {health}%. వాతావరణం ఆర్ద్రత కలిగి ఉంది ({rain_prob}% వర్ష సూచన). పొలం మురుగు నీటి నివారణ చర్యలు తీసుకోండి."
                
        elif lang == 'hi':  # Hindi
            if any(k in query_lower for k in ["स्थिति", "कैसी", "स्वास्थ्य", "health", "condition", "status", "फसल"]):
                ans = f"आपकी {crop} की फसल वर्तमान में {condition} स्थिति में है। फसल स्वास्थ्य स्कोर {health}% है। नियमित सिंचाई और निगरानी बनाए रखें।"
            elif any(k in query_lower for k in ["बारिश", "मौसम", "rain", "weather"]):
                ans = f"{location} में कल बारिश की संभावना {rain_prob}% है। तापमान {temp}°C है। खेत में जल निकासी की उचित व्यवस्था करें।"
            elif any(k in query_lower for k in ["बीमारी", "रोग", "disease", "पीला", "yellow", "धब्बे"]):
                ans = f"आपकी फसल में संभावित रोग स्थिति: {disease}। पत्तियों के निचले हिस्से की जांच करें और आवश्यकतानुसार नीम तेल का छिड़काव करें।"
            elif any(k in query_lower for k in ["मंडी", "बाजार", "मूल्य", "भाव", "price", "market"]):
                ans = f"{crop} का वर्तमान मंडी भाव ₹2,350 प्रति क्विंटल है। बाजार रुझान सकारात्मक है।"
            else:
                ans = f"आपकी {crop} फसल का स्वास्थ्य स्कोर {health}% है। कल {rain_prob}% बारिश का पूर्वानुमान है। फसल का नियमित निरीक्षण करते रहें।"

        else:  # English (default)
            if any(k in query_lower for k in ["health", "condition", "status", "how is", "crop"]):
                ans = f"Your {crop} crop is currently in {condition} condition with a health score of {health}%. Maintain regular irrigation and canopy observation."
            elif any(k in query_lower for k in ["rain", "weather", "rainy", "temperature"]):
                ans = f"Rain probability in {location} is {rain_prob}% tomorrow with temperature around {temp}°C. Ensure clear field drainage channels."
            elif any(k in query_lower for k in ["disease", "yellow", "blight", "spots", "fungus", "risk"]):
                ans = f"Current disease alert for your {crop}: {disease}. Check leaves for fungal spots and consult an agronomist if symptoms spread."
            elif any(k in query_lower for k in ["market", "price", "rate", "mandi"]):
                ans = f"Current market rate for {crop} at Vijayawada market is ₹2,350/Qtl (+3.2% trend)."
            else:
                ans = f"Your {crop} crop is {condition} ({health}% score). Expected weather shows {rain_prob}% rain probability. Keep proper drainage prepared."

        return {
            "query": query,
            "language": lang,
            "response": ans
        }

    @staticmethod
    def generate_full_crop_report(lang="en", context=None):
        """Generates dynamic audio-friendly summary report of the farm status."""
        ctx = context or {}
        crop = ctx.get('crop_name', 'Paddy')
        health = ctx.get('health_score', 86)
        condition = ctx.get('condition', 'Healthy')
        disease_risk = ctx.get('disease_risk', 'Medium')
        rain_prob = ctx.get('rain_probability', 60)
        location = ctx.get('location', 'Vijayawada')

        if lang == 'te':
            return f"మీ {crop} పంట ప్రస్తుతం {health} శాతం ఆరోగ్య స్కోరుతో ఆరోగ్యంగా ఉంది. వ్యాధి ప్రమాదం {disease_risk} స్థాయిలో ఉంది. రేపు {location} లో వర్షం పడే అవకాశం {rain_prob} శాతం ఉంది. కాబట్టి నీటి పారుదల కాలువలను సరిచూసుకోండి."
        elif lang == 'hi':
            return f"आपकी {crop} की फसल वर्तमान में {health} प्रतिशत स्वास्थ्य स्कोर के साथ अच्छी स्थिति में है। बीमारी का जोखिम {disease_risk} स्तर पर है। कल {location} में {rain_prob} प्रतिशत बारिश की संभावना है, इसलिए जल निकासी का ध्यान रखें।"
        else:
            return f"Your {crop} crop is currently {condition.lower()} with a health score of {health} percent. There is a {disease_risk.lower()} disease risk. Rain probability in {location} is {rain_prob} percent, so ensure proper field drainage."
