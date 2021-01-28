#!/usr/bin/env python3

import berserk
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Gets the user.
def getUser(username):
    return(client.users.get_public_data(username))

# Setup.
def setup():
    with open("lichess.token") as f:
        token = f.read()
    f.close()
    global session
    global client
    session = berserk.TokenSession(token)
    client = berserk.Client(session)
    print("Lichess module is initialised.")