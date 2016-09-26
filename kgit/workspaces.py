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

import kgit, sys, os, subprocess, time

my_dir = os.path.dirname(os.path.realpath(__file__))


#
# list_p
#
# Used to list all current profiles stored in the data store
def list_p():
    profiles = kgit.get_file("profiles")
    if profiles == "" or profiles == "\n":
        kgit.out("No profiles available")
        return
    lines = profiles.split("\n")
    kgit.out("===============================================")
    for line in lines:
        if line == "":
            continue
        vals = line.split("|")  # 0-repo 1-email 2-name
        kgit.out("Repository : " + vals[0])
        kgit.out("      Name : " + vals[2])
        kgit.out("     Email : " + vals[1])
        kgit.out("===============================================")


#
# add_p
#
# Used to add a profile to the data store
# Format:
# github.com|kris@nivenly.com|Kris Childress
def add_p():
    profiles = kgit.get_file("profiles")

    # Hostname
    if len(sys.argv) < 4:
        host = raw_input("Repository: ")
    else:
        host = sys.argv[3]

    # Name
    if len(sys.argv) < 5:
        name = raw_input("Name: ")
    else:
        name = sys.argv[4]

    # Email
    if len(sys.argv) < 6:
        email = raw_input("Email: ")
    else:
        email = sys.argv[5]

    wstr = host + "|" + email + "|" + name + "\n"

    # Check on all lower
    if wstr.lower() in profiles.lower():
        kgit.out("Profile exists - Not adding duplicate")
        return
    profiles = profiles + wstr
    kgit.write_data(profiles, "profiles")
    kgit.out("Profile added: " + host)
    list_p()
    kgit.out("Automaticall enforcing")
    enforce_p()


#
# delete_p
#
# Will delete a record by criteria, where criteria is any string that can be matched on a record
def delete_p():
    profiles = kgit.get_file("profiles")

    # Criteria
    if len(sys.argv) < 4:
        criteria = raw_input("Criteria: ")
    else:
        criteria = sys.argv[3]
    lines = profiles.split("\n")
    profileToWrite = ""
    delta = False
    i = -1
    llen = len(lines)
    for line in lines:
        i += 1
        if criteria in line:
            delta = True
            vals = line.split("|")  # 0-repo 1-email 2-name
            kgit.out("Removing: " + vals[0] + " " + vals[2] + " " + vals[1])
            if i != (llen - 2):
                profileToWrite += "\n"
            continue
        profileToWrite += line
    if delta == False:
        kgit.out("No profiles matching criteria found. Unable to delete.")
        return
    kgit.write_data(profileToWrite, "profiles")
    yn = raw_input("Continue? [y/n] : ")
    # while yn != "y" or yn != "n":
    #     kgit.out("Please enter `y` or `n`")
    #     yn = raw_input("Continue? [y/n] : ")
    if yn == "n":
        return
    # Okay we have confirmed, lets save
    kgit.write_data(profileToWrite, "profiles")
    list_p()


#
# enforce_p
#
# This will actually enforce the git hooks for our profiles
# Note: enforce requires a workspace directory
# TODO This should have tab hinting and support ~ expansion
def enforce_p():
    kgit.out("Enforcing git hooks across workspaces")
    workspaces = kgit.get_file("workspaces")
    if workspaces == "":
        kgit.out("No workspaces are configured for kgit")
        w = raw_input("Add workspace (Enter no value to move on): ")
        workspacesToWrite = w + "\n"
        while w != "":
            w = raw_input("Add workspace (Enter no value to move on): ")
            workspacesToWrite += w + "\n"
        kgit.write_data(workspacesToWrite, "workspaces")
        kgit.out("Writing workspaces")
    build_hook()
    workspace_init()


#
# workspace_init
#
# Will init all valid git repositories in each of the configured workspaces
def workspace_init():
    workspaces = kgit.get_file("workspaces").split("\n")
    for workspace in workspaces:
        if workspace == "":
            continue
        for dir in os.listdir(workspace):
            if is_git_repo(workspace + "/" + dir):
                # Idempotent enforcemenet
                pre_commit = workspace + "/" + dir + "/.git/hooks/pre-commit"
                os.unlink(pre_commit)
                p = subprocess.Popen(["git", "init"], cwd=workspace + "/" + dir, stdout=subprocess.PIPE)
                out, err = p.communicate()
                errcode = p.returncode
                kgit.out(out)
                # +x for good measure
                st = os.stat(pre_commit)
                os.chmod(pre_commit, st.st_mode | 0o111)


def is_git_repo(dir):
    if os.path.exists(dir + "/.git"):
        return True
    return False


#
# build_hook
#
# Will build the pre-commit git template
def build_hook():
    tag = "\n[init]\n"
    tag += "    templatedir = ~/.kgit\n"

    # Write the tag if nothing exists
    if not os.path.exists(os.path.expanduser('~') + "/.gitconfig"):
        f = open(os.path.expanduser('~') + "/.gitconfig", 'w')
        f.write(tag)
        f.close()

    # Get the config
    with open(os.path.expanduser('~') + "/.gitconfig") as f:
        config = f.read()

    # Check if [init] is already in there
    if "templatedir = ~/.kgit" not in config:
        newConfig = config + tag
        f = open(os.path.expanduser('~') + "/.gitconfig", 'w')
        f.write(newConfig)
        f.close()

    var_replace = "KGIT_MANAGED_REPOS_DICT = {"
    profiles = kgit.get_file("profiles").split("\n")
    i = 0
    plen = len(profiles)
    for line in profiles:
        if line == "":
            continue
        vals = line.split("|")  # 0-repo 1-email 2-name
        str = '"' + vals[0] + '": ["' + vals[1] + '", "' + vals[2] + '"]'
        if i != plen - 2:
            str += ","
        i += 1
        var_replace += str
    var_replace += "}"

    # Write the template
    with open(my_dir + "/pre-commit.py") as f:
        template = f.read()

    # Replace config
    newTemplate = template.replace('KGIT_MANAGED_REPOS_DICT = ""', var_replace)
    newTemplate = newTemplate.replace('KGIT_MANAGED_VERSIONS = ""', 'KGIT_MANAGED_VERSIONS = "' + kgit.version + '"')
    newTemplate = newTemplate.replace("<<t>>", time.strftime("%a, %d %b %Y %H:%M:%S"))

    # Write
    f = open(os.path.expanduser('~') + "/.kgit/hooks/pre-commit", 'w')
    f.write(newTemplate)
    f.close()


#
# add_workspace_p
#
# Will add a workspace to the data store
def add_workspace_p():
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
    workspaces += workspace + "\n"
    kgit.out("Adding workspace: " + workspace)
    kgit.out("Workspaces are stored in ~/.kgit/workspaces")
    kgit.write_data(workspaces, "workspaces")
