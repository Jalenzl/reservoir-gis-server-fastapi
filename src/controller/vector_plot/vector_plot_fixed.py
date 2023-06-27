import matplotlib.pyplot as plt
from pylab import hypot
from numpy import arange
from matplotlib.pyplot import subplots
from utils import get_centroid, get_geojson
from io import BytesIO
import base64


def create_vector_plot_fixed(url_x, url_y, prop_name_x, prop_name_y):

    def create_plot():
        # 获取数据
        geo_json_oil_vy = get_geojson(url_y)
        geo_json_oil_vx = get_geojson(url_x)

        # 处理数据
        features_arr_oil_vy = geo_json_oil_vy['features']
        features_arr_oil_vx = geo_json_oil_vx['features']

        # 获取中心点坐标
        centroid_coordinates = []
        for feature in features_arr_oil_vy:
            coordinates_arr = feature['geometry']['coordinates'][0][0]
            centroid = get_centroid(coordinates_arr)
            centroid_coordinates.append(centroid)

        # 获取属性值
        properties_arr_y = [feature['properties'][prop_name_y] for feature in features_arr_oil_vy]
        properties_arr_x = [feature['properties'][prop_name_x] for feature in features_arr_oil_vx]
        properties_arr_composition = [hypot(vx, vy) for vx, vy in zip(properties_arr_x, properties_arr_y)]

        # 绘图所需参数
        X = [centroid_coordinate[0] for centroid_coordinate in centroid_coordinates]
        Y = [centroid_coordinate[1] for centroid_coordinate in centroid_coordinates]
        U, V = properties_arr_x, properties_arr_y
        M = hypot(U, V)

        # 绘图
        fig, ax = subplots(figsize=(8, 5.36))

        # 绘制二维场图
        plot_range = max(properties_arr_composition) - min(properties_arr_composition)
        levels = arange(min(properties_arr_composition), max(properties_arr_composition), plot_range / 55)
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
        t = ax.tricontourf(X, Y, properties_arr_composition, levels=levels, colors=colors)

        # 绘制矢量箭头
        q = ax.quiver(X, Y, U / M, V / M, M)
        ax.set_title('Vector flow field of oil velocity', pad=18, fontsize=15, fontweight='bold')

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

    return create_plot()
