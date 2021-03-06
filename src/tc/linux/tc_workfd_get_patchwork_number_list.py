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
# python2.7 src/common/tbot.py -c tbot.cfg -t tc_workfd_get_patchwork_number_list.py
# get a list of patchworknumbers
# which are delegated to specific user
# tb.config.workfd_get_patchwork_number_user
# currently, this testcase reads "http://patchwork.ozlabs.org/project/uboot/list/"
# and filters out the patches, which are for
# tb.config.workfd_get_patchwork_number_user
# It would be better to login and look for the users
# ToDo list, but I did not find out, how to login ...
# ignore patches on blacklist:
# tb.config.tc_workfd_apply_patchwork_patches_blacklist
# also you can set the patch order with:
# tb.config.tc_workfd_get_patchwork_number_list_order
# End:

from tbotlib import tbot
import urllib2  # the lib that handles the url stuff
import urllib, sys

logging.info("args: workfd: %s %s %s %s", tb.workfd, tb.config.workfd_get_patchwork_number_user,
             tb.config.tc_workfd_apply_patchwork_patches_blacklist,
             tb.config.tc_workfd_get_patchwork_number_list_order)

tb.config.tc_workfd_apply_patchwork_patches_list = []
tb.config.tc_workfd_apply_patchwork_patches_list_title = []

target_url = 'http://patchwork.ozlabs.org/project/uboot/list/'

def analyse_one_page(tb, urll, url, page):
    reg = re.compile("patch_row")
    target = url + "?order=" + tb.config.tc_workfd_get_patchwork_number_list_order + "&page=" + page
    data = urll.urlopen(target) # it's a file like object and works just like a file

    fd =open('result.txt', 'w')
    line = data.readline()
    while line:
        fd.write(line)
        # if line contains "patch_row"
        res = reg.search(line)
        if res:
            nr = line.split(":")[1]
            nr = nr.split('"')[0]
            reg2 = re.compile(nr)
            tmp = False
            for line2 in data: # files are iterable
                fd.write(line2)
                if tmp == True:
                    # line2 contains now patchtitle
                    patchtitle = line2.split('\n')[0]
                    break
                res = reg2.search(line2)
                if res:
                    #read one more line -> patchtitle
                    tmp = True

            # read delegated to
            line = data.readline()
            fd.write(line)
            line = data.readline()
            fd.write(line)
            line = data.readline()
            fd.write(line)
            line = data.readline()
            fd.write(line)
            line = data.readline()
            fd.write(line)
            line = data.readline()
            fd.write(line)
            line = data.readline()
            fd.write(line)
            line = line.split('>')[1]
            line = line.split('<')[0]
            if line == tb.config.workfd_get_patchwork_number_user or tb.config.workfd_get_patchwork_number_user == 'all':
                applypatch = True
                for black in tb.config.tc_workfd_apply_patchwork_patches_blacklist:
                    if nr == black:
                        logging.info("blacklisted: %s %s\n" % (nr, patchtitle))
                        applypatch = False
                if applypatch == True:
                    tb.config.tc_workfd_apply_patchwork_patches_list.append(nr)
                    tb.config.tc_workfd_apply_patchwork_patches_list_title.append(patchtitle)

        line = data.readline()

    fd.close()

def search_next_page(tb):
    reg2 = re.compile('class="next"')
    page = 'end'
    fd =open('result.txt', 'r')
    tmp = True
    while tmp == True:
        line = fd.readline()
        if line:
            res = reg2.search(line)
            if res:
                line = fd.readline()
                pagetmp = line.split("=")[3]
                page = pagetmp.split('"')[0]
                fd.close()
                return page
        else:
            tmp = False
        
    fd.close()
    return page

#start with page 1 until end
page = "1"
while page != 'end':
    analyse_one_page(tb, urllib2, target_url, page)
    page = search_next_page(tb)

i = 0
for j in tb.config.tc_workfd_apply_patchwork_patches_list:
    logging.info("nr: %s %s\n" % (tb.config.tc_workfd_apply_patchwork_patches_list[i], tb.config.tc_workfd_apply_patchwork_patches_list_title[i]))
    i += 1
tb.end_tc(True)
