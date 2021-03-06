#!/usr/bin/env python3

import click
import os
from pathlib import Path
import platform
import re
import sqlite3

import zotler


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(zotler.__version__)
    ctx.exit()


def delete_files(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    remove_files(value)
    ctx.exit()


def system_specific_path_to_profiles():
    system = platform.system()
    if system == 'Linux':
        path = os.path.join('.zotero', 'zotero')
    elif system == 'Windows':
        path = os.path.join('AppData', 'Roaming', 'Zotero',
                            'Zotero', 'Profiles')
    else:
        raise OSError('Unidentified OS. Cannot predict preferences '
                      'directory location.')
    return os.path.join(str(Path.home()), path)


def get_prefs_file(prefs_path=None, silent=False):
    if prefs_path is None:

        assumed_profiles_dir = system_specific_path_to_profiles()

        for item in os.listdir(assumed_profiles_dir):
            complete_path = os.path.join(assumed_profiles_dir, item)
            if os.path.isdir(complete_path) and item.endswith('default'):
                prefs_path = os.path.join(complete_path, 'prefs.js')
        if not silent:
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
        yield os.path.normpath(os.path.join(base_path, relative_path))


def get_paths_to_existing_files(base_dir):
    for directory, subdirs, files in os.walk(base_dir):
        for i in files:
            yield os.path.normpath(os.path.join(directory, i))


def create_set_of_orphans(zotero_dbase, zotero_prefs):
    base_path = get_base_path(zotero_prefs)
    relative_paths = get_relative_paths(zotero_dbase)
    absolute_paths = set(get_absolute_paths(base_path, relative_paths))

    existing_files = set(get_paths_to_existing_files(base_path))
    return existing_files - absolute_paths


def remove_files(filepaths):
    for file in filepaths:
        path = file.strip()
        if path == '':
            continue
        print(f'Removing: {path}')
        try:
            os.remove(path)
        except FileNotFoundError:
            print(f'File {path} not found.')
