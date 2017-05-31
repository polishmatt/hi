import os
from tests import HiTest

class ImportTest(HiTest):
    def test_import(self):
        expected = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'hi'))
        expected = [
            os.path.join(expected, 'hi.py'),
            os.path.join(expected, 'hi.pyc'),
            os.path.join(expected, '__init__.py'),
            os.path.join(expected, '__init__.pyc')
        ]
        found = self.hi.__file__
        if found not in expected:
            self.fail("""
                Version of hi imported is not the version we want to test
                Found: '%s'
                Expected: '%s'
            """ % (found, expected))

