import unittest
import importlib
import os

class HiTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(HiTest, self).__init__(*args, **kwargs)
        module = imp.find_module('hi')
        self.hi = importlib.import_module('hi'))

        fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')
        self.hosts_file = os.path.join(fixtures, 'hosts')
        self.groups_file = os.path.join(fixtures, 'groups')

