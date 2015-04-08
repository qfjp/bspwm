#!/bin/bash
conky -c $HOME/.conky_dzen \
    | dzen2 -p -ta r -bg '#303030' -fn "Inconsolata for Powerline:Bold:size=10" \
      -h $PANEL_HEIGHT -w $PANEL_WIDTH -sa c -x $PANEL_OFFSET -y 0 -e 'onstart=lower'
