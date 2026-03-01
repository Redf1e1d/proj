from pydantic import BaseModel, Field
from typing import Optional
import json

class DeveloperSchema(BaseModel):
    name: str
    age: int
    lang: str
    salary: int = Field(gt=0)
    active: bool = True
    level: str = "middle"

    def is_python(self) -> bool:
        return self.lang.lower() == "python"
    
    def is_active(self) -> bool:
        return self.active
    

with open("employees.json") as f:
    data = json.load(f)

developers = [DeveloperSchema(**item) for item in data]

class DeveloperBase(BaseModel):
    name: str
    age: int
    lang: str
    salary: int = Field(gt=0)
    active: bool = True
    level: str = "middle"


class DeveloperCreate(DeveloperBase):
    pass

class DeveloperUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    lang: Optional[str] = None
    salary: Optional[int] = Field(default=None, gt=0)
    active: Optional[bool] = None
    level: Optional[str] = None

class DeveloperResponse(DeveloperBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username : str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

