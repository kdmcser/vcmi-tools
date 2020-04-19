from abc import ABC

import numpy

from color_convertor.rgb_convertor import RGBConvertor


class GrayDrawConvertor(RGBConvertor, ABC):
    def convert_pix(self, pix, config):
        red, green, blue = pix
        gray = (red + green + blue) // 3
        new_red = int(gray / 255.0 * config.red)
        new_green = int(gray / 255.0 * config.green)
        new_blue = int(gray / 255.0 * config.blue)
        return numpy.array([new_red, new_green, new_blue], dtype=pix.dtype)
