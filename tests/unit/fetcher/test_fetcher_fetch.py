import json
import os
from pathlib import Path
import tempfile

import boto3
from moto import mock_aws
import pytest

from unittest import mock
from invariant_client.lib import fetcher
from invariant_client import config
import copy
import shutil

TEST_SSH_KEY_DATA = "X" * 64 + "Y" * 20
TEST_SSH_KEY = f"-----BEGIN EC PRIVATE KEY-----   {TEST_SSH_KEY_DATA}   -----END EC PRIVATE KEY-----"
TEST_LMNS_API_KEY = "dummy_api_key"
TEST_AWS_SECRET_SSH_KEY = "-----BEGIN OPENSSH PRIVATE KEY-----\nMOCK_SSH_KEY_CONTENT\n-----END OPENSSH PRIVATE KEY-----"

ARISTA_EOS_MOCK_CONFIG = "hostname rtr.arista.core\ninterface Ethernet1\n no switchport\n ip address 10.0.0.1/24\n!"
JUNIPER_SRX_MOCK_CONFIG = "system {\n host-name fw.juniper.edge;\n services {\n  ssh;\n }\n}\ninterfaces {\n ge-0/0/0 {\n  unit 0 {\n   family inet {\n    address 192.168.1.1/24;\n   }\n  }\n }\n}"


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-west-1"



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
    org_client = boto3.client("organizations", region_name="us-west-1")
    try:
        org_client.create_organization(FeatureSet="ALL")
    except Exception:
        pass
    secrets_client = boto3.client("secretsmanager", region_name="us-west-1")
    secrets_client.create_secret(
        Name="prod/invariant/fetcher",
        SecretString=json.dumps({"LIBRENMS": TEST_LMNS_API_KEY, "API_KEY": TEST_LMNS_API_KEY}),
    )
    secrets_client.create_secret(
        Name="prod/ssh_key",
        SecretString=TEST_AWS_SECRET_SSH_KEY,
    )
    secrets_client.create_secret(
        Name="fooasdadsy",
        SecretString=TEST_AWS_SECRET_SSH_KEY,
    )
    # Add AWS resources in us-west-1 as per valid_yaml_dict AWS source
    ec2_uw1 = boto3.client("ec2", region_name="us-west-1")
    vpc_uw1 = ec2_uw1.create_vpc(CidrBlock="10.1.0.0/16")["Vpc"]
    subnet_uw1 = ec2_uw1.create_subnet(VpcId=vpc_uw1["VpcId"], CidrBlock="10.1.1.0/24")["Subnet"]
    sg_uw1 = ec2_uw1.create_security_group(GroupName="test-sg-uw1", Description="Test SG UW1", VpcId=vpc_uw1["VpcId"])["GroupId"]
    ec2_uw1.run_instances(ImageId="ami-12345678", InstanceType="t2.micro", MinCount=1, MaxCount=1, SubnetId=subnet_uw1["SubnetId"], SecurityGroupIds=[sg_uw1])
    rds_uw1 = boto3.client("rds", region_name="us-west-1")
    rds_uw1.create_db_instance(
        DBInstanceIdentifier="test-db-uw1",
        DBInstanceClass="db.t3.micro",
        Engine="postgres",
        AllocatedStorage=20,
        MasterUsername="user",
        MasterUserPassword="password"
    )
    elbv2_uw1 = boto3.client("elbv2", region_name="us-west-1")
    elbv2_uw1.create_load_balancer(Name="test-lb", Subnets=[subnet_uw1["SubnetId"]], SecurityGroups=[sg_uw1])


@pytest.fixture
def moto_account_id(standard_organization, mocked_aws):
    # Get the AWS account ID from moto
    org_client = boto3.client("organizations", region_name="us-west-1")
    accounts = org_client.list_accounts()["Accounts"]
    # Find the non-management account (the one created in the fixture)
    aws_account_id = None
    for acct in accounts:
        if acct["Name"] == "abc":
            aws_account_id = acct["Id"]
            break
    if not aws_account_id:
        # fallback: just use the first non-management account
        for acct in accounts:
            if acct["Name"] != "Root":
                aws_account_id = acct["Id"]
                break
    assert aws_account_id is not None
    return aws_account_id


@pytest.fixture
def valid_yaml_dict(moto_account_id):
    return {
        "sources": [
            {
                "kind": "librenms",
                "name": "librenms-inventory",
                "hostname": "http://localhost/",
                "device_group": "Backup",
                "api_key": TEST_LMNS_API_KEY,
                "ssh_key": "dummy_ssh_key",
                "ssh_user": "user"
            },
            {
                "kind": "aws",
                "name": "aws_prod",
                "regions": ["us-west-1"],
                "accounts": [moto_account_id]
            }
        ]
    }


@pytest.fixture
@mock.patch("invariant_client.lib.fetcher.librenms_client.LibreNMSClient")
@mock.patch("invariant_client.lib.fetcher.load")
@mock.patch("invariant_client.lib.fetcher.tempfile.TemporaryDirectory")
@mock.patch("invariant_client.lib.fetcher.os.chmod")
@mock.patch("builtins.open", new_callable=mock.mock_open)
def valid_fetcher(
    mock_open_file,
    mock_os_chmod,
    mock_temp_dir,
    mock_load,
    MockLibreNMSClient,
    valid_yaml_dict
):
    """
    Tests Fetcher.__init__ ensuring actual LibreNMSSource and AWSSource are instantiated,
    with LibreNMSClient and its dependencies mocked.
    """
    # Prepare a copy of the valid_yaml_dict to modify the ssh_key for reformat_pem
    test_config_dict = copy.deepcopy(valid_yaml_dict)
    test_config_dict["sources"][0]["ssh_key_path"] = None
    test_config_dict["sources"][0]["ssh_key"] = TEST_SSH_KEY

    mock_load.return_value = test_config_dict

    # 1. Mock for tempfile.TemporaryDirectory used by LibreNMSSource
    mock_temp_dir_instance = mock.Mock()
    mock_temp_dir_instance.name = "/fake/temp/ssh_keys_fetcher_init_test"
    mock_temp_dir.return_value = mock_temp_dir_instance

    # 2. Mock for LibreNMSClient instance (do NOT use spec, just a plain Mock)
    mock_librenms_client_instance = mock.Mock()
    # Mock test_connection called during LibreNMSClient.__init__
    mock_librenms_client_instance.test_connection.return_value = {"status": "ok", "message": "System operational"}
    # Mock methods for LibreNMSSource.fetch_data (though not called in this __init__ test, good for completeness)
    mock_librenms_client_instance.get_devices_by_group.return_value = {
        "devices": [
            {"device_id": "101", "hostname": "rtr.arista.core", "os": "arista_eos"},
            {"device_id": "102", "hostname": "fw.juniper.edge", "os": "junos"}
        ],
        "status": "ok"
    }
    def mock_get_device_side_effect(device_id_arg):
        if device_id_arg == "101":
            return {"devices": [{"device_id": "101", "os": "arista_eos", "hostname": "rtr.arista.core"}], "status": "ok"}
        elif device_id_arg == "102":
            return {"devices": [{"device_id": "102", "os": "junos", "hostname": "fw.juniper.edge"}], "status": "ok"}
        return {"devices": [], "status": "error", "message": "Device not found"}
    mock_librenms_client_instance.get_device.side_effect = mock_get_device_side_effect
    
    MockLibreNMSClient.return_value = mock_librenms_client_instance

    return fetcher.Fetcher(config_path="dummy_config_path", output_path="/tmp/test")



@mock.patch("invariant_client.lib.fetcher.anonymize_files.anonymize_files")
@mock.patch("invariant_client.lib.fetcher.ConnectHandler")
def test_fetch(
    MockConnectHandler,
    mock_anonymize_files,
    valid_fetcher,
    moto_account_id,
    standard_organization,
    mocked_aws,
    tmp_path,
    mocker
):
    with tempfile.TemporaryDirectory() as temp_output_dir:
        final_output_path = Path(temp_output_dir)
        valid_fetcher.output_path = final_output_path  # Set output_path directly

        mock_netmiko_connection = mock.MagicMock()
        def send_command_side_effect(command):
            if command == "show running-config":
                return ARISTA_EOS_MOCK_CONFIG
            elif command == "show":
                return JUNIPER_SRX_MOCK_CONFIG
            return ""
        mock_netmiko_connection.send_command.side_effect = send_command_side_effect
        MockConnectHandler.return_value = mock_netmiko_connection

        def fake_anonymize(unsafe_path, safe_path, anonymize_passwords, anonymize_ips, salt):
            if os.path.exists(safe_path):
                shutil.rmtree(safe_path)
            shutil.copytree(unsafe_path, safe_path, dirs_exist_ok=True)
        mock_anonymize_files.side_effect = fake_anonymize

        valid_fetcher.fetch()

        assert MockConnectHandler.call_count == 2
        calls = MockConnectHandler.call_args_list
        arista_call_args = calls[0][1]
        assert arista_call_args['host'] == "rtr.arista.core"
        assert arista_call_args['device_type'] == "arista_eos"
        assert arista_call_args['username'] == "user"
        assert 'key_file' in arista_call_args
        mock_netmiko_connection.enable.assert_any_call()
        juniper_call_args = calls[1][1]
        assert juniper_call_args['host'] == "fw.juniper.edge"
        assert juniper_call_args['device_type'] == "juniper"
        assert juniper_call_args['username'] == "user"
        assert 'key_file' in juniper_call_args
        mock_netmiko_connection.config_mode.assert_any_call()
        assert mock_netmiko_connection.send_command.call_count == 2
        mock_netmiko_connection.send_command.assert_any_call("show running-config")
        mock_netmiko_connection.send_command.assert_any_call("show")

        mock_anonymize_files.assert_called_once()
        args, kwargs = mock_anonymize_files.call_args
        assert args[0].name == "unsafe"
        assert args[1].name == "safe"
        assert args[2] is True
        assert args[3] is False
        assert "salt" in kwargs

        # Check output files in the real output directory
        librenms_output_dir = final_output_path / "configs" / "librenms-inventory"
        assert (librenms_output_dir / "rtr.arista.core.cfg").is_file()
        assert (librenms_output_dir / "rtr.arista.core.cfg").read_text() == ARISTA_EOS_MOCK_CONFIG
        assert (librenms_output_dir / "fw.juniper.edge.cfg").is_file()
        assert (librenms_output_dir / "fw.juniper.edge.cfg").read_text() == JUNIPER_SRX_MOCK_CONFIG
        aws_output_dir = final_output_path / "aws_configs" / moto_account_id / "us-west-1"
        # Debug: list files if assertion fails
        if not (aws_output_dir / "Reservations.json").is_file():
            print(f"aws_output_dir contents: {list(aws_output_dir.glob('*'))}")
        assert (aws_output_dir / "Reservations.json").is_file()
        assert (aws_output_dir / "Vpcs.json").is_file()
        assert (aws_output_dir / "Subnets.json").is_file()
        assert (aws_output_dir / "SecurityGroups.json").is_file()
        assert (aws_output_dir / "DBInstances.json").is_file()
        assert (aws_output_dir / "LoadBalancers.json").is_file()
        instances_data = json.loads((aws_output_dir / "Reservations.json").read_text())
        assert isinstance(instances_data, list) or "Reservations" in instances_data or "Reservations" in instances_data.get('Reservations', {})
        for source in valid_fetcher.sources:
            assert not source.fatal