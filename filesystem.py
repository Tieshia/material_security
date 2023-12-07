from fs.memoryfs import MemoryFS
import re

ROOT = '/'

class Filesystem:
    def __init__(self):
        self.mem_fs = MemoryFS()
        self.pwd = ROOT

    def listdir(self):
        return self.mem_fs.listdir(self.pwd)

    def makedir(self, path):
        abs_path = self.process_path(path)
        self.mem_fs.validatepath(abs_path)
        return self.mem_fs.makedir(abs_path)

    def scandir(self):
        return self.mem_fs.scandir(self.pwd)

    def removedir(self, path):
        return self.mem_fs.removedir(self.process_path(path))

    def changedir(self, path):
        self.pwd = self.mem_fs.validatepath(self.process_path(path))
        return self.mem_fs if self.pwd == ROOT else self.mem_fs.opendir(self.pwd)

    def process_path(self, path):
        if path == ROOT:
            return ROOT

        path_components = path.split('/')
        if path_components[0] == '.':
            return self.pwd if not path_components[1:] else '/'.join(path_components[1:])
        elif path_components[0] == '..':
            parent_path = '/'.join(self.pwd.split('/')[:-1])
            final_location = '/'.join(path_components[1:])
            return '/'.join([parent_path, final_location])
        elif path_components[0] == '~':
            return ROOT if len(path_components) == 1 else '/'.join(path_components[1:])
        else:
            return self.pwd + '/' + path

    def pwd(self):
        return self.pwd

    def touch(self, path):
        abs_filepath = self.process_path(path)
        return self.mem_fs.touch(abs_filepath)

    def appendtext(self, path, text):
        abs_filepath = self.process_path(path)
        self.mem_fs.appendtext(abs_filepath, text)

    def readtext(self, path):
        abs_filepath = self.process_path(path)
        return self.mem_fs.readtext(abs_filepath)

    def movedir(self, srcpath, dstpath):
        abs_srcpath = self.process_path(srcpath)
        abs_dstpath = self.process_path(dstpath)
        return self.mem_fs.movedir(abs_srcpath, abs_dstpath, create=True)

    def movefile(self, srcpath, dstpath):
        abs_srcpath = self.process_path(srcpath)
        abs_dstpath = self.process_path(dstpath)
        contents = self.mem_fs.readtext(abs_srcpath)
        self.mem_fs.appendtext(abs_dstpath, contents)
        self.mem_fs.remove(abs_srcpath)

    def removefile(self, path):
        abs_path = self.process_path(path)
        return self.mem_fs.remove(abs_path)

    def close(self):
        return self.mem_fs.close()

    def tree(self, **kwargs):
        return self.mem_fs.tree()

    def find(self, pattern):
        return [item for item in self.listdir() if re.fullmatch(pattern, item.split('.')[0])]

    def copyfile(self, srcpath, dstpath):
        abs_srcpath = self.process_path(srcpath)
        abs_dstpath = self.process_path(dstpath)
        contents = self.mem_fs.readtext(abs_srcpath)
        return self.mem_fs.appendtext(abs_dstpath, contents)

    def copydir(self, srcpath, dstpath):
        abs_srcpath = self.process_path(srcpath)
        abs_dstpath = self.process_path(dstpath)
        return self.mem_fs.copydir(abs_srcpath, abs_dstpath, create=True)
