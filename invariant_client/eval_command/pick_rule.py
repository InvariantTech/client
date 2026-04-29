import logging
import os
import pathlib
import re
import sys
import yaml

logger = logging.getLogger(__name__)


class RulePickError(Exception):
    """Base exception for RulePick errors."""

class SelectorError(RulePickError):
    """Base for errors related to selector parsing or matching."""

class SelectorFormatError(SelectorError):
    """Raised when the selector format is invalid."""

class PolicyNotFoundError(SelectorError):
    """Raised when the specified policy is not found."""

class RuleNotFoundError(SelectorError):
    """Raised when the specified rule (by index) is not found."""

class AmbiguousRuleNameError(SelectorError):
    """Raised when a rule name matches multiple rules."""

class InvalidPolicyFileFormatError(RulePickError):
    """Raised when the policy file format is invalid."""


# policy_name[rule_name_or_index]
SELECTOR_POLICY_RULE_REGEX = re.compile(r"^(?P<policy_name>[a-zA-Z0-9_\-]+)\[(?P<rule_selector>[a-zA-Z0-9_\-]+)\]$")
# just a number or rule name
SELECTOR_GLOBAL_REGEX = re.compile(r"^(?P<rule_selector>[a-zA-Z0-9_\-]+)$")


def pick_rule(target_policy_file: str | os.PathLike, selector: str | None) -> str:
    """
    Selects a specific rule from an access policy YAML file based on a selector
    and generates a new YAML string containing only that rule within its
    original parent policy structure.

    Prints user-facing error messages to stderr before raising exceptions
    for errors like file not found, bad YAML, invalid selector, or rule/policy
    not found.

    Supported Selector Formats:
      - 'policy_name[rule_name]': Selects rule by name within a named policy.
      - 'policy_index[rule_name]': Selects rule by name within a policy at a given index.
      - 'rule_name': Selects rule by its name across all policies in the file (must be unique within the file).
      - 'policy_name[index]': Selects rule by index within a named policy.
      - 'policy_index[index]': Selects rule by index within a policy at a given index.
      - 'index': Selects rule by its global index across all policies in the file.

    Args:
        target_yaml_file: Path to the input YAML file.
        selector: String specifying the rule to select.

    Returns:
        A string containing the YAML representation of the selected rule within its policy.

    Raises:
        FileNotFoundError: If the target_yaml_file does not exist.
        yaml.YAMLError: If the target_yaml_file is not valid YAML.
        InvalidPolicyFileFormatError: If the YAML structure is incorrect.
        SelectorFormatError: If the selector string format is invalid or ambiguous.
        PolicyNotFoundError: If the policy specified in the selector is not found.
        RuleNotFoundError: If the rule specified in the selector is not found.
        RulePickError: For other generic errors during processing.
    """
    target_path = pathlib.Path(target_policy_file)
    loaded_data = _load_yaml_file(target_path)
    policies = _validate_and_get_policies(loaded_data, target_path)

    selected_policy = None
    selected_rule = None

    if selector is None:
        selected_policy, selected_rule = _find_by_global_rule_selector(
            policies, '0', target_path, no_selector=True
        )
    else:
        # --- Determine selector type and find rule/policy ---
        policy_rule_match = SELECTOR_POLICY_RULE_REGEX.match(selector)
        global_match = SELECTOR_GLOBAL_REGEX.match(selector)

        if policy_rule_match:
            policy_selector = policy_rule_match.group('policy_name')
            rule_selector = policy_rule_match.group('rule_selector')
            selected_policy, selected_rule = _find_by_policy_and_rule_selector(
                policies, policy_selector, rule_selector, target_path
            )
        elif global_match:
            rule_selector = global_match.group('rule_selector')
            selected_policy, selected_rule = _find_by_global_rule_selector(
                policies, rule_selector, target_path
            )
        else:
            msg = f"Invalid selector format: '{selector}'. Policy and rule names must match the pattern [a-zA-Z0-9_\-]+."
            print(f"Error: {msg}", file=sys.stderr)
            raise SelectorFormatError(msg)

    # --- Reconstruct Output ---
    output_policy = {}
    # Copy top-level keys/values from the original policy, excluding 'rules'
    for key, value in selected_policy.items():
        if key != 'rules':
            output_policy[key] = value # Shallow copy of values is sufficient

    # Add the single selected rule (reference is fine)
    output_policy['rules'] = [selected_rule]

    # Wrap in the top-level structure
    output_data = {'access-policy': [output_policy]}

    # Write YAML
    return yaml.dump(output_data, sort_keys=False, default_flow_style=False, indent=2)

def _load_yaml_file(target_path: pathlib.Path) -> dict:
    """Loads and performs basic validation on the YAML file."""
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            loaded_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Policy file not found at '{target_path}'", file=sys.stderr)
        raise
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file '{target_path}': {e}", file=sys.stderr)
        raise
    except OSError as e: # Other potential OS errors
        print(f"Error: Could not read file '{target_path}': {e}", file=sys.stderr)
        raise RulePickError(f"Could not read file '{target_path}'") from e

    if not isinstance(loaded_data, dict):
        msg = f"Invalid policy file format: Top level must be a dictionary (object) in '{target_path}'"
        print(f"Error: {msg}", file=sys.stderr)
        raise InvalidPolicyFileFormatError(msg)

    return loaded_data

def _validate_and_get_policies(loaded_data: dict, target_path: pathlib.Path) -> list:
    """Validates the 'access-policy' key and returns the list of policies."""
    if 'access-policy' not in loaded_data:
        msg = f"Invalid policy file format: missing top-level 'access-policy' key in '{target_path}'"
        print(f"Error: {msg}", file=sys.stderr)
        raise InvalidPolicyFileFormatError(msg)

    policies = loaded_data.get('access-policy')
    if not isinstance(policies, list):
        msg = f"Invalid policy file format: 'access-policy' should contain a list in '{target_path}'"
        print(f"Error: {msg}", file=sys.stderr)
        raise InvalidPolicyFileFormatError(msg)
    return policies

def _find_by_policy_and_rule_selector(policies: list, policy_selector: str, rule_selector: str, target_path: pathlib.Path) -> tuple[dict, dict]:
    """Finds policy by name or index, then rule by name or index."""
    found_policy = _find_policy(policies, policy_selector, target_path)

    rules = found_policy.get('rules')
    if not isinstance(rules, list):
        policy_identifier = found_policy.get('name', f"at index {policies.index(found_policy)}")
        msg = f"Policy '{policy_identifier}' is missing or has an invalid 'rules' list in '{target_path}'"
        print(f"Error: {msg}", file=sys.stderr)
        raise InvalidPolicyFileFormatError(msg)

    if rule_selector.isdigit():
        rule_index = int(rule_selector)
        if not (0 <= rule_index < len(rules)):
            policy_identifier = found_policy.get('name', f"at index {policies.index(found_policy)}")
            msg = f"Rule index {rule_index} out of bounds for policy '{policy_identifier}' (has {len(rules)} rules) in '{target_path}'"
            print(f"Error: {msg}", file=sys.stderr)
            raise RuleNotFoundError(msg)

        selected_rule = rules[rule_index]
        if not isinstance(selected_rule, dict):
            policy_identifier = found_policy.get('name', f"at index {policies.index(found_policy)}")
            msg = f"Invalid rule format at index {rule_index} in policy '{policy_identifier}' (expected dictionary) in '{target_path}'"
            print(f"Error: {msg}", file=sys.stderr)
            raise InvalidPolicyFileFormatError(msg)
        return found_policy, selected_rule
    else:
        # Expected rule by name
        matched_rules = []
        for index, rule in enumerate(rules):
            if isinstance(rule, dict) and rule.get('name') == rule_selector:
                matched_rules.append((index, rule))

        if not matched_rules:
            policy_identifier = found_policy.get('name', f"at index {policies.index(found_policy)}")
            msg = f"Rule named '{rule_selector}' not found within policy '{policy_identifier}' in '{target_path}'"
            print(f"Error: {msg}", file=sys.stderr)
            raise RuleNotFoundError(msg)
        if len(matched_rules) > 1:
            msg = f"Ambiguous rule selector: Rule name '{rule_selector}' found multiple times within policy '{found_policy.get('name')}'"
            print(f"Error: {msg}", file=sys.stderr)
            raise AmbiguousRuleNameError(msg)

        return found_policy, matched_rules[0][1]


def _find_policy(policies: list, policy_selector: str, target_path: pathlib.Path) -> dict:
    """Finds policy by name or index."""
    found_policy = None
    # First, try to find a policy by name
    for policy in policies:
        if isinstance(policy, dict) and policy.get('name') == policy_selector:
            found_policy = policy
            break

    # If no policy is found by name and the selector is a number, try to use it as an index
    if found_policy is None and policy_selector.isdigit():
        policy_index = int(policy_selector)
        if 0 <= policy_index < len(policies):
            found_policy = policies[policy_index]
        else:
            msg = f"Policy index {policy_index} out of bounds (has {len(policies)} policies) in '{target_path}'"
            print(f"Error: {msg}", file=sys.stderr)
            raise PolicyNotFoundError(msg)

    if found_policy is None:
        msg = f"Policy '{policy_selector}' not found in '{target_path}'"
        print(f"Error: {msg}", file=sys.stderr)
        raise PolicyNotFoundError(msg)

    return found_policy


def _find_by_global_rule_selector(
        policies: list,
        rule_selector: str,
        target_path: pathlib.Path,
        no_selector: bool = False
    ) -> tuple[dict, dict]:
    """Finds a rule by its global index or name across all policies."""
    if no_selector:
        # Count all rules in policies (E.g. policies[0].rules)
        rule_count = sum(len(policy.get('rules', [])) for policy in policies if isinstance(policy, dict) and isinstance(policy.get('rules'), list))
        if rule_count > 1:
            msg = f"Missing --rule <selector>. Rule selector required as multiple rules ({rule_count}) exist in '{target_path}'."
            raise ValueError(msg)
        rule_selector = '0'

    if rule_selector.isdigit():
        rule_index = int(rule_selector)
        current_rule_count = 0
        for policy in policies:
            if not isinstance(policy, dict):
                continue
            rules = policy.get('rules')
            if not isinstance(rules, list):
                continue

            if current_rule_count <= rule_index < current_rule_count + len(rules):
                local_rule_index = rule_index - current_rule_count
                selected_rule = rules[local_rule_index]
                if not isinstance(selected_rule, dict):
                    msg = f"Invalid rule format at global index {rule_index} (expected dictionary) in '{target_path}'"
                    print(f"Error: {msg}", file=sys.stderr)
                    raise InvalidPolicyFileFormatError(msg)
                return policy, selected_rule

            current_rule_count += len(rules)

        msg = f"Global rule index {rule_index} out of bounds (total {current_rule_count} rules) in '{target_path}'"
        print(f"Error: {msg}", file=sys.stderr)
        raise RuleNotFoundError(msg)
    else:
        # Rule by name
        matched_rules = []
        for policy in policies:
            if not isinstance(policy, dict):
                continue
            rules = policy.get('rules')
            if not isinstance(rules, list):
                continue
            for rule in rules:
                if isinstance(rule, dict) and rule.get('name') == rule_selector:
                    matched_rules.append((policy, rule))

        if len(matched_rules) == 0:
            msg = f"Rule named '{rule_selector}' not found in any policy"
            print(f"Error: {msg}", file=sys.stderr)
            raise RuleNotFoundError(msg)
        if len(matched_rules) > 1:
            msg = f"Ambiguous rule selector: Rule name '{rule_selector}' found in multiple policies"
            print(f"Error: {msg}", file=sys.stderr)
            raise AmbiguousRuleNameError(msg)

        return matched_rules[0][0], matched_rules[0][1]
