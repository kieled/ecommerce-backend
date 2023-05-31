from pydantic import BaseModel


class InstagramLink(BaseModel):
    url: str
