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

import kgit, sys, subprocess, enforce


#
# list_p
#
# Used to list all current profiles stored in the data store
def list_p():
    profiles = kgit.get_file("profiles")
    vars = get_git_config_vars()
    noprofs = False
    if profiles == "" or profiles == "\n":
        kgit.out("No profiles available")
        noprofs = True

    # Current
    kgit.out("===============================================")
    kgit.out("******     Current Git Config Profile     *****")
    kgit.out("===============================================")
    kgit.out("Name  : " + vars["user.name"])
    kgit.out("Email : " + vars["user.email"])

    if noprofs:
        kgit.out("===============================================")
        return

    lines = profiles.split("\n")
    kgit.out("")
    kgit.out("===============================================")
    kgit.out("******     Current Registered Profiles    *****")
    kgit.out("===============================================")
    for line in lines:
        if line == "":
            continue
        vals = line.split("|")  # 0-repo 1-email 2-name
        kgit.out("Host  : " + vals[0])
        kgit.out("Name  : " + vals[2])
        kgit.out("Email : " + vals[1])
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
        host = raw_input("Git Host: ")
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
    kgit.out("Automatically enforcing")
    enforce.run()


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
    if not delta:
        kgit.out("No profiles matching criteria found. Unable to delete.")
        return
    yn = raw_input("Continue? [y/n] : ")
    if yn != "y":
        return
    # Okay we have confirmed, lets save
    kgit.write_data(profileToWrite, "profiles")
    list_p()


def use_p():
    profiles = kgit.get_file("profiles")

    # profile
    if len(sys.argv) < 4:
        profile = raw_input("Host: ")
    else:
        profile = sys.argv[3]

    for line in profiles.split("\n"):
        vals = line.split("|")  # 0-repo 1-email 2-name
        # repo = vals[0]
        if profile in line:
            kgit.out("Using profile: " + profile)
            subprocess.Popen(["git", "config", "--global", "user.name", vals[2]])
            subprocess.Popen(["git", "config", "--global", "user.email", vals[1]])
            list_p()
            return
    kgit.out("Unable to switch to profile " + profile + ". Profile not found.")


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
    # kgit.out("Running command: " + cmd)
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out
