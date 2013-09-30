#!/usr/bin/env python

"""
    :created: 2013 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import logging
import sys
import unittest

from configs import Dragon32Cfg
from cpu6809 import CPU
from Dragon32_mem_info import DragonMemInfo
from test_base import TextTestRunner2


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        cfg = Dragon32Cfg()
        cfg.mem_info = DragonMemInfo(log.debug)
        self.cpu = CPU(cfg)

    def cpu_test_run(self, start, end, mem):
        for cell in mem:
            self.assertLess(-1, cell, "$%x < 0" % cell)
            self.assertGreater(0x100, cell, "$%x > 0xff" % cell)
        self.cpu.memory.load(start, mem)
        if end is None:
            end = start + len(mem)
        self.cpu.test_run(start, end)


class Test6809_AddressModes(BaseTestCase):
    def test_base_page_direct01(self):
        self.cpu.memory.load(0x1000, [0x12, 0x34, 0xf])
        self.cpu.program_counter = 0x1000
        self.cpu.direct_page = 0xab

        value = self.cpu.direct()
        self.assertEqual(hex(value), hex(0xab12))

        value = self.cpu.direct()
        self.assertEqual(hex(value), hex(0xab34))

        self.cpu.direct_page = 0x0
        value = self.cpu.direct()
        self.assertEqual(hex(value), hex(0xf))


class Test6809_CC(BaseTestCase):
    """
    condition code register tests
    """
    def test_defaults(self):
        status_byte = self.cpu.cc.get()
        self.assertEqual(status_byte, 0)

    def test_from_to(self):
        for i in xrange(256):
            self.cpu.cc.set(i)
            status_byte = self.cpu.cc.get()
            self.assertEqual(status_byte, i)

    def test_set_register01(self):
        self.cpu.set_register(0x00, 0x1e12)
        self.assertEqual(self.cpu.accu_a.get(), 0x1e)
        self.assertEqual(self.cpu.accu_b.get(), 0x12)


class Test6809_Ops(BaseTestCase):
    def test_TFR01(self):
        self.cpu.index_x.set(512) # source
        self.assertEqual(self.cpu.index_y.get(), 0) # destination

        self.cpu_test_run(start=0x1000, end=0x1002, mem=[
            0x1f, # TFR
            0x12, # from index register X (0x01) to Y (0x02)
            0x1f, # TFR
            0x9a, # from accumulator B (0x09) to condition code register CC (0x9a)
        ])
        self.assertEqual(self.cpu.index_y.get(), 512)

    def test_TFR02(self):
        self.cpu.accu_b.set(0x55) # source
        self.assertEqual(self.cpu.cc.get(), 0) # destination

        self.cpu_test_run(start=0x1000, end=0x1002, mem=[
            0x1f, # TFR
            0x9a, # from accumulator B (0x09) to condition code register CC (0x9a)
        ])
        self.assertEqual(self.cpu.cc.get(), 0x55) # destination

    def test_ADDA_extended01(self):
        self.cpu_test_run(start=0x1000, end=0x1003, mem=[
            0xbb, # ADDA extended
            0x12, 0x34 # word to add on accu A
        ])
        self.assertEqual(self.cpu.cc.Z, 1)
        self.assertEqual(self.cpu.cc.get(), 0x04)
        self.assertEqual(self.cpu.accu_a.get(), 0x00)

    def test_CMPX_extended(self):
        """
        Compare M:M+1 from X
        Addressing Mode: extended
        """
        self.cpu.accu_a.set(0x0) # source

        self.cpu_test_run(start=0x1000, end=0x1003, mem=[
            0xbc, # CMPX extended
            0x10, 0x20 # word to add on accu A
        ])
        self.assertEqual(self.cpu.cc.get(), 0x04)
        self.assertEqual(self.cpu.cc.C, 1)


#     @opcode(0xbb)
#     def ADDA_extended(self):
#         """
#         A = A + M
#         """
#         self.cycles += 5
#         value = self.read_pc_word()
#         log.debug("%s - 0xbb ADDA extended: Add %s to accu A: %s" % (
#             hex(self.program_counter), hex(value), hex(self.accu_a)
#         ))
#         self.accu_a += value




if __name__ == '__main__':
    log = logging.getLogger("DragonPy")
    log.setLevel(
#         logging.ERROR
#         logging.INFO
#         logging.WARNING
        logging.DEBUG
    )
    log.addHandler(logging.StreamHandler())



    unittest.main(
        argv=(
            sys.argv[0],
#             "Test6809_Ops.test_TFR02",
#             "Test6809_Ops.test_CMPX_extended",
#             "Test6809_AddressModes",
        ),
        testRunner=TextTestRunner2,
#         verbosity=1,
        verbosity=2,
#         failfast=True,
    )
