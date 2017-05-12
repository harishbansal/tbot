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
# python2.7 src/common/tbot.py -c tbot.cfg -t tc_lx_check_reg_file.py
# checks if the default values in reg file tb.config.tc_lx_create_reg_file_name
# on the tbot host in tb.workdir have the same values, as the
# registers on the board. Needs devmem2 installed.
# format of the regfile:
# regaddr mask type defval
#
# If you have to call devmem2 with a "header"
# set it through tb.config.devmem2_pre
# so on the bbb with original rootfs -> no devmem2 installed
# so to use tc which use devmem2 you have to copy devmem2
# bin to the rootfs, and start it with 'sudo ...'
#
# ToDo: use the file from the lab host, not the tbot host
# End:

from tbotlib import tbot

try:
    tb.config.devmem2_pre
except:
    tb.config.devmem2_pre = ''

logging.info("args: %s", tb.config.tc_lx_create_reg_file_name)

# set board state for which the tc is valid
tb.set_board_state("linux")

pre = tb.config.devmem2_pre
c = tb.c_con
fname = tb.workdir + "/" + tb.config.tc_lx_create_reg_file_name
try:
    fd = open(fname, 'r')
except IOError:
    logging.warning("Could not open: %s", fname)
    tb.end_tc(False)

for line in fd.readlines():
    cols = line.split()
    if cols[0] == '#':
        continue
    tmp = pre + 'devmem2 ' + cols[0] + " " + cols[2]
    tb.eof_write(c, tmp)
    ret = tb.tbot_expect_string(c, 'opened')
    if ret == 'prompt':
        tb.end_tc(False)
    sl = ['Value at address', 'Read at address']
    ret = tb.tbot_rup_and_check_strings(c, sl)
    if ret == 'prompt':
        tb.end_tc(False)
    ret = tb.tbot_expect_string(c, '\n')
    if ret == 'prompt':
        tb.end_tc(False)
    tmp = tb.buf.split(":")[1]
    tmp = tmp[1:]
    tmp = tmp.strip()
    tb.tbot_expect_prompt(c)
    if (int(tmp, 16) & int(cols[1], 16)) != (int(cols[3], 16) & int(cols[1], 16)):
        logging.warning("pinmux diff args: %s %s@%s & %s != %s", tb.config.tc_lx_create_reg_file_name, tmp, cols[0], cols[1], cols[3])
        print("Error  ", tb.config.tc_lx_create_reg_file_name, cols[0], tmp, cols[1], cols[3])
        # tb.end_tc(False)

tb.end_tc(True)
