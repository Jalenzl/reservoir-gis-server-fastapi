from fastapi import FastAPI
from src.controller.vector_plot.vector_plot_fixed import create_vector_plot_fixed
from src.controller.vector_plot.vector_plot_interpolated import create_vector_plot_interpolated
from src.controller.vector_plot.vector_plot_calc import create_vector_plot_calc
from src.controller.calc_velocity.index import calc_velocity
from src.entity.vector_plot.vector_plot_entity_interpolated import VectorPlotEntityInterpolated
from src.entity.vector_plot.vector_plot_entity_fixed import VectorPlotEntityFixed
from src.entity.vector_plot.vector_plot_entity_calc import VectorPlotEntityCalc
from src.entity.calc_velocity.flow_velocity import FlowVelocityEntity

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/api/v1/vectorPlotFixed")
async def send_vector_plot(plot_entity: VectorPlotEntityFixed):
    img_base64 = create_vector_plot_fixed(plot_entity.url_x, plot_entity.url_y, plot_entity.prop_name_x,
                                          plot_entity.prop_name_y)
    return {
        "code": 200,
        "img_base64": "data:image/png;base64," + img_base64
    }


@app.post("/api/v1/vectorPlotInterpolated")
async def send_vector_plot(plot_entity: VectorPlotEntityInterpolated):
    img_base64 = create_vector_plot_interpolated(plot_entity.url_x, plot_entity.url_y, plot_entity.properties_arr_x,
                                                 plot_entity.properties_arr_y, plot_entity.properties_arr_composition)
    return {
        "code": 200,
        "img_base64": "data:image/png;base64," + img_base64
    }


@app.post("/api/v1/vectorPlotCalc")
async def send_vector_plot(plot_entity: VectorPlotEntityCalc):
    img_base64 = create_vector_plot_calc(plot_entity.type, plot_entity.layer, plot_entity.time)

    return {
        "code": 200,
        "img_base64": "data:image/png;base64," + img_base64
    }


@app.post("/api/v1/clacFlowVelocity")
async def send_flow_velocity(velocity_entity: FlowVelocityEntity):
    velocity_water, velocity_oil = calc_velocity(velocity_entity.layer, velocity_entity.time)
    return {
        "code": 200,
        "velocity_water": velocity_water,
        "velocity_oil": velocity_oil
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5301)
