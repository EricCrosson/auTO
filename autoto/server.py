#!/usr/bin/env python
# Written by davethecust
# 2016-06-03

import challonge
import os
from flask import Flask, request, render_template, jsonify
from flask.ext.api import status

api_email = os.environ['CHALLONGE_USERNAME']
api_key = os.environ['CHALLONGE_API_KEY']
tournament_url = os.environ['CHALLONGE_TOURNAMENT_URL']


challonge.set_credentials(api_email, api_key)
tournament_id = challonge.tournaments.show(tournament_url)['id']
players = {p['id']: p['name']
           for p in challonge.participants.index(tournament_id)}
matches = []


app = Flask('auTO')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/matches', methods=['GET'])
def _matches():
    return jsonify({'matches': matches})

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
# challonge api weird thing, if player two wins, we need to reverse the games
# won when updating the match, you have to do things centric to player one this
# explanation probably doesn't make sense, please see the challonge api
# reference - http://api.challonge.com/v1/documents/matches/update

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
        if match['state'] == 'open' or \
        match['player1-id'] is not None or \
        match['player2-id'] is not None:
            player1_id = match['player1-id']
            player2_id = match['player2-id']

            if player1_id:
                player1 = players[player1_id]
            else:
                prereq_match = challonge.matches.show(
                    tournament_id,
                    match['player1-prereq-match-id'])
                prefix = 'Loser' if match['player1-is-prereq-match-loser'] \
                          else 'Winner'
                player1 = prefix + ' of ' + prereq_match['identifier']

            if player2_id:
                player2 = players[player2_id]
            else:
                prereq_match = challonge.matches.show(
                    tournament_id,
                    match['player2-prereq-match-id'])
                prefix = 'Loser' if match['player2-is-prereq-match-loser'] \
                          else 'Winner'
                player2 = prefix + ' of ' + prereq_match['identifier']

            matches.append({
                'match_id': match['id'],
                'bracket_position': match['identifier'],
                'player1': (player1, player1_id),
                'player2': (player2, player2_id),
                'started_at': match['started-at']
            })


def configure():
    sync_state()

if __name__ == "__main__":
    configure()
    app.run()
