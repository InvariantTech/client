import datetime
import json
import logging
import random
import sys
import time
import typing
import uuid

import backoff
from rich import print_json

from invariant_client import pysdk, display
from invariant_client.base_command.base_command import BaseCommand
from invariant_client.pysdk import OutputFormat

if typing.TYPE_CHECKING:
    import argparse


logger = logging.getLogger(__name__)


DEFAULT_RETRY_SECONDS = 3


class ResubmitTerminationError(Exception):
    """An exception that is raised when a resubmit task is terminated."""

    def __init__(self, *args, retry_after: int):
        super().__init__(self, *args)
        self.retry_after = retry_after


class ResubmitCommand(BaseCommand):
    use_argument_debug = True
    use_argument_group_format = True
    use_argument_format_condensed = True

    @classmethod
    def parse_args(cls, subparsers: 'argparse._SubParsersAction[argparse.ArgumentParser]') -> None:
        command_resubmit = subparsers.add_parser(
            'resubmit',
            description='Re-evaluate an uploaded snapshot. '
                        'Re-checks rules, probes, and network map against the existing snapshot model.',
            help="Re-evaluate an uploaded snapshot.")

        cls._add_common_parser_arguments(command_resubmit)

        snapshot_group = command_resubmit.add_mutually_exclusive_group()
        snapshot_group.add_argument(
            '--snapshot',
            dest='snapshot_name',
            help='The snapshot to resubmit (UUID). If unset, environment variable INVARIANT_SNAPSHOT is used.'
        )
        snapshot_group.add_argument(
            '--network',
            dest='network',
            help='Resubmit the most recent snapshot for the given network.'
        )

        command_resubmit.add_argument(
            '--no-wait',
            dest='no_wait',
            action='store_true',
            help='Start the resubmit and exit without waiting for completion.',
        )

    def set_config(self, args: 'argparse.Namespace', env: dict[str, str]) -> None:
        super().set_config(args, env)
        env_snapshot = env.get('INVARIANT_SNAPSHOT', None)
        self.snapshot_name = args.snapshot_name
        self.network = getattr(args, 'network', None)
        if not self.snapshot_name and not self.network:
            # Fallback to env var only when neither flag is provided
            self.snapshot_name = env_snapshot
        self.no_wait = getattr(args, 'no_wait', False)

    def execute(self):
        super().execute()
        snapshot_name = self.snapshot_name

        # Resolve --network to the most recent snapshot
        if not snapshot_name and self.network:
            snapshots = self.sdk.list_snapshots(filter_net=self.network, limit=1)
            if not snapshots:
                raise ValueError(f"No snapshots found for network '{self.network}'.")
            snapshot_name = str(snapshots[0].snapshot.uuid)

        # Fallback: use latest snapshot for current session
        if not snapshot_name:
            last_snapshot = self.sdk.list_reports(filter_session=True, limit=1)
            if not last_snapshot or len(last_snapshot.reports) == 0:
                raise ValueError(
                    "No snapshot specified. Use --snapshot <uuid>, --network <name>, "
                    "or set the INVARIANT_SNAPSHOT environment variable.")
            snapshot_name = last_snapshot.reports[0].uuid

        # Validate UUID
        if isinstance(snapshot_name, uuid.UUID):
            snapshot_uuid = snapshot_name
        else:
            try:
                snapshot_uuid = uuid.UUID(snapshot_name, version=4)
            except ValueError as e:
                raise ValueError(
                    f"Expected {snapshot_name} to be a UUID like f5b4e387-e336-499e-b3a0-d6186c590572.") from e

        # Call the resubmit API (with backoff on termination)
        try:
            exec_uuid = resubmit_snapshot(
                self.sdk, snapshot_uuid, self.format, self.no_wait)
        except KeyboardInterrupt as e:
            print("Exiting...", file=sys.stderr)
            exit(1)

        if self.no_wait:
            return

        # Display results — identical to run command
        if self.format == OutputFormat.TABULATE:
            print("Resubmit complete.")
        response = self.sdk.report_detail(exec_uuid)
        if self.format == OutputFormat.JSON or self.format == OutputFormat.FAST_JSON:
            response_json = json.dumps(response.to_dict(), sort_keys=True)
            try:
                print_json(response_json)
            except:
                print(response_json)
        elif self.format == OutputFormat.CONDENSED:
            if response.status['state'] != 'COMPLETE':
                if response.summary['errors'] > 0:
                    errors_locator = response.report.reports.errors
                    errors_response = self.sdk.snapshot_file(errors_locator)
                    display.snapshot_errors(errors_response, self.format)
            display.snapshot_condensed_status(response)
        else:
            display.snapshot_status(response)
            if response.status['state'] == 'COMPLETE':
                display.snapshot_halted(response)
                print('')
                summary = self.sdk.report_detail_text(str(exec_uuid), json_mode=False)
                if summary.text:
                    print(summary.text)
                else:
                    display.snapshot_summary_table(response, self.format)

                print(f"\nRun 'invariant show <file>' to examine any file.")

                if response.summary['errors'] > 0:
                    print(f"\n{response.summary['errors']} {'error' if response.summary['errors'] == 1 else 'errors'} found.")
                    errors_locator = response.report.reports.errors
                    errors_response = self.sdk.snapshot_file(errors_locator)
                    display.snapshot_errors(errors_response, self.format)

            else:
                if response.summary['errors'] > 0:
                    errors_locator = response.report.reports.errors
                    errors_response = self.sdk.snapshot_file(errors_locator)
                    display.snapshot_errors(errors_response, self.format)


@backoff.on_exception(
        backoff.runtime,
        ResubmitTerminationError,
        value=lambda e: e.retry_after + random.uniform(0, e.retry_after),
        jitter=None,
        logger=None,
        on_backoff=lambda _: logger.warning('Resubmit was remotely terminated, retrying...'),
        max_tries=3)
def resubmit_snapshot(
    sdk: pysdk.Invariant,
    snapshot_uuid: uuid.UUID,
    format: OutputFormat,
    no_wait: bool = False,
) -> str:
    if format == OutputFormat.TABULATE:
        print(f"Resubmitting snapshot {snapshot_uuid}...")
    response = sdk.resubmit_snapshot(snapshot_uuid)
    exec_uuid = response.exec_uuid

    if format == OutputFormat.TABULATE:
        print(f"Processing... ({exec_uuid})")
    elif format == OutputFormat.CONDENSED:
        print(f"snapshot: {exec_uuid}")

    if no_wait:
        if format == OutputFormat.TABULATE:
            print("Resubmit started in --no-wait mode.")
        elif format == OutputFormat.CONDENSED:
            print(f"outcome: started")
        return exec_uuid

    end_time = datetime.datetime.now() + datetime.timedelta(weeks=1)
    while datetime.datetime.now() < end_time:
        status_response = sdk.upload_is_running(exec_uuid)
        if status_response.terminated:
            raise ResubmitTerminationError(
                f"Resubmit was remotely terminated, try again later",
                retry_after=status_response.retry_after_seconds or DEFAULT_RETRY_SECONDS)
        if not status_response.is_running:
            break
        time.sleep(4)
    if not status_response:
        print("Timed out.", file=sys.stderr)
        exit(1)
    return exec_uuid
