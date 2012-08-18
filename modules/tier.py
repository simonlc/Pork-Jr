#!/usr/bin/env python3

"""
Warsow player tier module for Pork Jr.

Authors: byce, Simon Laroche
"""

import bs4
import urllib.request

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

            #if len(msg[5:len(msg)]) > 0:
            #    irc.privmsg(command_tier(irc, player, gametype), msg[2])
            #else:
            #    irc.privmsg(command_tier(irc, player), msg[2])

def command_tier(irc, player, gametype="duel"):
    """Fetches the tier of the player for the specified gametype."""
    if gametype == "tdm":
        gametype = "Team Deathmatch"
    elif gametype == "ca":
        gametype = "Clan Arena"
    elif gametype == "da":
        gametype = "Duel Arena"
    elif gametype == "bomb":
        gametype = "Bomb & Defuse"
    elif gametype == "ffa":
        gametype = "Free For All"
    elif gametype == "ctf":
        gametype = "Capture The Flag"
    elif gametype == "tdo":
        gametype = "Team Domination"

    req = urllib.request.Request("http://www.warsow.net/wmm/profile/" + player)
    html = urllib.request.urlopen(req).read()

    soup = bs4.BeautifulSoup(html)
    gametypes = soup.findAll("div", "gametypeBars")

    if not len(gametypes):
        return "\x0310> \x0FUnknown player."

    for gt in gametypes:
        if gt.find("small").find(text=True).lower() == gametype.lower():
            tag = gt.find("div", "tierBarLegend").find(text=True)
            tier = tag.strip().split("\xa0")[1]
            return "\x0310> \x0F{} is tier {} in {}.".format(player, tier, gametype)
    return "\x0310> \x0F{} has no stats for that gametype.".format(player)
