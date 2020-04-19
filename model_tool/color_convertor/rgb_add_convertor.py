from abc import ABC

import numpy

from color_convertor.rgb_convertor import RGBConvertor


class RGBAddConvertor(RGBConvertor, ABC):
    def convert_pix(self, pix, config):
        red, green, blue = pix
        new_red = self.add_color(red, config.red)
        new_green = self.add_color(green, config.green)
        new_blue = self.add_color(blue, config.blue)
        return numpy.array([new_red, new_green, new_blue], dtype=pix.dtype)
