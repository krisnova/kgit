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

import os, kgit, subprocess


#
# run
#
# Will run the purge
def run():
    kgit.out("Removing hooks")
    workspaces = kgit.get_file("workspaces").split("\n")
    for workspace in workspaces:
        if workspace == "":
            continue
        for dir in os.listdir(workspace):
            if is_git_repo(workspace + "/" + dir):
                pre_commit = workspace + "/" + dir + "/.git/hooks/pre-commit"
                kgit.out("Remove: " + pre_commit)
                try:
                    os.unlink(pre_commit)
                except:
                    pass


#
# is_git_repo
#
# Well validate a dir is a valid git repo
def is_git_repo(dir):
    if os.path.exists(dir + "/.git"):
        return True
    return False
