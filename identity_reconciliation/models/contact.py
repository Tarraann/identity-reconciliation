from identity_reconciliation.constants.linked_precedence import LinkedPrecedence
from identity_reconciliation.models.base_model import DBBaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime, case, desc, alias
from sqlalchemy.orm import Session
from typing import List

from identity_reconciliation.types.request.create_contact_request import CreateContactRequest


class Contact(DBBaseModel):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String)
    email = Column(String)
    linked_id = Column(Integer)
    linked_precedence = Column(Integer, default=LinkedPrecedence.PRIMARY.value) # PRIMARY, SECONDARY
    deleted_at = Column(DateTime)

    @classmethod
    def create_contact(cls, session: Session, contact_data: CreateContactRequest):
        contact = Contact(
            phone_number=contact_data.phone_number,
            email=contact_data.email,
            linked_id=contact_data.linked_id,
            linked_precedence=contact_data.linked_precedence
        )
        session.add(contact)
        session.flush()