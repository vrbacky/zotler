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
@click.option('-p', '--prefs_file', type=click.Path(exists=True), default=None,
              help='Path to Zotero settings file prefs.js. If omitted, path to '
                   '~/.zotero/xxxxxxxx.default/prefs.js file is used.')
@click.option('-f', '--zotero_file', type=click.Path(exists=True, dir_okay=False),
              default=None,
              help='Path to Zotero database (zotero.sqlite file). If omitted, Home'
                   'directory specified by -d option or default location is used')
@click.option('-d', '--zotero_home_dir', type=click.Path(exists=True, file_okay=False),
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
def main(prefs_file, zotero_home_dir, zotero_file, force_delete,
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
    -f ~/Zotero/zotero.sqlite -o ~/orphans.txt

    Delete files listed in ~/orphans.txt file:

    python zotler.py -l ~/orphans.txt
    """

    if zotero_home_dir is None:
        zotero_home_dir = os.path.join(str(Path.home()), 'Zotero')

    if zotero_file is None:
        zotero_file = os.path.join(zotero_home_dir, 'zotero.sqlite')

    prefs_file = zotler.get_prefs_file(prefs_file)
    base_path = zotler.get_base_path(prefs_file)
    relative_paths = zotler.get_relative_paths(zotero_file)
    absolute_paths = set(zotler.get_absolute_paths(base_path, relative_paths))

    existing_files = set(zotler.get_paths_to_existing_files(base_path))
    orphan_files = existing_files - absolute_paths

    print(10 * '-')

    if force_delete:
        zotler.remove_files(orphan_files)
    else:
        print('\n'.join(orphan_files), file=output_file)


if __name__ == '__main__':
    exit(main())
