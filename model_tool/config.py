RGB_ADD = "rgb_add"
RGB_MIX = "rgb_mix"
GRAY_DRAW = "gray_draw"
SUPPORTED_METHODS = {RGB_ADD, RGB_MIX, GRAY_DRAW}


class Property(object):
    def __init__(self, input_str=None):
        if input_str is None:
            self.red = self.green = self.blue = 0.0
            return

        property_list = [float(str(x).strip()) for x in str(input_str).split(",")]
        if len(property_list) == 1:
            self.red = self.green = self.blue = property_list[0]
        elif len(property_list) == 3:
            self.red, self.green, self.blue = property_list
        else:
            raise Exception("Unsupport property %s" % input_str)
        pass

    def get_opposite(self):
        opposite_property = Property()
        opposite_property.red = 1.0 - self.red
        opposite_property.green = 1.0 - self.green
        opposite_property.blue = 1.0 - self.blue
        return opposite_property

    def __str__(self):
        return ", ".join([str(self.red), str(self.green), str(self.blue)])

    pass


class Config(object):
    def __init__(self):
        self.input_dir = ""
        self.output_dir = ""
        self.overwrite = False
        self.method = ""
        self.red = 0
        self.green = 0
        self.blue = 0
        self.src_property = Property()
        self.dest_property = Property()
        pass

    def load_from_args(self, args):
        for necessary_arg in ["input_dir", "output_dir", "method", "red", "green", "blue"]:
            arg_value = args.__dict__.get(necessary_arg)
            if not arg_value or not arg_value.strip():
                print("缺少必要参数：%s" % necessary_arg)
                return False
            if not self.set_and_convert_field(necessary_arg, arg_value):
                return False

        method = args.__dict__.get("method").lower()
        if method not in SUPPORTED_METHODS:
            print("未知的method参数：%s， 目前只支持 %s" % (method, "/".join(SUPPORTED_METHODS)))
            return False

        for color_arg in ["red", "green", "blue"]:
            # rgb_add模式允许颜色值为负数，其余模式不允许
            allow_negetive = method == RGB_ADD
            if not self.is_valid_color(color_arg, allow_negetive):
                return False

        if method == RGB_MIX:
            if not self.check_and_get_property_args(args.src_property, args.dest_property):
                return False
        self.overwrite = args.overwrite
        return True

    # noinspection PyBroadException
    def set_and_convert_field(self, name, value):
        initial_value = self.__dict__.get(name, None)
        if initial_value is None:
            print("内部错误：未知参数: [%s]" % name)
            return False
        if isinstance(initial_value, int):
            try:
                value = int(value)
            except:
                print("参数：%s，值：%s 非法，需要整数" % (name, value))
                return False
        elif isinstance(initial_value, Property):
            try:
                value = Property(value)
            except:
                print("参数：%s，值：%s 非法，需要浮点数或逗号分隔的三个浮点数" % (name, value))
                return False
        elif isinstance(initial_value, str):
            pass
        else:
            print("内部错误：无法识别的参数：%s。类型：%s" % (name, type(initial_value)))
        self.__dict__[name] = value
        return True

    def is_valid_color(self, name, allow_negetive=False):
        color_arg = self.__dict__.get(name)
        min_color = -255 if allow_negetive else 0
        if not min_color <= color_arg <= 255:
            print("参数：%s需要在%s~255之间。实际值：%s" % (name, min_color, color_arg))
            return False
        return True

    def check_and_get_property_args(self, src_property, dest_property):
        if src_property is None and dest_property is None:
            self.src_property = self.dest_property = Property(0.5)
            print("设置原始颜色比例和混合颜色比例默认值为0.5, 0.5, 0.5")
        elif src_property is None:
            if not self.set_and_convert_field("dest_property", dest_property):
                return False
            self.src_property = self.dest_property.get_opposite()
            print("设置原始颜色比例默认值为%s" % self.src_property)
        elif dest_property is None:
            if not self.set_and_convert_field("src_property", src_property):
                return False
            self.dest_property = self.src_property.get_opposite()
            print("设置混合颜色比例默认值为%s" % self.dest_property)
        else:
            if not self.set_and_convert_field("src_property", src_property):
                return False
            if not self.set_and_convert_field("dest_property", dest_property):
                return False
        return True
