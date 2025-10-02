import unittest
import pathlib
import tempfile
import os
import yaml
import io
import sys
from contextlib import redirect_stderr

# Assuming the function is in invariant_client.rule_pick
from invariant_client.eval_command.pick_rule import (
    pick_rule,
    SelectorFormatError,
    PolicyNotFoundError,
    RuleNotFoundError,
    AmbiguousRuleNameError,
    InvalidPolicyFileFormatError
)

# --- Test Data ---

VALID_YAML_MULTI_POLICY = """
access-policy:
  - name: policy1
    comment: First policy
    ingress-network: NET_X
    rules:
      - name: rule_name_1a # index 0
        protocol: tcp
        destination-port: 80
        source-address: 10.0.0.1
      - protocol: udp # index 1, no name
        destination-port: 53
        source-address: 10.0.0.2
      - name: rule_name_1c # index 2
        protocol: icmp
        source-address: 10.0.0.3
  - name: policy2
    comment: Second policy
    egress-network: NET_Y
    rules:
      - name: unique_rule_name_2a # index 0
        protocol: icmp
        destination-address: 8.8.8.8
      - name: another_rule_2b # index 1
        source-address: ANY
        destination-address: 1.1.1.1
"""

YAML_AMBIGUOUS_RULE_NAME = """
access-policy:
  - name: policyA
    rules:
      - name: shared_rule_name
        protocol: tcp
  - name: policyB
    rules:
      - name: shared_rule_name
        protocol: udp
"""

YAML_MISSING_ACCESS_POLICY_KEY = """
some-other-key:
  - name: policy1
    rules: []
"""

YAML_ACCESS_POLICY_NOT_LIST = """
access-policy:
  name: policy1
  rules: []
"""

YAML_POLICY_RULES_NOT_LIST = """
access-policy:
  - name: policy1
    rules: not_a_list
"""

YAML_RULE_NOT_DICT = """
access-policy:
  - name: policy1
    rules:
      - rule1
      - name: rule2 # this one is ok
"""


YAML_INVALID_SYNTAX = """
access-policy:
  - name: policy1
   rules: # Indentation error
    - name: rule1
"""

YAML_EMPTY = ""

# --- Expected Outputs ---

EXPECTED_POLICY1_RULE0 = """
access-policy:
- name: policy1
  comment: First policy
  ingress-network: NET_X
  rules:
  - name: rule_name_1a
    protocol: tcp
    destination-port: 80
    source-address: 10.0.0.1
"""

EXPECTED_POLICY1_RULE1 = """
access-policy:
- name: policy1
  comment: First policy
  ingress-network: NET_X
  rules:
  - protocol: udp
    destination-port: 53
    source-address: 10.0.0.2
"""

EXPECTED_POLICY2_RULE0 = """
access-policy:
- name: policy2
  comment: Second policy
  egress-network: NET_Y
  rules:
  - name: unique_rule_name_2a
    protocol: icmp
    destination-address: 8.8.8.8
"""

# --- Test Class ---

class TestPickRuleToYAML(unittest.TestCase):

    def _create_temp_file(self, content: str) -> str:
        """Helper to create a temporary file with content."""
        # Use delete=False and manage deletion with addCleanup
        with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False, suffix=".yaml") as temp_file:
            temp_file.write(content)
            file_path = temp_file.name
        # Ensure the file is removed even if the test fails after this point
        self.addCleanup(os.remove, file_path)
        return file_path

    def _assert_yaml_equal(self, actual_yaml_str: str, expected_yaml_str: str):
        """Asserts that two YAML strings represent the same Python structure."""
        try:
            actual_data = yaml.safe_load(actual_yaml_str)
            expected_data = yaml.safe_load(expected_yaml_str)
            self.assertEqual(actual_data, expected_data)
        except yaml.YAMLError as e:
            self.fail(f"Failed to parse YAML for comparison: {e}\nActual:\n{actual_yaml_str}\nExpected:\n{expected_yaml_str}")

    # --- Success Cases ---

    def test_select_by_policy_index_valid(self):
        """Test selecting a rule by policy name and index."""
        file_path = self._create_temp_file(VALID_YAML_MULTI_POLICY)
        result_yaml = pick_rule(file_path, "policy1[1]")
        self._assert_yaml_equal(result_yaml, EXPECTED_POLICY1_RULE1)

    def test_select_by_policy_index_first(self):
        """Test selecting the first rule by policy name and index."""
        file_path = self._create_temp_file(VALID_YAML_MULTI_POLICY)
        result_yaml = pick_rule(file_path, "policy1[0]")
        self._assert_yaml_equal(result_yaml, EXPECTED_POLICY1_RULE0)

    def test_select_by_policy_rule_name_valid(self):
        """Test selecting a rule by policy name and rule name."""
        file_path = self._create_temp_file(VALID_YAML_MULTI_POLICY)
        result_yaml = pick_rule(file_path, "policy1:rule_name_1a")
        self._assert_yaml_equal(result_yaml, EXPECTED_POLICY1_RULE0)

    def test_select_by_unique_rule_name(self):
        """Test selecting a rule by its unique name across all policies."""
        file_path = self._create_temp_file(VALID_YAML_MULTI_POLICY)
        result_yaml = pick_rule(file_path, "unique_rule_name_2a")
        self._assert_yaml_equal(result_yaml, EXPECTED_POLICY2_RULE0)

    # --- Error Cases - File/YAML ---

    def test_error_file_not_found(self):
        """Test error when the input file does not exist."""
        stderr_io = io.StringIO()
        with self.assertRaises(FileNotFoundError) as cm, redirect_stderr(stderr_io):
            pick_rule("non_existent_file.yaml", "policy[0]")
        self.assertIn("Policy file not found", stderr_io.getvalue())

    def test_error_invalid_yaml(self):
        """Test error when the input file has invalid YAML syntax."""
        file_path = self._create_temp_file(YAML_INVALID_SYNTAX)
        stderr_io = io.StringIO()
        with self.assertRaises(yaml.YAMLError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "policy1[0]")
        self.assertIn("Failed to parse YAML file", stderr_io.getvalue())

    def test_error_empty_file(self):
        """Test error when the input file is empty."""
        file_path = self._create_temp_file(YAML_EMPTY)
        stderr_io = io.StringIO()
        # yaml.safe_load returns None for empty input, triggering format error
        with self.assertRaises(InvalidPolicyFileFormatError) as cm, redirect_stderr(stderr_io):
             pick_rule(file_path, "policy1[0]")
        self.assertIn("Top level must be a dictionary", stderr_io.getvalue())


    # --- Error Cases - Invalid Policy Structure ---

    def test_error_no_access_policy_key(self):
        """Test error when 'access-policy' key is missing."""
        file_path = self._create_temp_file(YAML_MISSING_ACCESS_POLICY_KEY)
        stderr_io = io.StringIO()
        with self.assertRaises(InvalidPolicyFileFormatError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "policy1[0]")
        self.assertIn("missing top-level 'access-policy' key", stderr_io.getvalue())

    def test_error_access_policy_not_list(self):
        """Test error when 'access-policy' value is not a list."""
        file_path = self._create_temp_file(YAML_ACCESS_POLICY_NOT_LIST)
        stderr_io = io.StringIO()
        with self.assertRaises(InvalidPolicyFileFormatError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "policy1[0]")
        self.assertIn("'access-policy' should contain a list", stderr_io.getvalue())

    def test_error_policy_rules_not_list(self):
        """Test error when a policy's 'rules' value is not a list."""
        file_path = self._create_temp_file(YAML_POLICY_RULES_NOT_LIST)
        stderr_io = io.StringIO()
        with self.assertRaises(InvalidPolicyFileFormatError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "policy1[0]") # Selector targets the policy with bad rules
        self.assertIn("invalid 'rules' list", stderr_io.getvalue())
        self.assertIn("policy1", stderr_io.getvalue())

    def test_error_rule_not_dict(self):
        """Test error when an item in the 'rules' list is not a dictionary."""
        file_path = self._create_temp_file(YAML_RULE_NOT_DICT)
        stderr_io = io.StringIO()
        with self.assertRaises(InvalidPolicyFileFormatError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "policy1[0]") # Select the bad rule
        self.assertIn("Invalid rule format at index 0", stderr_io.getvalue())


    # --- Error Cases - Selector and Not Found ---

    def test_error_selector_format_invalid(self):
        """Test various invalid selector formats."""
        file_path = self._create_temp_file(VALID_YAML_MULTI_POLICY)
        invalid_selectors = ["policy[", "policy:name[1", ":rule", "policy[]", "policy1:rule name with space"]
        for selector in invalid_selectors:
            with self.subTest(selector=selector):
                stderr_io = io.StringIO()
                with self.assertRaises(SelectorFormatError) as cm, redirect_stderr(stderr_io):
                    pick_rule(file_path, selector)
                self.assertIn("names must match the pattern", stderr_io.getvalue())

    def test_error_policy_not_found_by_index(self):
        """Test error when policy name (from index selector) doesn't exist."""
        file_path = self._create_temp_file(VALID_YAML_MULTI_POLICY)
        stderr_io = io.StringIO()
        with self.assertRaises(PolicyNotFoundError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "nonexistent_policy[0]")
        self.assertIn("Policy 'nonexistent_policy' not found", stderr_io.getvalue())

    def test_error_policy_not_found_by_name(self):
        """Test error when policy name (from name selector) doesn't exist."""
        file_path = self._create_temp_file(VALID_YAML_MULTI_POLICY)
        stderr_io = io.StringIO()
        with self.assertRaises(PolicyNotFoundError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "nonexistent_policy:rule_name_1a")
        self.assertIn("Policy 'nonexistent_policy' not found", stderr_io.getvalue())

    def test_error_rule_index_out_of_bounds(self):
        """Test error when rule index is out of bounds for the policy."""
        file_path = self._create_temp_file(VALID_YAML_MULTI_POLICY)
        stderr_io = io.StringIO()
        with self.assertRaises(RuleNotFoundError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "policy1[99]")
        self.assertIn("Rule index 99 out of bounds for policy 'policy1'", stderr_io.getvalue())
        self.assertIn("(has 3 rules)", stderr_io.getvalue())

    def test_error_rule_name_not_found_in_policy(self):
        """Test error when rule name is not found within the specified policy."""
        file_path = self._create_temp_file(VALID_YAML_MULTI_POLICY)
        stderr_io = io.StringIO()
        with self.assertRaises(RuleNotFoundError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "policy1:nonexistent_rule")
        self.assertIn("Rule named 'nonexistent_rule' not found within policy 'policy1'", stderr_io.getvalue())

    def test_error_rule_name_not_found_unique(self):
        """Test error when rule name (unique selector) doesn't exist anywhere."""
        file_path = self._create_temp_file(VALID_YAML_MULTI_POLICY)
        stderr_io = io.StringIO()
        with self.assertRaises(RuleNotFoundError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "unique_nonexistent_rule")
        self.assertIn("Rule named 'unique_nonexistent_rule' not found in any policy", stderr_io.getvalue())

    def test_error_rule_name_ambiguous(self):
        """Test error when rule name (unique selector) matches multiple rules."""
        file_path = self._create_temp_file(YAML_AMBIGUOUS_RULE_NAME)
        stderr_io = io.StringIO()
        with self.assertRaises(AmbiguousRuleNameError) as cm, redirect_stderr(stderr_io):
            pick_rule(file_path, "shared_rule_name")
        self.assertIn("Ambiguous rule selector: Rule name 'shared_rule_name' found in multiple policies", stderr_io.getvalue())


if __name__ == '__main__':
    unittest.main()
