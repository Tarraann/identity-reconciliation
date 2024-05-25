from fastapi import APIRouter
from fastapi import HTTPException
from fastapi_sqlalchemy import db
from identity_reconciliation.lib.logger import logger
from identity_reconciliation.service.contact_service import ContactService
from identity_reconciliation.types.request.create_contact_request import CreateContactRequest
from identity_reconciliation.types.request.identify_contact_request import IdentifyContactRequest
from identity_reconciliation.types.response.base_response_model import BaseResponseModel
from identity_reconciliation.models.contact import Contact
from identity_reconciliation.types.response.identify_contact_response import IdentifyContactResponse

router = APIRouter()


@router.post("/create", response_model=BaseResponseModel)
async def create_contact(request: CreateContactRequest):
    session = db.session
    try:
        Contact.create_contact(
            session=session,
            email=request.email,
            phone_number=request.phone_number,
            linked_id=request.linked_id,
            linked_precedence=request.linked_precedence
        )
        session.commit()
        return BaseResponseModel(
            status=True, message="Contact Created Successfully"
        )
    except Exception as e:
        session.rollback()
        logger.error(f"Error while creating contact: {e}")
        raise HTTPException(status_code=500, detail="Error while creating contact")


@router.post("/identify")
async def identify_contact(request: IdentifyContactRequest):
    session = db.session
    try:
        contact_service = ContactService(
            session=session,
            email=request.email,
            phone_number=request.phone_number
        )
        response = contact_service.retrieve_contacts()
        session.commit()
        return response
    except Exception as e:
        session.rollback()
        logger.error(f"Error while retrieving contacts: {e}")
        raise HTTPException(status_code=500, detail="Error while retrieving contacts")
