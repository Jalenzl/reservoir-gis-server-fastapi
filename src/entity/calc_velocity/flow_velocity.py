from pydantic import BaseModel


class FlowVelocityEntity(BaseModel):
    layer: int
    time: int
