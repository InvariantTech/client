from copy import deepcopy
from pathlib import Path
import pytest
from unittest import mock

from invariant_client import config

VALID_YAML = {
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


INVALID_YAML_LIBRENMS_MISSING_SSH_API = {
    "sources": [
        {
            "kind": "librenms",
            "name": "librenms-inventory",
            "hostname": "http://localhost/",
            "device_group": "Backup",
            "ssh_user": "user"
        }
    ]
}

INVALID_YAML_UNKNOWN_KIND = {
    "sources": [
        {
            "kind": "unknown",
            "name": "bad-source"
        }
    ]
}

def test_valid_yaml_loads():
    cfg = config.validate_yaml(VALID_YAML)
    assert len(cfg.sources) == 2
    assert cfg.sources[0].kind == config.SourceKind.LIBRENMS
    assert cfg.sources[1].kind == config.SourceKind.AWS

def test_missing_ssh_key_and_path_raises_exactly_one():
    bad = deepcopy(INVALID_YAML_LIBRENMS_MISSING_SSH_API)
    bad["sources"][0] = dict(bad["sources"][0])
    bad["sources"][0]["api_key"] = "dummy_api_key"
    bad["sources"][0]["ssh_key"] = "dummy_ssh_key"
    bad["sources"][0]["ssh_key_path"] = "/tmp/dummy_ssh_key_path"

    with mock.patch("pathlib.Path.exists", return_value=True), \
         mock.patch("pathlib.Path.is_file", return_value=True), \
         mock.patch("pathlib.Path.is_dir", return_value=False):
        with pytest.raises(ValueError) as excinfo:
            config.validate_yaml(bad)
    msg = str(excinfo.value)
    assert "Fields 'ssh_key' and 'ssh_key_path' are mutually exclusive" in msg


def test_ssh_key_path():
    bad = deepcopy(INVALID_YAML_LIBRENMS_MISSING_SSH_API)
    bad["sources"][0] = dict(bad["sources"][0])
    bad["sources"][0]["api_key"] = "dummy_api_key"
    bad["sources"][0]["ssh_key_path"] = "/tmp/dummy_ssh_key_path"

    with mock.patch("pathlib.Path.exists", return_value=True), \
         mock.patch("pathlib.Path.is_file", return_value=True), \
         mock.patch("pathlib.Path.is_dir", return_value=False):
        config.validate_yaml(bad)

def test_missing_ssh_key_and_path_raises_field_required():
    bad = deepcopy(INVALID_YAML_LIBRENMS_MISSING_SSH_API)
    bad["sources"][0] = dict(bad["sources"][0])
    bad["sources"][0]["api_key"] = "dummy_api_key"
    with pytest.raises(ValueError) as excinfo:
        config.validate_yaml(bad)
    msg = str(excinfo.value)
    assert "Exactly one of 'ssh_key' or 'ssh_key_path' is required" in msg

def test_unknown_kind_raises():
    with pytest.raises(ValueError) as excinfo:
        config.validate_yaml(INVALID_YAML_UNKNOWN_KIND)
    msg = str(excinfo.value)
    assert "Input tag 'unknown' found using 'kind' does not match any of the expected tags" in msg

def test_invalid_yaml_type():
    with pytest.raises(Exception):
        config.validate_yaml("not a dict")

def test_secret_resolution(monkeypatch):
    # Patch the AWSSecretLoader.load method to simulate secret resolution
    with mock.patch("invariant_client.loaders.AWSSecretLoader.load", return_value="resolved_secret"):
        yaml = {
            "sources": [
                {
                    "kind": "librenms",
                    "name": "librenms-inventory",
                    "hostname": "http://localhost/",
                    "device_group": "Backup",
                    "api_key": "secret+aws://dummy",
                    "ssh_key": "secret+aws://dummy",
                    "ssh_user": "user"
                }
            ]
        }
        cfg = config.validate_yaml(yaml)
        src = cfg.sources[0]
        assert src.api_key.get_secret_value() == "resolved_secret"
        assert src.ssh_key.get_secret_value() == "resolved_secret"

def test_yaml_parsing_error():
    # Simulate a YAML error by passing a non-dict, non-list
    with pytest.raises(ValueError) as excinfo:
        config.validate_yaml(None)
    assert "Configuration validation error" in str(excinfo.value) or "Invalid YAML" in str(excinfo.value)

def test_minimal_librenms_config():
    minimal = {
        "sources": [
            {
                "kind": "librenms",
                "name": "librenms-minimal",
                "hostname": "http://localhost/",
                "device_group": "Backup",
                "api_key": "dummy_api_key",
                "ssh_key": "dummy_ssh_key"
            }
        ]
    }
    cfg = config.validate_yaml(minimal)
    assert len(cfg.sources) == 1
    src = cfg.sources[0]
    assert src.kind == config.SourceKind.LIBRENMS
    assert src.api_key.get_secret_value() == "dummy_api_key"
    assert src.ssh_key.get_secret_value() == "dummy_ssh_key"
    assert src.ssh_key_path is None


def test_minimal_aws_config():
    minimal = {
        "sources": [
            {
                "kind": "aws",
                "name": "aws-minimal",
                "accounts": ["123456789012"]
            }
        ]
    }
    cfg = config.validate_yaml(minimal)
    assert len(cfg.sources) == 1
    src = cfg.sources[0]
    assert src.kind == config.SourceKind.AWS
    assert src.accounts == ["123456789012"]
    assert src.regions == []


def test_multiple_sources_each_kind():
    config_dict = {
        "sources": [
            {
                "kind": "librenms",
                "name": "librenms-1",
                "hostname": "http://localhost/",
                "device_group": "Backup",
                "api_key": "key1",
                "ssh_key": "ssh1"
            },
            {
                "kind": "librenms",
                "name": "librenms-2",
                "hostname": "http://localhost/",
                "device_group": "Backup",
                "api_key": "key2",
                "ssh_key": "ssh2"
            },
            {
                "kind": "aws",
                "name": "aws-1",
                "accounts": ["111111111111"]
            },
            {
                "kind": "aws",
                "name": "aws-2",
                "accounts": ["222222222222"]
            }
        ]
    }
    cfg = config.validate_yaml(config_dict)
    assert len(cfg.sources) == 4
    librenms_names = [s.name for s in cfg.sources if s.kind == config.SourceKind.LIBRENMS]
    aws_names = [s.name for s in cfg.sources if s.kind == config.SourceKind.AWS]
    assert set(librenms_names) == {"librenms-1", "librenms-2"}
    assert set(aws_names) == {"aws-1", "aws-2"}
