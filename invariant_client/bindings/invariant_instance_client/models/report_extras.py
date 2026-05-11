from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.report_extras_map_error_type_0 import ReportExtrasMapErrorType0
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportExtras")


@_attrs_define
class ReportExtras:
    """
    Attributes:
        report_uuid (UUID):
        network_name (str):
        cf_violations (int):
        ap_violations (int):
        node_count (int):
        rule_count (int):
        status (str):
        errors_count (int):
        errors_lines (list[str]):
        session_uuid (Union[None, UUID, Unset]):
        session_login_uuid (Union[None, UUID, Unset]):
        session_user (Union[None, Unset, str]):
        batfish_commit (Union[None, Unset, str]):
        batfish_commit_date (Union[None, Unset, str]):
        map_error (Union[None, ReportExtrasMapErrorType0, Unset]):
    """

    report_uuid: UUID
    network_name: str
    cf_violations: int
    ap_violations: int
    node_count: int
    rule_count: int
    status: str
    errors_count: int
    errors_lines: list[str]
    session_uuid: Union[None, UUID, Unset] = UNSET
    session_login_uuid: Union[None, UUID, Unset] = UNSET
    session_user: Union[None, Unset, str] = UNSET
    batfish_commit: Union[None, Unset, str] = UNSET
    batfish_commit_date: Union[None, Unset, str] = UNSET
    map_error: Union[None, ReportExtrasMapErrorType0, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        report_uuid = str(self.report_uuid)

        network_name = self.network_name

        cf_violations = self.cf_violations

        ap_violations = self.ap_violations

        node_count = self.node_count

        rule_count = self.rule_count

        status = self.status

        errors_count = self.errors_count

        errors_lines = self.errors_lines

        session_uuid: Union[None, Unset, str]
        if isinstance(self.session_uuid, Unset):
            session_uuid = UNSET
        elif isinstance(self.session_uuid, UUID):
            session_uuid = str(self.session_uuid)
        else:
            session_uuid = self.session_uuid

        session_login_uuid: Union[None, Unset, str]
        if isinstance(self.session_login_uuid, Unset):
            session_login_uuid = UNSET
        elif isinstance(self.session_login_uuid, UUID):
            session_login_uuid = str(self.session_login_uuid)
        else:
            session_login_uuid = self.session_login_uuid

        session_user: Union[None, Unset, str]
        if isinstance(self.session_user, Unset):
            session_user = UNSET
        else:
            session_user = self.session_user

        batfish_commit: Union[None, Unset, str]
        if isinstance(self.batfish_commit, Unset):
            batfish_commit = UNSET
        else:
            batfish_commit = self.batfish_commit

        batfish_commit_date: Union[None, Unset, str]
        if isinstance(self.batfish_commit_date, Unset):
            batfish_commit_date = UNSET
        else:
            batfish_commit_date = self.batfish_commit_date

        map_error: Union[None, Unset, str]
        if isinstance(self.map_error, Unset):
            map_error = UNSET
        elif isinstance(self.map_error, ReportExtrasMapErrorType0):
            map_error = self.map_error.value
        else:
            map_error = self.map_error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "report_uuid": report_uuid,
                "network_name": network_name,
                "cf_violations": cf_violations,
                "ap_violations": ap_violations,
                "node_count": node_count,
                "rule_count": rule_count,
                "status": status,
                "errors_count": errors_count,
                "errors_lines": errors_lines,
            }
        )
        if session_uuid is not UNSET:
            field_dict["session_uuid"] = session_uuid
        if session_login_uuid is not UNSET:
            field_dict["session_login_uuid"] = session_login_uuid
        if session_user is not UNSET:
            field_dict["session_user"] = session_user
        if batfish_commit is not UNSET:
            field_dict["batfish_commit"] = batfish_commit
        if batfish_commit_date is not UNSET:
            field_dict["batfish_commit_date"] = batfish_commit_date
        if map_error is not UNSET:
            field_dict["map_error"] = map_error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        report_uuid = UUID(d.pop("report_uuid"))

        network_name = d.pop("network_name")

        cf_violations = d.pop("cf_violations")

        ap_violations = d.pop("ap_violations")

        node_count = d.pop("node_count")

        rule_count = d.pop("rule_count")

        status = d.pop("status")

        errors_count = d.pop("errors_count")

        errors_lines = cast(list[str], d.pop("errors_lines"))

        def _parse_session_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                session_uuid_type_0 = UUID(data)

                return session_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        session_uuid = _parse_session_uuid(d.pop("session_uuid", UNSET))

        def _parse_session_login_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                session_login_uuid_type_0 = UUID(data)

                return session_login_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        session_login_uuid = _parse_session_login_uuid(
            d.pop("session_login_uuid", UNSET)
        )

        def _parse_session_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_user = _parse_session_user(d.pop("session_user", UNSET))

        def _parse_batfish_commit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        batfish_commit = _parse_batfish_commit(d.pop("batfish_commit", UNSET))

        def _parse_batfish_commit_date(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        batfish_commit_date = _parse_batfish_commit_date(
            d.pop("batfish_commit_date", UNSET)
        )

        def _parse_map_error(
            data: object,
        ) -> Union[None, ReportExtrasMapErrorType0, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                map_error_type_0 = ReportExtrasMapErrorType0(data)

                return map_error_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ReportExtrasMapErrorType0, Unset], data)

        map_error = _parse_map_error(d.pop("map_error", UNSET))

        report_extras = cls(
            report_uuid=report_uuid,
            network_name=network_name,
            cf_violations=cf_violations,
            ap_violations=ap_violations,
            node_count=node_count,
            rule_count=rule_count,
            status=status,
            errors_count=errors_count,
            errors_lines=errors_lines,
            session_uuid=session_uuid,
            session_login_uuid=session_login_uuid,
            session_user=session_user,
            batfish_commit=batfish_commit,
            batfish_commit_date=batfish_commit_date,
            map_error=map_error,
        )

        report_extras.additional_properties = d
        return report_extras

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
