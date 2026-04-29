import logging
import sys
import typing

from xdg_base_dirs import xdg_data_home

from invariant_client.base_command.base_command import CREDS_FILE_PATH, BaseCommand

if typing.TYPE_CHECKING:
    import argparse

logger = logging.getLogger(__name__)


class LogoutCommand(BaseCommand):
    needs_authn = False
    use_argument_debug = True
    # No format options for this command

    @classmethod
    def parse_args(cls, subparsers: 'argparse._SubParsersAction[argparse.ArgumentParser]') -> None:
        command_logout = subparsers.add_parser(
            'logout',
            description='Remove locally stored authentication credentials.',
            help="Remove locally stored authentication credentials.")

        cls._add_common_parser_arguments(command_logout)

    def set_config(self, args: 'argparse.Namespace', env: dict[str, str]) -> None:
        super().set_config(args, env)

    def execute(self):
        super().execute()
        removed_any = False

        # Remove MSAL token cache
        cache_path = xdg_data_home().joinpath("invariantcli.token.cache")
        if cache_path.exists():
            try:
                cache_path.unlink()
                logger.debug(f"Removed token cache at {cache_path}")
                removed_any = True
            except OSError as e:
                print(f"Warning: could not remove {cache_path}: {e}", file=sys.stderr)

        # Remove legacy credentials file
        if CREDS_FILE_PATH.exists():
            try:
                CREDS_FILE_PATH.unlink()
                logger.debug(f"Removed credentials file at {CREDS_FILE_PATH}")
                removed_any = True
            except OSError as e:
                print(f"Warning: could not remove {CREDS_FILE_PATH}: {e}", file=sys.stderr)

        if removed_any:
            print("Logged out.")
        else:
            print("No stored credentials found. Already logged out.")
