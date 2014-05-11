#!/usr/bin/env python

import os
import sys
import subprocess

def test(args, simulated_output):
  sys.stderr.write("\n\n>>> svn " + " ".join(args))
  sys.stdin.readline()
  cmd = [os.path.join(os.path.dirname(__file__), "svn-color.py"), "--__test__"] + args
  process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
  process.communicate(simulated_output)

test(["st"], """\
A       added.txt
M       modified.txt
D       deleted.txt
""")

test("log --limit 2".split(), """\
------------------------------------------------------------------------
r57 | josh | 2014-03-15 10:23:59 -0700 (Sat, 15 Mar 2014) | 1 line

christians v2
------------------------------------------------------------------------
r56 | josh | 2014-03-10 17:35:11 -0700 (Mon, 10 Mar 2014) | 1 line

ignore preview/
------------------------------------------------------------------------
""")


test("log --limit 2 -v".split(), """\
------------------------------------------------------------------------
r57 | josh | 2014-03-15 10:23:59 -0700 (Sat, 15 Mar 2014) | 1 line
Changed paths:
   M /christians/Crusade.png
   M /christians/Exorcist.png
   A /christians/God.png
   M /christians/Heart of a Child.png
   M /christians/Infallible Word of God.png
   M /christians/Love Your Neighbor.png
   M /christians/Martyrdom.png
   M /christians/Missionary.png
   D /christians/Pope.png
   M /christians/Preacher.png
   M /christians/The Meek Shall Inherit the Earth.png
   M /christians/Treasures in Heaven.png
   M /christians/Turn the Other Cheek.png
   A /christians/src/Sist_Sun_and_Moon_Ball2_08-09.jpg
   D /christians/src/popejohnpaulii_468x484.jpg
   M /gimp.xcf

christians v2
------------------------------------------------------------------------
r56 | josh | 2014-03-10 17:35:11 -0700 (Mon, 10 Mar 2014) | 1 line
Changed paths:
   M /

ignore preview/
------------------------------------------------------------------------
""")

test("log -r 55:56 -v".split(), """\
------------------------------------------------------------------------
r55 | josh | 2014-03-06 18:56:36 -0700 (Thu, 06 Mar 2014) | 1 line
Changed paths:
   M /base.xcf
   M /bases/Bomb Lab.png
   A /bases/Trollhouse.png
   A /bases/src/troll face.png
   A /bases/src/troll-house.jpg

add trollhouse base
------------------------------------------------------------------------
r56 | josh | 2014-03-10 17:35:11 -0700 (Mon, 10 Mar 2014) | 1 line
Changed paths:
   M /

ignore preview/
------------------------------------------------------------------------
""")


test("log -r 55:56 -v --diff".split(), """\
------------------------------------------------------------------------
r55 | josh | 2014-03-06 18:56:36 -0700 (Thu, 06 Mar 2014) | 1 line
Changed paths:
   M /base.xcf
   M /bases/Bomb Lab.png
   A /bases/Trollhouse.png
   A /bases/src/troll face.png
   A /bases/src/troll-house.jpg

add trollhouse base

Index: bases/Bomb Lab.png
===================================================================
Cannot display: file marked as a binary type.
svn:mime-type = image/png
Index: bases/Trollhouse.png
===================================================================
Cannot display: file marked as a binary type.
svn:mime-type = application/octet-stream
Index: bases/Trollhouse.png
===================================================================
--- bases/Trollhouse.png  (revision 0)
+++ bases/Trollhouse.png  (revision 55)

Property changes on: bases/Trollhouse.png
___________________________________________________________________
Added: svn:mime-type
## -0,0 +1 ##
+application/octet-stream
\ No newline at end of property
Index: bases/src/troll-house.jpg
===================================================================
Cannot display: file marked as a binary type.
svn:mime-type = application/octet-stream
Index: bases/src/troll-house.jpg
===================================================================
--- bases/src/troll-house.jpg (revision 0)
+++ bases/src/troll-house.jpg (revision 55)

Property changes on: bases/src/troll-house.jpg
___________________________________________________________________
Added: svn:mime-type
## -0,0 +1 ##
+application/octet-stream
\ No newline at end of property
Index: bases/src/troll face.png
===================================================================
Cannot display: file marked as a binary type.
svn:mime-type = application/octet-stream
Index: bases/src/troll face.png
===================================================================
--- bases/src/troll face.png  (revision 0)
+++ bases/src/troll face.png  (revision 55)

Property changes on: bases/src/troll face.png
___________________________________________________________________
Added: svn:mime-type
## -0,0 +1 ##
+application/octet-stream
\ No newline at end of property
Index: base.xcf
===================================================================
Cannot display: file marked as a binary type.
svn:mime-type = image/x-xcf

------------------------------------------------------------------------
r56 | josh | 2014-03-10 17:35:11 -0700 (Mon, 10 Mar 2014) | 1 line
Changed paths:
   M /

ignore preview/

Index: .
===================================================================
--- . (revision 55)
+++ . (revision 56)

Property changes on: .
___________________________________________________________________
Modified: svn:ignore
## -1 +1,2 ##
 out
+preview

------------------------------------------------------------------------
""")
