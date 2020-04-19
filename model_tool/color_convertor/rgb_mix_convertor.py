from abc import ABC

import numpy

from color_convertor.rgb_convertor import RGBConvertor


class RGBMixConvertor(RGBConvertor, ABC):
    def convert_pix(self, pix, config):
        red, green, blue = pix
        new_red = self.add_color(red * config.src_property.red, config.red * config.dest_property.red)
        new_green = self.add_color(green * config.src_property.green, config.green * config.dest_property.green)
        new_blue = self.add_color(blue * config.src_property.blue, config.blue * config.dest_property.blue)
        return numpy.array([new_red, new_green, new_blue], dtype=pix.dtype)
