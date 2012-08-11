#!/usr/bin/env python

import sys, subprocess
import re

def lazy_lines(file_object):
    line_builder = []
    while True:
        c = file_object.read(1)
        if c == "":
            return
        line_builder.append(c)
        if c == "\n":
            yield "".join(line_builder)
            del line_builder[:]

def color(line, foreground=None, background=None):
    prefixes = []
    if background:
        prefixes.append("\x1b[48;5;" + background + "m")
    if foreground:
        prefixes.append("\x1b[38;5;" + foreground + "m")
    if prefixes:
        line = "".join(prefixes) + line + "\x1b[0m\x1b[0;0m"
    return line

def decorate(line):
    if re.search(r"^Index: |^@@|^=",   line): return color(line, "38")      # File Name          = Blue
    if re.search(r"^-",                line): return color(line, "1")       # Removed            = Red
    if re.search(r"^\+",               line): return color(line, "2")       # Added              = Green
    if re.search(r"^ ?M|^ ?U",         line): return color(line, "38")      # Modified/Updated   = Blue
    if re.search(r"^ ?C|^E",           line): return color(line, "7", "1")  # Conflicted/Existed = Red Alert
    if re.search(r"^A",                line): return color(line, "2")       # Added              = Green
    if re.search(r"^D",                line): return color(line, "1")       # Deleted            = Red
    if re.search(r"^!",                line): return color(line, "7", "94") # Item Missing       = Amber Alert
    if re.search(r"^R|^G",             line): return color(line, "5")       # Replaced or Merged = Purple
    if re.search(r"^\?",               line): return color(line, "242")     # No Version Control = Light Grey
    if re.search(r"^I|^X|^Performing", line): return color(line, "236")     # Ignored            = Dark Grey
    return line

def main(args):
    actions = "add checkout co cp del diff export merge mkdir move mv remove rm ren st sw up".split()
    command = (args + [""])[0]
    if command not in actions:
        global decorate; decorate = lambda line: line
    process = subprocess.Popen(["svn"] + args, stdout=subprocess.PIPE)
    for line in lazy_lines(process.stdout):
        sys.stdout.write(decorate(line.rstrip()))
        sys.stdout.write("\n")

main(sys.argv[1:])
