import os
import random

import cv2
import numpy

from color_convertor.color_convertor_factory import ColorConvertorFactory
from file_util import FileUtil


class ImagesColorProcessor(object):
    EXCLUDE_DIR = {"shadow"}
    @staticmethod
    def process(config):
        all_files = FileUtil.list_all_subfiles(config.input_dir)
        for file in all_files:
            file_type = os.path.splitext(file)[1].lower()
            if ImagesColorProcessor.need_process(file, file_type):
                if not ImagesColorProcessor.process_image_file(config, file):
                    return False
                print("%s 文件颜色处理成功！" % file)
            else:
                if not ImagesColorProcessor.process_normal_file(config, file):
                    return False
                print("%s 文件拷贝成功，未进行颜色处理！" % file)

        return True

    @staticmethod
    def get_output_path(input_absolute_path, input_dir, output_dir):
        relative_path = os.path.relpath(input_absolute_path, input_dir)
        return os.path.join(output_dir, relative_path)

    @staticmethod
    def need_process(file_name, file_type):
        dir_name = os.path.dirname(file_name)
        path_splits = dir_name.replace("/", os.path.sep).split(os.path.sep)
        for path in path_splits:
            if path.lower() in ImagesColorProcessor.EXCLUDE_DIR:
                return False
        file_type = file_type[1:] if file_type.startswith(".") else file_type
        return file_type.lower() in {"bmp", "jpg", "jpeg", "pcx", "png"}

    @staticmethod
    def process_image_file(config, file):
        image = cv2.imread(file)
        if image is None:
            print("读取图片：%s失败！") % file
            return False
        convertor = ColorConvertorFactory.create_color_convertor(config.method)
        if convertor is None:
            return False
        output_image = convertor.convert(image, config)
        if output_image is None:
            return False
        output_path = ImagesColorProcessor.get_output_path(file, config.input_dir, config.output_dir)
        if config.overwrite and FileUtil.exists(output_path):
            FileUtil.delete(output_path)
        if not cv2.imwrite(output_path, output_image):
            print("输出图片到：%s失败！") % output_path
            return False
        return True

    @staticmethod
    def process_normal_file(config, file):
        output_path = ImagesColorProcessor.get_output_path(file, config.input_dir, config.output_dir)
        return FileUtil.copy_file(file, output_path, config.overwrite)

    @staticmethod
    def dry_run(config):
        all_files = FileUtil.list_all_subfiles(config.input_dir)
        all_images = [file for file in all_files
                      if ImagesColorProcessor.need_process(file, os.path.splitext(file)[1].lower())]
        if len(all_images) == 0:
            print("目录中无图像，无法试运行！")
            return False
        index = random.randint(0, len(all_images) - 1)
        file = all_images[index]
        return ImagesColorProcessor.process_and_compair_image(config, file)

    @staticmethod
    def process_and_compair_image(config, file):
        image = cv2.imread(file)
        if image is None:
            print("读取图片：%s失败！") % file
            return False
        convertor = ColorConvertorFactory.create_color_convertor(config.method)
        if convertor is None:
            return False
        output_image = convertor.convert(image, config)
        if output_image is None:
            return False
        show_image = numpy.concatenate((image, output_image), axis=1)
        cv2.imshow("Convert Result", show_image)
        cv2.waitKey(0)
        return True




