import sys
from argparse import ArgumentParser

from config import Config

if __name__ == "__main__":
    usage = "对目录里的所有图片文件批量进行颜色转换操作"
    description = '''
递归遍历输入目录，把检测到的图片文件进行颜色转换后写到输出目录相同的相对路径下。
目前支持格式为bmp, jpg, png和pcx。如果格式不支持，原样拷贝文件。目前暂打算支持三种颜色转换方式：
    1. 加减固定RGB颜色
    2. 按比例和固定RGB颜色混合
    3. 灰度化后按照亮度着色固定RGB颜色
该工具可用于批量处理VCMI生物模型，做简单的换色操作。
'''
    parser = ArgumentParser(usage=usage, description=description)
    parser.add_argument("-i", "--input_dir", dest="input_dir", help="输入目录")
    parser.add_argument("-o", "--output_dir", dest="output_dir", help="输出目录")
    parser.add_argument("-m", "--method", dest="method", help='''颜色转换方式：
    add - 加固定rgb分量到原始颜色中，需要配置-r -g -b
    mix - 混合固定rgb颜色到原始颜色中, 需要配置-r -g -b [-s -d]
    gray_draw - 灰度化后用固定颜色按亮度着色, 需要配置-r -g -b''')
    parser.add_argument("-r", "--red", dest="red", help="需要转换的颜色红色分量, 示例: 32")
    parser.add_argument("-g", "--green", dest="green", help="需要转换的颜色绿色分量, 示例： 16")
    parser.add_argument("-b", "--blue", dest="blue", help="需要转换的颜色蓝色分量, 示例: 8")
    parser.add_argument("-s", "--src_property", dest="src_property", help="mix模式中原始颜色所占比例。"
                                                     "示例1：0.5，示例2：0.1,0.5,0.1，默认值：0.5")
    parser.add_argument("-d", "--dest_property", dest="dest_property", help="mix模式中原始颜色所占比例。"
                                                      "示例1：0.5，示例2：0.9,0.5,0.9，默认值：0.5")
    args = parser.parse_args()
    config = Config()
    if not config.load_from_args(args):
        parser.print_help()
        sys.exit(1)