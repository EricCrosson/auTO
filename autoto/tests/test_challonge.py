#!/usr/bin/env python
# Written by davethecust
# 2016-06-03

import challonge
import os
import random
import string
import unittest




class TestChallonge(unittest.TestCase):

    def setUp(self):
        self.api_username = os.environ['CHALLONGE_USERNAME']
        self.api_key = os.environ['CHALLONGE_API_KEY']

        challonge.set_credentials(self.api_username, self.api_key)

        self.t = challonge.tournaments.create('AuTO Test Tournament',
                                              "autoto_" + "".join(
                                                  random.choice(
                                                      string.ascii_lowercase)
                                                  for _ in range(0, 15)))

        self.p1 = challonge.participants.create(self.t['id'],
                                                'DTMP')
        self.p2 = challonge.participants.create(self.t['id'],
                                                'hamroctopus')
        challonge.tournaments.start(self.t['id'])

    def tearDown(self):
        challonge.tournaments.destroy(self.t['id'])

    def test_get_tournament(self):
        tournament = challonge.tournaments.show(self.t['id'])
        self.assertEqual(tournament['name'], self.t['name'])

    def test_get_participants(self):
        participants = challonge.participants.index(self.t["id"])
        test_players = ['DTMP', 'hamroctopus']
        for player in participants:
            self.assertIn(player['name'], test_players)

    def test_get_matches(self):
        matches = challonge.matches.index(self.t['id'])
        self.assertEqual(len(matches), 1)

        final_match = matches[0]
        self.assertIn(self.p1['id'], [final_match['player1-id'],
                                      final_match['player2-id']])
        self.assertIn(self.p2['id'], [final_match['player1-id'],
                                      final_match['player2-id']])

    def test_update_match(self):
        matches = challonge.matches.index(self.t["id"])
        final_match = matches[0]
        self.assertEqual(final_match["state"], "open")

        challonge.matches.update(
                self.t["id"],
                final_match["id"],
                **{'scores_csv': '3-2',
                   'winner_id': final_match["player1-id"]})

        m = challonge.matches.show(self.t["id"], final_match["id"])
        self.assertEqual(m["state"], "complete")


if __name__ == '__main__':
    unittest.main()
