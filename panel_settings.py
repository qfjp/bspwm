"""
Constants related to bspwm panels
"""
import utils
import os
import subprocess

HEIGHT = '18'
FIFO = '/tmp/panel-fifo'
BG_COLOR = '#303030'
FONT = 'Inconsolata for Powerline:Bold:size=10'
WIDTH = '{}'.format(int(utils.get_x_resolution() / 2 - 5))
OFFSET = '{}'.format(int(utils.get_x_resolution() / 2))
TOG_FILE = '{}/.config/bspwm/state/panel_toggle'.format(os.environ['HOME'])


def set_height():
    """
    Sets the height of the panel based on the dpi
    """
    dpi = subprocess.check_output(['xdpyinfo'])
    dpi = dpi.decode('utf-8')
    x_dpi = 96
    y_dpi = 96
    dpi_line = ""
    for line in dpi.split('\n'):
        if 'dots' in line:
            dpi_line = line
    dpi_line = dpi_line.strip()
    dpi_line = dpi_line.split()[1]
    x_dpi = int(dpi_line.split('x')[0])
    y_dpi = int(dpi_line.split('x')[1])
    global HEIGHT
    HEIGHT = '{}'.format(int(.1875 * y_dpi))

set_height()
