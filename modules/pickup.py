#!/usr/bin/env python3

"""
Pickup game (PUG) module for Pork Jr.

Authors: Simon Laroche, byce
"""

from random import sample

topic = "Welcome to #warsow.na!"
pickup_server = "connect darkbox.us:44430;password pickupftw"

pickup_slots = {
    "bomb"   : 10,
    "ctf"    : 8,
    "ca"     : 8,
    "tdm"    : 8,
    "tdm2v2" : 4
}

pickup_games = {
    "bomb"   : {},
    "ctf"    : {},
    "ca"     : {},
    "tdm"    : {},
    "tdm2v2" : {}
}

def module_reloaded(irc):
    refresh_topic(irc)

def module_update(irc, msg):
    global topic

    if msg[1] == "PRIVMSG" and msg[2] == irc.home and msg[3][:2] in (":.", ":!"):
        nick, host = msg[0].lstrip(":").split("!")
        if msg[3][2:] == "add":
            command_add(irc, nick, host, msg[4:len(msg)])
        elif msg[3][2:] == "remove":
            command_remove(irc, nick, host, msg[4:len(msg)])
        elif msg[3][2:] == "who":
            command_who(irc, nick, msg[4:len(msg)])
        elif msg[3][2:] == "topic" and (nick, host) == irc.owner:
            set_topic(" ".join(msg[4:len(msg)]))
            refresh_topic(irc)

    if msg[1] == "PART" and msg[2] == irc.home:
        nick, host = msg[0].lstrip(":").split("!")
        command_remove(irc, nick, host, [])

    if msg[1] == "QUIT" and msg[2] == irc.home:
        nick, host = msg[0].lstrip(":").split("!")
        command_remove(irc, nick, host, [])

    if msg[1] == "NICK" and msg[2] == irc.home:
        host = msg[0].lstrip(":").split("!")[1]
        nick_change(host, msg[2][1:])

    if msg[1] == "JOIN" and msg[2] == irc.home:
        nick = msg[0].lstrip(":").split("!")[0]
        if nick == irc.nick:
            refresh_topic(irc)

def set_topic(new_topic):
    global topic
    topic = new_topic

def nick_change(host, new_nick):
    """Update nicks in pickup_games."""
    for i in pickup_games:
        if host in pickup_games[i]:
            pickup_games[i][host] = new_nick

def values(d):
    """Return a list of values from a dict."""
    return list(d.values())

def command_add(irc, nick, host, games):
    """Add to pickups."""
    valid = False
    if len(games) == 0:
        for i in pickup_games:
            if host not in pickup_games[i]:
                pickup_games[i][host] = nick
                valid = True

    elif games[0] in pickup_games:
        for i in games:
            if i in pickup_games and nick not in pickup_games[i]:
                pickup_games[i][host] = nick
                valid = True

    # Check for full pickup
    for i in pickup_games:
        if len(pickup_games[i]) == pickup_slots[i]:
            pickup_start(irc, i)

    if valid:
        # TODO If a pickup was started make this not exec
        refresh_topic(irc)

def command_remove(irc, nick, host, games):
    valid = False
    while True:
        if len(games) == 0:
            for i in pickup_games:
                if host in pickup_games[i]:
                    del pickup_games[i][host]
                    valid = True
            break
        for i in games:
            if i in pickup_games and host in pickup_games[i]:
                del pickup_games[i][host]
                valid = True
        break

    if valid:
        refresh_topic(irc)

def command_who(irc, nick, games):
    """Sends a notice to the user listing the added players."""
    who_list = ""

    if len(games) == 0:
        for i in pickup_games:
            temp = "\x0310{}: \x0F{} ".format(i, "/".join(values(pickup_games[i])))
            who_list += temp

    elif games[0] in pickup_games:
        for i in games:
            if i in pickup_games:
                temp = "\x0310{}: \x0F{} ".format(i, "/".join(values(pickup_games[i])))
                who_list += temp

    irc.notice(who_list, nick)

def pickup_start(pickup):
    captains = ", ".join(sample(values(pickup_games[pickup]), 2))
    irc.privmsg("\x0310Game ready @\x0F {}\x0310 - Players:\x0F {}\x0310 \
Captains:\x0F {}".format(pickup_server, ", ".join(values(pickup_games[pickup])), captains), irc.home)
    # Remove players that are playing in this pickup from the lists.
    for i in pickup_games[pickup].copy():
        for j in pickup_games:
            if i in pickup_games[j]:
                del pickup_games[j][i]
    pickup_games[pickup] = {}
    refresh_topic(mask)

def refresh_topic(irc):
    #TODO: Only refresh if changed
    #TODO: get old topic after reconnecting
    #TODO: Format this better
    full_topic = "\x0310> Bomb\x0F " + str(len(pickup_games["bomb"])) +"/"+ str(pickup_slots["bomb"]) + \
            ",\x0310 CTF\x0F " + str(len(pickup_games["ctf"])) +"/"+ str(pickup_slots["ctf"]) + \
            ",\x0310 CA\x0F " + str(len(pickup_games["ca"])) +"/"+ str(pickup_slots["ca"]) + \
            ",\x0310 TDM\x0F " + str(len(pickup_games["tdm"])) +"/"+ str(pickup_slots["tdm"]) + \
            ",\x0310 TDM2v2\x0F " + str(len(pickup_games["tdm2v2"])) +"/"+ str(pickup_slots["tdm2v2"]) + \
            " | " + topic

    if irc.authed:
        irc.qtopic(full_topic)
    else:
        irc.privmsg(full_topic, irc.home)
