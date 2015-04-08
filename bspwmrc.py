#!/usr/bin/env python
"""
Main bspwm config file
"""
import subprocess
import utils
import panel_settings


class BspwmConf():
    """
    A class that generates a bspwm config
    """

    def __init__(self):
        self.panel_height = panel_settings.PANEL_HEIGHT
        self.panel_fifo = panel_settings.PANEL_FIFO

        self.settings = {}
        self.settings['border_width'] = '2'
        self.settings['window_gap'] = '5'
        self.settings['split_ratio'] = '0.52'
        self.settings['borderless_monocle'] = 'true'
        self.settings['gapless_monocle'] = 'true'
        self.settings['focused_border_color'] = '#ff950e'
        self.top_padding = panel_settings.PANEL_HEIGHT

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

CONF = BspwmConf()
CONF.execute()
