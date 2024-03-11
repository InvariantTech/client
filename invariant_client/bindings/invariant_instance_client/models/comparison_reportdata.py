from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast, Union
from typing import Union


T = TypeVar("T", bound="ComparisonReportdata")


@_attrs_define
class ComparisonReportdata:
    """
    Attributes:
        issues (Union[None, Unset, str]):
        edges (Union[None, Unset, str]):
        routers (Union[None, Unset, str]):
        nodes (Union[None, Unset, str]):
        exposed_ports (Union[None, Unset, str]):
        rule_findings (Union[None, Unset, str]):
        connect_to (Union[None, Unset, str]):
        errors (Union[None, Unset, str]):
        multipath (Union[None, Unset, str]):
        blackholes (Union[None, Unset, str]):
        ignored_lines (Union[None, Unset, str]):
        routes (Union[None, Unset, str]):
        policy_violations_ingress (Union[None, Unset, str]):
        policy_violations_egress (Union[None, Unset, str]):
        policy_violations_connect_to (Union[None, Unset, str]):
        policy_rules (Union[None, Unset, str]):
        solutions (Union[None, Unset, str]):
        unconnected_nodes (Union[None, Unset, str]):
    """

    issues: Union[None, Unset, str] = UNSET
    edges: Union[None, Unset, str] = UNSET
    routers: Union[None, Unset, str] = UNSET
    nodes: Union[None, Unset, str] = UNSET
    exposed_ports: Union[None, Unset, str] = UNSET
    rule_findings: Union[None, Unset, str] = UNSET
    connect_to: Union[None, Unset, str] = UNSET
    errors: Union[None, Unset, str] = UNSET
    multipath: Union[None, Unset, str] = UNSET
    blackholes: Union[None, Unset, str] = UNSET
    ignored_lines: Union[None, Unset, str] = UNSET
    routes: Union[None, Unset, str] = UNSET
    policy_violations_ingress: Union[None, Unset, str] = UNSET
    policy_violations_egress: Union[None, Unset, str] = UNSET
    policy_violations_connect_to: Union[None, Unset, str] = UNSET
    policy_rules: Union[None, Unset, str] = UNSET
    solutions: Union[None, Unset, str] = UNSET
    unconnected_nodes: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        issues: Union[None, Unset, str]
        if isinstance(self.issues, Unset):
            issues = UNSET

        else:
            issues = self.issues

        edges: Union[None, Unset, str]
        if isinstance(self.edges, Unset):
            edges = UNSET

        else:
            edges = self.edges

        routers: Union[None, Unset, str]
        if isinstance(self.routers, Unset):
            routers = UNSET

        else:
            routers = self.routers

        nodes: Union[None, Unset, str]
        if isinstance(self.nodes, Unset):
            nodes = UNSET

        else:
            nodes = self.nodes

        exposed_ports: Union[None, Unset, str]
        if isinstance(self.exposed_ports, Unset):
            exposed_ports = UNSET

        else:
            exposed_ports = self.exposed_ports

        rule_findings: Union[None, Unset, str]
        if isinstance(self.rule_findings, Unset):
            rule_findings = UNSET

        else:
            rule_findings = self.rule_findings

        connect_to: Union[None, Unset, str]
        if isinstance(self.connect_to, Unset):
            connect_to = UNSET

        else:
            connect_to = self.connect_to

        errors: Union[None, Unset, str]
        if isinstance(self.errors, Unset):
            errors = UNSET

        else:
            errors = self.errors

        multipath: Union[None, Unset, str]
        if isinstance(self.multipath, Unset):
            multipath = UNSET

        else:
            multipath = self.multipath

        blackholes: Union[None, Unset, str]
        if isinstance(self.blackholes, Unset):
            blackholes = UNSET

        else:
            blackholes = self.blackholes

        ignored_lines: Union[None, Unset, str]
        if isinstance(self.ignored_lines, Unset):
            ignored_lines = UNSET

        else:
            ignored_lines = self.ignored_lines

        routes: Union[None, Unset, str]
        if isinstance(self.routes, Unset):
            routes = UNSET

        else:
            routes = self.routes

        policy_violations_ingress: Union[None, Unset, str]
        if isinstance(self.policy_violations_ingress, Unset):
            policy_violations_ingress = UNSET

        else:
            policy_violations_ingress = self.policy_violations_ingress

        policy_violations_egress: Union[None, Unset, str]
        if isinstance(self.policy_violations_egress, Unset):
            policy_violations_egress = UNSET

        else:
            policy_violations_egress = self.policy_violations_egress

        policy_violations_connect_to: Union[None, Unset, str]
        if isinstance(self.policy_violations_connect_to, Unset):
            policy_violations_connect_to = UNSET

        else:
            policy_violations_connect_to = self.policy_violations_connect_to

        policy_rules: Union[None, Unset, str]
        if isinstance(self.policy_rules, Unset):
            policy_rules = UNSET

        else:
            policy_rules = self.policy_rules

        solutions: Union[None, Unset, str]
        if isinstance(self.solutions, Unset):
            solutions = UNSET

        else:
            solutions = self.solutions

        unconnected_nodes: Union[None, Unset, str]
        if isinstance(self.unconnected_nodes, Unset):
            unconnected_nodes = UNSET

        else:
            unconnected_nodes = self.unconnected_nodes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if issues is not UNSET:
            field_dict["issues"] = issues
        if edges is not UNSET:
            field_dict["edges"] = edges
        if routers is not UNSET:
            field_dict["routers"] = routers
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if exposed_ports is not UNSET:
            field_dict["exposed_ports"] = exposed_ports
        if rule_findings is not UNSET:
            field_dict["rule_findings"] = rule_findings
        if connect_to is not UNSET:
            field_dict["connectTo"] = connect_to
        if errors is not UNSET:
            field_dict["errors"] = errors
        if multipath is not UNSET:
            field_dict["multipath"] = multipath
        if blackholes is not UNSET:
            field_dict["blackholes"] = blackholes
        if ignored_lines is not UNSET:
            field_dict["ignored_lines"] = ignored_lines
        if routes is not UNSET:
            field_dict["routes"] = routes
        if policy_violations_ingress is not UNSET:
            field_dict["policy_violations_ingress"] = policy_violations_ingress
        if policy_violations_egress is not UNSET:
            field_dict["policy_violations_egress"] = policy_violations_egress
        if policy_violations_connect_to is not UNSET:
            field_dict["policy_violations_connect_to"] = policy_violations_connect_to
        if policy_rules is not UNSET:
            field_dict["policy_rules"] = policy_rules
        if solutions is not UNSET:
            field_dict["solutions"] = solutions
        if unconnected_nodes is not UNSET:
            field_dict["unconnected_nodes"] = unconnected_nodes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_issues(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        issues = _parse_issues(d.pop("issues", UNSET))

        def _parse_edges(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        edges = _parse_edges(d.pop("edges", UNSET))

        def _parse_routers(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        routers = _parse_routers(d.pop("routers", UNSET))

        def _parse_nodes(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        nodes = _parse_nodes(d.pop("nodes", UNSET))

        def _parse_exposed_ports(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        exposed_ports = _parse_exposed_ports(d.pop("exposed_ports", UNSET))

        def _parse_rule_findings(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        rule_findings = _parse_rule_findings(d.pop("rule_findings", UNSET))

        def _parse_connect_to(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        connect_to = _parse_connect_to(d.pop("connectTo", UNSET))

        def _parse_errors(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        errors = _parse_errors(d.pop("errors", UNSET))

        def _parse_multipath(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        multipath = _parse_multipath(d.pop("multipath", UNSET))

        def _parse_blackholes(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        blackholes = _parse_blackholes(d.pop("blackholes", UNSET))

        def _parse_ignored_lines(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ignored_lines = _parse_ignored_lines(d.pop("ignored_lines", UNSET))

        def _parse_routes(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        routes = _parse_routes(d.pop("routes", UNSET))

        def _parse_policy_violations_ingress(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        policy_violations_ingress = _parse_policy_violations_ingress(
            d.pop("policy_violations_ingress", UNSET)
        )

        def _parse_policy_violations_egress(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        policy_violations_egress = _parse_policy_violations_egress(
            d.pop("policy_violations_egress", UNSET)
        )

        def _parse_policy_violations_connect_to(
            data: object,
        ) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        policy_violations_connect_to = _parse_policy_violations_connect_to(
            d.pop("policy_violations_connect_to", UNSET)
        )

        def _parse_policy_rules(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        policy_rules = _parse_policy_rules(d.pop("policy_rules", UNSET))

        def _parse_solutions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        solutions = _parse_solutions(d.pop("solutions", UNSET))

        def _parse_unconnected_nodes(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        unconnected_nodes = _parse_unconnected_nodes(d.pop("unconnected_nodes", UNSET))

        comparison_reportdata = cls(
            issues=issues,
            edges=edges,
            routers=routers,
            nodes=nodes,
            exposed_ports=exposed_ports,
            rule_findings=rule_findings,
            connect_to=connect_to,
            errors=errors,
            multipath=multipath,
            blackholes=blackholes,
            ignored_lines=ignored_lines,
            routes=routes,
            policy_violations_ingress=policy_violations_ingress,
            policy_violations_egress=policy_violations_egress,
            policy_violations_connect_to=policy_violations_connect_to,
            policy_rules=policy_rules,
            solutions=solutions,
            unconnected_nodes=unconnected_nodes,
        )

        comparison_reportdata.additional_properties = d
        return comparison_reportdata

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
