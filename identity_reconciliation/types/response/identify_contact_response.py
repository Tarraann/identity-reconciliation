from pydantic import BaseModel, Field
from typing import List


class ContactResponse(BaseModel):
    primary_contact_id: int
    emails: List[str]
    phone_numbers: List[str] = Field(default_factory=List, alias='phoneNumbers')
    secondary_contact_ids: List[int] = Field(default_factory=List, alias='secondaryContactIds')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = lambda string: ''.join(
            word.capitalize() if i > 0 else word for i, word in enumerate(string.split('_')))
        allow_population_by_alias = True


class IdentifyContactResponse(BaseModel):
    contact: ContactResponse

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = lambda string: ''.join(
            word.capitalize() if i > 0 else word for i, word in enumerate(string.split('_')))
        allow_population_by_alias = True
