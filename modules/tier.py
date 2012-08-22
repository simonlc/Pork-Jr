#!/usr/bin/env python3

"""
Warsow player tier module for Pork Jr.

Authors: byce, Simon Laroche
"""

import bs4
from urllib.request import urlopen

def module_update(irc, msg):
    if msg[1] == "PRIVMSG" and msg[3][:2] in (":.", ":!"):
        if msg[3][2:] in ("t", "tier"):
            if len(msg) == 5:
                player = msg[4]
                irc.privmsg(command_tier(irc, player), msg[2])
            elif len(msg) > 5:
                player = msg[4]
                gametype = " ".join(msg[5:len(msg)])
                irc.privmsg(command_tier(irc, player, gametype), msg[2])
            else:
                irc.privmsg("\x0310> \x0FUsage: .tier <player> [<gametype>]", msg[2])

def command_tier(irc, player, gametype="duel"):
    """Fetches the tier of the player for the specified gametype."""
    gametypes = {
        'tdm':  'Team Deathmatch',
        'ca':   'Clan Arena',
        'da':   'Duel Arena',
        'bomb': 'Bomb & Defuse',
        'ffa':  'Free For All',
        'ctf':  'Capture The Flag',
        'tdo':  'Team Domination',
    }

    if gametype in gametypes.keys():
        gametype = gametypes.get(gametype)

    url = "http://www.warsow.net/wmm/profile/" + player

    try:
        html = urlopen(url).read()

        soup = bs4.BeautifulSoup(html)
        gametypeBars = soup.findAll("div", "gametypeBars")

        if not len(gametypeBars):
            return "\x0310> \x0FUnknown player."

        for gt in gametypeBars:
            if gt.find("small").find(text=True).lower() == gametype.lower():
                tag = gt.find("div", "tierBarLegend").find(text=True)
                tier = tag.strip().split("\xa0")[1]
                return "\x0310> \x0F{} is tier {} in {}.".format(player, tier, gametype)
    except:
        return "\x0310> \x0F{} is not a valid name.".format(player)

    return "\x0310> \x0F{} has no stats for that gametype.".format(player)
