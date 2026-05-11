from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location_selector_part import LocationSelectorPart


T = TypeVar("T", bound="AdHocSpecInput")


@_attrs_define
class AdHocSpecInput:
    """Resolve an ad-hoc location spec (list of LocationSelectorPart dicts).

    Attributes:
        spec (list['LocationSelectorPart']):
        type_ (Union[Literal['spec'], Unset]):  Default: 'spec'.
        invert (Union[Unset, bool]):  Default: False.
    """

    spec: list["LocationSelectorPart"]
    type_: Union[Literal["spec"], Unset] = "spec"
    invert: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        spec = []
        for spec_item_data in self.spec:
            spec_item = spec_item_data.to_dict()
            spec.append(spec_item)

        type_ = self.type_

        invert = self.invert

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "spec": spec,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if invert is not UNSET:
            field_dict["invert"] = invert

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.location_selector_part import LocationSelectorPart

        d = dict(src_dict)
        spec = []
        _spec = d.pop("spec")
        for spec_item_data in _spec:
            spec_item = LocationSelectorPart.from_dict(spec_item_data)

            spec.append(spec_item)

        type_ = cast(Union[Literal["spec"], Unset], d.pop("type", UNSET))
        if type_ != "spec" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'spec', got '{type_}'")

        invert = d.pop("invert", UNSET)

        ad_hoc_spec_input = cls(
            spec=spec,
            type_=type_,
            invert=invert,
        )

        ad_hoc_spec_input.additional_properties = d
        return ad_hoc_spec_input

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
