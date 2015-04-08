#!/usr/bin/env python
"""
Parses the window string from bspwm fifo
"""
import sys
import subprocess

FOCUSED_WORKSPACE = subprocess.check_output(["bspc", "query", "-d", "focused", "-D"])
FOCUSED_WORKSPACE = FOCUSED_WORKSPACE.decode('utf-8')
FOCUSED_WORKSPACE = FOCUSED_WORKSPACE.strip()

COLORS = {"ltest_bg"      : '#d0d0d0',
          "ltest_fg"      : '#303030',
          "lter_bg"       : '#585858',
          "lter_fg"       : '#303030',
          "red_bg"        : '#ac0000',
          "blue_fade_bg"  : '#00627f',
          "blue_fade_fg"  : '#8ea5ab',
          "blue_bg"       : '#0097af',
          "blue_fg"       : '#d2eaf0',
          "fg"            : '#999d9d',
         }


## Find the sort key for the workspace
#
# @param rawKey The tuple (workspace, flag), where workspace is a
#               string of the form "%d %s"
def get_sort_key(raw_key):
    """
    Find the sort key for the workspace

    Params:
      raw_key (tuple): The tuple (workspace, flag), where
                       workspace is a string of the form "%d %s"
    """
    workspace = raw_key[0]
    sort_key = int(workspace.split()[0])
    return sort_key


def decorate_field(field, flag, next_flag=None):
    """
    Adds colors and decorators to the fields, as appropriate

    Params:
      field (str): A token within the window string
      flag (str): A state denoter within the window string (e.g. l for layout)
      next_flag (bool): Whether a workspace comes after the current field
    """
    # pre_bg is the background of the field
    # pst_bg is the background after the field
    # arrow_bg is the background of the powerline style arrow
    if flag.isupper():
        # Visible workspaces
        pre_bg = COLORS["blue_fade_bg"]
        pre_fg = COLORS["blue_fade_fg"]
        sys.stderr.write("%s %s\n" % (field, FOCUSED_WORKSPACE))
        if field == FOCUSED_WORKSPACE:
            sys.stderr.write("HEY")
            pre_bg = COLORS["blue_bg"]
            pre_fg = COLORS["blue_fg"]

        pst_bg = COLORS["lter_bg"]
        pst_fg = pre_bg

        arrow_bg = pre_bg
        arrow_fg = COLORS["lter_bg"]
        last_char = ""

    elif flag == 'u':
        pre_bg = COLORS["red_bg"]
        pre_fg = COLORS["blue_bg"]

        pst_bg = COLORS["lter_bg"]
        pst_fg = COLORS["red_bg"]

        arrow_bg = COLORS["red_bg"]
        arrow_fg = COLORS["lter_bg"]
        last_char = ""

    elif flag == 'l':  # the layout, not a workspace
        pre_bg = COLORS["ltest_bg"]
        pre_fg = COLORS["ltest_fg"]

        pst_bg = COLORS["ltest_fg"]
        pst_fg = COLORS["ltest_bg"]

        arrow_bg = COLORS["ltest_bg"]
        arrow_fg = COLORS["lter_bg"]
        last_char = ""
    else:  # flag == 'o'
        arrow_bg = COLORS["lter_bg"]
        arrow_fg = COLORS["lter_bg"]

        pre_bg = COLORS["lter_bg"]
        pre_fg = COLORS["ltest_bg"]

        pst_bg = pre_bg
        pst_fg = pre_fg
        if next_flag is None or next_flag.isupper():
            pst_bg = arrow_bg
            pst_fg = arrow_fg
        last_char = ""

    output = "^bg(" + arrow_bg + ")"           \
           + "^fg(" + arrow_fg + ")" + " "    \
                                               \
           + '^bg(' + pre_bg + ')'             \
           + '^fg(' + pre_fg + ')' + field     \
           + ' '                               \
           + '^bg(' + pst_bg + ')'             \
           + '^fg(' + pst_fg + ')' + last_char
    return output


def print_usage():
    """
    Prints how to use the program
    """
    program = sys.argv[0].split("/")
    program = program[len(program) - 1]
    sys.stderr.write('USAGE: {} <workspaces>\n'.format(program))
    sys.exit()

def main():
    """
    entry point for script
    """
    try:
        workspace_string = sys.argv[1]
    except IndexError:
        print_usage()


    occupied_workspaces = []

    layout = ""
    # flags to check for:
    #   o means occupied
    #   u means urgent
    #   l is the layout (not a workspace!)
    for field in workspace_string.split(":"):
        flag = field[0]
        field = field[1:]
        if flag.lower() in "ou":
            occupied_workspaces.append((field, flag))
        elif flag.lower() in "l":
            layout = field
        elif flag.lower() in "f" and flag.isupper():
            occupied_workspaces.append((field, flag))

    #print(FOCUSED_WORKSPACE)
    occupied_workspaces = sorted(occupied_workspaces, key=get_sort_key)

    output = "^fg(" + COLORS["ltest_fg"] + ")" \
           + "^bg(" + COLORS["lter_bg"]  + ")" \
           + ""
    for i, workspace_tuple in enumerate(occupied_workspaces):
        try:
            nxt_tuple = occupied_workspaces[i + 1]
            nxt_flag = nxt_tuple[1]
        except IndexError:
            nxt_flag = None
        output += decorate_field(workspace_tuple[0], workspace_tuple[1], nxt_flag)
    output += decorate_field(layout, 'l')

    print(output)

main()
