TOPLEVEL_LANG ?= vhdl
SIM ?= ghdl
SIM_ARGS ?= --wave=waveform.ghw

PWD=$(shell pwd)

ifeq ($(TOPLEVEL_LANG),vhdl)
    VHDL_SOURCES = $(PWD)/../hdl/src/spw_pkg_timeout.vhd $(PWD)/../hdl/tb/tb_top.vhd
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

TOPLEVEL := tb_top
MODULE   := $(TOPLEVEL)_cocotb

include $(shell cocotb-config --makefiles)/Makefile.sim
