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
		if self.pwd != ROOT:
			self.mem_fs.validatepath(self.pwd + '/' + path)
			return self.mem_fs.makedir(self.pwd + '/' + path)
		else:
			self.mem_fs.validatepath(path)
			return self.mem_fs.makedir(path)

	def scandir(self):
		return self.mem_fs.scandir(self.pwd)

	def removedir(self, path):
		# Nothing explicitly returned
		return self.mem_fs.removedir(path)

	def changedir(self, path):
		self.pwd = self.mem_fs.validatepath(self.process_path(path))
		if self.pwd == ROOT:
			return self.mem_fs
		else:
			return self.mem_fs.opendir(self.pwd)

	def process_path(self, path):
		if path == ROOT:
			return ROOT

		path_components = path.split('/')
		# if len(path_components) == 1:
		# 	return '/' + path
		if path_components[0] == '.':
			return self.pwd
		elif path_components[0] == '..':
			# return parent directory
			parent_path = self.pwd.split('/')[-2]

			if parent_path == '':
				if path.split('..')[1:] == ['']:
					return ROOT
				else:
					return ('/').join(path.split('..')[1:])
			else:
				return ('/').join(self.pwd.split('/')[:-1])
		elif path_components[0] == '~':
			if len(path_components) == 1:
				return ROOT
			else:
				return ('/').join(path_components[1:])
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
		filename = dstpath.split('/')[-1]
		abs_srcpath = self.process_path(srcpath)
		abs_dstpath = self.process_path(dstpath) + '/' + filename
		contents = self.mem_fs.readtext(abs_srcpath)
		self.mem_fs.appendtext(abs_dstpath , contents)
		self.mem_fs.remove(abs_srcpath)

	def removefile(self, path):
		# Nothing explicitly returned
		abs_path = self.process_path(path)
		return self.mem_fs.remove(abs_path)

	def close(self):
		return self.mem_fs.close()

	def tree(self, **kwargs):
		return self.mem_fs.tree()

	def find(self, pattern):
		result = []
		for item in self.listdir():
			itemname = item.split('.')[0]
			if re.fullmatch(pattern, itemname):
				result.append(item)
		return result

	def copyfile(self, srcpath, dstpath):
		abs_srcpath = self.process_path(srcpath)
		abs_dstpath = self.process_path(dstpath)
		contents = self.mem_fs.readtext(abs_srcpath)
		return self.mem_fs.appendtext(abs_dstpath , contents)

	def copydir(self, srcpath, dstpath):
		abs_srcpath = self.process_path(srcpath)
		abs_dstpath = self.process_path(dstpath)
		return self.mem_fs.copydir(abs_srcpath, abs_dstpath, create=True)

