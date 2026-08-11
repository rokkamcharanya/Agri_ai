import os
import sys
import unittest
import tempfile

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from database.db import init_db
from services.risk_engine import RiskEngine
from services.crop_ai import CropAIService
from services.voice_service import VoiceAgronomistService

class AgriAITestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['DATABASE_PATH'] = self.db_path
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        init_db(self.db_path)
        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_login_redirect(self):
        """Test accessing root redirects to login when unauthenticated."""
        response = self.client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_demo_login(self):
        """Test demo farmer login route."""
        response = self.client.get('/demo-login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Good Morning', response.data)

    def test_risk_engine(self):
        """Test risk engine calculation service."""
        weather = {"temperature": 34, "humidity": 82, "rain_probability": 75}
        risks = RiskEngine.calculate_crop_risks("Paddy", weather, 85, "Vijayawada")
        self.assertTrue(len(risks) > 0)
        risk_titles = [r['title'] for r in risks]
        self.assertIn("HIGH RAINFALL RISK", risk_titles)

    def test_voice_agronomist(self):
        """Test multi-language voice agronomist Q&A."""
        ctx = {"crop_name": "Paddy", "health_score": 88, "condition": "Healthy", "rain_probability": 60, "location": "Vijayawada"}
        res_en = VoiceAgronomistService.answer_query("What is the condition of my crop?", lang="en", context=ctx)
        self.assertIn("Paddy", res_en['response'])
        self.assertIn("Healthy", res_en['response'])

        res_te = VoiceAgronomistService.answer_query("నా పంట పరిస్థితి ఎలా ఉంది?", lang="te", context=ctx)
        self.assertIn("పంట", res_te['response'])

        res_hi = VoiceAgronomistService.answer_query("मेरी फसल की स्थिति कैसी है?", lang="hi", context=ctx)
        self.assertIn("फसल", res_hi['response'])

    def test_market_prices_api(self):
        """Test market prices API endpoint."""
        with self.client as c:
            c.get('/demo-login') # authenticate
            response = c.get('/api/market-prices')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('prices', data)
            self.assertTrue(len(data['prices']) > 0)

if __name__ == '__main__':
    unittest.main()
