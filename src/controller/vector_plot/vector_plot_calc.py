import matplotlib.pyplot as plt
from pylab import hypot
from numpy import arange
from matplotlib.pyplot import subplots, show
from mpl_toolkits.basemap import Basemap
from src.utils.index import get_centroid, get_geojson
from src.controller.calc_velocity.index import calc_velocity, get_pressure_gradient, get_original_data
from io import BytesIO
import base64


def create_vector_plot_calc(type, layer, time):
    # 读取数据
    properties_arr_pressure, properties_arr_waterSaturation, properties_arr_permeability = get_original_data(layer,
                                                                                                             time)

    # 获取各个网格中心点坐标
    geo_json = get_geojson(
        'http://geoserver.vip.cpolar.cn/geoserver/permeability_I/ows?service=WFS&version=1.0.0&request=GetFeature'
        '&typeName=permeability_I%3Aperme_i_l6_vector&maxFeatures=5000&outputFormat=application%2Fjson')
    features_arr = geo_json['features']
    centroid_coordinates = []
    for feature in features_arr:
        coordinates_arr = feature['geometry']['coordinates'][0][0]
        centroid = get_centroid(coordinates_arr)
        centroid_coordinates.append(centroid)

    # 绘图所需参数
    gradient_x_778, gradient_y_778, gradient_magnitude_778 = get_pressure_gradient(properties_arr_pressure)
    velocity_water, velocity_oil = calc_velocity(layer, time)
    X = [centroid_coordinate[0] for centroid_coordinate in centroid_coordinates]
    Y = [centroid_coordinate[1] for centroid_coordinate in centroid_coordinates]
    U, V = gradient_x_778, gradient_y_778
    M = hypot(U, V)

    # 绘图
    fig, ax = subplots(figsize=(8, 5.36))

    # basemap 设置
    m = Basemap(llcrnrlon=118.555374, llcrnrlat=37.525674, urcrnrlon=118.562485, urcrnrlat=37.529734,
                resolution='i', projection='tmerc', lat_0=37.545, lon_0=118.559504, lat_1=37.527553, ax=ax)
    lon, lat = m(X, Y)
    m.drawmeridians([118.557000, 118.56100], labels=[1, 0, 0, 1], linewidth=0.7, color="#424242", dashes=[5, 5])
    m.drawparallels([37.526500, 37.5288], labels=[1, 0, 0, 1], linewidth=0.7, dashes=[5, 5])

    # 绘制二维场图
    velocity = []
    peak = 1.41
    if type == 'water':
        velocity = velocity_water
        peak = max(velocity) if max(velocity) > 1.41 else 1.41
    elif type == 'oil':
        velocity = velocity_oil
        peak = max(velocity) if max(velocity) > 0.19 else 0.19

    levels = arange(0, peak, peak / 55)
    colors = [
        "#0000ff",
        "#000eff",
        "#001dff",
        "#002bff",
        "#003aff",
        "#0048ff",
        "#0057ff",
        "#0065ff",
        "#0073ff",
        "#0082ff",
        "#0090ff",
        "#009fff",
        "#00adff",
        "#00bcff",
        "#00caff",
        "#00d9ff",
        "#00e7ff",
        "#00f5ff",
        "#05fffa",
        "#13ffec",
        "#22ffdd",
        "#30ffcf",
        "#3effc0",
        "#4dffb2",
        "#5bffa4",
        "#6aff95",
        "#78ff87",
        "#87ff78",
        "#95ff6a",
        "#a4ff5b",
        "#b2ff4d",
        "#c0ff3f",
        "#cfff30",
        "#ddff22",
        "#ecff13",
        "#faff05",
        "#fff500",
        "#ffe700",
        "#ffd900",
        "#ffca00",
        "#ffbc00",
        "#ffad00",
        "#ff9f00",
        "#ff9000",
        "#ff8200",
        "#ff7300",
        "#ff6500",
        "#ff5700",
        "#ff4800",
        "#ff3a00",
        "#ff2b00",
        "#ff1d00",
        "#ff0e00",
        "#ff0000",
    ]
    t = ax.tricontourf(lon, lat, velocity, levels=levels, colors=colors)

    # 绘制矢量箭头
    q = ax.quiver(lon, lat, U, V, M)
    ax.set_title(f'Flow vector field of {type} velocity', pad=18, fontsize=15, fontweight='bold')

    # color bar
    plt.colorbar(mappable=t, ax=ax, shrink=0.5, pad=-0.07, aspect=10, format='%.3f', anchor=(0.9, 0.5),
                 label='(m/day)')

    # 将图片存入内存
    save_file = BytesIO()
    fig.savefig(save_file, format='png', bbox_inches='tight', pad_inches=0.1, dpi=200)

    # 从内存中读取图片并转化为base64
    data = save_file.getvalue()
    img_base64 = base64.b64encode(data).decode('utf-8')

    return img_base64
