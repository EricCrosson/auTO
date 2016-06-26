#!/usr/bin/env python
# written by davethecust
# 2016-06-19

import challonge
import http.client
import os
import random
import string
import unittest
from flask import request


class TestAutoTO(unittest.TestCase):
    def setUp(self):
        self.api_username = os.environ['CHALLONGE_USERNAME']
        self.api_key = os.environ['CHALLONGE_API_KEY']

        challonge.set_credentials(self.api_username, self.api_key)
        self.t = challonge.tournaments.create(
            'AuTO Test Tournament',
            "autoto_" + "".join(random.choice(string.ascii_lowercase)
                                for _ in range(0, 15)))
        self.p1 = challonge.participants.create(self.t['id'], 'DTMP')
        self.p2 = challonge.participants.create(self.t['id'], 'hamroctopus')
        challonge.tournaments.start(self.t['id'])

    def tearDown(self):
        challonge.tournaments.destroy(self.t['id'])

    def test_state_dump_of_match(self):
        conn = http.client.HTTPConnection("localhost:5000")
        body = '{"winner": "DTMP", "scores_csv": "3-1" }'
        headers = {'Content-type': 'application/json'}
        conn.request('PUT', '/dump', body, headers)
        response = conn.getresponse()

        self.assertTrue(response.getcode(), 200)


if __name__ == "__main__":
    unittest.main()
