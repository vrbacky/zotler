#!/usr/bin/env python3

import os
from pathlib import Path
import re
import sqlite3

import zotler


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    print(zotler.__version__)
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
