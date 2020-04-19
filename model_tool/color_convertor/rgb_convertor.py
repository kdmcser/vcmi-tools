import cv2
from abc import ABC, abstractmethod
from color_convertor.convertor_base import ConvertorBase


class RGBConvertor(ConvertorBase, ABC):
    RESERVE_LIST = ([0, 255, 255],)

    def convert(self, input_image, config):
        rgb_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        convert_image = [self.convert_pix(pix, config) if not self.is_reserve_color(pix) else pix
                         for row in rgb_image for pix in row]
        convert_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)
        return convert_image

    @staticmethod
    def is_reserve_color(pix):
        if pix.to_list() in RGBConvertor.RESERVE_LIST:
            return True
        return False

    @abstractmethod
    def convert_pix(self, pix, config):
        raise Exception("内部错误：convert_pix方法未实现！")

