from fastapi import APIRouter
from fastapi import HTTPException
from fastapi_sqlalchemy import db
from identity_reconciliation.lib.logger import logger
from identity_reconciliation.types.request.create_contact_request import CreateContactRequest
from identity_reconciliation.types.response.base_response_model import BaseResponseModel
from identity_reconciliation.models.contact import Contact

router = APIRouter()


@router.post("/create", response_model=BaseResponseModel)
async def create_contact(request: CreateContactRequest):
    session = db.session
    try:
        Contact.create_contact(
            session=session, contact_data=request
        )
        session.commit()
        return BaseResponseModel(
            status=True, message="Contact Created Successfully"
        )
    except Exception as e:
        session.rollback()
        logger.error(f"Error while creating contact: {e}")
        raise HTTPException(status_code=500, detail="Error while creating contact")

