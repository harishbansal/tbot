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
# start with
# python2.7 src/common/tbot.py -c tbot.cfg -t tc_ub_setenv.py
from tbotlib import tbot

# here starts the real test
logging.info("testcase arg: %s %s", tb.setenv_name, tb.setenv_value)
# set board state for which the tc is valid
tb.set_board_state("u-boot")

# set env var
c = tb.c_con

tmp = 'setenv ' + tb.setenv_name + ' ' + tb.setenv_value
tb.eof_write(c, tmp)
tb.tbot_expect_prompt(c)

# check if it is set with the correct value
tmp = 'printenv ' + tb.setenv_name
tb.eof_write(c, tmp)
str3 = tb.setenv_name + '=' + tb.setenv_value
ret = tb.tbot_expect_string(c, str3)
if ret == 'prompt':
    tb.end_tc(False)

tb.tbot_expect_prompt(c)
tb.end_tc(True)