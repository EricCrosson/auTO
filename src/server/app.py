import challonge
from flask import Flask, request

api_email = 'davethecust'
api_key = 'bMSeYjdu2GA5CtC4Dc3dPz8l6C1VgS4x5bpnV4cv'
tournament_url = '42k5wcre'
tournament_id = challonge.tournaments.show(tournament_url)['id']
players = []
matches = []
app = Flask('auTO')

# method takes in a state from the tournament and updates challonge
# state_dump should be passed the following data via http PUT
#
# {
#   'winner_id': int,
#   'scores_csv': string - "3-1"
# }
@app.route('/dump', methods=['PUT'])
def state_dump():
    print(request.data)


def sync_state():
    players = {p['id']: p['name']
               for p in challonge.participants.index(tournament_id)}

    matches = [{
                   'match_id': match['id'],
                   'player1': (players[match['player1-id']], match['player1-id']),
                   'player2': (players[match['player2-id']], match['player2-id'])
               }
               for match in challonge.matches.index(tournament_id)]


def configure():
    challonge.set_credentials(api_email, api_key)

if __name__ == "__main__":
    configure()
    app.run()
