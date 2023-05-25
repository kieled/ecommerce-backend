import json

from pydantic import BaseModel, validator


class MessageSchema(BaseModel):
    action: str
    body: dict

    @validator('action')
    def action_validator(cls, v):
        if len(v.split(':')) != 2:
            raise ValueError('action is not valid')
        return v

    @validator('body', pre=True)
    def body_prepare(cls, v):
        if not isinstance(v, dict):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError('body is not valid')
        return v
