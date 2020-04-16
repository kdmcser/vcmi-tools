class Config(object):
    def __init__(self):
        self.input_dir = ""
        self.output_dir = ""
        self.method = ""
        self.red = 0
        self.green = 0
        self.blue = 0
        self.src_property = 0.0
        self.dest_property = 0.0
        pass

    def load_from_args(self, args):
        for necessary_arg in ["input_dir", "output_dir", "method", "red", "green", "blue"]:
            arg_value = args.__dict__.get(necessary_arg)
            if not arg_value or not arg_value.strip():
                print("缺少必要参数：%s" % necessary_arg)
                return False
            if not self.set_and_convert_field(necessary_arg, args):
                return False

        for color_arg in ["red", "green", "blue"]:
            if not self.is_valid_color(color_arg):
                return False

        if not self.check_and_get_property_args(arg_value.src_property, arg_value.dest_property):
            return False
        return True

    # noinspection PyBroadException
    def set_and_convert_field(self, name, value):
        initial_value = self.__dict__.get(name)
        if not initial_value:
            print("内部错误：未知参数: [%s]" % initial_value)
            return False
        if isinstance(initial_value, int):
            try:
                value = int(value)
            except:
                print("参数：%s，值：%s 非法，需要整数" % (name, value))
                return False
        elif isinstance(initial_value, float):
            try:
                value = float(value)
            except:
                print("参数：%s，值：%s 非法，需要浮点数" % (name, value))
                return False
        elif isinstance(initial_value, str):
            pass
        else:
            print("内部错误：无法识别的参数：%s。类型：%s" % (name, type(initial_value)))
        self.__dict__[name] = value
        return True

    def is_valid_color(self, name):
        color_arg = self.__dict__.get(name)
        if not 0 <= color_arg <= 255:
            print("参数：%s需要在0~255之间。实际值：%s" % (name, color_arg))
            return False
        return True

    def check_and_get_property_args(self, src_property, dest_property):
        if src_property is None and dest_property is None:
            self.src_property = self.dest_property = 0.5
            print("设置原始颜色比例和混合颜色比例默认值为0.5（如果不是rgb_mix模式将不会用到）")
        elif src_property is None:
            if not self.set_and_convert_field("dest_property", dest_property):
                return False
            self.src_property = 1.0 - self.dest_property
            print("设置原始颜色比例默认值为%s（如果不是rgb_mix模式将不会用到）" % self.src_property)
        elif dest_property is None:
            if not self.set_and_convert_field("src_property", src_property):
                return False
            self.dest_property = 1.0 - self.src_property
            print("设置混合颜色比例默认值为%s（如果不是rgb_mix模式将不会用到）" % self.dest_property)
        return True

