from color_convertor.gray_draw_convertor import GrayDrawConvertor
from color_convertor.rgb_add_convertor import RGBAddConvertor
from color_convertor.rgb_mix_convertor import RGBMixConvertor


class ColorConvertorFactory(object):
    @staticmethod
    def create_color_convertor(name):
        if name == "rgb_add":
            return RGBAddConvertor()
        elif name == "rgb_mix":
            return RGBMixConvertor()
        elif name == "gray_draw":
            return GrayDrawConvertor()
        else:
            print("不支持创建%s的处理器" % name)
            return None
