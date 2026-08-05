from pydantic import BaseModel, EmailStr


class RecruiterCreate(BaseModel):
    full_name: str
    email: EmailStr
    employee_id: int | None = None