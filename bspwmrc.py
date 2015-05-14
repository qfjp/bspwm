#!/usr/bin/env python
"""
Main bspwm config file
"""
import os
import subprocess
import sys
import threading

import panel_settings
import panels
import rules
import switch_desktop
import utils


class BspwmConf():
    """
    A class that generates a bspwm config
    """

    def __init__(self):
        self.panel_height = panel_settings.HEIGHT
        self.icon_height = panel_settings.ICON_HEIGHT
        self.panel_fifo = panel_settings.FIFO

        self.settings = {}
        self.settings['border_width'] = '2'
        self.settings['window_gap'] = '5'
        self.settings['split_ratio'] = '0.52'
        self.settings['borderless_monocle'] = 'true'
        self.settings['gapless_monocle'] = 'true'
        self.settings['focused_border_color'] = '#ff950e'
        self.top_padding = panel_settings.HEIGHT

        self.monitors = utils.get_monitors()
        self.workspcs = utils.get_workspcs()

    def attach_workspcs_cmds(self, monitors=None, workspcs=None):
        """
        Returns a list of commands that set the workspaces for each monitor
        e.g.
        [ "bspc monitor DFP10 -d 1 3 5 7 9"
        , "bspc monitor DFP11 -d 2 4 6 8 10"
        ]
        """
        if not monitors:
            monitors = self.monitors
        if not workspcs:
            workspcs = self.workspcs
        cmds = []
        for (i, monitor) in enumerate(monitors):
            sliced = [elem for (ind, elem) in enumerate(workspcs)
                      if ind % len(monitors) == i]
            precmd = ['bspc', 'monitor', '{}'.format(monitor), '-d']
            cmd = precmd + sliced
            cmds.append(cmd)
        return cmds

    def config_cmds(self):
        """
        Various config setting cmds
        """
        settings = self.settings
        cmds = [['bspc', 'config', '{}'.format(key),
                 '{}'.format(settings[key])]
                for key in settings]

        panel_height_cmd = ['bspc', 'config', '-m', self.monitors[0],
                            'top_padding', self.top_padding]
        cmds.append(panel_height_cmd)
        return cmds

    def compton_target(self):
        """
        run the compton command.
        """
        x_res = utils.get_x_resolution()
        comp_reg = x_res - 10
        height = self.panel_height
        comp_reg_str = '{}x{}+5+0'.format(comp_reg, height)
        comp_cfg_str = '{}/.config/compton/compton.conf'\
                       .format(os.environ['HOME'])
        compton_cmd = ['compton', '-G', '--shadow-exclude-reg',
                       comp_reg_str, '--config', comp_cfg_str]
        ret_val = subprocess.call(compton_cmd)
        assert ret_val == 0

    def stalonetray_target(self):
        """
        Run stalonetray
        """
        height = self.icon_height
        x_res = utils.get_x_resolution()
        geo_x = int(x_res * .88)
        geo_string = '1x1+{}+1'.format(geo_x)
        tray_cmd = ['stalonetray', '-i', height, '--kludges',
                    'force_icons_size', '--geometry', geo_string,
                    '-bg', '#121212', '--grow-gravity', 'E']
        ret_val = subprocess.call(tray_cmd)
        assert ret_val == 0

    def run_compton(self):
        """
        Run the compton thread.
        """
        thread = threading.Thread(target=self.compton_target)
        thread.start()

    def run_stalonetray(self):
        """
        Run the stalonetray thread.
        """
        thread = threading.Thread(target=self.stalonetray_target)
        thread.start()

    def execute(self):
        """
        Run the configuration
        """
        for cmd in self.attach_workspcs_cmds():
            return_code = subprocess.call(cmd)
            assert return_code == 0

        for cmd in self.config_cmds():
            return_code = subprocess.call(cmd)
            assert return_code == 0

        panels.activate_writer()
        panels.activate_left_panel()
        panels.activate_right_panel()
        rules.reset_rules()
        self.run_compton()
        self.run_stalonetray()

try:
    FIRST_ARG = sys.argv[1]
except IndexError:
    CONF = BspwmConf()
    CONF.execute()
    sys.exit()

if FIRST_ARG == 'switch':
    # switch to desktop named in second argument
    INDEX = int(sys.argv[2])
    switch_desktop.main(INDEX)
elif FIRST_ARG == 'move':
    INDEX = int(sys.argv[2])
    switch_desktop.main(INDEX, move=True)
elif FIRST_ARG == 'panel':
    panels.toggle_visible()
