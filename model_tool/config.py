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
        return False
