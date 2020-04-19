import os

import cv2

from color_convertor.color_convertor_factory import ColorConvertorFactory
from file_util import FileUtil


class ImagesColorProcessor(object):
    @staticmethod
    def process(config):
        all_files = FileUtil.list_all_subfiles(config.input_dir)
        for file in all_files:
            file_type = os.path.splitext(file)[1].lower()
            if ImagesColorProcessor.is_supported_image_file(file_type):
                if not ImagesColorProcessor.process_image_file(config, file):
                    return False
            else:
                if not ImagesColorProcessor.process_normal_file(config, file):
                    return False
            print("%s 文件处理成功！" % file)
        return True

    @staticmethod
    def get_output_path(input_absolute_path, input_dir, output_dir):
        relative_path = os.path.relpath(input_absolute_path, input_dir)
        return os.path.join(output_dir, relative_path)

    @staticmethod
    def is_supported_image_file(file_type):
        return file_type in {"bmp", "jpg", "jpeg", "pcx", "png"}

    @staticmethod
    def process_image_file(config, file):
        image = cv2.imread(file)
        if image is None:
            print("读取图片：%s失败！") % file
            return False
        convertor = ColorConvertorFactory.create_color_convertor(config.method)
        output_image = convertor.convert(image)
        if output_image is None:
            return False
        output_path = ImagesColorProcessor.get_output_path(file, config.input_dir, config.output_dir)
        if not cv2.imwrite(output_path, output_image):
            print("输出图片到：%s失败！") % output_path
            return False
        return True

    @staticmethod
    def process_normal_file(config, file):
        output_path = ImagesColorProcessor.get_output_path(file, config.input_dir, config.output_dir)
        return FileUtil.copy_file(file, output_path)




