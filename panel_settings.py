"""
Constants related to bspwm panels
"""
import utils
import os

HEIGHT = '18'
FIFO = '/tmp/panel-fifo'
BG_COLOR = '#303030'
FONT = 'Inconsolata for Powerline:Bold:size=10'
WIDTH = '{}'.format(int(utils.get_x_resolution() / 2 - 5))
OFFSET = '{}'.format(int(utils.get_x_resolution() / 2))
TOG_FILE = '{}/.config/bspwm/state/panel_toggle'.format(os.environ['HOME'])
