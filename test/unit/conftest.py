#!/usr/bin/env python3

import click
import os
import pytest


@pytest.fixture()
def ctx():
    command = click.command()
    ctx = click.Context(command,
                        allow_extra_args=True,
                        allow_interspersed_args=True,
                        ignore_unknown_options=True)
    return ctx


@pytest.fixture()
def profiles_dir(tmpdir):
    tmpdir.mkdir('profile1')
    dir2 = tmpdir.mkdir('profile2')
    default = tmpdir.mkdir('profile3.default')
    files = (dir2.join('file21.txt'),
             dir2.join('file22.txt'),
             default.join('file1.txt'),
             default.join('file2.txt'),
             default.join('prefs.js')
             )
    for file in files:
        file.write('lorem ipsum')

    return tmpdir


@pytest.fixture()
def prefs_path(tmpdir):
    prefs_file = tmpdir.join('prefs.js')
    txt = ('user_pref("extensions.zotero.baseAttachmentPath",'
           '"/home/user/lorem/ipsum/Zotero");\n'
           'user_pref("extensions.zotero.dataDir", "/home/user/Zotero");\n'
           'user_pref("extensions.zotero.export.lastLocale", "en-US");\n'
           'user_pref("extensions.zotero.export.lastStyle",'
           '"http://www.zotero.org/styles/ieee");\n'
           'user_pref("extensions.zotero.export.quickCopy.setting",'
           '"bibliography=http://www.zotero.org/styles/nature");\n'
           'user_pref("extensions.zotero.firstRun.skipFirefoxProfileAccessCheck",'
           'true);\n'
           'user_pref("extensions.zotfile.dest_dir", "/home/user/lorem/ipsum/Zotero");\n'
           'user_pref("extensions.zotfile.import", false);\n'
           'user_pref("extensions.zotfile.removeDiacritics", true);\n'
           'user_pref("extensions.zotfile.renameFormat", "{%a-}{%y-}{%t}");\n'
           'user_pref("extensions.zotfile.renameFormat_patent", "{%a-}{%y-}{%t}");\n'
           'user_pref("extensions.zotfile.replace_blanks", true);')
    prefs_file.write(txt)
    return prefs_file


@pytest.fixture()
def cursor():
    import sqlite3
    connection = sqlite3.connect("")
    return connection.cursor()


@pytest.fixture()
def sql_result():
    return (
            ('attachments:Programming/R/Packages/lorem.pdf', ),
            ('attachments:Programming/R/Packages/lorem.R.html', ),
            ('attachments:Programming/Python/isum.pdf', ),
            ('attachments:Programming/Python/PEP/PEP_8.pdf', )
    )


@pytest.fixture()
def relative_paths():
    return [
        'Programming/R/Packages/lorem.pdf',
        'Programming/R/Packages/lorem.R.html',
        'Programming/Python/isum.pdf',
        'Programming/Python/PEP/PEP_8.pdf'
    ]


@pytest.fixture()
def absolute_paths(relative_paths):
    return (os.path.normpath(os.path.join('lorem', i)) for i in relative_paths)


@pytest.fixture()
def expected_relative_paths():
    paths = ['profile3.default/file2.txt',
             'profile3.default/file1.txt',
             'profile3.default/prefs.js',
             'profile2/file21.txt',
             'profile2/file22.txt',
             ]
    return paths


@pytest.fixture()
def paths_to_files():
    return [i for i in ('lorem.txt', 'ipsum.txt  ', 'dolor.txt\n')]
