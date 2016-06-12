#!/usr/bin/env python
# Written by davethecust
# 2016-06-03

import challonge
from flask import Flask, request
from flask.ext.api import status

api_email = 'davethecust'
api_key = 'bMSeYjdu2GA5CtC4Dc3dPz8l6C1VgS4x5bpnV4cv'
tournament_url = '42k5wcre'


challonge.set_credentials(api_email, api_key)
tournament_id = challonge.tournaments.show(tournament_url)['id']
players = {p['id']: p['name']
           for p in challonge.participants.index(tournament_id)}
matches = []


app = Flask('auTO')


# method takes in a state from the tournament and updates challonge
# state_dump should be passed the following data via http PUT
#
# {
#   'winner': string,
#   'scores_csv': string ex, "3-1"
# }
#
# i'm making the assumption the UI will have text boxes for
# 'tag' and 'games won', 'games lost'
# where for example, tag = hamroctopus, games won = 3, games lost = 1
# in the front end we put together a json object that is similar to the above
#
# challonge api weird thing, if player two wins, we need to reverse the games won
# when updating the match, you have to do things centric to player one
# this explanation probably doesn't make sense,
# please see the challonge api reference -
#   http://api.challonge.com/v1/documents/matches/update

@app.route('/dump', methods=['PUT'])
def state_dump():
    data = request.json
    winner_tag = ''
    scores = ''

    if 'winner' in data:
        winner_tag = data['winner']
    if 'scores_csv' in data:
        scores = data['scores_csv']

    for match in matches:
        if match['player1'][0] == winner_tag:
            challonge.matches.update(tournament_id, match['match_id'],
                                     **{'scores_csv': scores,
                                        'winner_id': match['player1'][1]})
        if match['player2'][0] == winner_tag:
            challonge.matches.update(tournament_id, match['match_id'],
                                     **{'scores_csv': scores[::-1],
                                        'winner_id': match['player2'][1]})

    sync_state()

    return '', status.HTTP_200_OK

def sync_state():
    global matches
    for match in challonge.matches.index(tournament_id):
        if match['state'] == 'open':
            matches.append({
                'match_id': match['id'],
                'player1': (players[match['player1-id']],
                            match['player1-id']),
                'player2': (players[match['player2-id']],
                            match['player2-id']),
                'started_at': match['started-at']
            })


def configure():
    sync_state()

if __name__ == "__main__":
    configure()
    app.run()
