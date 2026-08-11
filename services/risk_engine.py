class RiskEngine:
    @staticmethod
    def calculate_crop_risks(crop, weather, crop_health, location):
        """
        Dynamically generates upcoming farm risk alerts based on crop type, weather telemetry,
        health score, and geography.
        """
        risks = []
        temp = weather.get('temperature', 30)
        humidity = weather.get('humidity', 70)
        rain_prob = weather.get('rain_probability', 50)
        health = crop_health if crop_health is not None else 85
        crop_name = (crop or 'Paddy').capitalize()

        # 1. High Rainfall & Waterlogging Risk
        if rain_prob >= 65:
            risks.append({
                "title": "HIGH RAINFALL RISK",
                "severity": "🔴 Critical" if rain_prob >= 80 else "🔴 High",
                "timing": "Tomorrow",
                "description": f"Heavy rainfall forecast ({rain_prob}% probability) in {location}. High risk of waterlogging for {crop_name}.",
                "recommendation": "Prepare proper field drainage channels immediately to prevent root rot.",
                "color_code": "red"
            })
        elif rain_prob >= 40:
            risks.append({
                "title": "MODERATE RAIN ALERT",
                "severity": "🟡 Medium",
                "timing": "Next 48 Hours",
                "description": f"Moderate rainfall expected ({rain_prob}% probability).",
                "recommendation": "Postpone pesticide spraying until dry clear weather.",
                "color_code": "yellow"
            })

        # 2. Fungal / Leaf Disease Risk
        if humidity >= 70 and temp >= 24:
            risks.append({
                "title": "FUNGAL DISEASE RISK",
                "severity": "🟠 High" if humidity > 80 else "🟠 High",
                "timing": "Next 3–5 Days",
                "description": f"High humidity ({humidity}%) and temperature ({temp}°C) create optimal conditions for fungal blast and leaf blight in {crop_name}.",
                "recommendation": "Inspect leaf undersides for brownish lesions. Apply recommended organic neem spray if spots appear.",
                "color_code": "orange"
            })
        elif health < 75:
            risks.append({
                "title": "CROP VULNERABILITY ALERT",
                "severity": "🟡 Medium",
                "timing": "Immediate",
                "description": f"Current crop health is at {health}%. Plant immunity to local pathogens is reduced.",
                "recommendation": "Apply bio-stimulants or micro-nutrients as per agronomic guidelines.",
                "color_code": "yellow"
            })

        # 3. High Temperature & Moisture Stress Risk
        if temp >= 35:
            risks.append({
                "title": "HEAT & WATER STRESS RISK",
                "severity": "🔴 Critical" if temp >= 38 else "🟠 High",
                "timing": "Next 2 Days",
                "description": f"High temperature ({temp}°C) will accelerate evapotranspiration and reduce soil moisture.",
                "recommendation": "Schedule early morning or evening light irrigation to protect root systems.",
                "color_code": "orange" if temp < 38 else "red"
            })
        else:
            risks.append({
                "title": "WATER STRESS RISK",
                "severity": "🟡 Medium",
                "timing": "Next 2 Days",
                "description": "Temperature fluctuations may cause transient soil moisture drop.",
                "recommendation": "Check soil moisture at root depth regularly before next watering cycle.",
                "color_code": "yellow"
            })

        # 4. Low Risk Baseline if no severe risks detected
        if len(risks) == 0:
            risks.append({
                "title": "STABLE FARM CONDITIONS",
                "severity": "🟢 Low",
                "timing": "Next 7 Days",
                "description": f"Weather and health metrics for {crop_name} in {location} remain within optimal ranges.",
                "recommendation": "Continue standard crop management routine.",
                "color_code": "green"
            })

        return risks
