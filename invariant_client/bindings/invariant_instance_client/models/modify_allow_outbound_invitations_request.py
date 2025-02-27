from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Literal


T = TypeVar("T", bound="ModifyAllowOutboundInvitationsRequest")


@_attrs_define
class ModifyAllowOutboundInvitationsRequest:
    """
    Attributes:
        policy_key (Literal['allow_outbound_invitations']):
        value (bool):
    """

    policy_key: Literal["allow_outbound_invitations"]
    value: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        policy_key = self.policy_key
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "policy_key": policy_key,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        policy_key = d.pop("policy_key")

        value = d.pop("value")

        modify_allow_outbound_invitations_request = cls(
            policy_key=policy_key,
            value=value,
        )

        modify_allow_outbound_invitations_request.additional_properties = d
        return modify_allow_outbound_invitations_request

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
