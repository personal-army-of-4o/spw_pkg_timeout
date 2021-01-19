import random
import cocotb
import itertools

from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Edge, ClockCycles, Timer

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

@cocotb.coroutine
def get_signal(clk, ack, data):
    yield FallingEdge(clk)
    ack <= 1
    return data.value

@cocotb.coroutine
def write_symbol(dut, s):
    print ('sending symbol ', hex(s))    
    yield FallingEdge(dut.iClk)
    dut.iData = s
    dut.iValid = 1
    yield RisingEdge(dut.iClk)
    while dut.oAck == 0:
        yield RisingEdge(dut.iClk)
    yield Timer(1, units="ns")
    dut.iValid = 0

@cocotb.coroutine
def write_pkg(dut, len, seed, hangup = False):
    eop = [256]
    random.seed(seed)
    package = (random.randint(0, 127) for _ in range (len-1))
    if hangup == False:
        package = itertools.chain(package, iter(eop))
    while True:
        try:
            yield write_symbol(dut, next(package))
        except StopIteration:
            break

@cocotb.coroutine
def get_symbol(dut):
    if SIM_UNDERFLOW_READ:
        dut.iAck = 1;
        yield RisingEdge(dut.iClk)
        while dut.oValid == 0:
            yield RisingEdge(dut.iClk)
        return dut.oData.value
    
    else:
        yield Timer (1, units='ns')
        dut.iAck = 0
        while dut.oValid == 0:
            yield RisingEdge(dut.iClk)
        yield FallingEdge(dut.iClk)
        s = dut.oData
        dut.iAck = 1
        yield RisingEdge(dut.iClk)
        return s.value

@cocotb.coroutine
def check_symbol(dut, s):
    ss = yield get_symbol(dut)
    print ('got symbol ', hex(ss))    
    if s != ss:
        pass

@cocotb.coroutine
def read_pkg(dut, len, seed, do_eep = False):
    eop = [256]
    eep = [257]
    random.seed(seed)
    rare_package = (random.randint(0, 127) for _ in range (len-1))
    if do_eep:
        package = itertools.chain(rare_package, iter(eop))
    else:
        package = itertools.chain(rare_package, iter(eep))
 
    dut.iAck = 0
    yield RisingEdge(dut.iClk)
    while True:
        try:
            yield check_symbol(dut, next(package))
        except StopIteration:
            break

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
    cocotb.fork(write_pkg(dut, 8, seed))
    cocotb.fork(read_pkg(dut, 16, seed))

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
    cocotb.fork(write_pkg(dut, 8, seed, True))
    cocotb.fork(read_pkg(dut, 16, seed, True))

    yield ClockCycles(dut.iClk, 500)

    assert True

