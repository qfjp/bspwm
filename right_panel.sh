#!/bin/bash
conky -c $HOME/.conky_dzen \
    | dzen2 -p -ta r -bg '#303030' -fn "Inconsolata for Powerline:Bold:size=10" \
      -h $PANEL_HEIGHT -w 795 -sa c -x 800 -y 0 -e 'onstart=lower'
