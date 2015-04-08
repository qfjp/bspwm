import os
import subprocess
import threading

import utils
import panel_settings

try:
    os.mkfifo(panel_settings.PANEL_FIFO)
except FileExistsError:
    pass


def writer_control():
    with open(panel_settings.PANEL_FIFO, 'wb') as fifo:
        ret_code1 = subprocess.call(['bspc', 'control', '--subscribe'],
                                    stdout=fifo)
        assert ret_code1 == 0


def writer_title():
    with open(panel_settings.PANEL_FIFO, 'wb') as fifo:
        ret_code2 = subprocess.call(['xtitle', '-sf', 'T%s'], stdout=fifo)
        assert ret_code2 == 0


def reader():
    test_file = open('/tmp/test', 'wb')
    with open(panel_settings.PANEL_FIFO, 'rb') as fifo:
        for line in fifo:
            test_file.write(line)
            test_file.flush()


def activate_writer():
    write_thread = threading.Thread(target=writer_control)
    write_thread.start()
    write_thread = threading.Thread(target=writer_title)
    write_thread.start()


def activate_reader():
    read_thread = threading.Thread(target=reader)
    read_thread.start()
