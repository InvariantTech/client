from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LocationNameInput")


@_attrs_define
class LocationNameInput:
    """Resolve a named location from the location resource set.

    Attributes:
        location_name (str):
        type_ (Union[Literal['location_name'], Unset]):  Default: 'location_name'.
        invert (Union[Unset, bool]):  Default: False.
    """

    location_name: str
    type_: Union[Literal["location_name"], Unset] = "location_name"
    invert: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        location_name = self.location_name

        type_ = self.type_

        invert = self.invert

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "location_name": location_name,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if invert is not UNSET:
            field_dict["invert"] = invert

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        location_name = d.pop("location_name")

        type_ = cast(Union[Literal["location_name"], Unset], d.pop("type", UNSET))
        if type_ != "location_name" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'location_name', got '{type_}'")

        invert = d.pop("invert", UNSET)

        location_name_input = cls(
            location_name=location_name,
            type_=type_,
            invert=invert,
        )

        location_name_input.additional_properties = d
        return location_name_input

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
