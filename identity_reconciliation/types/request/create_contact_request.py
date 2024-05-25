from pydantic import BaseModel, Field
from typing import Optional


class CreateContactRequest(BaseModel):
    email: str
    phone_number: str
    linked_id: Optional[int] = Field(None, alias='linkedId')
    linked_precedence: Optional[str] = Field(None, alias='linkedPrecedence')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = lambda string: ''.join(
            word.capitalize() if i > 0 else word for i, word in enumerate(string.split('_')))
        allow_population_by_alias = True

