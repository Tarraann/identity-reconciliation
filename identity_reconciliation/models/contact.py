from identity_reconciliation.constants.linked_precedence import LinkedPrecedence
from identity_reconciliation.models.base_model import DBBaseModel
from sqlalchemy import Column, Integer, String, DateTime, or_
from sqlalchemy.orm import Session

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
    def create_contact(cls, session: Session, phone_number: str, email: str, linked_id: int = None, linked_precedence: str = LinkedPrecedence.PRIMARY.value):
        contact = Contact(
            phone_number=phone_number,
            email=email,
            linked_id=linked_id,
            linked_precedence=linked_precedence
        )
        session.add(contact)
        session.flush()
        session.refresh(contact)
        return contact

    @classmethod
    def retrieve_contacts(cls, session: Session, email: str, phone_number: str):
        query = session.query(Contact).filter(
            or_(
                Contact.email == email,
                Contact.phone_number == phone_number
            )
        )
        query = query.order_by(Contact.id)
        return query.all()

    @classmethod
    def update_linked_precedence(cls, session: Session, id: int, linked_precedence: str, linked_id: int = None):
        contact = session.query(Contact).filter(Contact.id == id).first()
        contact.linked_precedence = linked_precedence
        contact.linked_id = linked_id
        session.add(contact)
        session.flush()
