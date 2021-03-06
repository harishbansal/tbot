# This file is part of tbot.  tbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Description:
# start with
# tbot.py -s lab_denx -c mcx -t tc_board_mcx.py
# start all testcases for the mcx board linux stable and linux-ml
# End:

from tbotlib import tbot

tb.statusprint("tc_mcx testing linux stable")
tb.config.tc_lx_regulator_nrs = ['0 regulator-dummy -', '1 hsusb1_vbus 5000000',
		'2 vmmc 3300000', '3 vdd_core 1200000',
		'4 vddshv 3300000', '5 vdds 1800000',
		'6 LDO1 1800000', '7 LDO2 3300000']
#tb.eof_call_tc("tc_board_mcx_tests.py")

tb.statusprint("tc_mcx testing linux mainline")
tb.config.tc_lx_regulator_nrs = ['0 regulator-dummy -', '1 hsusb1_vbus 5000000',
		'2 vmmc 3300000', '3 pbias_mmc_omap2430 3000000',
		'4 DCDC1 1200000', '5 DCDC2 3300000', '6 DCDC3 1800000',
		'7 LDO1 1800000', '8 LDO2 3300000']
tb.config.ub_boot_linux_cmd = 'run tbot_boot_linux_ml'
tb.eof_call_tc("tc_board_mcx_tests.py")
tb.end_tc(True)
