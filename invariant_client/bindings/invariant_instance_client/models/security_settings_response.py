from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast
from typing import cast, Union
from typing import cast, List
from typing import Dict

if TYPE_CHECKING:
    from ..models.security_policy_metadata import SecurityPolicyMetadata
    from ..models.security_integration import SecurityIntegration


T = TypeVar("T", bound="SecuritySettingsResponse")


@_attrs_define
class SecuritySettingsResponse:
    """
    Attributes:
        domain_reservations (List[str]):
        security_integrations (List['SecurityIntegration']):
        security_policy (Union['SecurityPolicyMetadata', None]):
    """

    domain_reservations: List[str]
    security_integrations: List["SecurityIntegration"]
    security_policy: Union["SecurityPolicyMetadata", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.security_policy_metadata import SecurityPolicyMetadata

        domain_reservations = self.domain_reservations

        security_integrations = []
        for security_integrations_item_data in self.security_integrations:
            security_integrations_item = security_integrations_item_data.to_dict()

            security_integrations.append(security_integrations_item)

        security_policy: Union[Dict[str, Any], None]

        if isinstance(self.security_policy, SecurityPolicyMetadata):
            security_policy = self.security_policy.to_dict()

        else:
            security_policy = self.security_policy

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain_reservations": domain_reservations,
                "security_integrations": security_integrations,
                "security_policy": security_policy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.security_policy_metadata import SecurityPolicyMetadata
        from ..models.security_integration import SecurityIntegration

        d = src_dict.copy()
        domain_reservations = cast(List[str], d.pop("domain_reservations"))

        security_integrations = []
        _security_integrations = d.pop("security_integrations")
        for security_integrations_item_data in _security_integrations:
            security_integrations_item = SecurityIntegration.from_dict(
                security_integrations_item_data
            )

            security_integrations.append(security_integrations_item)

        def _parse_security_policy(
            data: object,
        ) -> Union["SecurityPolicyMetadata", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                security_policy_type_0 = SecurityPolicyMetadata.from_dict(data)

                return security_policy_type_0
            except:  # noqa: E722
                pass
            return cast(Union["SecurityPolicyMetadata", None], data)

        security_policy = _parse_security_policy(d.pop("security_policy"))

        security_settings_response = cls(
            domain_reservations=domain_reservations,
            security_integrations=security_integrations,
            security_policy=security_policy,
        )

        security_settings_response.additional_properties = d
        return security_settings_response

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
