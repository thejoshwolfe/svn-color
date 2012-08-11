Setup
====

Source this `svn-color.sh` from your `.bashrc`. Something like:

    . ~/svn-color/svn-color.sh


What is this
============

The script decorates the output of most svn commands with terminal colors.
Performing the setup above (and restarting bash) will cause `svn` executed from the bash environment to be executed through this `svn-color.py` script in here.
Colored commands include `diff`, and 'status'-like commands, such as `status`, `update`, etc.
The colors were chosen with dark backgrounds in mind.

Additionally, this script omits output that I consider boring, such as:

* mentioning external items that don't change
* reporting the revision number after doing an update

If an external item *does* change, the `Performing status on external item...` or `Updating external item into...` header is preserved.

If you want the old `svn` behavior, you can use `` `which svn` `` instead of `svn`.
This script produces color, even if stdout is not a tty (so that you can pipe the output through `less -RXF`).
Keep in mind that this is just a bash alias, so `svn` from outside your bash environment will be unmodified.

This project was inspired by https://github.com/jmlacroix/svn-color by Jean-Michel Lacroix.


Examples of omitting boring things
==================================

Before:

    $ svn st
    X       external_item
    
    Performing status on external item at 'external_item':

After:

    $ svn st

Before:

    $ svn st
    X       external_item
    
    Performing status on external item at 'external_item':
    ?       external_item/new_file

After:

    $ svn st
    Performing status on external item at 'external_item':
    ?       external_item/new_file

Before:

    $ svn up
    Updating '.':
    
    Fetching external item into 'openarborCommon':
    External at revision 1234.
    
    At revision 5678.

After:

    $ svn st

Before:

    $ svn up
    Updating '.':
    
    Fetching external item into 'openarborCommon':
    U       external_item/new_file
    External at revision 1234.
    
    At revision 5678.

After:

    $ svn up
    
    Fetching external item into 'openarborCommon':
    U       external_item/new_file

