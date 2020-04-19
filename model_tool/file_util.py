import os
import shutil


class FileUtil:
    MAX_COPY_BUFFER = 1024 * 1024
    @staticmethod
    def list_all_subfiles(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                yield os.path.join(root, file)
        pass

    @staticmethod
    def write_file(output_path, result_content):
        open_type = "w" if isinstance(result_content, str) else "wb"
        with open(output_path, open_type) as fp:
            fp.write(result_content)

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def delete(path):
        if not os.path.exists(path):
            return
        if os.path.isdir(path):
            return shutil.rmtree(path)
        return os.remove(path)

    # noinspection PyBroadException
    @staticmethod
    def copy_file(src, dest, overwrite=False):
        if os.path.isdir(src):
            print("内部错误：拷贝的文件：%s为目录" % src)
            return False

        if os.path.isfile(dest) and not overwrite:
            print("复制文件失败！目标文件: %s 已存在！" % dest)
            return False

        dest_dir = dest if os.path.isdir(dest) else os.path.dirname(dest)
        if dest_dir and not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except:
                print("创建目录：%s 失败！") % dest_dir
                return False

        try:
            with open(src, "rb") as fp_read:
                with open(dest, "wb") as fp_write:
                    content = fp_read.read(FileUtil.MAX_COPY_BUFFER)
                    while content:
                        fp_write.write(content)
                        content = fp_read.read(FileUtil.MAX_COPY_BUFFER)
                        pass
                    pass
                pass
            pass
        except:
            print("复制文件：%s 到 %s 失败！") % (src, dest)
            return False
        return True
    pass


