from pydantic import BaseModel


class TokenInfo(BaseModel):
    token: str
    token_type: str
