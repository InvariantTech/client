from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ad_hoc_spec_input import AdHocSpecInput
    from ..models.location_name_input import LocationNameInput


T = TypeVar("T", bound="GetInterfacesRequest")


@_attrs_define
class GetInterfacesRequest:
    """
    Attributes:
        inputs (list[Union['AdHocSpecInput', 'LocationNameInput']]):
    """

    inputs: list[Union["AdHocSpecInput", "LocationNameInput"]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.location_name_input import LocationNameInput

        inputs = []
        for inputs_item_data in self.inputs:
            inputs_item: dict[str, Any]
            if isinstance(inputs_item_data, LocationNameInput):
                inputs_item = inputs_item_data.to_dict()
            else:
                inputs_item = inputs_item_data.to_dict()

            inputs.append(inputs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputs": inputs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ad_hoc_spec_input import AdHocSpecInput
        from ..models.location_name_input import LocationNameInput

        d = dict(src_dict)
        inputs = []
        _inputs = d.pop("inputs")
        for inputs_item_data in _inputs:

            def _parse_inputs_item(
                data: object,
            ) -> Union["AdHocSpecInput", "LocationNameInput"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    inputs_item_type_0 = LocationNameInput.from_dict(data)

                    return inputs_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                inputs_item_type_1 = AdHocSpecInput.from_dict(data)

                return inputs_item_type_1

            inputs_item = _parse_inputs_item(inputs_item_data)

            inputs.append(inputs_item)

        get_interfaces_request = cls(
            inputs=inputs,
        )

        get_interfaces_request.additional_properties = d
        return get_interfaces_request

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
