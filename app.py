from fastapi import FastAPI
from src.controller.vector_plot.vector_plot_fixed import create_vector_plot_fixed
from src.controller.vector_plot.vector_plot_interpolated import create_vector_plot_interpolated
from src.entity.vector_plot.vector_plot_entity_interpolated import VectorPlotEntityInterpolated
from src.entity.vector_plot.vector_plot_entity_fixed import VectorPlotEntityFixed

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5301)
