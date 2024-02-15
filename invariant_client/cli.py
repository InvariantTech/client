import argparse
import datetime
import io
import json
import logging
import logging.config
import os
import pathlib
import ssl
import stat
import sys
import time
import pprint

from attrs import asdict
from tabulate import tabulate

from invariant_client import auth, display, zip_util
from invariant_client import pysdk
from invariant_client.display import OutputFormat


CREDS_FILE_PATH = pathlib.Path.cwd()
try:
    CREDS_FILE_PATH = pathlib.Path.home()
except RuntimeError:
    pass
finally:
    CREDS_FILE_PATH = CREDS_FILE_PATH.joinpath('.invariant_creds')


def parse_args():
    parser = argparse.ArgumentParser(
        prog='invariant',
        description='Invariant analyzes network snapshots',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        title='available commands',
        description='Run [command] --help for more information.',
        dest='command')
    command_login       = subparsers.add_parser(
        'login',
        description='Authenticate by opening a link in your browser. Saves credentials to ~/.invariant_creds.',
        help="Authenticate by opening a link in your browser. Saves credentials to ~/.invariant_creds.")
    command_run         = subparsers.add_parser(
        'run',
        description='Analyze the current directory.',
        help="Analyze the current directory.")
    command_show        = subparsers.add_parser(
        'show',
        description='Examine Invariant analysis results.',
        help="Examine Invariant analysis results.")
    command_solution    = subparsers.add_parser(
        'show_solution',
        description='Display a suggested patch result.',
        help="Display a suggested patch result.")
    command_snapshots   = subparsers.add_parser(
        'snapshots',
        description='List prior snapshot analysis results.',
        help="List prior snapshot analysis results.")

    def add_common_arguments(parser):
        parser.add_argument(
            '--json',
            dest='json',
            action='store_true',
            help='Output data as JSON.',
        )
        parser.add_argument(
            '--tsv',
            dest='tsv',
            action='store_true',
            help='Output data as TSV.',
        )
        parser.add_argument(
            '--debug',
            dest='debug',
            action='store_true',
            help='Enable detailed logging.',
        )
    
    add_common_arguments(command_login)
    add_common_arguments(command_run)
    add_common_arguments(command_snapshots)
    add_common_arguments(command_show)
    add_common_arguments(command_solution)

    command_run.add_argument(
        '--compare-to',
        dest='compare_to',
        help='Compare this snapshot to another by its git ref. Ref must refer to the primary git repository.',
    )

    command_run.add_argument(
        '--target',
        dest='target',
        help='An Invariant project root directory. Default is current directory.',
    )

    command_show.add_argument(
        'snapshot_name',
        help='The snapshot to examine.'
    )

    command_show.add_argument(
        'file_name',
        help='The snapshot file to examine.'
    )

    command_solution.add_argument(
        'snapshot_name',
        help='The snapshot to examine.'
    )

    command_solution.add_argument(
        'solution_name',
        help='The solution to examine.'
    )

    args = parser.parse_args()

    command = getattr(args, 'command')
    if not command:
        parser.print_usage()
        exit(0)

    return args


def serialize(inst, field, value):
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


def configure_logging(debug: bool):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.config.dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "incremental": True,
                "loggers": {
                    "multipart.multipart": {"level": "INFO"},
                },
            }
        )
    try:
        import rich.console
        import rich.logging
        root_logger = logging.getLogger()
        rich_handler = rich.logging.RichHandler(
            rich_tracebacks=True,
            omit_repeated_times=False,
            tracebacks_show_locals=True,
            tracebacks_suppress=[],
            show_time=False,
            show_path=False,
            console=rich.console.Console(stderr=True),
        )
        root_logger.addHandler(rich_handler)
    except ImportError:
        pass

    
def EntryPoint():
    args = parse_args()

    command = getattr(args, 'command')

    format = OutputFormat.TABULATE
    if getattr(args, 'json'):
        format = OutputFormat.JSON
    elif getattr(args, 'tsv'):
        format = OutputFormat.TSV
    
    debug = getattr(args, 'debug') or False
    configure_logging(debug)
    
    try:
        EntryPoint_inner(args, command, format, debug)
    except Exception as e:
        if debug:
            raise e
        print('Error: %s' % e, file=sys.stderr)
        exit(1)


def EntryPoint_inner(args, command, format, debug):
    settings: pysdk.Settings = {
        'format': format,
        'debug': debug,
    }

    env = dict(os.environ)
    invariant_domain = env.get('INVARIANT_DOMAIN', 'https://invariant.tech')

    creds = None

    if command == 'login':
        # TODO warn before logging in if an API token is present (possibly check if it works?)
        workflow = auth.BrowserLoginFlow(invariant_domain, ssl.create_default_context())
        link = workflow.start()
        print("Open this link in your browser to log in:")
        print(link)
        try:
            end_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
            # time.sleep(10)  # poor man's websocket
            time.sleep(6)  # poor man's websocket
            # TODO consider a nice animated "waiting" message for interactive terminal
            while not creds and end_time > datetime.datetime.now():
                result = workflow.poll_await_browser_creds()
                if isinstance(result, pysdk.AccessCredential):
                    creds = result
                    break
                elif isinstance(result, int):
                    time.sleep(result)
                else:
                    time.sleep(2)
            if not creds:
                print("Timed out.")
                exit(1)
            with open(CREDS_FILE_PATH, 'w') as f:
                f.write(creds.to_json())
            CREDS_FILE_PATH.chmod(
                stat.S_IRUSR |
                stat.S_IWUSR
            )
            print("Login successful.")
        except KeyboardInterrupt as e:
            print("Exiting...")
            exit(1)

        exit(0)
    
    # Load credentials or error
    try:
        creds = pysdk.AccessCredential.from_env(env, base_url=invariant_domain)
        if not creds:
            try:
                creds = pysdk.AccessCredential.from_file(CREDS_FILE_PATH, base_url=invariant_domain)
            except FileNotFoundError:
                # Expected
                creds = None
            if not creds:
                print("Please run 'invariant login' to authenticate.", file=sys.stderr)
                exit(1)

    except pysdk.AuthorizationException as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please run 'invariant login' to authenticate.", file=sys.stderr)
        if debug:
            raise e
        exit(1)
    except pysdk.RemoteError as e:
        print(f"Error: {e}", file=sys.stderr)
        if debug:
            raise e
        exit(1)

    sdk = pysdk.Invariant(
        creds=creds,
        settings=settings,
        base_url=invariant_domain)

    if command == "run":
        target = getattr(args, 'target') or '.'
        bytes = None
        if pathlib.Path(target).is_file():
            with open(target, "rb") as f:
                bytes = io.BytesIO(f.read())
        elif pathlib.Path(target).is_dir():
            bytes = io.BytesIO()
            zip_util.zip_dir(target, bytes)  # Write a zip file into 'bytes'
        else:
            print("Unacceptable target", file=sys.stderr)
            print(str(target), file=sys.stderr)
            exit(1)

        compare_to = getattr(args, 'compare_to')
        print("Uploading snapshot...")
        exec_uuid = sdk.upload_snapshot(
            source=bytes,
            compare_to=compare_to)
        exec_uuid = exec_uuid.exec_uuid
        end_time = datetime.datetime.now() + datetime.timedelta(weeks=1)
        print(f"Processing... ({exec_uuid})")
        while datetime.datetime.now() < end_time:
            response = sdk.upload_is_running(exec_uuid)
            if not response.is_running:
                break
            # TODO send some RetryAfter header to control this
            # TODO separately, exponential back-off on error
            time.sleep(4)
        if not response:
            print("Timed out.")
            exit(1)
        print("Analysis complete.")
        response = sdk.snapshot_detail(exec_uuid)
        # pprint.pprint(asdict(response), width=200)
        display.snapshot_status(response)
        if response.status['state'] == 'COMPLETED':
            display.snapshot_halted(response)
            print('')
            display.snapshot_summary_table(response, format)

            if response.summary['errors'] > 0:
                print(f"{response.summary['errors']} found. Run 'invariant errors {exec_uuid}' to examine.")
        else:
            if response.summary['errors'] > 0:
                errors_uuid = response.report.reports.errors
                errors_response = sdk.snapshot_file(errors_uuid)
                display.snapshot_errors(errors_response, format)

    elif command == "snapshots":
        snapshots = sdk.list_snapshots()
        if format == OutputFormat.JSON:
            print(json.dumps(asdict(snapshots, value_serializer=serialize), default=vars))
        elif format == OutputFormat.TSV:
            reports = asdict(snapshots)
            reports = reports['reports']
            print(tabulate(reports, headers='keys', tablefmt='tsv'))
        # if format == 'markdown':
        #     return tabulate(result, headers='keys', tablefmt='github')
        else:
            reports = asdict(snapshots)
            reports = reports['reports']
            print(tabulate(reports, headers='keys', tablefmt='psql'))


    elif command == "snapshot":
        sdk.snapshot_detail(
            report_uuid=args.snapshot_name)

    elif command == "show":
        sdk.show(
            snapshot=args.snapshot_name,
            file=args.file_name)

    elif command == "show_solution":
        sdk.show_solution(
            snapshot=args.snapshot_name,
            solution=args.solution_name)

    else:
        print(f"Unknown command {command}", file=sys.stderr)
