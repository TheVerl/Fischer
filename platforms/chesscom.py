#!/usr/bin/env python3

# Import modules
from chessdotcom import *
import os, sys, json

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Checks whether the user is online or not.
def getUserStatus(username):
    if (is_player_online(username)):
        return True
    else:
        return False

# Gets the user's info.
def getUserInfo(username):
    return get_player_profile(username)

# Gets the user's statistics.
def getUserStat(username):
    return get_player_stats(username)

# Gets the user's match statistics.
def getUserMatches(username, stats):
    matches = {}
    matches["win"] = {
        "rapid": stats["chess_rapid"]["record"]["win"],
        "blitz": stats["chess_blitz"]["record"]["win"],
        "bullet": stats["chess_bullet"]["record"]["win"]
    }
    matches["loss"] = {
        "rapid": stats["chess_rapid"]["record"]["loss"],
        "blitz": stats["chess_blitz"]["record"]["loss"],
        "bullet": stats["chess_bullet"]["record"]["loss"]
    }
    matches["draw"] = {
        "rapid": stats["chess_rapid"]["record"]["draw"],
        "blitz": stats["chess_blitz"]["record"]["draw"],
        "bullet": stats["chess_bullet"]["record"]["draw"]
    }
    matches["sum"] = {
        "rapid": matches["win"]["rapid"] + matches["loss"]["rapid"] + matches["draw"]["rapid"],
        "blitz": matches["win"]["blitz"] + matches["loss"]["blitz"] + matches["draw"]["blitz"],
        "bullet": matches["win"]["bullet"] + matches["loss"]["bullet"] + matches["draw"]["bullet"],
        "win": matches["win"]["rapid"] + matches["win"]["blitz"] + matches["win"]["bullet"],
        "loss": matches["loss"]["rapid"] + matches["loss"]["blitz"] + matches["loss"]["bullet"],
        "draw": matches["draw"]["rapid"] + matches["draw"]["blitz"] + matches["draw"]["bullet"]
    }
    matches["total"] = matches["sum"]["rapid"] + matches["sum"]["blitz"] + matches["sum"]["bullet"]
    return matches

# Setup.
def setup():
    print("Chess.com module is initialised.")