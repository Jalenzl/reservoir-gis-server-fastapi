from pydantic import BaseModel


class VectorPlotEntityCalc(BaseModel):
    type: str
    layer: int
    time: int
