from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True
