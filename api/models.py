from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """Tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowEmployeeData(TunedModel):
    """For user_get_endpoint"""

    current_salary: str
    next_promotion_date: str


class Token(TunedModel):
    """jwt-response model"""

    access_token: str
    token_type: str
