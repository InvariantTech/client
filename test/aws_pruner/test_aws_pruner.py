import json
import pathlib
import tempfile
import unittest

from invariant_client.aws_pruner import AwsPruneTool, UserConfig, PruneLevel
from test.data_gen.generate_ec2_json import generate_aws_json
import shutil


class TestAwsPruner(unittest.TestCase):
    def setUp(self):
        """Setup temp directory and initial JSON data before each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.aws_config_dir = pathlib.Path(self.temp_dir.name)
        self.aws_config_dir.mkdir(exist_ok=True)  # Ensure the directory exists
        src_dir = pathlib.Path("test/aws_pruner/hybrid-cloud/us-east-2")
        for filename in ["Reservations.json", "NetworkInterfaces.json", "SecurityGroups.json"]:
            shutil.copy(src_dir / filename, self.aws_config_dir / filename)


    def tearDown(self):
        """Clean up the temporary directory after each test."""
        self.temp_dir.cleanup()

    def _run_pruner(self, user_config_dict: dict):
        """Helper function to run the pruner with a given configuration."""
        user_config = UserConfig.from_dict(user_config_dict)
        pruner = AwsPruneTool(
            self.aws_config_dir,
            user_config.prune_level,
            user_config.filter_exclude,
            user_config.filter_include,
            user_config.group_by,
        )
        pruner.load()
        pruner.execute()
        return pruner  # Return the pruner object for assertions.

    def _assert_eni_count(self, pruner, expected_count):
        """Helper function to assert the number of ENIs."""
        with open(self.aws_config_dir / "NetworkInterfaces.json", "r") as f:
            data = json.load(f)
            actual_count = len(data["NetworkInterfaces"])
        self.assertEqual(actual_count, expected_count)

    def _assert_ec2_count(self, pruner, expected_count):
        with open(self.aws_config_dir / "Reservations.json", "r") as f:
            data = json.load(f)
            actual_count = sum(len(res["Instances"]) for res in data["Reservations"])
        self.assertEqual(actual_count, expected_count)

    def _generate_and_write_data(self, num_instances):
        """Helper to generate and write AWS data to files."""
        reservations_data, network_interfaces_data, security_groups_data = generate_aws_json(
            self.aws_config_dir, num_instances
        )
        with open(self.aws_config_dir / "Reservations.json", "w") as f:
            json.dump(reservations_data, f, indent=1)
        with open(self.aws_config_dir / "NetworkInterfaces.json", "w") as f:
            json.dump(network_interfaces_data, f, indent=1)
        with open(self.aws_config_dir / "SecurityGroups.json", "w") as f:
            json.dump(security_groups_data, f, indent=1)


    def test_level_0_remove_all_ec2(self):
        """Test LEVEL_0_REMOVE_ALL_EC2: Remove all EC2 instances and ENIs."""
        self._generate_and_write_data(num_instances=5)
        user_config = {
            "prune_level": "LEVEL_0_REMOVE_ALL_EC2",
        }
        pruner = self._run_pruner(user_config)
        pruner.write()
        self._assert_ec2_count(pruner, 0)
        self._assert_eni_count(pruner, 2)  # There are some non-EC2 ENIs that remain.

    def test_level_1_one_ec2_per_subnet(self):
        """Test LEVEL_1_ONE_EC2_PER_SUBNET: Keep only one EC2 instance and ENI."""
        self._generate_and_write_data(num_instances=5)
        user_config = {
            "prune_level": "LEVEL_1_ONE_EC2_PER_SUBNET",
        }
        pruner = self._run_pruner(user_config)
        pruner.write()
        self._assert_ec2_count(pruner, 2)
        self._assert_eni_count(pruner, 4)  # There are some non-EC2 ENIs that remain.

    def test_level_1_one_ec2_per_subnet_with_group_by(self):
        """Test LEVEL_1_ONE_EC2_PER_SUBNET with group_by: Three EC2s and ENIs."""
        self._generate_and_write_data(num_instances=5)
        user_config = {
            "prune_level": "LEVEL_1_ONE_EC2_PER_SUBNET",
            "group_by": ["application_id"],
        }
        pruner = self._run_pruner(user_config)
        pruner.write()
        self._assert_ec2_count(pruner, 5)
        self._assert_eni_count(pruner, 7)  # There are some non-EC2 ENIs that remain.

    def test_level_2_one_ec2_per_subnet_and_sg(self):
        """Test LEVEL_2_ONE_EC2_PER_SUBNET_AND_SECURITY_GROUP: Keep only one EC2 instance and ENI."""
        self._generate_and_write_data(num_instances=5)
        user_config = {
            "prune_level": "LEVEL_2_ONE_EC2_PER_SUBNET_AND_SECURITY_GROUP",
        }
        pruner = self._run_pruner(user_config)
        pruner.write()
        self._assert_ec2_count(pruner, 4)
        self._assert_eni_count(pruner, 6)

    def test_level_2_one_ec2_per_subnet_and_sg_and_groups(self):
        """Test LEVEL_2_ONE_EC2_PER_SUBNET_AND_SECURITY_GROUP with grouping (no removal expected)"""
        self._generate_and_write_data(num_instances=5)
        user_config = {
            "prune_level": "LEVEL_2_ONE_EC2_PER_SUBNET_AND_SECURITY_GROUP",
            "group_by": ["application_id"],
        }
        pruner = self._run_pruner(user_config)
        pruner.write()
        self._assert_ec2_count(pruner, 7)
        self._assert_eni_count(pruner, 9)

    def test_level_2_one_ec2_per_subnet_and_sg_and_groups_no_remove(self):
        """Test LEVEL_2_ONE_EC2_PER_SUBNET_AND_SECURITY_GROUP with grouping (removal expected, unused tag)"""
        self._generate_and_write_data(num_instances=5)
        user_config = {
            "prune_level": "LEVEL_2_ONE_EC2_PER_SUBNET_AND_SECURITY_GROUP",
            "group_by": ["Other"],
        }
        pruner = self._run_pruner(user_config)
        pruner.write()
        self._assert_ec2_count(pruner, 4)
        self._assert_eni_count(pruner, 6)
