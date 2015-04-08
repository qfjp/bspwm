#!/usr/bin/env python2
"""
Implement desktop switching in bspwm to be like xMonad (shared desktops
over multiple monitors)
"""
import sys
import subprocess
import utils
import rules

PROG_NAME = sys.argv[0]


def focus_desktop(desktop):
    """
    Bring the given desktop selector into focus

    Params:
      desktop (str): A bspwm desktop selector
    """
    subprocess.call(["bspc", "desktop", "-f", desktop])


def move_desktop_to_monitor(desktop, monitor):
    """
    Move a given desktop to a given monitor

    Params:
      desktop (str): A bspwm desktop selector
      monitor (str): A bspwm monitor selector
    """
    subprocess.call(["bspc", "desktop", desktop, "-m", monitor])


def print_usage(prog_name):
    """
    A method to print the usage of this script

    Params:
      prog_name (str): The name of the program
    """
    program = prog_name.split("/")
    program = program[len(program) - 1]
    sys.stderr.write("USAGE: %s <target_desktop>\n" % program)
    sys.exit()


def swap_desktops(desktop1, desktop2):
    """
    Swap the given desktops

    Params:
      desktop1 (str): a bspwm desktop selector
      desktop2 (str): a bspwm desktop selector
    """
    subprocess.call(["bspc", "desktop", desktop1, "-s", desktop2])


def move_window_to_desktop(target_desktop):
    """
    Moves the active window to the target desktop

    Params:
      target_desktop (str): A bspwm desktop selector
    """
    subprocess.call(['bspc', 'window', '-d', target_desktop])
    sys.exit()


def main(target_desktop_index, move=False):
    """
    The main entry point for the script
    """
    active_monitor = subprocess.check_output(["bspc", "query", "-m",
                                              "focused", "-M"])
    active_desktop = subprocess.check_output(["bspc", "query", "-d",
                                              "focused", "-D"])
    active_monitor = active_monitor.strip()
    active_desktop = active_desktop.strip()

    target_desktop = utils.get_workspcs()[target_desktop_index - 1]

    if move:
        move_window_to_desktop(target_desktop)

    # Find the target monitor
    target_monitor = utils.get_monitor(target_desktop)

    # If the target monitor is the same as active monitor,
    # we must move the target desktop to a different monitor
    # before the swap
    if target_monitor == active_monitor:
        focus_desktop(target_desktop)
    else:
        swap_desktops(target_desktop, active_desktop)
    rules.reset_rules()


try:
    TARGET_DESKTOP_INDEX = int(sys.argv[1])
except IndexError:
    print_usage(PROG_NAME)
except ValueError:
    print_usage(PROG_NAME)

try:
    MOVE = sys.argv[2]
    MOVE = True
except IndexError:
    MOVE = False

if TARGET_DESKTOP_INDEX > len(utils.get_workspcs()) or \
   TARGET_DESKTOP_INDEX < 0:
    print_usage(PROG_NAME)

main(TARGET_DESKTOP_INDEX, move=MOVE)
