from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, Union
from ..types import UNSET, Unset
from typing import Union


T = TypeVar("T", bound="ReportMetadata")


@_attrs_define
class ReportMetadata:
    """
    Attributes:
        session_uuid (Union[None, Unset, str]):
        role (Union[None, Unset, str]):
        source_urn (Union[None, Unset, str]):
        source_monitor (Union[None, Unset, str]):
        source_cli (Union[None, Unset, str]):
    """

    session_uuid: Union[None, Unset, str] = UNSET
    role: Union[None, Unset, str] = UNSET
    source_urn: Union[None, Unset, str] = UNSET
    source_monitor: Union[None, Unset, str] = UNSET
    source_cli: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        session_uuid: Union[None, Unset, str]
        if isinstance(self.session_uuid, Unset):
            session_uuid = UNSET

        else:
            session_uuid = self.session_uuid

        role: Union[None, Unset, str]
        if isinstance(self.role, Unset):
            role = UNSET

        else:
            role = self.role

        source_urn: Union[None, Unset, str]
        if isinstance(self.source_urn, Unset):
            source_urn = UNSET

        else:
            source_urn = self.source_urn

        source_monitor: Union[None, Unset, str]
        if isinstance(self.source_monitor, Unset):
            source_monitor = UNSET

        else:
            source_monitor = self.source_monitor

        source_cli: Union[None, Unset, str]
        if isinstance(self.source_cli, Unset):
            source_cli = UNSET

        else:
            source_cli = self.source_cli

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if session_uuid is not UNSET:
            field_dict["session_uuid"] = session_uuid
        if role is not UNSET:
            field_dict["role"] = role
        if source_urn is not UNSET:
            field_dict["source_urn"] = source_urn
        if source_monitor is not UNSET:
            field_dict["source_monitor"] = source_monitor
        if source_cli is not UNSET:
            field_dict["source_cli"] = source_cli

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_session_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_uuid = _parse_session_uuid(d.pop("session_uuid", UNSET))

        def _parse_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_source_urn(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source_urn = _parse_source_urn(d.pop("source_urn", UNSET))

        def _parse_source_monitor(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source_monitor = _parse_source_monitor(d.pop("source_monitor", UNSET))

        def _parse_source_cli(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source_cli = _parse_source_cli(d.pop("source_cli", UNSET))

        report_metadata = cls(
            session_uuid=session_uuid,
            role=role,
            source_urn=source_urn,
            source_monitor=source_monitor,
            source_cli=source_cli,
        )

        report_metadata.additional_properties = d
        return report_metadata

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