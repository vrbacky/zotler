#!/usr/bin/env python3

from pathlib import Path
import pytest
import os

from zotler import zotler


def test_print_version_prints_version_and_exits(mocker, ctx):
    mocked_exit = mocker.patch.object(ctx, 'exit')
    mocked_echo = mocker.patch('click.echo')
    zotler.print_version(ctx, None, 'lorem')

    mocked_echo.assert_called_once_with('0.0.1')
    mocked_exit.assert_called_once_with()


def test_print_version_returns_none_if_value_is_sent(mocker, ctx):
    mocked_exit = mocker.patch.object(ctx, 'exit')
    mocked_echo = mocker.patch('click.echo')

    assert zotler.print_version(ctx, None, None) is None
    mocked_echo.assert_not_called()
    mocked_exit.assert_not_called()


def test_delete_files_calls_remove_files(mocker, ctx):
    mocked_exit = mocker.patch.object(ctx, 'exit')
    mocked_remove_files = mocker.patch.object(zotler, 'remove_files')
    zotler.delete_files(ctx, None, 'lorem')

    mocked_remove_files.assert_called_once_with('lorem')
    mocked_exit.assert_called_once_with()


def test_delete_files_returns_none_if_value_iscalls_remove_files(mocker, ctx):
    mocked_exit = mocker.patch.object(ctx, 'exit')
    mocked_remove_files = mocker.patch.object(zotler, 'remove_files')

    assert zotler.delete_files(ctx, None, None) is None
    mocked_remove_files.assert_not_called()
    mocked_exit.assert_not_called()


@pytest.mark.parametrize('system, expected', [
    ('Linux', os.path.join(str(Path.home()), '.zotero', 'zotero')),
    ('Windows', os.path.join(str(Path.home()), 'AppData', 'Roaming', 'Zotero',
                             'Zotero', 'Profiles'))
])
def test_system_specific_path_to_profiles_in_linux(system, expected, mocker):
    mocked_platform = mocker.patch('platform.system')
    mocked_platform.return_value = system

    assert zotler.system_specific_path_to_profiles() == expected


def test_system_specific_path_to_profiles_unidentified_os(mocker):
    mocked_platform = mocker.patch('platform.system')
    mocked_platform.return_value = 'lorem'

    with pytest.raises(OSError):
        zotler.system_specific_path_to_profiles()


@pytest.mark.parametrize('value', ['Lorem', 5])
def test_get_prefs_file_returns_path_if_provided(value):
    assert zotler.get_prefs_file(value) == value


def test_get_prefs_file_finds_proper_path_in_profiles_did(mocker, profiles_dir):
    mocked_system_specific_path = mocker.patch.object(zotler,
                                                      'system_specific_path_to_profiles')
    mocked_system_specific_path.return_value = profiles_dir
    expected = os.path.join(profiles_dir, 'profile3.default', 'prefs.js')

    assert zotler.get_prefs_file(None) == expected


def test_get_base_path_returns_proper_value(prefs_path):
    assert zotler.get_base_path(prefs_path) == '/home/user/lorem/ipsum/Zotero'


def test_get_relative_paths_parses_correct_values(mocker, sql_result,
                                                  relative_paths):
    mocked_sql = mocker.patch.object(zotler, 'sqlite3')
    mocked_sql.connect().cursor().fetchall.return_value = sql_result
    found_paths = list(zotler.get_relative_paths(''))

    assert sorted(found_paths) == sorted(relative_paths)


def test_get_absolute_paths(relative_paths, absolute_paths):
    abs_paths = list(zotler.get_absolute_paths('lorem', relative_paths))

    assert sorted(abs_paths) == sorted(list(absolute_paths))


def test_get_pahs_to_existing_files(profiles_dir, expected_relative_paths):
    existing_paths = list(zotler.get_paths_to_existing_files(profiles_dir))
    expected_paths = [os.path.normpath(os.path.join(profiles_dir, i))
                      for i in expected_relative_paths]

    assert sorted(existing_paths) == sorted(expected_paths)


def test_remove_files_removes_stripped_files(mocker, paths_to_files):
    mocked_remove = mocker.patch('os.remove')
    zotler.remove_files(paths_to_files)

    mocked_remove.assert_any_call('lorem.txt')
    mocked_remove.assert_any_call('ipsum.txt')
    mocked_remove.assert_any_call('dolor.txt')
