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
Version = "1.1.0"

BAD_WORDS_LIST = [
    "kappa", "lul", "pogchamp", "poggers", "kewk", "PJSalt", "TriHard", "GayPride", "monkaS", "<3", "NotLikeThis",
    "biblethump", "FeelsBadMan", "FeelsGoodMan", "Kreygasm", "SwiftRage", "ResidentSleeper", "Keepo", "DansGame",
    ":)", ":(", ";-)", ";)", ":D", "D:", ":O"
]

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
            "acceptLimit": 5,
            "resultPm": "FrittenfettSenpai",
            "languageStartGame": "/me Chatduell gestartet. Deine nächste Nachricht wird gewertet.'",
            "languageEndGame": "/me Chatduell Runde Ende. Keine Nachrichten werden mehr akzeptiert.'",
        }
    ResetGame()
    return


# ---------------------------------------
#   [Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
    global settings, activeFor, userDict, wordDict

    if data.IsWhisper():
        user = data.User
        if Parent.HasPermission(user, "Caster", "") is True:
            command = data.GetParam(0)
            if command == settings["command"]:
                activeFor = int(settings['gameLength'])
                Parent.SendTwitchMessage(settings["languageStartGame"])
                return
    if data.IsChatMessage() and activeFor > 0:
        user = data.User
        #if user in userDict:
        #    return
        userDict[user] = 1

        message = data.Message.lower()
        for word in BAD_WORDS_LIST:
            message = message.replace(word.lower(), "")

        if message in wordDict:
            wordDict[message] = wordDict[message] + 1
        else:
            wordDict[message] = 1
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
    if activeFor == 0:
        # Game end
        Parent.SendTwitchMessage(settings["languageEndGame"])

        fullCount = 0
        sortedDict = sorted(wordDict.items(), key=operator.itemgetter(1), reverse=True)

        result = []
        keyCount = 0
        for key, value in sortedDict:
            keyCount = keyCount + 1
            if keyCount > settings["acceptLimit"]:
                break
            fullCount = fullCount + int(value)

        keyCount = 0
        for key, value in sortedDict:
            keyCount = keyCount + 1
            if keyCount > settings["acceptLimit"]:
                break
            result.append({
                "word": key,
                "count": int(value),
                "percent": int(float(value) / float(fullCount) * 100)
            })

        Parent.SendStreamWhisper(settings["resultPm"], str(result))
        ResetGame()
    return


def ResetGame():
    global activeFor, userDict, wordDict
    activeFor = 0
    userDict = {}
    wordDict = {}
