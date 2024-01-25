#!/usr/bin/env python

"""
    Multicomp 6809
    ~~~~~~~~~~~~~~

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import logging

from dragonpy.core.machine import MachineGUI, Machine
from dragonpy.mx6309.config import MX6309Config
from dragonpy.mx6309.gui import MX6309TkinterGUI
from dragonpy.mx6309.periphery import MX6309Periphery


log = logging.getLogger(__name__)


# class MX6309Machine(Machine):
#     def __init__(self, cfg, periphery_class, display_callback, user_input_queue):
#
#         super().__init__(cfg, periphery_class, display_callback, user_input_queue)
#
# class MX6309Gui(MachineGUI):
#     def __init__(self, cfg, gui_class):
#         self.gui = gui_class(
#             self.cfg,
#             self.user_input_queue
#         )
#         self.machine = MX6309Machine(cfg=cfg, periphery_class=MX6309Periphery, d)
#         super().__init__(cfg)


def run_mx6309(cfg_dict: dict):
    machine = MachineGUI(
        cfg=MX6309Config(cfg_dict)
    )
    machine.run(
        PeripheryClass=MX6309Periphery,
        GUI_Class=MX6309TkinterGUI
    )
