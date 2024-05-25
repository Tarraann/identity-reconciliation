from pydantic import BaseModel, Field
from typing import Optional


class IdentifyContactRequest(BaseModel):
    email: Optional[str]
    phone_number: Optional[str] = Field(None, alias='phoneNumber')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = lambda string: ''.join(
            word.capitalize() if i > 0 else word for i, word in enumerate(string.split('_')))
        allow_population_by_alias = True
