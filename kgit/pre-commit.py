#!/usr/bin/python
########################################################################################################################
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
#
# [pre-commit]
#
# This is an AUTOMATICALLY GENERATED pre-commit executable that was created by kgit. This script will attempt to
# enforce kgit profile configuration for every commit.
#
# creation time : <<t>>
#
# It is recommended to let kgit manage this file.
#
########################################################################################################################

import os, sys, subprocess

########################################################################################################################
# Automatically generated variables by kgit
# DO NOT CHANGE
#
#
KGIT_MANAGED_REPOS_DICT = ""
KGIT_MANAGED_VERSIONS = ""
#
#
# DO NOT CHANGE
# Automatically generated variables by kgit
########################################################################################################################

# Friendly names
r = KGIT_MANAGED_REPOS_DICT
version = KGIT_MANAGED_VERSIONS

# The directory of this script
my_dir = os.path.dirname(os.path.realpath(__file__))

# Repository configuration at time of commit
vars = {}


def main():
    global vars
    out("===========================================================================================")
    out("[kgit] v" + version)
    out("This pre-commit hook is located in " + my_dir)
    vars = get_git_config_vars()
    s = validate()
    if s:
        # Okay!
        out("Valid commit..")
        exit_code = 0
    else:
        # Fail!
        exit_code = 1

    out("===========================================================================================")
    sys.exit(exit_code)


def validate():
    this_remote = vars["remote.origin.url"]
    this_user = vars["user.name"]
    this_email = vars["user.email"]

    for repo in r:
        email = r[repo][0]
        user = r[repo][1]

        # We have a kgit managed profile
        if repo in this_remote:
            out("Running in kgit managed repository")
            if this_user == user and this_email == email:
                return True
            else:
                out("Invalid Username/Email configuration!")
                out("----------------------------------------------------")
                out("| Current   : " + this_user + " " + this_email)
                out("| Expecting : " + user + " " + email)
                out("----------------------------------------------------")
                find_matching_profile()
                return False

    out("This repository is not managed by kgit")
    return True


def find_matching_profile(remote):
    with open(os.path.expanduser('~') + "/.kgit/profiles") as f:
        profiles = f.read()

    for line in profiles.split("\n"):
        if line == "":
            continue
        vals = line.split("|")  # 0-repo 1-email 2-name
        if vals[0] in remote:
            out("Found matching profile: " + vals[0])
            out("kgit profiles use " + vals[0])
            return


def get_git_config_vars():
    vars = {}
    raw = sh("git config -l")
    for line in raw.split("\n"):
        if line == "":
            continue
        kv = line.split("=")
        vars[kv[0]] = kv[1]
    return vars


def sh(cmd):
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out


########################################################################################################################
#
# OUTPUT
#
def out(message):
    print "\033[1mkgit : \033[0m \033[95m%s\033[0m" % (message)


if __name__ == "__main__":
    main()
