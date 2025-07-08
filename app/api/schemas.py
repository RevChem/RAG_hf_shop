from typing import Literal

from pydantic import BaseModel


class AskResponse(BaseModel):
    response: str


class AskWithAIResponse(BaseModel):
    response: str
    provider: Literal["mistral", "mistral_Nemo"] = "mistral"


class SUserAuth(BaseModel):
    login: str
    password: str
