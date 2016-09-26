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

import os

# ~/.kgit
if not os.path.exists(os.path.expanduser('~') + "/.kgit"):
    os.makedirs(os.path.expanduser('~') + "/.kgit")

# ~/.kgit/hooks
if not os.path.exists(os.path.expanduser('~') + "/.kgit/hooks"):
    os.makedirs(os.path.expanduser('~') + "/.kgit/hooks")

# ~/.kgit/profiles
if not os.path.exists(os.path.expanduser('~') + "/.kgit/profiles"):
    f = open(os.path.expanduser('~') + "/.kgit/profiles", 'w')
    f.write("")
    f.close()

# ~/.kgit/workspaces
if not os.path.exists(os.path.expanduser('~') + "/.kgit/workspaces"):
    f = open(os.path.expanduser('~') + "/.kgit/workspaces", 'w')
    f.write("")
    f.close()
