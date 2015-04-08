#!/bin/bash
parse_line()
{
    local line="$*"
    echo "$(python3 << PYTHONSCRIPT

workspaces = "$line"
workspaces = workspaces[1:]
workspaces = workspaces.split(':')

# Two cases:
# 1. The workspace is the last visible workspace:
#       remove the boundary in the name
#       i.e change "1 example >" to "1 example  "
#       (remember to keep the spaces the same!)
# 2. The workspace is the last visible workspace adjacent to the active one
#       Same as above.

current_found = False
last_workspace_num = 0
last_workspace_adj_num = 0

inactive_mon = []
active_mon = []

isActiveMonitor = False

# first pass, no drawing
for i,workspace_plus in enumerate(workspaces):
    firstChar = workspace_plus[0]

    if firstChar == 'M':
        isActiveMonitor = True
    elif firstChar == 'm':
        isActiveMonitor = False

    elif firstChar == 'L':
        pass
    elif firstChar.isupper():
        current_found = True
    elif firstChar == 'o':
        last_workspace_num = i
        if not current_found:
            last_workspace_adj_num = i

    if isActiveMonitor:
        active_mon.append(i)
    else:
        inactive_mon.append(i)


colors = { "ltest_bg"      : '#d0d0d0'
         , "ltest_fg"      : '#303030'
         , "lter_bg"       : '#585858'
         , "lter_fg"       : '#303030'
         , "red_bg"        : '#ac0000'
         , "blue_fade_bg"  : '#00627f'
         , "blue_fade_fg"  : '#8ea5ab'
         , "blue_bg"       : '#0097af'
         , "blue_fg"       : '#d2eaf0'
         , "fg"            : '#999d9d'
         }

output = "^fg(" + colors["lter_fg"] + ")"       \
       + "^bg(" + colors["lter_bg"] + ")" + ""

for i,workspace_plus in enumerate(workspaces):
    firstChar = workspace_plus[0]
    workspace = workspace_plus[1:]
    if firstChar == 'L':
        # this is the arrangement (tiled or monocle)
        output += "^fg(" + colors["lter_bg"]  + ")"       \
                + "^bg(" + colors["ltest_bg"] + ")" + "" \
                + "^fg(" + colors["ltest_fg"] + ")" + " "
        output += workspace + " "                         \
                + "^fg(" + colors["ltest_bg"] + ")"       \
                + "^bg(" + colors["ltest_fg"] + ")" + "" \
                + "^fg(" + colors["fg"]       + ")"
    elif firstChar == 'm' or firstChar == 'M':
        pass
    elif firstChar == 'u':
        # for workspaces that are urgent (but not focused)
        output += "^bg(" + colors["red_bg"]  + ")"       \
                + "^fg(" + colors["lter_bg"] + ")" + "" \
                + "^fg(" + colors["blue_fg"] + ")"       \
                + "^bg(" + colors["red_bg"]  + ")" + " "
        output += workspace + " "
        output += "^fg(" + colors["red_bg"]  + ")"       \
                + "^bg(" + colors["lter_bg"] + ")" + ""
    elif firstChar.isupper():
        # this is the current workspace
        if i in active_mon:
            bg = colors["blue_bg"]
            fg = colors["blue_fg"]
        else:
            bg = colors["blue_fade_bg"]
            fg = colors["blue_fade_fg"]

        output += "^bg(" + bg + ")"                      \
                + "^fg(" + colors["lter_bg"] + ")" + "" \
                + "^fg(" + fg + ")"                      \
                + "^bg(" + bg + ")" + " "
        output += workspace + " "
        output += "^fg(" + bg + ")"                      \
                + "^bg(" + colors["lter_bg"] + ")" + ""
    elif firstChar == 'o':
        # this means the workspace is "occupied"
        output += "^fg(" + colors["ltest_bg"] + ")"      \
                + "^bg(" + colors["lter_bg"]  + ")" + "  "
        output += workspace + " "
        if i != last_workspace_num and i != last_workspace_adj_num:
            output += ""
        else:
            output += " "

print(output)
PYTHONSCRIPT
    )"
}

while read -r line; do
    case $line in
        T*) title=${line:1}
            ;;
        W*) win_string="$($HOME/.config/bspwm/parse_windows.py "${line:1}")"
             ;;
        #W*) win_string="$(parse_line "$line")"
        #    echo $line > $HOME/test
        #    # Only updates on workspace change, needs to be fixed...
        #    ;;
    esac
    echo "$win_string" "$title"
done
