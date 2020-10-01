# -*- coding: utf-8 -*-
# ---------------------------------------
#   Import Libraries
# ---------------------------------------
import clr
import re
import json
import codecs
import os
import time
import operator

clr.AddReference("IronPython.Modules.dll")

# ---------------------------------------
#   [Required]  Script Information
# ---------------------------------------
ScriptName = "Chatduell"
Website = "https://www.twitch.tv/frittenfettsenpai"
Description = "Chatduell Quizshow"
Creator = "frittenfettsenpai"
Version = "0.1.0"


# ---------------------------------------
#   [Required] Intialize Data (Only called on Load)
# ---------------------------------------
def Init():
    global settings
    settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")

    try:
        with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
            settings = json.load(f, encoding="utf-8")
            f.close()
    except:
        settings = {
            "command": "!chatduellStart",
            "gameLength": 60,
            "languageStartGame": "/me Chatduell gestartet. Deine nächste Nachricht wird gewertet.'",
            "languageEndGame": "/me Chatduell Runde Ende. Keine Nachrichten werden mehr akzeptiert.'",
        }
    ResetGame()
    return


# ---------------------------------------
#   [Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
    global settings, activeFor, userDict, wordDict, counter

    if data.IsWhisper():
        user = data.User
        if Parent.HasPermission(user, "Caster", "") is True:
            command = data.GetParam(0).lower()
            if command == settings["command"]:
                activeFor = settings['activeFor']
                Parent.SendTwitchMessage(settings["languageStartGame"])
                return
    if data.IsChatMessage() and activeFor > 0:
        user = data.User
        if user in userDict:
            return
        userDict[user] = 1

        message = data.Message.lower()
        if message in wordDict:
            wordDict[message] = wordDict[message] + 1
        else:
            wordDict[message] = 1
        counter = counter + 1
    return


# ---------------------------------------
#	[Required] Tick Function
# ---------------------------------------
def Tick():
    global settings, activeFor, wordDict

    time.sleep(1)
    if activeFor == 0:
        return

    activeFor = activeFor - 1
    if activeFor > 0:
        activeFor = activeFor - 1
    else:
        # Game end
        Parent.SendTwitchMessage(settings["languageEndGame"])

        #{k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
        #import collections
        #sorted_dict = collections.OrderedDict(sorted_x)
        result = sorted(wordDict.items(), key=operator.itemgetter(1))
        datafile = os.path.join(os.path.dirname(__file__), "result.json")
        try:
            with codecs.open(datafile, encoding="utf-8-sig", mode="w") as f:
                f.write(json.dumps(result))
                f.close()
        except:
            return
        ResetGame()
    return


def ResetGame():
    global activeFor, userDict, wordDict, counter
    activeFor = 0
    counter = 0
    userDict = {}
    wordDict = {}
