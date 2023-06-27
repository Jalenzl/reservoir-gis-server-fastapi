from pydantic import BaseModel


class VectorPlotEntityFixed(BaseModel):
    url_x: str
    url_y: str
    prop_name_x: str
    prop_name_y: str
