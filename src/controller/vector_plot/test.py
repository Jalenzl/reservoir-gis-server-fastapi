from vector_plot_fixed import create_vector_plot_fixed

url_oil_vy = 'https://geoserver.vip.cpolar.cn/geoserver/velocityOil_Y/ows?service=WFS&version=1.0.0&request' \
             '=GetFeature&typeName=velocityOil_Y%3Av_oil_y_l1_t1_vector&maxFeatures=1000&outputFormat=application' \
             '%2Fjson'
url_oil_vx = 'https://geoserver.vip.cpolar.cn/geoserver/velocityOil_X/ows?service=WFS&version=1.0.0&request' \
             '=GetFeature&typeName=velocityOil_X%3Av_oil_x_l1_t1_vector&maxFeatures=1000&outputFormat=application' \
             '%2Fjson'
name_x = 'v_oil_x'
name_y = 'v_oil_y'

create_vector_plot_fixed(url_oil_vx, url_oil_vy, name_x, name_y)
