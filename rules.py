#!/usr/bin/env python
"""
Set bspwm rules (e.g. which window classes should float)
"""
import os
import subprocess
import utils

BSPACE1 = ["Iceweasel", "MainBrowser", "Firefox", "qutebrowser"]
BSPACE2 = []
BSPACE3 = ["Deluge"]
BSPACE4 = ["Chromium", "chromium-browser"]
BSPACE5 = ["Steam"]
BSPACE6 = []
BSPACE7 = ["Vidalia"]
BSPACE8 = ["Skype"]
BSPACE9 = []
BSPACE0 = []

FLOATS = ["mplayer2", "mpv", "Steam", "Skype", "Tk", "Vlc", "Eclipse", "Java", "GraphDisplay"]


def set_float_rule(class_g):
    """
    Set a particular window class to float

    Params:
      class_g (str): A window class (can find from 'xprop')
    """
    subprocess.call(["bspc", "rule", "-r", class_g])
    subprocess.call(["bspc", "rule", "-a", class_g, "floating=on"])


##
#
# @param lst     A list of class variables
# @param desktop The environment variable that corresponds to the name
#                of the workspace we want to have the rule for
def set_move_rule(lst, desktop):
    """
    Set a list of window classes to only be opened on a particular
    desktop

    Params:
      lst (list): A list of window classes
      desktop (str): A bspwm desktop selector
    """
    for class_g in lst:
        # remove the old rules
        subprocess.call(["bspc", "rule", "-r", class_g])

        # Find the index of the desktop to move to (+1 -> python is 0 indexed
        #                                           and bspc is 1 indexed)
        d_index = utils.get_current_desktops().index(desktop) + 1

        # Add the new rules
        subprocess.call(["bspc", "rule", "-a", class_g, "desktop=^{}".format(d_index)])
        if desktop in FLOATS:
            set_float_rule(class_g)


def reset_rules():
    """
    Reset the bspwm rules
    """
    for class_g in FLOATS:
        set_float_rule(class_g)
    set_move_rule(BSPACE1, os.environ['BSPACE1'])
    set_move_rule(BSPACE2, os.environ['BSPACE2'])
    set_move_rule(BSPACE3, os.environ['BSPACE3'])
    set_move_rule(BSPACE4, os.environ['BSPACE4'])
    set_move_rule(BSPACE5, os.environ['BSPACE5'])
    set_move_rule(BSPACE6, os.environ['BSPACE6'])
    set_move_rule(BSPACE7, os.environ['BSPACE7'])
    set_move_rule(BSPACE8, os.environ['BSPACE8'])
    set_move_rule(BSPACE9, os.environ['BSPACE9'])
    set_move_rule(BSPACE0, os.environ['BSPACE0'])
