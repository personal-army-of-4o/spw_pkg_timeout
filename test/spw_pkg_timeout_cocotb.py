import random
import warnings
import math
import cocotb

from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

@cocotb.test()
async def test_timeout_simple(dut):
    """ Simple test """

    clock = Clock(dut.iClk, 10, units="us") # create a 10 us period clock
    cocotb.fork(clock.start()) # start the clock

    await FallingEdge(dut.iClk) # sync with the clock
    for i in range(0, 2**9):
        dut.iData <= i
        await FallingEdge(dut.iClk)
        assert dut.oData == i, f"given:{dut.oData} expected:{bin(i)}"
