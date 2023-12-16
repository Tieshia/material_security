import re

ROOT = '/'

class File:
    def __init__(self):
        self.is_file = False
        self.content = ""
        self.files = {}

class Filesystem:
    def __init__(self):
        self.pwd = ROOT
        self.root = File()  

    def listdir(self):
        temp = self.root
        files = []

        if self.pwd != ROOT:
            dirs = self.pwd.split('/')
            for item in dirs[1:]:
                temp = temp.files[item]
            if temp.is_file:
                files.append(dirs[-1])
                return files
        result = temp.files.keys()
        return sorted(result)  

    def makedir(self, path):
        temp = self.root
        dirs = self.validate_path(path).split('/')
        for item in dirs[1:]:
            if item not in temp.files:
                temp.files[item] = File()
            temp = temp.files[item]

    def get_files_at_path(self, path):
        temp = self.root
        abs_path = self.validate_path(path)
       
        if abs_path != ROOT:
            dirs = abs_path.split('/')
            for item in dirs[1:-1]:
                temp = temp.files[item]

        return (temp, dirs)

    def removedir(self, path):
        temp, dirs = self.get_files_at_path(path)

        if temp.files[dirs[-1]].is_file:
                raise KeyError("Path must be directory.")

        del temp.files[dirs[-1]]
        

    def changedir(self, path):
        self.pwd = self.validate_path(path)

    def process_path(self, path):
        if path in [ROOT, '~']:
            return ROOT

        path_components = path.split('/')

        if self.pwd == ROOT and len(path_components) == 1:
            return self.pwd + path
        elif path_components[0] == '.':
            return self.pwd if not path_components[1:] else '/'.join(path_components[1:])
        elif path_components[0] == '..':
            parent_path = '/'.join(self.pwd.split('/')[:-1])
            final_location = '/'.join(path_components[1:])
            return '/'.join([parent_path, final_location]) if final_location else ROOT if not parent_path else parent_path
        elif path_components[0] == '~':
            return '/'.join(path_components[1:])
        else:
            return self.pwd + '/' + path if self.pwd != ROOT else self.pwd + path

    def pwd(self):
        return self.pwd

    def validate_path(self, path):
        abs_path = self.process_path(path)
        if abs_path == ROOT:
            return abs_path
       
        pattern = re.compile('^\/([A-z0-9-_+]+\/)*([A-z0-9]+)')
        if not pattern.match(abs_path):
            raise KeyError('Invalid filepath given.')
        else:
            return abs_path

    def touch(self, path, content=""):
        temp, dirs = self.get_files_at_path(path)

        if dirs[-1] not in temp.files:
            temp.files[dirs[-1]] = File()
        temp = temp.files[dirs[-1]]
        temp.is_file = True
        temp.content = temp.content + content

    def readtext(self, path):
        temp, dirs = self.get_files_at_path(path)

        return temp.files[dirs[-1]].content

    def movedir(self, srcpath, dstpath):
        self.copydir(srcpath, dstpath)
        self.removedir(srcpath)

    def movefile(self, srcpath, dstpath):
        self.copyfile(srcpath, dstpath)
        self.removefile(srcpath)

    def removefile(self, path):
        temp, dirs = self.get_files_at_path(path)

        file = temp.files[dirs[-1]]

        if not file.is_file:
            raise KeyError("Directory provided instead of file.")
        else:
            del temp.files[dirs[-1]]

    def find(self, pattern):
        return [item for item in self.listdir() if re.fullmatch(pattern, item.split('.')[0])]

    def copyfile(self, srcpath, dstpath):
        abs_srcpath = self.validate_path(srcpath)
        contents = self.readtext(srcpath)
        self.touch(dstpath, contents)


    def copydir(self, srcpath, dstpath):
        temp = self.get_dir_contents(srcpath)
        dir_contents = temp.files

        self.makedir(dstpath)

        temp = self.get_dir_contents(dstpath)
        temp.files.update(dir_contents)

    def get_dir_contents(self, path):
        abspath = self.validate_path(path)
        temp = self.root

        if abspath != ROOT:
            dirs = abspath.split('/')
            for item in dirs[1:]:
                temp = temp.files[item]

        return temp
