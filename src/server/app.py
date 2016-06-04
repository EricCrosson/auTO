#!/usr/bin/env python
# Written by davethecust
# 2016-06-03

import sys
import pdb

import challonge
from flask import Flask

# from client/prototype_client.py import client as prototype_client

api_email = 'davethecust'
api_key = 'bMSeYjdu2GA5CtC4Dc3dPz8l6C1VgS4x5bpnV4cv'

app = Flask('auTO')


@app.route('/dump', methods=['PUT'])
def state_dump():
    pass


@app.route('/sync_state', methods=['GET'])
def sync_state():
    pass


def configure():
    challonge.set_credentials(api_email, api_key)


if __name__ == "__main__":
    configure()
    tournament_url = sys.argv[1]
    tournament = challonge.tournaments.show(tournament_url)
    app.run()
