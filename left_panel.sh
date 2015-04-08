#!/bin/sh
cat $PANEL_FIFO \
    | $HOME/.config/bspwm/panel_dzen.sh \
    | dzen2 -p -ta l -bg '#303030' -fn 'Inconsolata for Powerline:Bold:size=10' \
      -h $PANEL_HEIGHT -w "795" -sa c -x 5 -y 0 -e 'onstart=lower'
