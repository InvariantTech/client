from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast, Union
from typing import Dict
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.comparison_reportdata import ComparisonReportdata


T = TypeVar("T", bound="SnapshotReportData")


@_attrs_define
class SnapshotReportData:
    """
    Attributes:
        errors (str):
        summary (str):
        status (str):
        issues (Union[None, Unset, str]):
        edges (Union[None, Unset, str]):
        routers (Union[None, Unset, str]):
        nodes (Union[None, Unset, str]):
        external_ports (Union[None, Unset, str]):
        rule_findings (Union[None, Unset, str]):
        connect_to (Union[None, Unset, str]):
        multipath (Union[None, Unset, str]):
        blackholes (Union[None, Unset, str]):
        ignored_lines (Union[None, Unset, str]):
        routes (Union[None, Unset, str]):
        policy_violations_ingress (Union[None, Unset, str]):
        policy_violations_egress (Union[None, Unset, str]):
        policy_violations_connect_to (Union[None, Unset, str]):
        policy_rules (Union[None, Unset, str]):
        solutions (Union[None, Unset, str]):
        compare_to (Union['ComparisonReportdata', None, Unset]):
    """

    errors: str
    summary: str
    status: str
    issues: Union[None, Unset, str] = UNSET
    edges: Union[None, Unset, str] = UNSET
    routers: Union[None, Unset, str] = UNSET
    nodes: Union[None, Unset, str] = UNSET
    external_ports: Union[None, Unset, str] = UNSET
    rule_findings: Union[None, Unset, str] = UNSET
    connect_to: Union[None, Unset, str] = UNSET
    multipath: Union[None, Unset, str] = UNSET
    blackholes: Union[None, Unset, str] = UNSET
    ignored_lines: Union[None, Unset, str] = UNSET
    routes: Union[None, Unset, str] = UNSET
    policy_violations_ingress: Union[None, Unset, str] = UNSET
    policy_violations_egress: Union[None, Unset, str] = UNSET
    policy_violations_connect_to: Union[None, Unset, str] = UNSET
    policy_rules: Union[None, Unset, str] = UNSET
    solutions: Union[None, Unset, str] = UNSET
    compare_to: Union["ComparisonReportdata", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.comparison_reportdata import ComparisonReportdata

        errors = self.errors
        summary = self.summary
        status = self.status
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

        external_ports: Union[None, Unset, str]
        if isinstance(self.external_ports, Unset):
            external_ports = UNSET

        else:
            external_ports = self.external_ports

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

        compare_to: Union[Dict[str, Any], None, Unset]
        if isinstance(self.compare_to, Unset):
            compare_to = UNSET

        elif isinstance(self.compare_to, ComparisonReportdata):
            compare_to = UNSET
            if not isinstance(self.compare_to, Unset):
                compare_to = self.compare_to.to_dict()

        else:
            compare_to = self.compare_to

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "errors": errors,
                "summary": summary,
                "status": status,
            }
        )
        if issues is not UNSET:
            field_dict["issues"] = issues
        if edges is not UNSET:
            field_dict["edges"] = edges
        if routers is not UNSET:
            field_dict["routers"] = routers
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if external_ports is not UNSET:
            field_dict["external_ports"] = external_ports
        if rule_findings is not UNSET:
            field_dict["rule_findings"] = rule_findings
        if connect_to is not UNSET:
            field_dict["connectTo"] = connect_to
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
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.comparison_reportdata import ComparisonReportdata

        d = src_dict.copy()
        errors = d.pop("errors")

        summary = d.pop("summary")

        status = d.pop("status")

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

        def _parse_external_ports(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_ports = _parse_external_ports(d.pop("external_ports", UNSET))

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

        def _parse_compare_to(
            data: object,
        ) -> Union["ComparisonReportdata", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _compare_to_type_0 = data
                compare_to_type_0: Union[Unset, ComparisonReportdata]
                if isinstance(_compare_to_type_0, Unset):
                    compare_to_type_0 = UNSET
                else:
                    compare_to_type_0 = ComparisonReportdata.from_dict(
                        _compare_to_type_0
                    )

                return compare_to_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ComparisonReportdata", None, Unset], data)

        compare_to = _parse_compare_to(d.pop("compare_to", UNSET))

        snapshot_report_data = cls(
            errors=errors,
            summary=summary,
            status=status,
            issues=issues,
            edges=edges,
            routers=routers,
            nodes=nodes,
            external_ports=external_ports,
            rule_findings=rule_findings,
            connect_to=connect_to,
            multipath=multipath,
            blackholes=blackholes,
            ignored_lines=ignored_lines,
            routes=routes,
            policy_violations_ingress=policy_violations_ingress,
            policy_violations_egress=policy_violations_egress,
            policy_violations_connect_to=policy_violations_connect_to,
            policy_rules=policy_rules,
            solutions=solutions,
            compare_to=compare_to,
        )

        snapshot_report_data.additional_properties = d
        return snapshot_report_data

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
