#from unittest.mock import patch
from mock import patch, call
from tests import HiTest

class RunTest(HiTest):

    @patch('hi.hi.log')
    def assert_run(self, argv, output, mock_log):
        if not hasattr(argv, '__iter__'):
            argv = [argv]

        kwargs = {
            'hosts': self.hi.load_hosts(file=self.hosts_file),
            'groups': self.hi.load_groups(file=self.groups_file),
            'run': False,
            'argv': argv,
        }
        self.hi.run(**kwargs)

        if hasattr(output, '__iter__'):
            mock_log.assert_has_calls([call(line) for line in output])
        else:
            mock_log.assert_called_once_with(output)

    def test_command(self):
        self.assert_run('command', 'start command')

    def test_group(self):
        self.assert_run('group', 'start group end')

    def test_args(self):
        self.assert_run('args', 'start args end')

    def test_exact(self):
        self.assert_run('exact', 'start exact')

    def test_multiple(self):
        self.assert_run('multiple', ['multiple1', 'multiple2'])

