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

import kgit, sys, os


#
# list_w
#
# Used to list all current workspaces stored in the data store
def list_w():
    workspaces = kgit.get_file("workspaces")
    if workspaces == "" or workspaces == "\n":
        kgit.out("No workspaces available")
        return
    lines = workspaces.split("\n")
    kgit.out("===============================================")
    for line in lines:
        if line == "":
            continue
        kgit.out(line)
        kgit.out("===============================================")


#
# add_w
#
# Will add a workspace to the data store
def add_w():
    workspaces = kgit.get_file("workspaces")
    if len(sys.argv) < 4:
        workspace = raw_input("Workspace: ")
    else:
        workspace = sys.argv[3]
    lines = workspaces.split("\n")
    for line in lines:
        if line == workspace:
            kgit.out("Workspace exists - Not adding duplicate")
            return
    workspace = workspace.replace("~", os.path.expanduser('~'))
    workspaces += workspace + "\n"
    kgit.out("Adding workspace: " + workspace)
    kgit.out("Workspaces are stored in ~/.kgit/workspaces")
    kgit.write_data(workspaces, "workspaces")


#
# delete_w
#
# Will delete a workspace by criteria, where criteria is any string that can be matched on a record
def delete_w():
    workspaces = kgit.get_file("workspaces")

    # Criteria
    if len(sys.argv) < 4:
        criteria = raw_input("Criteria: ")
    else:
        criteria = sys.argv[3]
    lines = workspaces.split("\n")
    workspacesToWrite = ""
    delta = False
    i = -1
    llen = len(lines)
    for line in lines:
        i += 1
        if criteria in line:
            delta = True
            kgit.out("Removing: " + line)
            if i != (llen - 2):
                workspacesToWrite += "\n"
            continue
        workspacesToWrite += line
    if not delta:
        kgit.out("No workspaces matching criteria found. Unable to delete.")
        return
    yn = raw_input("Continue? [y/n] : ")
    if yn != "y":
        return
    # Okay we have confirmed, lets save
    kgit.write_data(workspacesToWrite, "workspaces")
    list_w()
