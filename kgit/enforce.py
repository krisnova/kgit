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

import kgit, os, time, subprocess

my_dir = os.path.dirname(os.path.realpath(__file__))


#
# enforce_p
#
# This will actually enforce the git hooks for our profiles
# Note: enforce requires a workspace directory
# TODO This should have tab hinting and support ~ expansion
def run():
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
                try:
                    os.unlink(pre_commit)
                except:
                    pass
                p = subprocess.Popen(["git", "init"], cwd=workspace + "/" + dir, stdout=subprocess.PIPE)
                out, err = p.communicate()
                errcode = p.returncode
                kgit.out(out)
                # +x for good measure
                st = os.stat(pre_commit)
                os.chmod(pre_commit, st.st_mode | 0o111)


#
# is_git_repo
#
# Well validate a dir is a valid git repo
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
    tag += "        templatedir = ~/.kgit\n"

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

    # Idempotent Write
    try:
        os.unlink(os.path.expanduser('~') + "/.kgit/hooks/pre-commit")
    except:
        pass
    f = open(os.path.expanduser('~') + "/.kgit/hooks/pre-commit", 'w')
    f.write(newTemplate)
    f.close()
