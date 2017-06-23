try:
    from mock import patch, call
except ImportError:
    from unittest.mock import patch
from tests import HiTest

class RunTest(HiTest):

    def run_hi(self, args):
        if not isinstance(args, dict):
            if isinstance(args, str):
                argv = (args,)
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

    @patch('hi.logger.info')
    @patch('hi.logger._log')
    def assert_run(self, args, output, mock_log, mock_info):
        self.run_hi(args)

        if isinstance(output, str):
            mock_info.assert_called_once_with(output)
        elif output is not None:
            mock_info.assert_has_calls([call(line) for line in output])

    @patch('hi.logger.error')
    @patch('hi.logger._log')
    def assert_run_error(self, args, output, mock_log, mock_error):
        self.run_hi(args)

        for call in mock_error.call_args_list:
            assert call[0][0].index(output) == 0

    def test_command(self):
        self.assert_run('command', 'start command')

    def test_group(self):
        self.assert_run('group_command', 'start group_command end')

    def test_group_override(self):
        self.assert_run('group_override', 'child group_override replaced')

    def test_nested_group(self):
        self.assert_run('nested_command', 'start nested_command end')

    def test_nested_group_override(self):
        self.assert_run('nested_override', 'child nested_override replaced')

    def test_fail_circular_groups(self):
        self.assert_run_error('circular_group', 'Invalid config')

    def test_fail_undefined_group(self):
        self.assert_run_error('undefined_group', 'Invalid config')

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
        self.assert_run('explicit', 'start explicit-test')

    def test_explicit_no_rules(self):
        self.assert_run({
            'argv': ('explicit',),
            'rules': False,
        }, ('explicit-test', 'explicit-cron', 'explicit-db'))

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

    def test_valid_alias(self):
        self.assert_run('valid_alias', 'command')

    def test_invalid_alias(self):
        self.assert_run_error('invalid_alias', 'Invalid config')

    def test_variable_replace(self):
        self.assert_run('variable_replace', 'val variable_replace val')

    def test_variable_not_replaced(self):
        self.assert_run('variable_noreplace', '{var} variable_noreplace {var}')

