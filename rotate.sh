#!/bin/sh
# $HOME/.config/bspwm/.rotate contains the state:
#   true  for rotated 90 degrees
#   false for default orientation

tog_file="$HOME/.config/bspwm/.rotate"

if $(cat $tog_file); then
    $HOME/bin/dualhead.sh
    echo "false" > $tog_file
else
    $HOME/bin/dualhead-rot.sh
    echo "true" > $tog_file
fi
