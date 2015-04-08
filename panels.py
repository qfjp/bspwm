"""
Methods for panel communication and activation
"""
import os
import subprocess
import threading

import panel_settings
import parse_windows

try:
    os.mkfifo(panel_settings.FIFO)
except FileExistsError:
    pass


def writer_control():
    """
    The target for the window string thread.
    Writes the bspc window string to the fifo
    """
    with open(panel_settings.FIFO, 'wb') as fifo:
        ret_code1 = subprocess.call(['bspc', 'control', '--subscribe'],
                                    stdout=fifo)
        assert ret_code1 == 0


def writer_title():
    """
    The target for the title string thread.
    Writes the window title to the fifo
    """
    with open(panel_settings.FIFO, 'wb') as fifo:
        ret_code2 = subprocess.call(['xtitle', '-sf', 'T%s'], stdout=fifo)
        assert ret_code2 == 0


def activate_writer():
    """
    Creates both threads for the fifo writer.
    Ensures both the window string and the title string threads
    are active
    """
    write_thread = threading.Thread(target=writer_control)
    write_thread.start()
    write_thread = threading.Thread(target=writer_title)
    write_thread.start()


def left_panel_target():
    """
    The target for the left panel thread.

    Communicates with the panel fifo to find the window string
    and title strings. These are parsed, then passed on to an
    instance of dzen2 (created locally)
    """
    title = ''
    win_string = ''
    o_title = ''
    o_win_string = ''
    dzen_cmd = ['dzen2', '-p', '-ta', 'l', '-bg', panel_settings.BG_COLOR,
                '-fn', panel_settings.FONT, '-h', panel_settings.HEIGHT,
                '-w', panel_settings.WIDTH, '-sa', 'c',
                '-x', '5', '-y', '0',
                '-e', 'onstart=lower']
    dzen = subprocess.Popen(dzen_cmd, stdin=subprocess.PIPE)
    with open(panel_settings.FIFO, 'r') as fifo:
        for line in fifo:
            if line[0] == 'T':
                o_title = line[1:]
                title = o_title
            elif line[0] == 'W':
                o_win_string = line[1:]
                win_string = parse_windows.parse(o_win_string)

            title = title.replace('\n', '')
            win_string = win_string.replace('\n', '')

            o_title = o_title.replace('\n', '')
            o_win_string = o_win_string.replace('\n', '')
            # o_string = '{} {}\n'.format(o_win_string, o_title)

            pipe_string = '{} {}\n'.format(win_string, title)
            pipe_string = pipe_string.encode('utf-8')
            dzen.stdin.write(pipe_string)
            dzen.stdin.flush()


def activate_left_panel():
    """
    Create the left panel
    """
    panel_thread = threading.Thread(target=left_panel_target)
    panel_thread.start()


def right_panel_target():
    """
    The target for the right panel thread
    """
    conky_cmd = ['conky', '-c', '{}/.conky_dzen'.format(os.environ['HOME'])]
    with subprocess.Popen(conky_cmd, stdout=subprocess.PIPE) as conky:
        dzen_cmd = ['dzen2', '-p', '-ta', 'r', '-bg', panel_settings.BG_COLOR,
                    '-fn', panel_settings.FONT, '-h', panel_settings.HEIGHT,
                    '-w', panel_settings.WIDTH, '-sa', 'c',
                    '-x', panel_settings.OFFSET, '-y', '0',
                    '-e', 'onstart=lower']
        ret_code = subprocess.call(dzen_cmd, stdin=conky.stdout)
        assert ret_code == 0


def activate_right_panel():
    """
    Create the right panel
    """
    panel_thread = threading.Thread(target=right_panel_target)
    panel_thread.start()
