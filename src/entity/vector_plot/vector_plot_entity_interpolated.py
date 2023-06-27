from pydantic import BaseModel


class VectorPlotEntityInterpolated(BaseModel):
    url_x: str
    url_y: str
    properties_arr_x: list
    properties_arr_y: list
    properties_arr_composition: list
