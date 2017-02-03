#!/usr/bin/env python
# Francesco Conti <f.conti@unibo.it>
#
# Copyright (C) 2016 ETH Zurich, University of Bologna.
# All rights reserved.

import sys,os,subprocess

devnull = open(os.devnull, 'wb')

class tcolors:
    OK      = '\033[92m'
    WARNING = '\033[93m'
    ERROR   = '\033[91m'
    ENDC    = '\033[0m'

def execute(cmd, silent=False):
    if silent:
        stdout = devnull
    else:
        stdout = None
    return subprocess.call(cmd.split(), stdout=stdout)

def execute_out(cmd, silent=False):
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out

# download IPApproX tools in ./ipstools and import them
if os.path.exists("ipstools") and os.path.isdir("ipstools"):
    cwd = os.getcwd()
    os.chdir("ipstools")
    execute("git pull", silent=True)
    os.chdir(cwd)
    import ipstools
else:
    execute("git clone git@iis-git.ee.ethz.ch:pulp-tools/IPApproX ipstools")
    import ipstools
execute("mkdir -p vsim/vcompile/ips")
execute("rm -rf vsim/vcompile/ips/*")

# creates an IPApproX database
ipdb = ipstools.IPDatabase(ips_dir="./ips", rtl_dir="./rtl", vsim_dir="./vsim")
# generate ModelSim/QuestaSim compilation scripts
ipdb.export_vsim(script_path="vsim/vcompile/ips", target_tech='umc65')
# generate vsim.tcl with ModelSim/QuestaSim "linking" script
ipdb.generate_vsim_tcl("vsim/tcl_files/config/vsim_ips.tcl")
# generate script to compile all IPs for ModelSim/QuestaSim
ipdb.generate_vcompile_libs_csh("vsim/vcompile/vcompile_ips.csh")

# generate Vivado compilation scripts
ipdb.export_vivado(script_path="fpga/pulpino/tcl/ips_src_files.tcl", alternatives=['riscv'])
# generate Vivado add_files.tcl
ipdb.generate_vivado_add_files("fpga/pulpino/tcl/ips_add_files.tcl", alternatives=['riscv'])
# generate Vivado inc_dirs.tcl
ipdb.generate_vivado_inc_dirs("fpga/pulpino/tcl/ips_inc_dirs.tcl", alternatives=['riscv'])


print tcolors.OK + "Generated new scripts for IPs!" + tcolors.ENDC
