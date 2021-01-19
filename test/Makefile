TOPLEVEL_LANG ?= vhdl
SIM ?= ghdl
SIM_ARGS ?= --wave=waveform.ghw
COMPILE_ARGS ?= --std=08

PWD=$(shell pwd)
SRC_PREFIX=$(PWD)/../
FILELIST=$(shell cat ../filelist)

ifeq ($(TOPLEVEL_LANG),vhdl)
    VHDL_SOURCES = $(addprefix $(SRC_PREFIX), $(FILELIST))
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

TOPLEVEL := spw_pkg_timeout
MODULE   := $(TOPLEVEL)_cocotb

include $(shell cocotb-config --makefiles)/Makefile.sim
