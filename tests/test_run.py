#from unittest.mock import patch
from mock import patch
from tests import HiTest

class RunTest(HiTest):

    @patch('hi.hi.log')
    def assert_run(self, argv, command, mock_log):
        if not hasattr(argv, '__iter__'):
            argv = [argv]

        kwargs = {
            'hosts': self.hi.load_hosts(file=self.hosts_file),
            'groups': self.hi.load_groups(file=self.groups_file),
            'run': False,
            'argv': argv,
        }
        self.hi.run(**kwargs)
        mock_log.assert_called_once_with(command)

    def test_command(self):
        self.assert_run('command', 'ssh command')

