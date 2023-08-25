import numpy as np
import math
from src.utils.index import get_geojson


# 读取数据
def get_prop_values(url, prop_name):
    geo_json = get_geojson(url)
    features_arr = geo_json['features']
    properties_arr = [feature['properties'][prop_name] for feature in features_arr]
    return properties_arr


def get_original_data(layer, time):
    properties_arr_pressure = get_prop_values(
        f'http://geoserver.vip.cpolar.cn/geoserver/pressure/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=pressure%3Apressure_l{layer}_t{time}_vector&maxFeatures=5000&outputFormat=application%2Fjson',
        'pressure')
    properties_arr_waterSaturation = get_prop_values(
        f'http://geoserver.vip.cpolar.cn/geoserver/waterSaturation/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=waterSaturation%3Awater_sat_l{layer}_t{time}_vector&maxFeatures=5000&outputFormat=application%2Fjson',
        'water_sat')
    properties_arr_permeability = get_prop_values(
        f'http://geoserver.vip.cpolar.cn/geoserver/permeability_I/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=permeability_I%3Aperme_i_l{layer}_vector&maxFeatures=5000&outputFormat=application%2Fjson',
        'perme_i')
    return properties_arr_pressure, properties_arr_waterSaturation, properties_arr_permeability


# 根据网格位置替换数据
def replace_data(original_arr, replace_arr):
    for i in range(32, 39):
        original_arr[i] = replace_arr[i - 32]
    for i in range(54, 78):
        original_arr[i] = replace_arr[i - 47]
    for i in range(84, 117):
        original_arr[i] = replace_arr[i - 53]
    for i in range(123, 156):
        original_arr[i] = replace_arr[i - 59]
    for i in range(162, 195):
        original_arr[i] = replace_arr[i - 65]
    for i in range(201, 233):
        original_arr[i] = replace_arr[i - 71]
    for i in range(240, 272):
        original_arr[i] = replace_arr[i - 78]
    for i in range(279, 311):
        original_arr[i] = replace_arr[i - 85]
    for i in range(318, 349):
        original_arr[i] = replace_arr[i - 92]
    for i in range(356, 388):
        original_arr[i] = replace_arr[i - 99]
    for i in range(395, 427):
        original_arr[i] = replace_arr[i - 106]
    for i in range(433, 465):
        original_arr[i] = replace_arr[i - 112]
    for i in range(472, 504):
        original_arr[i] = replace_arr[i - 119]
    for i in range(510, 543):
        original_arr[i] = replace_arr[i - 125]
    for i in range(548, 582):
        original_arr[i] = replace_arr[i - 130]
    for i in range(587, 621):
        original_arr[i] = replace_arr[i - 135]
    for i in range(625, 660):
        original_arr[i] = replace_arr[i - 139]
    for i in range(664, 699):
        original_arr[i] = replace_arr[i - 143]
    for i in range(702, 739):
        original_arr[i] = replace_arr[i - 146]
    for i in range(742, 778):
        original_arr[i] = replace_arr[i - 149]
    for i in range(784, 817):
        original_arr[i] = replace_arr[i - 155]
    for i in range(827, 856):
        original_arr[i] = replace_arr[i - 165]
    for i in range(869, 895):
        original_arr[i] = replace_arr[i - 178]
    for i in range(910, 934):
        original_arr[i] = replace_arr[i - 193]
    for i in range(951, 972):
        original_arr[i] = replace_arr[i - 210]
    for i in range(992, 1008):
        original_arr[i] = replace_arr[i - 230]


# 求压力梯度
def get_pressure_gradient(properties_arr_pressure):
    pressure_matrix = []
    for i in range(0, 1014):
        pressure_matrix.append(np.nan)
    # 将778个原始压力数值替换nan
    replace_data(pressure_matrix, properties_arr_pressure)
    pressure_matrix_reshaped = np.reshape(pressure_matrix, (26, 39))
    # 差分算法求梯度
    [Fx, Fy] = np.gradient(pressure_matrix_reshaped, 16)
    gradient_magnitude = np.sqrt(np.multiply(Fx, Fx) + np.multiply(Fy, Fy))
    # 取出778个点的梯度值
    gradient_x_reshaped = np.reshape(Fx, (1014, 1)).flatten().tolist()
    gradient_y_reshaped = np.reshape(Fy, (1014, 1)).flatten().tolist()
    gradient_magnitude_reshaped = np.reshape(gradient_magnitude, (1014, 1)).flatten().tolist()
    gradient_x_778 = []
    gradient_y_778 = []
    gradient_magnitude_778 = []
    for i in range(32, 39):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(54, 78):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(84, 117):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(123, 156):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(162, 195):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(201, 233):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(240, 272):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(279, 311):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(318, 349):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(356, 388):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(395, 427):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(433, 465):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(472, 504):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(510, 543):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(548, 582):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(587, 621):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(625, 660):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(664, 699):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(702, 739):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(742, 778):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(784, 817):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(827, 856):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(869, 895):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(910, 934):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(951, 972):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])
    for i in range(992, 1008):
        gradient_x_778.append(gradient_x_reshaped[i])
        gradient_y_778.append(gradient_y_reshaped[i])
        gradient_magnitude_778.append(gradient_magnitude_reshaped[i])

    # 将nan替换为0
    gradient_x_778 = [0 if math.isnan(grad) else grad for grad in gradient_x_778]
    gradient_y_778 = [0 if math.isnan(grad) else grad for grad in gradient_y_778]
    gradient_magnitude_778 = [0 if math.isnan(grad) else grad for grad in gradient_magnitude_778]

    return gradient_x_778, gradient_y_778, gradient_magnitude_778


# 根据相渗曲线求相对渗透率
def get_relative_permeability(properties_arr_waterSaturation):
    krw = [(2.3121 * Sw * Sw - 1.4891 * Sw + 0.2447) for Sw in properties_arr_waterSaturation]
    krow = [(
            -598.0 * Sw ** 6 +2064.9 * Sw ** 5 - 2941.8 * Sw ** 4 + 2192.7 * Sw ** 3 - 887.48 * Sw ** 2 + 178.92 * Sw - 12.838)
        for Sw in properties_arr_waterSaturation]

    # 确保所有相对渗透率在0到1范围内
    for index, krwi in enumerate(krw):
        if krwi > 1:
            krw[index] = 1
        elif krwi < 0:
            krw[index] = 0
    for index, krowi in enumerate(krow):
        if krowi > 1:
            krow[index] = 1
        elif krowi < 0:
            krow[index] = 0
    return krw, krow


# 根据达西定律求流速
def calc_velocity(layer, time):
    properties_arr_pressure, properties_arr_waterSaturation, properties_arr_permeability = get_original_data(layer,
                                                                                                             time)
    gradient_x_778, gradient_y_778, gradient_magnitude_778 = get_pressure_gradient(properties_arr_pressure)
    krw, krow = get_relative_permeability(properties_arr_waterSaturation)
    velocity_water = [(grad * krw * ko / 0.3368 / 10000) for grad, krw, ko in
                      zip(gradient_magnitude_778, krw, properties_arr_permeability)]
    velocity_oil = [(grad * krow * kw / 0.3368 / 10000 / 165) for grad, krow, kw in
                    zip(gradient_magnitude_778, krow, properties_arr_permeability)]
    return velocity_water, velocity_oil
