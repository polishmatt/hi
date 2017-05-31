import unittest
import imp

class HiTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(HiTest, self).__init__(*args, **kwargs)
        module = imp.find_module('hi')
        self.hi = imp.load_module(*('hi',) + module)

