from abc import abstractmethod


class ConvertorBase(object):
    @abstractmethod
    def convert(self, input_image, config):
        """
            @param input_image: 输入图片，BGR颜色格式的numpy数组
            @param config: 图片处理配置
            @return outout_image: 输出图片，BGR颜色格式的numpy数组
        """
        print("内部错误：convert方法未实现！")
        return None

    @staticmethod
    def add_color(x, y):
        result = x + y
        result = 255 if result > 255 else result
        result = 0 if result < 0 else result
        return result

