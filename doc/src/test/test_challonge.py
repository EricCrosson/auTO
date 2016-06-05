#!/usr/bin/env python
# Written by davethecust
# 2016-06-03

import challonge
import unittest


class TestChallonge(unittest.TestCase):

    def setUp(self):
        self.api_username = 'davethecust'
        self.api_key = 'bMSeYjdu2GA5CtC4Dc3dPz8l6C1VgS4x5bpnV4cv'
        self.tournament_url = '42k5wcre'

    def test_get_tournament(self):
        challonge.set_credentials(self.api_username, self.api_key)
        tournament = challonge.tournaments.show(self.tournament_url)
        self.assertEqual(tournament['name'], 'test')

    def test_get_participants(self):
        challonge.set_credentials(self.api_username, self.api_key)
        tournament = challonge.tournaments.show(self.tournament_url)
        participants = challonge.participants.index(tournament["id"])

        test_players = ['DTMP', 'zaxtorp', 'hamroctopus', 'davethecust']
        for player in participants:
            self.assertIn(player['name'], test_players)


if __name__ == '__main__':
    unittest.main()
