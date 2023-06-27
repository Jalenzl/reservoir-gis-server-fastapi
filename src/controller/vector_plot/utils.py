from numpy import mean
from requests import get as requests_get
from json import loads as json_loads


def get_centroid(coordinates_arr):
    centroid_x_arr = [coordinate[0] for coordinate in coordinates_arr]
    centroid_y_arr = [coordinate[1] for coordinate in coordinates_arr]

    centroid_x = mean(centroid_x_arr)
    centroid_y = mean(centroid_y_arr)

    return [centroid_x, centroid_y]


def get_geojson(url):
    return json_loads(requests_get(url).text)
