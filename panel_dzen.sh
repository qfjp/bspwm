#!/bin/bash
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
