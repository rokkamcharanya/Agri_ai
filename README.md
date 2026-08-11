# 🌱 AgriAI — AI-Powered Smart Agriculture Platform

AgriAI is a realistic, production-style, full-stack decision-support web platform built with Python Flask, SQLite, HTML5/CSS3, JavaScript, Chart.js, and browser Web Speech APIs.

Designed for modern farming, AgriAI acts as an intelligent real-time bridge between raw field conditions and agronomic guidance.

---

## 🌟 Key Features

1. **Farmer Authentication & 1-Click Demo**:
   - Secure register/login system using Werkzeug password hashing.
   - 1-Click "Demo Farmer Login" for instant testing without manual registration.

2. **Responsive Hackathon-Quality Dashboard**:
   - Clean agricultural design system (emerald green accents, rounded cards, soft shadows).
   - Real-time welcome header, crop summary cards, and dynamic health status rings.

3. **📷 AI Crop Leaf Image Analysis**:
   - Upload leaf or field images via drag-and-drop or file selector.
   - Pillow-based feature inspection engine calculating greenness ratio, lesion density, and spot metrics.
   - Modular AI service layer (`crop_ai.py`) ready for deep learning model integration (PyTorch/TensorFlow).
   - Generates crop condition, health percentage (0-100), possible disease alerts, AI confidence %, and actionable agronomist recommendations.
   - Saves all analysis history to SQLite database.

4. **⚠️ Predictive Risk Engine (`RiskEngine`)**:
   - Dynamic `calculate_crop_risks()` backend service.
   - Generates severity-coded warnings (🔴 High Rainfall, 🟠 Disease Risk, 🟡 Water Stress, 🟢 Stable Conditions) based on crop, weather telemetry, health, and location.

5. **🌦️ Weather & Geolocation Telemetry**:
   - Browser Geolocation API integration with automatic reverse geocoding.
   - Manual farm location picker modal.
   - Live OpenWeatherMap API support with fallback demo weather feed.

6. **📊 Interactive 7-Day Crop & Climate Chart**:
   - Built using Chart.js.
   - Interactive toggle buttons to switch between **Crop Health %**, **Temperature (°C)**, and **Rainfall Probability (%)**.

7. **🤖 Multilingual AI Agronomist & Voice Assistant**:
   - Text & Voice question input support.
   - Native Web Speech API integration (Speech Recognition & Speech Synthesis).
   - Full support for **English**, **Telugu (తెలుగు)**, and **Hindi (हिन्दी)**.
   - Dynamic audio report generator (`🔊 Listen to Report`) reading live dashboard data.

8. **💰 Live Agricultural Market Prices**:
   - Displays mandi prices, crop varieties, unit rates, and price trend indicators (📈 / 📉).
   - Highlights the farmer's current crop.
   - Service layer (`market_service.py`) ready for live Agmarknet API integration.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask, SQLite3, Werkzeug, Pillow, Requests
- **Frontend**: HTML5, CSS3 (Vanilla CSS variables), Bootstrap 5, JavaScript (ES6+), Chart.js
- **Voice Telemetry**: Browser Web Speech API (`SpeechRecognition`, `SpeechSynthesis`)
- **Database**: SQLite3 (`agri_ai/database/database.db`)

---

## 📁 Project Structure

```
agri_ai/
├── app.py                  # Main Flask entry point
├── config.py               # Application configuration
├── requirements.txt        # Python package dependencies
├── .env.example            # Sample environment variables
├── README.md               # Documentation
│
├── database/
│   ├── db.py               # Database initialization & seeds
│   └── database.db         # SQLite database file
│
├── models/
│   ├── user.py             # User authentication model
│   ├── farm.py             # Farm & location model
│   ├── crop_analysis.py    # Crop analysis history model
│   ├── weather.py          # Weather telemetry model
│   └── market.py           # Market prices model
│
├── services/
│   ├── crop_ai.py          # AI image analysis engine
│   ├── weather_service.py  # Weather API & fallback service
│   ├── risk_engine.py      # Dynamic risk engine
│   ├── market_service.py   # Market prices service
│   └── voice_service.py    # Multilingual AI Q&A service
│
├── routes/
│   ├── auth.py             # Auth & demo login routes
│   ├── dashboard.py        # Dashboard view route
│   ├── crop.py             # Crop image analysis API
│   ├── weather.py          # Weather & location APIs
│   ├── market.py           # Market prices API
│   └── voice.py            # AI Agronomist & Voice APIs
│
├── templates/
│   ├── login.html          # Login view
│   ├── register.html       # Register view
│   └── dashboard.html      # Main dashboard view
│
├── static/
│   ├── css/
│   │   └── style.css       # Agriculture UI styles
│   ├── js/
│   │   ├── dashboard.js    # UI translations & location script
│   │   ├── voice.js        # Speech API voice assistant
│   │   ├── crop.js         # Image upload & score circle animation
│   │   └── chart.js        # Chart.js graph configuration
│   └── uploads/            # Uploaded crop images directory
│
└── tests/
    └── test_app.py         # Pytest / unittest suite
```

---

## 🚀 Installation & Running

### 1. Prerequisites
- Python 3.8+ installed on your system.

### 2. Set Up Virtual Environment

```bash
# Navigate to project folder
cd agri_ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

To enable live weather data, add your OpenWeatherMap API key:
```env
WEATHER_API_KEY=your_openweathermap_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`.

Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 💡 How to Use

1. **Login / Test Demo**:
   - Click **"1-Click Demo Farmer Login"** on the login page to immediately log in as Farmer Ramesh.
2. **Scan a Crop**:
   - In the **📷 CROP ANALYSIS** card, click **"Choose Leaf Image"** or drag-and-drop a crop leaf photo.
   - Click **"🔍 Analyze Crop"** to see instant crop health %, condition, disease risk, AI confidence, and recommendations.
3. **Change Language**:
   - Select **English**, **తెలుగు (Telugu)**, or **हिन्दी (Hindi)** from the top navbar language dropdown.
   - Dashboard labels, AI agronomist responses, and voice speech output update instantly.
4. **Voice Assistance**:
   - Click **"🎤 Start Voice Command"** and speak your question in the selected language.
   - Click **"🔊 Listen to Report"** to hear a complete dynamic summary of your field condition.
5. **Interactive Graphs & Market Prices**:
   - Toggle graph metrics between Crop Health, Temperature, and Rainfall.
   - Scroll down to view local market price trends for Paddy, Chilli, Cotton, Groundnut, and Maize.

---

## 🧪 Running Unit Tests

```bash
python -m unittest tests/test_app.py
```

---

## 🛡️ License & Disclaimer

AgriAI is designed as an agronomic decision-support tool for educational and hackathon demonstrations. AI suggestions should be verified with local agricultural extension officers before applying treatments.
