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
import random

clr.AddReference("IronPython.Modules.dll")

# ---------------------------------------
#   [Required]  Script Information
# ---------------------------------------
ScriptName = "Chatduell"
Website = "https://www.twitch.tv/frittenfettsenpai"
Description = "Chatduell Quizshow"
Creator = "frittenfettsenpai"
Version = "0.0.1"


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
            "pickCommand": "!chatduellPick",
        }
    ResetGame()
    return


# ---------------------------------------
#   [Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
    global settings, activeFor

    if data.IsWhisper():
        user = data.User
        command = data.GetParam(0).lower()
        if command == settings["command"]:
            activeFor = settings['activeFor']
            return
        if command == settings["pickCommand"]:
            choice = int(data.GetParam(1))
            return
    return


# ---------------------------------------
#	[Required] Tick Function
# ---------------------------------------
def Tick():
    global settings, activeFor

    time.sleep(1)
    if activeFor == 0:
        return

    activeFor = activeFor - 1
    if activeFor > 0:
        activeFor = activeFor - 1
    else:
        # Game end
        message = "Nothing happend AAAA"
        Parent.SendTwitchMessage(message)
        ResetGame()
    return


def ResetGame():
    global activeFor
    activeFor = 0
