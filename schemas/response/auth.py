from pydantic import BaseModel

from schemas.token_schemas import TokenInfo


class AuthorizationRegistrationResponse(BaseModel):
    status: str
    token_info: TokenInfo
