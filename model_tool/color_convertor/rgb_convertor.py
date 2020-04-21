import cv2
from abc import ABC, abstractmethod

import numpy

from color_convertor.convertor_base import ConvertorBase
from config import DEF_TOOL

DEF_TOOl_RESERVE_COLORS = {[0, 255, 255]}
DEF_MAKER_RESERVE_COLORS = {[0, 255, 255], [255, 0, 255], [255, 150, 255], [255, 255, 0]}


class RGBConvertor(ConvertorBase, ABC):

    def convert(self, input_image, config):
        rgb_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        convert_image = numpy.array([self.convert_pix(pix, config)
                                     if not self.is_reserve_color(pix, config.format) else pix
                                     for row in rgb_image for pix in row]).reshape(input_image.shape)
        convert_image = cv2.cvtColor(convert_image, cv2.COLOR_RGB2BGR)
        return convert_image

    @staticmethod
    def is_reserve_color(pix, fmt):
        reserve_colors = DEF_TOOl_RESERVE_COLORS if fmt == DEF_TOOL else DEF_MAKER_RESERVE_COLORS
        if pix.tolist() in reserve_colors:
            return True
        return False

    @abstractmethod
    def convert_pix(self, pix, config):
        raise Exception("内部错误：convert_pix方法未实现！")
