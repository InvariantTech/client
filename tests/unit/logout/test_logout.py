import argparse
from pathlib import Path
from unittest import mock

import pytest

from invariant_client.logout_command.logout import LogoutCommand


@pytest.fixture
def logout_cmd():
    cmd = LogoutCommand()
    args = argparse.Namespace(verbose=False, debug=False)
    env = {}
    cmd.set_config(args, env)
    return cmd


class TestParseArgs:
    def test_registers_logout_subcommand(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')
        LogoutCommand.parse_args(subparsers)
        args = parser.parse_args(['logout'])
        assert args.command == 'logout'


class TestExecute:
    def test_removes_msal_cache(self, logout_cmd, tmp_path, capsys):
        cache_file = tmp_path / "invariantcli.token.cache"
        cache_file.write_text('{"token": "abc"}')

        with mock.patch("invariant_client.logout_command.logout.xdg_data_home", return_value=tmp_path), \
             mock.patch("invariant_client.logout_command.logout.CREDS_FILE_PATH", tmp_path / ".invariant_creds"):
            logout_cmd.execute()

        assert not cache_file.exists()
        captured = capsys.readouterr()
        assert "Logged out." in captured.out

    def test_removes_legacy_creds_file(self, logout_cmd, tmp_path, capsys):
        creds_file = tmp_path / ".invariant_creds"
        creds_file.write_text('{"token": "abc"}')

        with mock.patch("invariant_client.logout_command.logout.xdg_data_home", return_value=tmp_path), \
             mock.patch("invariant_client.logout_command.logout.CREDS_FILE_PATH", creds_file):
            logout_cmd.execute()

        assert not creds_file.exists()
        captured = capsys.readouterr()
        assert "Logged out." in captured.out

    def test_removes_both_files(self, logout_cmd, tmp_path, capsys):
        cache_file = tmp_path / "invariantcli.token.cache"
        cache_file.write_text('{"token": "abc"}')
        creds_file = tmp_path / ".invariant_creds"
        creds_file.write_text('{"token": "def"}')

        with mock.patch("invariant_client.logout_command.logout.xdg_data_home", return_value=tmp_path), \
             mock.patch("invariant_client.logout_command.logout.CREDS_FILE_PATH", creds_file):
            logout_cmd.execute()

        assert not cache_file.exists()
        assert not creds_file.exists()
        captured = capsys.readouterr()
        assert "Logged out." in captured.out

    def test_no_credentials_found(self, logout_cmd, tmp_path, capsys):
        with mock.patch("invariant_client.logout_command.logout.xdg_data_home", return_value=tmp_path), \
             mock.patch("invariant_client.logout_command.logout.CREDS_FILE_PATH", tmp_path / ".invariant_creds"):
            logout_cmd.execute()

        captured = capsys.readouterr()
        assert "Already logged out." in captured.out

    def test_oserror_on_cache_removal(self, logout_cmd, tmp_path, capsys):
        cache_file = tmp_path / "invariantcli.token.cache"
        cache_file.write_text('{"token": "abc"}')

        with mock.patch("invariant_client.logout_command.logout.xdg_data_home", return_value=tmp_path), \
             mock.patch("invariant_client.logout_command.logout.CREDS_FILE_PATH", tmp_path / ".invariant_creds"), \
             mock.patch.object(Path, "unlink", side_effect=OSError("permission denied")):
            logout_cmd.execute()

        captured = capsys.readouterr()
        assert "Warning" in captured.err
        assert "permission denied" in captured.err

    def test_oserror_on_creds_removal_still_succeeds_for_cache(self, logout_cmd, tmp_path, capsys):
        cache_file = tmp_path / "invariantcli.token.cache"
        cache_file.write_text('{"token": "abc"}')
        creds_file = tmp_path / ".invariant_creds"
        creds_file.write_text('{"token": "def"}')

        original_unlink = Path.unlink

        def selective_unlink(self_, *args, **kwargs):
            if self_.name == ".invariant_creds":
                raise OSError("permission denied")
            original_unlink(self_, *args, **kwargs)

        with mock.patch("invariant_client.logout_command.logout.xdg_data_home", return_value=tmp_path), \
             mock.patch("invariant_client.logout_command.logout.CREDS_FILE_PATH", creds_file), \
             mock.patch.object(Path, "unlink", selective_unlink):
            logout_cmd.execute()

        assert not cache_file.exists()
        assert creds_file.exists()  # removal failed
        captured = capsys.readouterr()
        assert "Logged out." in captured.out  # still reports success because cache was removed
        assert "Warning" in captured.err
