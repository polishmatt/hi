import unittest
import importlib
import os


class HiTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(HiTest, self).__init__(*args, **kwargs)
        self.hi = importlib.import_module("hicli")
        self.actions = importlib.import_module("hicli.actions")

        fixtures = os.path.join(os.path.dirname(__file__), "fixtures")
        self.hosts_file = os.path.join(fixtures, "hosts")
        self.groups_file = os.path.join(fixtures, "groups")
