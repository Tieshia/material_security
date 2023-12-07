import unittest
from filesystem import Filesystem

class Test(unittest.TestCase):
	def setUp(self):
		self.fs = Filesystem()

	def tearDown(self):
		self.fs.close()

	def test_change_dir_with_basic_path_operations(self):
		self.fs.touch('projects_overview.py')

		self.fs.changedir('~')
		actual = self.fs.pwd
		expected = '/'
		self.assertEqual(actual, expected)

		self.fs.changedir('/')
		actual = self.fs.pwd
		expected = '/'
		self.assertEqual(actual, expected)

		self.fs.makedir('projects')
		self.fs.changedir('projects')
		actual = self.fs.pwd
		expected = '/projects'
		self.assertEqual(actual, expected)

		self.fs.changedir('.')
		actual = self.fs.pwd
		expected = '/projects'
		self.assertEqual(actual, expected)

		self.fs.changedir('..')
		actual = self.fs.pwd
		expected = '/'
		self.assertEqual(actual, expected)

		self.fs.changedir('projects')
		
		with self.assertRaises(Exception):
			self.fs.changedir('../projects_overview.py')

		self.fs.changedir('/')
		self.fs.makedir('expenses')

		self.fs.changedir('projects')
		self.fs.changedir('../expenses')
		actual = self.fs.pwd
		expected = '/expenses'
		self.assertEqual(actual, expected)

		with self.assertRaises(Exception):
			self.fs.changedir('/invalid_path')
			self.fs.changedir('//')
			self.fs.changdir('?tke/2kt')

	def test_listdir_returns_subdirectories_and_files(self):
		actual = self.fs.listdir()
		expected = []
		self.assertEqual(expected, actual)

		self.fs.makedir('projects')
		self.fs.touch('projects_script.py')
		actual = self.fs.listdir()
		expected = ['projects', 'projects_script.py']
		self.assertListEqual(actual, expected)

	def test_makedir_creates_a_new_subdirectory(self):
		previous = self.fs.listdir()
		self.fs.makedir('projects')
		actual = self.fs.listdir()
		self.assertGreater(len(actual), len(previous))
		self.assertNotEqual(actual, previous)

		with self.assertRaises(Exception):
			self.fs.makedir('//')
			self.fs.makedir('?/')

	def test_removedir_removes_specified_subdirectory(self):
		self.fs.makedir('projects')
		previous = self.fs.listdir()

		self.fs.removedir('projects')
		actual = self.fs.listdir()
		self.assertLess(len(actual), len(previous))
		self.assertNotEqual(actual, previous)

	def test_removedir_raises_error_when_file_passed(self):
		self.fs.touch('project1.py')
		with self.assertRaises(Exception):
			self.fs.removedir('project1.py')

	def test_pwd_return_current_working_directory(self):
		self.fs.makedir('projects')
		self.fs.changedir('projects')
		actual = self.fs.pwd
		expected = '/projects'
		self.assertEqual(actual, expected)

		self.fs.changedir('..')
		actual = self.fs.pwd
		expected = '/'
		self.assertEqual(actual, expected)

	def test_touch_creates_a_new_file_within_specified_path(self):
		previous = self.fs.listdir()
		self.fs.touch('projects.py')
		actual = self.fs.listdir()
		self.assertNotEqual(previous, actual)
		self.assertIn('projects.py', actual)

	def test_appendtext_writes_text_to_file(self):
		self.fs.touch('project1.py')
		previous = self.fs.readtext('project1.py')
		self.fs.appendtext('project1.py', 'Hello world!')
		actual = self.fs.readtext('project1.py')
		self.assertNotEqual(actual, previous)
		self.assertEqual(actual, 'Hello world!')

		previous = self.fs.listdir()
		self.fs.appendtext('new_file.py', 'Hello world!')
		actual = self.fs.listdir()
		self.assertGreater(len(actual), len(previous))
		self.assertEqual(self.fs.readtext('new_file.py'), 'Hello world!')

	def test_read_text_returns_specified_file_contents(self):
		self.fs.appendtext('project1.py', 'Hello world!')
		actual = self.fs.readtext('project1.py')
		expected = 'Hello world!'
		self.assertEqual(actual, expected)

		with self.assertRaises(Exception):
			self.fs.readtext('invalid_file.py')

	def test_movedir_moves_specified_directory_to_correct_destination(self):
		self.fs.makedir('projects')
		self.fs.makedir('projects/project1')
		self.fs.changedir('projects/')
		previous = self.fs.listdir()

		self.fs.movedir('project1', '../project1')
		actual = self.fs.listdir()

		self.assertLess(len(actual), len(previous))
		self.fs.changedir('/')
		self.assertIn('project1', self.fs.listdir())

		self.fs.touch('project1.py')

		with self.assertRaises(Exception):
			self.movedir('project1.py', 'projects')

	def test_movefile_moves_specified_file_to_correct_destination(self):
		self.fs.makedir('projects')
		self.fs.changedir('projects')
		self.fs.makedir('project1')
		self.fs.changedir('project1')
		self.fs.appendtext('project1.py', 'Hello world!')
		previous = self.fs.listdir()

		self.fs.movefile('project1.py', '../project1.py')
		actual = self.fs.listdir()
		

		self.assertLess(len(actual), len(previous))
		self.fs.changedir('..')
		self.assertIn('project1.py', self.fs.listdir())

		self.fs.makedir('extra_directory')
		with self.assertRaises(Exception):
			self.fs.movefile('extra_directory', '..')

	def test_find_returns_files_and_directories_matching_specified_parameters(self):
		self.fs.makedir('projects')
		self.fs.appendtext('project1.py', 'Hello world.')
		self.fs.appendtext('unrelated.py', 'Hello world.')
		actual = self.fs.find('project1')
		expected = ['project1.py']
		self.assertEqual(actual, expected)

		actual = self.fs.find('invalid')
		expected = []
		self.assertEqual(actual, expected)

	def test_remove_removes_specified_file(self):
		self.fs.touch('project1.py')
		previous = self.fs.listdir()

		self.fs.removefile('project1.py')
		actual = self.fs.listdir()

		self.assertLess(len(actual), len(previous))
		self.assertNotIn('project1.py', actual)

		self.fs.makedir('projects')
		with self.assertRaises(Exception):
			self.fs.removefile('projects')

	def test_copyfile_copies_file_into_specified_directory(self):
		self.fs.makedir('projects')
		self.fs.appendtext('project1.py', 'Hello world!')
		self.fs.copyfile('project1.py', 'projects/project1.py')

		self.fs.changedir('projects')
		actual = self.fs.listdir()
		expected = ['project1.py']
		self.assertEqual(actual, expected)

		self.fs.changedir('..')
		actual = self.fs.listdir()
		self.assertIn('project1.py', actual)

	def test_copydir_copies_directory_into_specified_directory(self):
		self.fs.makedir('projects')
		self.fs.makedir('project1')
		self.fs.changedir('project1')
		self.fs.appendtext('project1.py', 'Hellow world!')
		self.fs.changedir('..')
		self.fs.copydir('project1', 'projects')

		self.fs.changedir('projects')
		actual = self.fs.listdir()
		expected = ['project1.py']
		self.assertEqual(actual, expected)

		self.fs.changedir('..')
		actual = self.fs.listdir()

		self.assertIn('project1', actual)


unittest.main(verbosity=2)	
