from pydantic import BaseModel

class UserSessionDTO(BaseModel):
    user_id: str
    role: str
