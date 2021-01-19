import random
import cocotb
import itertools

from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Edge, ClockCycles, Timer

from DataInterface import DataInterface

SIM_UNDERFLOW_READ=True

def init_dut(dut):
    dut.iData <= 0
    dut.iValid <= 0
    dut.iTimeout_ticks <= 0
    dut.iAck <= 0

def set_timeout(dut, val):
    dut.iTimeout_ticks <= val

@cocotb.coroutine
def do_reset(dut, len):
    dut.iReset <= 0
    yield ClockCycles(dut.iClk, len)
    dut.iReset <= 1

@cocotb.test()
def positive_test(dut):
    """ Test where package should be read full """

    clock = Clock(dut.iClk, 10, units="ns") # create a 10 us period clock
    cocotb.fork(clock.start()) # start the clock

    yield FallingEdge(dut.iClk)
    init_dut(dut)
    set_timeout(dut, 10)

    yield do_reset(dut, 4)

    yield ClockCycles(dut.iClk, 2)

    seed = 0
    length = 5
    eop = [256]
    prng1 = random.Random(seed)
    prng2 = random.Random(seed)

    pkg1 = (prng1.randint(0, 127) for _ in range (length-1))
    pkg1 = itertools.chain(pkg1, iter(eop))

    pkg2 = (prng2.randint(0, 127) for _ in range (length-1))
    pkg2 = itertools.chain(pkg2, iter(eop))

    reader = DataInterface(dut.iClk, dut.oValid, dut.oData, dut.iAck)
    writer = DataInterface(dut.iClk, dut.iValid, dut.iData, dut.oAck)

    cocotb.fork(reader.Read(pkg1))
    cocotb.fork(writer.Write(pkg2))

    yield ClockCycles(dut.iClk, 500)

    assert True

@cocotb.test()
def timeout_test(dut):
    """ Test where package should be read full """

    clock = Clock(dut.iClk, 10, units="ns") # create a 10 us period clock
    cocotb.fork(clock.start()) # start the clock

    yield FallingEdge(dut.iClk)
    init_dut(dut)
    set_timeout(dut, 10)

    yield do_reset(dut, 4)

    yield ClockCycles(dut.iClk, 2)

    seed = 0
    length = 5
    eep = [257]
    prng1 = random.Random(seed)
    prng2 = random.Random(seed)

    pkg1 = (prng1.randint(0, 127) for _ in range (length-1))

    pkg2 = (prng2.randint(0, 127) for _ in range (length-1))
    pkg2 = itertools.chain(pkg2, iter(eep))

    reader = DataInterface(dut.iClk, dut.oValid, dut.oData, dut.iAck)
    writer = DataInterface(dut.iClk, dut.iValid, dut.iData, dut.oAck)

    cocotb.fork(reader.Read(pkg1))
    cocotb.fork(writer.Write(pkg2))

    yield ClockCycles(dut.iClk, 500)

    assert True

