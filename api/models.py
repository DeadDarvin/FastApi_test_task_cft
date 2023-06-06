from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowEmployeeData(TunedModel):
    current_salary: str
    next_promotion_date: str
