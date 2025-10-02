from pathlib import Path

import pytest

from unittest import mock
from invariant_client.lib import fetcher
from invariant_client import config
import copy

# Test Plan: Only valid YAML inputs, mock out loaders.load.

@pytest.fixture
def valid_yaml_dict():
    return {
        "sources": [
            {
                "kind": "librenms",
                "name": "librenms-inventory",
                "hostname": "http://localhost/",
                "device_group": "Backup",
                "api_key": "dummy_api_key",
                "ssh_key": "dummy_ssh_key",
                "ssh_user": "user"
            },
            {
                "kind": "aws",
                "name": "aws_prod",
                "regions": ["us-west-1"],
                "accounts": ["123456789012"]
            }
        ]
    }

@mock.patch("invariant_client.lib.fetcher.AWSSource")
@mock.patch("invariant_client.lib.fetcher.LibreNMSSource")
@mock.patch("invariant_client.lib.fetcher.load")
def test_fetcher_init_valid_yaml(mock_load, mock_librenms_source, mock_aws_source, valid_yaml_dict):
    """
    Tests Fetcher.__init__ with valid YAML data.
    Ensures that loaders.load is called, and the correct source classes are instantiated.
    """
    mock_load.return_value = valid_yaml_dict

    # Patch the SOURCE_TYPE_TO_CLASS_MAP to use the mocks
    with mock.patch.dict(
        fetcher.SOURCE_TYPE_TO_CLASS_MAP,
        {
            config.SourceKind.LIBRENMS: mock_librenms_source,
            config.SourceKind.AWS: mock_aws_source,
        }
    ):
        # Create Pydantic model instances from the raw dict for assertion,
        # as this is what Fetcher will pass to the source constructors.
        expected_librenms_config = config.LibreNMSConfig(**valid_yaml_dict["sources"][0])
        expected_aws_config = config.AWSConfig(**valid_yaml_dict["sources"][1])

        fetcher_instance = fetcher.Fetcher(config_path="dummy_path", output_path="/tmp/test")

        mock_load.assert_called_once_with("dummy_path")
        assert isinstance(fetcher_instance.config, config.TopLevelConfig)
        assert len(fetcher_instance.sources) == 2

        # Check that LibreNMSSource was called with the correct Pydantic model
        mock_librenms_source.assert_called_once()
        called_librenms_config = mock_librenms_source.call_args[1]['source_config']
        assert called_librenms_config == expected_librenms_config

        # Check that AWSSource was called with the correct Pydantic model
        mock_aws_source.assert_called_once()
        called_aws_config = mock_aws_source.call_args[1]['source_config']
        assert called_aws_config == expected_aws_config

        assert fetcher_instance.sources[0] == mock_librenms_source.return_value
        assert fetcher_instance.sources[1] == mock_aws_source.return_value

@mock.patch("invariant_client.lib.fetcher.librenms_client.LibreNMSClient")
@mock.patch("invariant_client.lib.fetcher.tempfile.TemporaryDirectory")
@mock.patch("invariant_client.lib.fetcher.os.chmod")
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_librenms_source_init_with_ssh_key_content(
    mock_open_file,
    mock_os_chmod,
    mock_temp_dir,
    mock_librenms_client_class,
    valid_yaml_dict
):
    """
    Tests LibreNMSSource.__init__ when ssh_key content is provided.
    Ensures a temporary file is created with correctly formatted PEM content,
    permissions are set, and LibreNMSClient is initialized.
    """
    # Setup mock for TemporaryDirectory
    mock_temp_dir_instance = mock.Mock()
    mock_temp_dir_instance.name = "/fake/temp/ssh_keys_dir"
    mock_temp_dir.return_value = mock_temp_dir_instance

    # Mock for LibreNMSClient instance
    mock_librenms_client_instance = mock.Mock()
    mock_librenms_client_class.return_value = mock_librenms_client_instance

    # Prepare LibreNMSConfig data
    librenms_config_data = valid_yaml_dict["sources"][0].copy()
    
    # Raw key content that needs reformatting (84 chars of key data)
    key_data = "A" * 64 + "B" * 20
    unformatted_ssh_key = f"-----BEGIN OPENSSH PRIVATE KEY-----   {key_data}   -----END OPENSSH PRIVATE KEY-----"
    
    librenms_config_data["ssh_key"] = unformatted_ssh_key
    librenms_config_data["ssh_key_path"] = None # Ensure ssh_key_path is None for this test case

    source_config = config.LibreNMSConfig(**librenms_config_data)

    # Instantiate LibreNMSSource
    librenms_source = fetcher.LibreNMSSource(source_config=source_config)

    # 1. Assert tempfile.TemporaryDirectory was called
    mock_temp_dir.assert_called_once_with(prefix="ssh_keys_")

    # 2. Assert open was called to write the key to the correct path
    expected_key_file_path = "/fake/temp/ssh_keys_dir/ssh_key"
    mock_open_file.assert_called_once_with(expected_key_file_path, "w", encoding="utf-8")

    # 3. Assert content written to the file is correctly PEM formatted
    expected_pem_content = (
        "-----BEGIN OPENSSH PRIVATE KEY-----\n"
        f"{key_data[:64]}\n"
        f"{key_data[64:]}\n"
        "-----END OPENSSH PRIVATE KEY-----\n"
    )
    file_handle_mock = mock_open_file() 
    written_content = file_handle_mock.write.call_args[0][0]
    assert written_content == expected_pem_content

    # 4. Assert os.chmod was called with correct path and mode
    mock_os_chmod.assert_called_once_with(expected_key_file_path, 0o600)

    # 5. Assert LibreNMSClient was instantiated correctly
    mock_librenms_client_class.assert_called_once_with(
        source_config.hostname,
        source_config.api_key.get_secret_value()
    )

    # 6. Assert the ssh_key_path attribute is set correctly
    assert librenms_source.ssh_key_path == expected_key_file_path

    # 7. Test cleanup
    librenms_source.close()
    mock_temp_dir_instance.cleanup.assert_called_once()


@mock.patch("invariant_client.lib.fetcher.librenms_client.LibreNMSClient")
@mock.patch("invariant_client.lib.fetcher.os.path.isfile")
def test_librenms_source_init_with_ssh_key_path(
    mock_os_path_isfile,
    mock_librenms_client_class,
    valid_yaml_dict
):
    """
    Tests LibreNMSSource.__init__ when ssh_key_path is provided.
    Ensures that no temporary file is created for the key, and os.path.isfile is checked.
    """
    with mock.patch("pathlib.Path.is_file", return_value=True):
        mock_os_path_isfile.return_value = True # Simulate that the key file exists

        # Mock for LibreNMSClient instance
        mock_librenms_client_instance = mock.Mock()
        mock_librenms_client_class.return_value = mock_librenms_client_instance

        # Prepare LibreNMSConfig data
        librenms_config_data = valid_yaml_dict["sources"][0].copy()
        provided_ssh_key_path = "/path/to/my/existing_key.pem"
        librenms_config_data["ssh_key"] = None # Ensure ssh_key is None
        librenms_config_data["ssh_key_path"] = provided_ssh_key_path
        
        source_config = config.LibreNMSConfig(**librenms_config_data)

        # Instantiate LibreNMSSource
        librenms_source = fetcher.LibreNMSSource(source_config=source_config)

        # 1. Assert os.path.isfile was called with the provided path
        mock_os_path_isfile.assert_called_once_with(Path(provided_ssh_key_path))

        # 2. Assert LibreNMSClient was instantiated correctly
        mock_librenms_client_class.assert_called_once_with(
            source_config.hostname,
            source_config.api_key.get_secret_value()
        )

        # 3. Assert the ssh_key_path attribute is set to the provided path
        assert librenms_source.ssh_key_path == Path(provided_ssh_key_path)

        # 4. Test cleanup (temp dir manager should be None)
        assert librenms_source._temp_dir_manager is None
        librenms_source.close() # Should be a no-op for _temp_dir_manager

@mock.patch("invariant_client.lib.fetcher.librenms_client.LibreNMSClient")
@mock.patch("invariant_client.lib.fetcher.load")
@mock.patch("invariant_client.lib.fetcher.tempfile.TemporaryDirectory")
@mock.patch("invariant_client.lib.fetcher.os.chmod")
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_fetcher_with_sources(
    mock_open_file,
    mock_os_chmod,
    mock_temp_dir,
    mock_load,
    MockLibreNMSClient,  # Mock for the LibreNMSClient class
    valid_yaml_dict
):
    """
    Tests Fetcher.__init__ ensuring actual LibreNMSSource and AWSSource are instantiated,
    with LibreNMSClient and its dependencies mocked.
    """
    # Prepare a copy of the valid_yaml_dict to modify the ssh_key for reformat_pem
    test_config_dict = copy.deepcopy(valid_yaml_dict)
    key_data = "X" * 64 + "Y" * 20
    unformatted_ssh_key = f"-----BEGIN EC PRIVATE KEY-----   {key_data}   -----END EC PRIVATE KEY-----"
    test_config_dict["sources"][0]["ssh_key_path"] = None
    test_config_dict["sources"][0]["ssh_key"] = unformatted_ssh_key

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

    # --- Instantiate Fetcher ---
    fetcher_instance = fetcher.Fetcher(config_path="dummy_config_path", output_path="/tmp/test")

    # --- Assertions ---

    # 1. Assert 'load' was called
    mock_load.assert_called_once_with("dummy_config_path")
    assert isinstance(fetcher_instance.config, config.TopLevelConfig)
    assert len(fetcher_instance.sources) == 2

    # 2. Assert LibreNMSSource instantiation and its internal calls
    assert isinstance(fetcher_instance.sources[0], fetcher.LibreNMSSource)
    librenms_source = fetcher_instance.sources[0]

    # Assert LibreNMSClient was instantiated correctly by LibreNMSSource
    expected_hostname = test_config_dict["sources"][0]["hostname"]
    expected_api_key = test_config_dict["sources"][0]["api_key"]
    MockLibreNMSClient.assert_called_once_with(
        expected_hostname,
        expected_api_key
    )

    # Assert temporary directory and SSH key file operations by LibreNMSSource
    mock_temp_dir.assert_called_once_with(prefix="ssh_keys_")
    
    expected_key_file_path = f"{mock_temp_dir_instance.name}/ssh_key"
    mock_open_file.assert_called_once_with(expected_key_file_path, "w", encoding="utf-8")
    
    # Assert content written to the file (after reformat_pem)
    expected_formatted_key_content = (
        "-----BEGIN EC PRIVATE KEY-----\n"
        f"{key_data[:64]}\n"
        f"{key_data[64:]}\n"
        "-----END EC PRIVATE KEY-----\n"
    )
    file_handle_mock = mock_open_file() 
    written_content = file_handle_mock.write.call_args[0][0]
    assert written_content == expected_formatted_key_content
    
    mock_os_chmod.assert_called_once_with(expected_key_file_path, 0o600)
    # Only check ssh_key_path before close(), since close() sets it to None
    assert librenms_source.ssh_key_path == expected_key_file_path
    
    # Now close and check cleanup
    librenms_source.close()
    mock_temp_dir_instance.cleanup.assert_called_once()

    # 3. Assert AWSSource instantiation
    assert isinstance(fetcher_instance.sources[1], fetcher.AWSSource)
    aws_source = fetcher_instance.sources[1]
    expected_aws = test_config_dict["sources"][1]
    assert aws_source.name == expected_aws["name"]
    assert aws_source.regions == expected_aws["regions"]
    assert aws_source.accounts == expected_aws["accounts"]

    # Cleanup check for LibreNMSSource
    mock_temp_dir_instance.cleanup.assert_called_once()

    # Now run .fetch()

