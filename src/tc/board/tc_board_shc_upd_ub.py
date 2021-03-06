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
# tbot.py -s lab_denx -c shc -t tc_board_shc_upd_ub.py
# update MLO and u-boot.img on the SD card or the eMMC
# card, and boot it ...
# End:

from tbotlib import tbot

logging.info("typ: %s", tb.config.tc_board_shc_upd_ub_typ)

#set board state for which the tc is valid
tb.set_board_state("linux")

tb.workfd = tb.c_con
# mount eMMc or SD
tb.config.tc_lx_mount_dir = '/home/hs/mnt'
tb.config.tc_lx_mount_fs_type = 'vfat'
if tb.config.tc_board_shc_upd_ub_typ == 'eMMC':
    tb.config.tc_lx_mount_dev = '/dev/mmcblk1p1'
elif tb.config.tc_board_shc_upd_ub_typ == 'SD':
    tb.config.tc_lx_mount_dev = '/dev/mmcblk0p1'
else:
    logging.error("typ %s not supported", tb.config.tc_board_shc_upd_ub_typ)

tb.eof_call_tc("tc_lx_mount.py")

# get rootfspath from cmdline ToDo
rootfspath = '/opt/eldk-5.5/armv5te/rootfs-qte-sdk'
rootfsworkdir = '/home/hs'

tb.workfd = tb.c_ctrl
#copy files to rootfs dir
tb.statusprint("copy files")
c = tb.workfd
so = "/tftpboot/" + tb.config.tftpboardname + "/" + tb.config.ub_load_board_env_subdir + '/u-boot.img'
ta = rootfspath + rootfsworkdir + '/u-boot.img'
tb.eof_call_tc("tc_lab_cp_file.py", ch=c, s=so, t=ta)
so = "/tftpboot/" + tb.config.tftpboardname + "/" + tb.config.ub_load_board_env_subdir + '/MLO'
ta = rootfspath + rootfsworkdir + '/MLO'
tb.eof_call_tc("tc_lab_cp_file.py", ch=c, s=so, t=ta)

tb.workfd = tb.c_con
tmp = 'cp ' + rootfsworkdir + '/MLO ' + tb.config.tc_lx_mount_dir
tb.write_lx_cmd_check(tb.workfd, tmp)
tmp = 'cp ' + rootfsworkdir + '/u-boot.img ' + tb.config.tc_lx_mount_dir
tb.write_lx_cmd_check(tb.workfd, tmp)

# umount the partition
tmp = "umount " + tb.config.tc_lx_mount_dev
tb.write_lx_cmd_check(tb.workfd, tmp)

tb.workfd = tb.c_ctrl
# set bootmode
tmp = 'relais   relsrv-08-01  4  off'
tb.write_lx_cmd_check(tb.workfd, tmp)
if tb.config.tc_board_shc_upd_ub_typ == 'eMMC':
    tmp = 'relais   relsrv-08-01  3  off'
elif tb.config.tc_board_shc_upd_ub_typ == 'SD':
    tmp = 'relais   relsrv-08-01  3  on'
tb.write_lx_cmd_check(tb.workfd, tmp)

# power off
tb.eof_call_tc("tc_lab_poweroff.py")

# check U-Boot version
tb.workfd = tb.c_ctrl
tb.tc_ub_get_version_file = "/tftpboot/" + tb.config.tftpboardname + "/" + tb.config.ub_load_board_env_subdir + '/u-boot.bin'
tb.tc_ub_get_version_string = 'U-Boot 20'
tb.eof_call_tc("tc_ub_get_version.py")
tb.uboot_vers = tb.config.tc_return
tb.tc_ub_get_version_file = "/tftpboot/" + tb.config.tftpboardname + "/" + tb.config.ub_load_board_env_subdir + '/u-boot-spl.bin'
tb.tc_ub_get_version_string = 'U-Boot SPL'
tb.eof_call_tc("tc_ub_get_version.py")
tb.spl_vers = tb.config.tc_return

tb.eof_call_tc("tc_ub_check_version.py")
tb.end_tc(True)
