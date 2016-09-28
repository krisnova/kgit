#!/usr/bin/python
########################################################################################################################
#
# MIT License
#
# Copyright (c) [2016] [Kris Childress] [kris@nivenly.com]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
########################################################################################################################

########################################################################################################################
#
version = "1.0.2"
#
########################################################################################################################

import sys, readline, os, profiles, workspaces, enforce, purge
from subprocess import call

# Usage for the tool
description = '''
\033[1m[kgit]\033[0m V%s Written by Kris Childress <kris@nivenly.com>

    \033[1mkgit\033[0m is a simple utility for managing convenience functionality for git.

    Use \033[1mkgit\033[0m just as you would use git. All commands are supported, and \033[1mkgit\033[0m will
    run whatever version of git you currently have installed.

    \033[1mkgit\033[0m implements a few unique actions that tradition git does not. They are listed below.

    [ACTIONS]

    \033[95m[profiles]\033[0m Interact with kgit profiles. Profiles link kgit configuration to repositories.

        kgit profiles                                 Will list all available profiles, and show the current profile
        kgit profiles add <\033[91mrepository-name\033[0m>           Will add a new profile
        kgit profiles delete <\033[91mrepository-name\033[0m>        Will delete an existing profile by regex match string
        kgit profiles use <\033[91mrepository-name\033[0m>           Will use this profile as a global .gitconfig

    \033[95m[workspaces]\033[0m Interact with kgit workspaces. Workspaces are directories with nested git repositories.

        kgit workspaces                               Will list all available workspaces
        kgit workspaces add <\033[91mworkspace\033[0m>               Will add a new workspace
        kgit workspaces delete <\033[91mworkspace\033[0m>            Will delete an existing workspace by regex match string

    \033[95m[enforce]\033[0m Will enforce kgit configurations across all workspaces

        kgit enforce                                  Will enforce kgit configurations across all workspaces

    \033[95m[purge]\033[0m Will purge all kgit hooks

        kgit purge                                    Will purge all kgit configurations and reset all hooks
''' % version


########################################################################################################################
#
# MAIN
#
def main():
    try:
        firstarg = sys.argv[1]
        if firstarg == "-h" or firstarg == "--help":
            sys.exit(1)
    except:
        print description
        sys.exit(1)
    if firstarg == "profiles":
        run_profiles()
    elif firstarg == "workspaces":
        run_workspaces()
    elif firstarg == "enforce":
        run_enforce()
    elif firstarg == "purge":
        run_purge()
    else:
        git_passthru()


########################################################################################################################
#
# PURGE
#
def run_purge():
    purge.run()


########################################################################################################################
#
# ENFORCE
#
def run_enforce():
    enforce.run()


########################################################################################################################
#
# WORKSPACES
#
def run_workspaces():
    try:
        action = sys.argv[2]
    except:
        workspaces.list_w()
        return
    if action == "list":
        workspaces.list_w()
    if action == "add":
        workspaces.add_w()
    if action == "delete":
        workspaces.delete_w()


########################################################################################################################
#
# PROFILES
#
def run_profiles():
    try:
        action = sys.argv[2]
    except:
        profiles.list_p()
        return
    if action == "list":
        profiles.list_p()
    if action == "add":
        profiles.add_p()
    if action == "delete":
        profiles.delete_p()
    if action == "use":
        profiles.use_p()


########################################################################################################################
#
# GIT_PASSTHRU
#
def git_passthru():
    git_cmd = ["git"]
    git_cmd_str = "git"
    i = -1
    for a in sys.argv:
        i += 1
        if i < 1:
            continue
        git_cmd.append(a)
        git_cmd_str += " " + a
    out(git_cmd_str)
    call(git_cmd)


########################################################################################################################
#
# OUTPUT
#
def out(message):
    message = message.replace("\n", "")
    print "\033[1mkgit : \033[0m \033[95m%s\033[0m" % (message)


########################################################################################################################
#
# ERROR
#
def error(message):
    print "\033[1mkgit : \033[0m \033[91m%s\033[0m" % (message)


########################################################################################################################
#
# READ
#
def get_file(file):
    with open(os.path.expanduser('~') + "/.kgit/" + file) as f:
        return f.read()


########################################################################################################################
#
# WRITE
#
def write_data(data, file):
    f = open(os.path.expanduser('~') + "/.kgit/" + file, 'w')
    f.write(data)
    f.close()


########################################################################################################################
#
# BOOTSTRAP
#
if __name__ == "__main__":
    main()
