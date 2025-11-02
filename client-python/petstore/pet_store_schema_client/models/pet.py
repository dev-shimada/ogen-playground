from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.pet_status import PetStatus
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="Pet")



@_attrs_define
class Pet:
    """ 
        Attributes:
            name (str):  Example: doggie.
            id (int | Unset):  Example: 10.
            photo_urls (list[str] | Unset):
            status (PetStatus | Unset): pet status in the store
     """

    name: str
    id: int | Unset = UNSET
    photo_urls: list[str] | Unset = UNSET
    status: PetStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        id = self.id

        photo_urls: list[str] | Unset = UNSET
        if not isinstance(self.photo_urls, Unset):
            photo_urls = self.photo_urls



        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
        })
        if id is not UNSET:
            field_dict["id"] = id
        if photo_urls is not UNSET:
            field_dict["photoUrls"] = photo_urls
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        id = d.pop("id", UNSET)

        photo_urls = cast(list[str], d.pop("photoUrls", UNSET))


        _status = d.pop("status", UNSET)
        status: PetStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = PetStatus(_status)




        pet = cls(
            name=name,
            id=id,
            photo_urls=photo_urls,
            status=status,
        )


        pet.additional_properties = d
        return pet

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
