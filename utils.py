#!/usr/bin/env python
"""
Contains workspace names for bspwm
"""
import subprocess


def get_workspcs():
    """
    Returns a list of workspace names
    """
    return ["1 fire", "2 scien", "3 delg", "4 chrome", "5 game",
            "6 btc", "7 sec", "8 phone", "9 blank", "10 blank"]


def get_monitors():
    """
    Returns a list of available monitors
    """
    monitor_string = subprocess.check_output(["bspc", "query", "-M"])
    monitor_string = monitor_string.decode('ascii')
    monitor_list = []
    for monitor in monitor_string.split():
        monitor_list.append(monitor)
    return monitor_list


def get_monitor(target_desktop):
    """
    Params:
      A desktop selector

    Return:
      The monitor for which target_desktop is a node
    """
    desktop_names = get_current_desktops()
    cur_desktop = ''
    tree = subprocess.check_output(['bspc', 'query', '-T'])
    tree = tree.decode('utf-8')
    for line in tree.split('\n'):
        try:
            firstchar = line[0]
        except IndexError:
            # blank line in the tree, so skip it
            continue

        if firstchar != ' ' and firstchar != '\t':
            # This is a monitor
            cur_monitor = line.split()[0]
        else:
            desktop_num = line.split()[0]
            desktop_nam = line.split()[1]
            tntv_desktop = '{} {}'.format(desktop_num, desktop_nam)
            if tntv_desktop in desktop_names:
                cur_desktop = tntv_desktop
        if cur_desktop == target_desktop:
            return cur_monitor


def get_current_desktops():
    """
    Gives a list of the current desktops as reported by bspwm (in
    order of usage)
    """
    desktop_names = []
    desktops = subprocess.check_output(['bspc', 'query', '-D'])
    desktops = desktops.decode('utf-8')
    desktops = desktops.strip()
    for desktop in desktops.split('\n'):
        desktop_names.append(desktop)
    return desktop_names
