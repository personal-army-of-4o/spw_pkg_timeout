TOPLEVEL_LANG ?= vhdl
SIM ?= ghdl
SIM_ARGS ?= --vcd=waveform.vcd

PWD=$(shell pwd)

export PYTHONPATH := $(PWD)/../model:$(PYTHONPATH)

ifeq ($(TOPLEVEL_LANG),vhdl)
    VHDL_SOURCES = $(PWD)/../hdl/src/spw_pkg_timeout.vhd
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

TOPLEVEL := spw_pkg_timeout
MODULE   := $(TOPLEVEL)_cocotb

include $(shell cocotb-config --makefiles)/Makefile.sim
