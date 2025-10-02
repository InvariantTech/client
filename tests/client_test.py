import json
import os
import pathlib
import tempfile
import unittest
from pathlib import PosixPath

import boto3
import pytest
from moto import mock_aws
from pydantic import SecretStr

from invariant_client import config
from invariant_client.config import SourceKind
from invariant_client import pysdk
from invariant_client.lib import fetcher
from pathlib import Path

######
# WARNING
# Always make sure commands use the mocked_aws fixture
# As a safe guard you can set the following environment variables
# export AWS_ACCESS_KEY_ID='testing'
# export AWS_SECRET_ACCESS_KEY='testing'
# export AWS_SECURITY_TOKEN='testing'
# export AWS_SESSION_TOKEN='testing'
# export AWS_DEFAULT_REGION='us-east-1'
####

LIBRENMS_API_KEY = "MOCK_LIBRENMS_API_KEY_FROM_AWS"
API_KEY = "abcdefg1234567"
SSH_KEY = "-----BEGIN OPENSSH PRIVATE KEY-----\nMOCK_SSH_KEY_CONTENT\n-----END OPENSSH PRIVATE KEY-----"


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-west-2"


##
# AWS Fixtures
##
@pytest.fixture(scope="function")
def mocked_aws(aws_credentials):
    """
    Mock all AWS interactions
    Requires you to create your own boto3 clients
    """
    with mock_aws():
        yield


@pytest.fixture(scope="function")
def standard_organization(mocked_aws):
    org_client = boto3.client("organizations")
    org_client.create_organization()
    org_client.create_account(Email="foobar@gmail.com", AccountName="abc")

    secrets_client = boto3.client("secretsmanager", region_name="us-west-2")
    secrets_client.create_secret(
        Name="prod/invariant/fetcher",
        SecretString=json.dumps({"LIBRENMS": LIBRENMS_API_KEY, "API_KEY": API_KEY}),
    )
    secrets_client.create_secret(
        Name="prod/ssh_key",
        SecretString=SSH_KEY,
    )
    secrets_client.create_secret(
        Name="fooasdadsy",
        SecretString=SSH_KEY,
    )


##
# LibreNMS Fixtures
##
@pytest.fixture(scope="function")
def mock_librenms(mocker):
    mock = mocker.patch("invariant_client.lib.librenms.client.LibreNMSClient")
    return mock


##
# Netmiko Fixtures
##


@pytest.fixture(scope="function")
def mock_netmiko(mocker):
    mock = mocker.patch("netmiko.Netmiko")
    return mock


class TestFetcher(unittest.TestCase):
    """
    Outline for fetcher tests using pytest.
    """

    @pytest.fixture(autouse=True)
    def setup(self, standard_organization, mock_librenms, mock_netmiko, mocker):
        """
        Setup for each test, automatically used.
        """
        self.standard_organization = standard_organization
        self.mock_librenms = mock_librenms
        self.mock_netmiko = mock_netmiko
        self.mocker = mocker

    @pytest.fixture(autouse=True)
    def testFull(self, standard_organization, mock_librenms, mock_netmiko, tmp_path):
        # move to using pysdk
        current_dir = Path(__file__).parent
        current_dir = str(current_dir.joinpath("config1.yaml"))
        fetcher.Fetcher(current_dir, output_path=tmp_path).fetch()

    # def test_fetcher_valid_config_with_secret_resolution(self):
    #     input_config = """
    #     sources:
    #       - kind: librenms
    #         name: librenms-inventory
    #         hostname: http://192.168.1.153:8889/
    #         device_group: Backup
    #         api_key: "secret+aws://prod/invariant/fetcher?key=LIBRENMS"
    #         ssh_key: "secret+aws://prod/ssh_key"
    #         ssh_user: vscode
    #       - kind: aws
    #         name: aws_prod
    #         regions:
    #           - us-west-1
    #           - us-west-2
    #         accounts:
    #           - '381492141036'
    #           - '831926619701'
    #     output_path: /workspaces/www/p/client/test_out
    #     """
    #     with tempfile.NamedTemporaryFile(mode="w+", suffix=".yaml") as tmpfile:
    #         tmpfile.write(input_config)
    #         tmpfile.flush()
    #         tmpfile_path = tmpfile.name
    #         result = config.load_and_validate_yaml(tmpfile_path)
    #         expected = {
    #             "output_path": PosixPath("/workspaces/www/p/client/test_out"),
    #             "sources": [
    #                 {
    #                     "name": "librenms-inventory",
    #                     "kind": SourceKind.LIBRENMS,
    #                     "hostname": "http://192.168.1.153:8889/",
    #                     "device_group": "Backup",
    #                     "api_key": SecretStr(LIBRENMS_API_KEY),
    #                     "ssh_key": SecretStr(SSH_KEY),
    #                     "ssh_key_path": None,
    #                     "ssh_user": "vscode",
    #                 },
    #                 {
    #                     "name": "aws_prod",
    #                     "kind": SourceKind.AWS,
    #                     "profile": None,
    #                     "role": None,
    #                     "regions": ["us-west-1", "us-west-2"],
    #                     "accounts": ["381492141036", "831926619701"],
    #                     "ignore_accounts": [],
    #                     "skip_resources": [],
    #                 },
    #             ],
    #         }
    #         self.assertEqual(result.model_dump(), expected)

    # def test_valid_config_env_secrets_resolution(self):
    #     self.mocker.patch.dict(
    #         os.environ,
    #         {
    #             "MY_ENV_API_KEY": "api_key_from_env_var",
    #             "MY_ENV_SSH_KEY": "ssh_key_content_from_env_var",
    #         },
    #     )
    #     input_config = """
    #     sources:
    #       - kind: librenms
    #         name: librenms-inventory
    #         hostname: http://192.168.1.153:8889/
    #         device_group: Backup
    #         api_key:
    #           store: env
    #           path: MY_ENV_API_KEY
    #         ssh_key:
    #           store: env
    #           path: MY_ENV_SSH_KEY
    #         ssh_user: vscode
    #     output_path: /workspaces/www/p/client/test_out
    #     """
    #     with tempfile.NamedTemporaryFile(mode="w+", suffix=".yaml") as tmpfile:
    #         tmpfile.write(input_config)
    #         tmpfile.flush()
    #         tmpfile_path = tmpfile.name
    #         result = config.load_and_validate_yaml(tmpfile_path)
    #         result_source = result.sources[0]
    #         self.assertEqual(result_source.api_key, SecretStr("api_key_from_env_var"))
    #         self.assertEqual(
    #             result_source.ssh_key, SecretStr("ssh_key_content_from_env_var")
    #         )

    # def test_valid_config_plain_string_secrets(self):
    #     input_config = """
    #     sources:
    #       - kind: librenms
    #         name: librenms-inventory
    #         hostname: http://192.168.1.153:8889/
    #         device_group: Backup
    #         api_key: BAR
    #         ssh_key: FOO
    #     output_path: /workspaces/www/p/client/test_out
    #     """
    #     with tempfile.NamedTemporaryFile(mode="w+", suffix=".yaml") as tmpfile:
    #         tmpfile.write(input_config)
    #         tmpfile.flush()
    #         tmpfile_path = tmpfile.name
    #         result = config.load_and_validate_yaml(tmpfile_path)
    #         result_source = result.sources[0]
    #         self.assertEqual(result_source.api_key, SecretStr("BAR"))
    #         self.assertEqual(result_source.ssh_key, SecretStr("FOO"))

    # def test_valid_config_invalid_out_path(self):
    #     input_config = """
    #     sources:
    #       - kind: librenms
    #         name: librenms-inventory
    #         hostname: http://192.168.1.153:8889/
    #         device_group: Backup
    #         api_key: BAR
    #         ssh_key: FOO
    #         ssh_key_path: /not/real/path
    #     output_path: /workspaces/www/p/client/test_out
    #     """
    #     with tempfile.NamedTemporaryFile(mode="w+", suffix=".yaml") as tmpfile:
    #         tmpfile.write(input_config)
    #         tmpfile.flush()
    #         tmpfile_path = tmpfile.name
    #         with self.assertRaisesRegex(ValueError, "Path does not point to a file"):
    #             config.load_and_validate_yaml(tmpfile_path)

    # def test_valid_config_conflict_ssh_key_and_path(self):
    #     """Test valid config with secrets provided as plain strings."""

    #     with tempfile.TemporaryDirectory() as tmpdir:
    #         tmp_test_dir = pathlib.Path(tmpdir)
    #         dummy_ssh_key_file = tmp_test_dir / "key.pem"
    #         dummy_ssh_key_file.touch()
    #         input_config = f"""
    #         sources:
    #         - kind: librenms
    #           name: librenms-inventory
    #           hostname: "http://192.168.1.153:8889/"
    #           device_group: Backup
    #           api_key: BAR
    #           ssh_key: FOO
    #           ssh_key_path: "{dummy_ssh_key_file.as_posix()}"
    #         output_path: /workspaces/www/p/client/test_out
    #         """
    #         config_temp_file = tmp_test_dir / "config.yaml"
    #         with open(config_temp_file, "w") as f:
    #             f.write(input_config)

    #         with self.assertRaisesRegex(
    #             ValueError, "Fields 'ssh_key' and 'ssh_key_path' are mutually exclusive"
    #         ):
    #             config.load_and_validate_yaml(config_temp_file)
