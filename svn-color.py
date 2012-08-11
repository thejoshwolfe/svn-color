#!/usr/bin/env python

import sys, subprocess
import re

def lazy_lines(file_object):
    line_builder = []
    while True:
        c = file_object.read(1)
        if c == "":
            return
        if c == "\n":
            yield "".join(line_builder)
            del line_builder[:]
        else:
            line_builder.append(c)

red         = "1"
green       = "2"
purple      = "5"
white       = "7"
blue        = "38"
amber       = "94"
gray        = "242"
red_alert   = lambda line: apply_color(line, white, red)
amber_alert = lambda line: apply_color(line, white, amber)

def apply_color(text, foreground=None, background=None):
    prefixes = []
    if background:
        prefixes.append("\x1b[48;5;" + background + "m")
    if foreground:
        prefixes.append("\x1b[38;5;" + foreground + "m")
    return "".join(prefixes) + text + "\x1b[0m\x1b[0;0m"

diff_metadata_color = blue
diff_currently_in_metadata = False
def make_diff_metadata_control(is_start):
    def diff_metadata_control(line):
        global diff_currently_in_metadata; diff_currently_in_metadata = is_start
        return apply_color(line, diff_metadata_color)
    return diff_metadata_control
diff_metadata_start = make_diff_metadata_control(True)
diff_metadata_end = make_diff_metadata_control(False)
def make_diff_normal(color):
    def diff_normal(line):
        if diff_currently_in_metadata:
            return apply_color(line, diff_metadata_color)
        if color:
            return apply_color(line, color)
        return line
    return diff_normal
diff_add = make_diff_normal(green)
diff_delete = make_diff_normal(red)
diff_unknown = make_diff_normal(None)

diff_formatting = [
    (r"^Index: ", diff_metadata_start),
    (r"^@@",      diff_metadata_end),
    (r"^\+",      diff_add),
    (r"^-",       diff_delete),
    (r"",         diff_unknown),
]
def summary_of_conflicts(line):
    # the final summary is not in any context
    global context; context = None
    return red_alert(line)
status_formatting = [
    (r"^..L",                     amber_alert), # Locked
    (r"^Summary of conflicts:$",  summary_of_conflicts),
    (r"^E|^C|^.C|^...C|^......C", red_alert),   # Conflicted/Existed
    (r"^.       \*",              amber),       # Modified Remotely
    (r"^ ?M|^ ?U",                blue),        # Modified/Updated
    (r"^A|^   A",                 green),       # Added
    (r"^D|Removed external '.+'", red),         # Deleted
    (r"^R|^G",                    purple),      # Replaced or Merged
    (r"^\?|^I",                   gray),        # No Version Control/Ignored
    (r"^!",                       amber_alert), # Item Missing
]

update_stack = []
def set_context():
    if update_stack:
        global context; context = update_stack[-1]
def updating_start(line):
    line = apply_color(line, gray)
    if printed_anything:
        line = "\n" + line
    update_stack.append(line)
    set_context()
    return None
def updating_end(line):
    del update_stack[-1]
    set_context()
    return None
def external_status_start(line):
    global context; context = apply_color(line, gray)
    return None
def ignore(line):
    return None
hide_stuff_formatting = [] + 1 * [
    (r"^(Updating|Fetching external item into) '.+':$", updating_start),
    (r"^(External a|A)t revision \d+\.",                updating_end),
    (r"^Updated (external )?to revision \d+\.",         updating_end),
    (r"^Performing status on external item at '.+':$",  external_status_start),
    (r"^X|^    X",                                      ignore),
    (r"^Status against revision:[ \d]+",                ignore),
    (r"^$",                                             ignore),
]

context = None
printed_anything = False

def decorate(line, formatting_list):
    for regex, color in formatting_list:
        if not re.search(regex, line):
            continue

        # could be a function
        try: color.__call__
        except AttributeError: pass
        else: return color(line)

        # could be a color
        return apply_color(line, color)

    return line

def contains_accept_edit(args):
    # look for --accept edit
    accept = "--accept"
    edit_names = ("e", "edit")
    if any(accept + "=" + edit_name in args for edit_name in edit_names):
        return True
    try: accept_index = args.index(accept)
    except ValueError: return False
    try: return args[accept_index+1] in edit_names
    except IndexError: return False

commands_that_can_use_an_external_editor = "commit ci copy cp delete del remove rm import mkdir move mv rename ren propedit pedit pe update up".split()
commands_to_hide_stuff_from = "st status up update".split()
status_like_commands = "add checkout co cp del export merge mkdir move mv remove rm ren sw".split() + commands_to_hide_stuff_from
def main(args):
    command = ""
    for arg in args:
        if not arg.startswith("-"):
            command = arg
            break
    formatting_list = []
    if command in status_like_commands:
        formatting_list = status_formatting
        if command in commands_to_hide_stuff_from:
            formatting_list = hide_stuff_formatting + formatting_list
    if command == "diff":
        formatting_list = diff_formatting
    subprocess_command = ["svn"] + args
    accept_edit = contains_accept_edit(args)
    if command in commands_that_can_use_an_external_editor or accept_edit:
        # figuring out exactly when svn will run vim is too hard.
        # if the user doesn't explicitly ask for the editor, don't allow it.
        if accept_edit or "--editor-cmd" in args:
            # stay out of the way
            return subprocess.call(subprocess_command)
        # no editor allowed
        subprocess_command.append("--non-interactive")

    process = subprocess.Popen(subprocess_command, stdout=subprocess.PIPE)
    for input_line in lazy_lines(process.stdout):
        output_line = decorate(input_line, formatting_list)
        if output_line == None:
            continue
        global context
        if context != None:
            print(context)
            context = None
        print(output_line)
        global printed_anything; printed_anything = True
    return process.wait()

try:
    sys.exit(main(sys.argv[1:]))
except KeyboardInterrupt:
    sys.exit("")

