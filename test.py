from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """Before every test"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_input_guess(self):
        with self.client:
            resp = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('high_score'))
            self.assertIsNone(session.get('num_play'))
            self.assertIn(b'<h5>Higest Score</h5>', resp.data)
            # print(session['board'])

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session["board"] = [["B", "O", "Y", "Y", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["T", "B", "T", "D", "E"],
                                           ["A", "B", "C", "L", "E"],
                                           ["A", "B", "C", "D", "E"]]
        resp = self.client.get('/check-word?word=apple')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['result'], 'ok')

    def test_invalid_word(self):
        self.client.get('/')
        resp = self.client.get('/check-word?word=something')
        self.assertEqual(resp.json['result'], 'not-on-board')

    def test_not_word(self):
        self.client.get('/')
        resp = self.client.get('/check-word?word=asd')
        self.assertEqual(resp.json['result'], 'not-word')
