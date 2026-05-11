from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LocationSelectorPart")


@_attrs_define
class LocationSelectorPart:
    """
    Attributes:
        devices (Union[None, list[str], str]):
        interfaces (Union[None, list[str], str]):
        ips (Union[None, list[str], str]):
        vrfs (Union[None, list[str], str]):
        zones (Union[None, list[str], str]):
    """

    devices: Union[None, list[str], str]
    interfaces: Union[None, list[str], str]
    ips: Union[None, list[str], str]
    vrfs: Union[None, list[str], str]
    zones: Union[None, list[str], str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        devices: Union[None, list[str], str]
        if isinstance(self.devices, list):
            devices = self.devices

        else:
            devices = self.devices

        interfaces: Union[None, list[str], str]
        if isinstance(self.interfaces, list):
            interfaces = self.interfaces

        else:
            interfaces = self.interfaces

        ips: Union[None, list[str], str]
        if isinstance(self.ips, list):
            ips = self.ips

        else:
            ips = self.ips

        vrfs: Union[None, list[str], str]
        if isinstance(self.vrfs, list):
            vrfs = self.vrfs

        else:
            vrfs = self.vrfs

        zones: Union[None, list[str], str]
        if isinstance(self.zones, list):
            zones = self.zones

        else:
            zones = self.zones

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "devices": devices,
                "interfaces": interfaces,
                "ips": ips,
                "vrfs": vrfs,
                "zones": zones,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_devices(data: object) -> Union[None, list[str], str]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                devices_type_0 = cast(list[str], data)

                return devices_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str], str], data)

        devices = _parse_devices(d.pop("devices"))

        def _parse_interfaces(data: object) -> Union[None, list[str], str]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                interfaces_type_0 = cast(list[str], data)

                return interfaces_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str], str], data)

        interfaces = _parse_interfaces(d.pop("interfaces"))

        def _parse_ips(data: object) -> Union[None, list[str], str]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ips_type_0 = cast(list[str], data)

                return ips_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str], str], data)

        ips = _parse_ips(d.pop("ips"))

        def _parse_vrfs(data: object) -> Union[None, list[str], str]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                vrfs_type_0 = cast(list[str], data)

                return vrfs_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str], str], data)

        vrfs = _parse_vrfs(d.pop("vrfs"))

        def _parse_zones(data: object) -> Union[None, list[str], str]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                zones_type_0 = cast(list[str], data)

                return zones_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str], str], data)

        zones = _parse_zones(d.pop("zones"))

        location_selector_part = cls(
            devices=devices,
            interfaces=interfaces,
            ips=ips,
            vrfs=vrfs,
            zones=zones,
        )

        location_selector_part.additional_properties = d
        return location_selector_part

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
