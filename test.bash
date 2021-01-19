#!/bin/bash
export PYTHONPATH=$PYTHONPATH:`pwd`/cocotb_helper
cp config.json test
pushd test
make
popd
ls test/sim_build
echo "listing test files"
ls test
echo "listing root files"
echo `pwd`
ls -al
find / -name 'spw_pkg_timeout*' 2>/dev/null
echo t2
touch test/spw_pkg_timeout
ls test
