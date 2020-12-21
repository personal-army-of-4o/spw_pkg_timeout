import random
import warnings
import math
import cocotb

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

def init_dut(dut):
    dut.iReset <= 1
    dut.iData <= 0
    dut.iValid <= 0
    dut.iTimeout_ticks <= 0

@cocotb.test()
async def test_all_data(dut):
    """ Simple test """

    clock = Clock(dut.iClk, 10, units="us") # create a 10 us period clock
    cocotb.fork(clock.start()) # start the clock

    await RisingEdge(dut.iClk) # sync with the clock
    init_dut(dut)
    dut.iValid <= 1

    await RisingEdge(dut.iClk)
    dut.iReset <= 0

    await RisingEdge(dut.iClk)

    for i in range(0, 2**9):
        dut.iData <= i
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
        assert dut.oData == i, f"given:{dut.oData} expected:{bin(i)}"

@cocotb.test()
async def test_valid(dut):
    """ Simple test """

    clock = Clock(dut.iClk, 10, units="us") # create a 10 us period clock
    cocotb.fork(clock.start()) # start the clock

    await RisingEdge(dut.iClk) # sync with the clock
    init_dut(dut)

    await RisingEdge(dut.iClk)
    dut.iReset <= 0
    dut.iValid <= 0

    await RisingEdge(dut.iClk)

    await RisingEdge(dut.iClk)
    for i in range(0, 2**9):
        dut.iData <= i
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
        assert dut.oData == 0, f"given:{dut.oData} expected:{0}"
