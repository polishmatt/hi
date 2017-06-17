try:
    from mock import patch, call
except ImportError:
    from unittest.mock import patch
from tests import HiTest

class RunTest(HiTest):

    @patch('hi.hi.log')
    def assert_run(self, args, output, mock_log):
        if not isinstance(args, dict):
            if isinstance(args, str):
                argv = [args]
            else:
                argv = args
            args = {
                'argv': argv,
            }

        kwargs = {
            'hosts': self.hi.load_hosts(file=self.hosts_file),
            'groups': self.hi.load_groups(file=self.groups_file),
            'run': False,
        } 
        kwargs.update(args)
        self.hi.run(**kwargs)

        if isinstance(output, str):
            mock_log.assert_called_once_with(output)
        else:
            mock_log.assert_has_calls([call(line) for line in output])

    def test_command(self):
        self.assert_run('command', 'start command')

    def test_group(self):
        self.assert_run('group', 'start group end')

    def test_args(self):
        self.assert_run('args', 'start args end')

    def test_exact(self):
        self.assert_run('exact', 'start exact')

    def test_multiple(self):
        self.assert_run('multiple', ('multiple1', 'multiple2'))

    def test_prod(self):
        self.assert_run(('example', 'prod'), 'start example.com')

    def test_no_prod(self):
        self.assert_run({
            'argv': ('example', 'prod'),
            'rules': False,
        }, 'start example-prod')

    def test_pad_digit(self):
        self.assert_run(('pad', '1'), 'start 01-pad')

    def test_no_pad(self):
        self.assert_run({
            'argv': ('pad', '1'),
            'rules': False,
        }, ('01-pad', '10-pad'))

    def test_cron(self):
        self.assert_run('cron', 'start explicit-cron')

    def test_db(self):
        self.assert_run('db', 'start explicit-db')

    def test_missing_explicit_not_matched(self):
        self.assert_run('explicit', 'start explicit')

    def test_explicit_no_rules(self):
        self.assert_run({
            'argv': ('explicit'),
            'rules': False,
        }, ('explicit', 'explicit-cron', 'explicit-db'))

    def test_arg_rule(self):
        self.assert_run({
            'argv': ('example', 'prod'),
            'rules': False,
            'arg_rule': ('hi.rules.prod',),
        }, 'start example.com')

    def test_host_rule(self):
        self.assert_run({
            'argv': ('cron',),
            'rules': False,
            'host_rule': ('hi.rules.cron',),
        }, 'start explicit-cron')

