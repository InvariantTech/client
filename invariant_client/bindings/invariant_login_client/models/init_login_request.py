from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Literal
from typing import Union
from typing import cast, Union
from ..types import UNSET, Unset


T = TypeVar("T", bound="InitLoginRequest")


@_attrs_define
class InitLoginRequest:
    """This request initiates a login session. It does not require any credential.

    Attributes:
        type (Literal['init_login']):
        email (str):
        slink (Union[None, Unset, str]):
    """

    type: Literal["init_login"]
    email: str
    slink: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        email = self.email
        slink: Union[None, Unset, str]
        if isinstance(self.slink, Unset):
            slink = UNSET

        else:
            slink = self.slink

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "email": email,
            }
        )
        if slink is not UNSET:
            field_dict["slink"] = slink

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        email = d.pop("email")

        def _parse_slink(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        slink = _parse_slink(d.pop("slink", UNSET))

        init_login_request = cls(
            type=type,
            email=email,
            slink=slink,
        )

        init_login_request.additional_properties = d
        return init_login_request

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
