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
# python2.7 src/common/tbot.py -c tbot.cfg -t tc_workfd_apply_patchwork_patches.py
# apply patchworkpatches to current dir
# creates event:
# - PW_NR: which patchwork number used
# - PW_CLEAN: is it checkpatch clean
# - PW_AA: already applied
# - PW_APPLY: apply it clean to source
#
from tbotlib import tbot

logging.info("args: workfd: %s %s %s %s", tb.workfd,
             tb.tc_workfd_apply_patchwork_patches_list,
             tb.tc_workfd_apply_patchwork_patches_checkpatch_cmd,
             tb.tc_workfd_apply_patchwork_patches_eof)

def apply_one_patch(tb, nr):
    tb.tc_workfd_rm_file_name = 'mbox'
    ret = tb.call_tc("tc_workfd_rm_file.py")
    tmp = 'wget http://patchwork.ozlabs.org/patch/' + nr + '/mbox'
    tb.eof_write_lx_cmd_check(tb.workfd, tmp)
    tb.event.create_event('main', 'func', 'PW_NR', nr)
    if tb.tc_workfd_apply_patchwork_patches_checkpatch_cmd != 'none':
        tmp = tb.tc_workfd_apply_patchwork_patches_checkpatch_cmd + ' mbox'
        tb.eof_write_cmd(tb.workfd, tmp)
        ret = tb.call_tc("tc_workfd_check_cmd_success.py")
        if ret != True:
            logging.warn("checkpatch error")
            tmp = 'cat mbox | grep Subject'
            tb.eof_write_lx_cmd_check(tb.workfd, tmp)
            tb.event.create_event('main', 'func', 'PW_CLEAN', 'False')
        else:
            tb.event.create_event('main', 'func', 'PW_CLEAN', 'True')

    tmp = 'git am -3 mbox'
    loop = True
    se = ['Patch already applied']
    tb.eof_write(tb.workfd, tmp)
    while loop == True:
        tmp = tb.tbot_read_line_and_check_strings(tb.workfd, se)
        if tmp == '0':
            tb.event.create_event('main', 'func', 'PW_AA', 'True')
        if tmp == 'prompt':
            ret = tb.call_tc("tc_workfd_check_cmd_success.py")
            tb.event.create_event('main', 'func', 'PW_APPLY', ret)
            if tb.tc_workfd_apply_patchwork_patches_eof == 'yes':
                if ret == False:
                    tb.end_tc(False)
            loop = False
            if ret == False:
                # restore source
                tmp = 'git am --abort'
                tb.eof_write_lx_cmd_check(tb.workfd, tmp)

# print some infos
tb.eof_write_cmd(tb.workfd, 'pwd')
tb.eof_write_lx_cmd_check(tb.workfd, 'git describe')
for nr in tb.tc_workfd_apply_patchwork_patches_list:
    apply_one_patch(tb, nr)

tb.end_tc(True)