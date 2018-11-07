#!/usr/bin/env python3

import click
import os
from pathlib import Path
import re
import sqlite3
import sys

VERSION = '0.0.1'


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    print(VERSION)
    exit()


def delete_files(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    remove_files(value)
    exit()


def get_prefs_file(prefs_path):
    if prefs_path is None:
        assumend_settings_dir = os.path.join(str(Path.home()), '.zotero', 'zotero')
        for item in os.listdir(assumend_settings_dir):
            complete_path = os.path.join(assumend_settings_dir, item)
            if os.path.isdir(complete_path) and item.endswith('default'):
                prefs_path = os.path.join(complete_path, 'prefs.js')
        print(f'*** No Zotero settings prefs.js file specified by -p option. '
              f'Default file {prefs_path} will be used.')
    return prefs_path


def get_base_path(prefs_path):
    with open(prefs_path, 'r') as js_file:
        pattern = re.compile(
            r'^user_pref\("extensions\.zotfile\.dest_dir", "(.*)"\);$'
        )
        for line in js_file:
            match = re.match(pattern, line)
            if match:
                return match.group(1)


def get_relative_paths(sql_file):
    connection = sqlite3.connect(sql_file)
    cursor = connection.cursor()
    cursor.execute('SELECT path FROM itemAttachments WHERE path IS NOT NULL')
    pattern = re.compile('^attachments:(.*)$')
    for records in cursor.fetchall():
        match = re.match(pattern, records[0])
        yield match.group(1)


def get_absolute_paths(base_path, relative_paths):
    for relative_path in relative_paths:
        yield os.path.join(base_path, relative_path)


def get_paths_to_existing_files(base_dir):
    for directory, subdirs, files in os.walk(base_dir):
        for i in files:
            yield os.path.join(directory, i)


def remove_files(filepaths):
    for file in filepaths:
        path = file.strip()
        print(f'Removing: {path}')
        os.remove(path)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-l', '--list_of_files', type=click.File('r'),
              callback=delete_files, expose_value=False, is_eager=True,
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
@click.option('-v', '--version', is_flag=True, callback=print_version,
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

    prefs_file = get_prefs_file(prefs_file)
    base_path = get_base_path(prefs_file)
    relative_paths = get_relative_paths(zotero_file)
    absolute_paths = set(get_absolute_paths(base_path, relative_paths))

    existing_files = set(get_paths_to_existing_files(base_path))
    orphan_files = existing_files - absolute_paths

    print(10 * '-')

    if force_delete:
        remove_files(orphan_files)
    else:
        print('\n'.join(orphan_files), file=output_file)


if __name__ == '__main__':
    exit(main())
