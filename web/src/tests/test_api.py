from project import app
import unittest
from flask import Response
import json

class TestApi(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_big(self):
        p1_id = new_player_id(self.client)
        p2_id = new_player_id(self.client)
        game = self.client.get('/game/create')


def new_player_id(client):
    res = client.get('/register/web_player')
    dict_res = json.loads(res.get_data(as_text=True))
    return dict_res['data']['player_id']