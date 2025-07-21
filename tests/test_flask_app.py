import unittest
from flask_app.app import app

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()


    #if webpage loaded or not means status code is 200
    #if page loaded has title sentiment analysis
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Sentiment Analysis</title>', response.data)

    #if webpage loaded or not means status code is 200
    #test if output matches
    def test_predict_page(self):
        response = self.client.post('/predict', data=dict(text="I love this!"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b'Happy' in response.data or b'Sad' in response.data,
            "Response should contain either 'Happy' or 'Sad'"
        )

if __name__ == '__main__':
    unittest.main()