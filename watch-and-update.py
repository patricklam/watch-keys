import os
import pyinotify

# Update user-directory .ssh/authorized_keys from a central directory.
# Expects keys to be of the form 'plam@django-130', throws out
# everything after the @, concatenates, and puts the result in
# /home/plam/.ssh/authorized_keys.

# Uses pyinotify to watch for changes.

# Copyright 2013 Patrick Lam
#
# Released under the Expat license:
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

KEYDIR = os.path.join(os.getenv("HOME"), "keydir")
HOMES = '/home'
AUTHORIZED_KEYS = '.ssh/authorized_keys'

class UpdateKeys(pyinotify.ProcessEvent):
  def process_default(self, event):
    userid = event.name.split("@")[0]
    userdir = os.path.join(HOMES, userid)
    if (not os.path.exists(userdir)):
      return
    #print("Received event on filename {0}, userid {1}".format(event.name, userid))
    newKey = '';
    for root, _, files in os.walk(event.path):
      for f in files:
        if (f.startswith(userid)):
          key = os.path.join(root, f)
          f = open(key, 'r')
          newKey = newKey + f.read()
          f.close()
    combinedKeyFile = os.path.join(userdir, AUTHORIZED_KEYS)
    kk = open(combinedKeyFile, 'w')
    kk.write(newKey)
    kk.close()

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, UpdateKeys())
wm.add_watch(KEYDIR, pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MODIFY)
notifier.loop()
