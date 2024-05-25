from sqlalchemy.orm import Session
from typing import List, Set, Tuple, Optional
from identity_reconciliation.constants.linked_precedence import LinkedPrecedence
from identity_reconciliation.models.contact import Contact
from identity_reconciliation.types.response.identify_contact_response import IdentifyContactResponse, ContactResponse


class ContactService:
    def __init__(self, session: Session, email: str, phone_number: str):
        self.session = session
        self.email = email
        self.phone_number = phone_number

    def retrieve_contacts(self) -> IdentifyContactResponse:
        contacts = Contact.retrieve_contacts(
            session=self.session,
            email=self.email,
            phone_number=self.phone_number
        )
        if not contacts:
            return self.__create_primary_contact()
        return self.__retrieve_contact_data(contacts)

    def __create_primary_contact(self) -> IdentifyContactResponse:
        contact = Contact.create_contact(
            session=self.session,
            email=self.email,
            phone_number=self.phone_number
        )
        return IdentifyContactResponse(
            contact=ContactResponse(
                primary_contact_id=contact.id,
                emails=[contact.email],
                phone_numbers=[contact.phone_number],
                secondary_contact_ids=[]
            )
        )

    def __retrieve_contact_data(self, contacts: List[Contact]) -> IdentifyContactResponse:
        emails, phone_numbers, secondary_contact_ids = self.__initialize_contact_data(contacts)
        primary_contact_id, secondary_contact_id = self.__determine_primary_contact_id(contacts)
        if secondary_contact_id is not None:
            secondary_contact_ids.append(secondary_contact_id)
        self.__add_new_contact_if_not_present(emails, phone_numbers, secondary_contact_ids, primary_contact_id)
        return IdentifyContactResponse(
            contact=ContactResponse(
                primary_contact_id=primary_contact_id,
                emails=emails,
                phone_numbers=phone_numbers,
                secondary_contact_ids=secondary_contact_ids
            )
        )

    @classmethod
    def __initialize_contact_data(cls, contacts: List[Contact]) -> (Set[str], Set[str], Set[int]):
        emails = set()
        phone_numbers = set()
        secondary_contact_ids = set()

        for contact in contacts:
            emails.add(contact.email)
            phone_numbers.add(contact.phone_number)
            if contact.linked_precedence != LinkedPrecedence.PRIMARY.value:
                secondary_contact_ids.add(contact.id)

        return list(emails), list(phone_numbers), list(secondary_contact_ids)

    def __determine_primary_contact_id(self, contacts: List[Contact]) -> tuple[int, Optional[int]]:
        primary_contact_id = None
        secondary_contact_id = None
        for contact in contacts:
            if contact.linked_precedence == LinkedPrecedence.PRIMARY.value:
                if primary_contact_id is None:
                    primary_contact_id = contact.id
                else:
                    Contact.update_linked_precedence(
                        session=self.session,
                        id=contact.id,
                        linked_id=primary_contact_id,
                        linked_precedence=LinkedPrecedence.SECONDARY.value
                    )
                    secondary_contact_id = contact.id
        return primary_contact_id, secondary_contact_id

    def __add_new_contact_if_not_present(self, emails: Set[str], phone_numbers: Set[str],
                                         secondary_contact_ids: Set[int], primary_contact_id: int):
        if self.email and self.email not in emails:
            contact = self.__create_secondary_contact(primary_contact_id)
            emails.add(self.email)
            secondary_contact_ids.add(contact.id)
        if self.phone_number and self.phone_number not in phone_numbers:
            contact = self.__create_secondary_contact(primary_contact_id)
            phone_numbers.add(self.phone_number)
            secondary_contact_ids.add(contact.id)

    def __create_secondary_contact(self, linked_id: int) -> Contact:
        return Contact.create_contact(
            session=self.session,
            email=self.email,
            phone_number=self.phone_number,
            linked_id=linked_id,
            linked_precedence=LinkedPrecedence.SECONDARY.value
        )
