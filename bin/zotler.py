#!/usr/bin/env python3

import click
import os
from pathlib import Path
import sys

from zotler import zotler


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-l', '--list_of_files', type=click.File('r'),
              callback=zotler.delete_files, expose_value=False, is_eager=True,
              help=('File containing list of files to be deleted. Usually created by '
                    'this script and specified by -o option. '
                    'All other options will be omitted if this one is used.'))
@click.option('-p', '--zotero_prefs', type=click.Path(exists=True), default=None,
              help='Path to Zotero settings file prefs.js. If omitted, path to '
                   '~/.zotero/xxxxxxxx.default/prefs.js file is used.')
@click.option('-d', '--zotero_dbase', type=click.Path(exists=True, dir_okay=False),
              default=None,
              help='Path to Zotero database (zotero.sqlite file). If omitted, Home'
                   'directory specified by -d option or default location is used')
@click.option('-D', '--zotero_home_dir', type=click.Path(exists=True, file_okay=False),
              default=None,
              help='Path to Zotero home directory. It is not used, if path to Zotero '
                   'database file (-f) is provided. If omitted, default path'
                   '~/Zotero/ is used.')
@click.option('-x', '--force_delete', is_flag=True,
              help='Delete all orphan files immediately (default: False).')
@click.option('-o', '--output_file', type=click.File('w'), default=sys.stdout,
              help='Save list of orphan files to the file (default: STDOUT).')
@click.option('-v', '--version', is_flag=True, callback=zotler.print_version,
              expose_value=False, is_eager=True,
              help='Show version number and exit.')
def main(zotero_prefs, zotero_home_dir, zotero_dbase, force_delete,
         output_file):
    """
    Clean attachments in ZotFile Custom Location directory.

    Zotler (ZotFile Butler) searches ZotFile Custom Location of attachment files and
    makes a list containing files not linked in Zotero database. The files can be
    deleted directly or saved to a file. The file can be edited and used as a template
    for subsequent removal of the orphan files.

    Path to location of the files is parsed from the Custom Location setting in
    ZotFile preferences saved in the prefs.js file. Path to the file can be passed
    as an option -p or it can be created automatically using default path
    ~/.zotero/xxxxxxxx.default/prefs.js (Linux only). The first dictionary ending with
    .default is used.

    Path to the Zotero database file zotero.sqlite can be specified using -f option or
    -d option. Later option sets path to the Zotero home dictionary containing
    zotero.sqlite file. Default path ~/Zotero/zotero.sqlite (Linux only) is used
    if both options are omitted.

    \b
    Examples:
    ----

    Parse path to ZotFile attachments from ~/.zotero/zotero/xxxxxxx.default/pref.js
    file, use default path to Zotero database file (~/Zotero/zotero.sqlite), find
    orphan files and save paths to the files to ~/orphans.txt file:

    $ python zotler.py -o ~/orphans.txt

    or

    $ python zotler.py -p ~/.zotero/zotero/xxxxxxx.default/pref.js
    -d ~/Zotero/zotero.sqlite -o ~/orphans.txt

    Delete files listed in ~/orphans.txt file:

    python zotler.py -l ~/orphans.txt
    """

    if zotero_home_dir is None:
        zotero_home_dir = os.path.join(str(Path.home()), 'Zotero')

    if zotero_dbase is None:
        zotero_dbase = os.path.join(zotero_home_dir, 'zotero.sqlite')

    zotero_prefs = zotler.get_prefs_file(zotero_prefs)
    orphan_files = zotler.create_set_of_orphans(zotero_dbase, zotero_prefs)

    print(10 * '-')

    if force_delete:
        zotler.remove_files(orphan_files)
    else:
        print('\n'.join(orphan_files), file=output_file)


if __name__ == '__main__':
    exit(main())
