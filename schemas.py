from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    username: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class QueryBase(BaseModel):
    prompt: str

class Query(QueryBase):
    response: str
    id: int
    user_id: int
    llm_name: str
    tokens: int
    
    class Config:
        from_attributes = True
