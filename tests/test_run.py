import os
#from unittest.mock import patch
from mock import patch
from tests import HiTest

start_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

class RunTest(HiTest):

    @patch('hi.hi.log')
    def test_command(self, mock_log):
        kwargs = {
            'hosts': self.hi.load_hosts(file=os.path.join(start_dir, 'hosts')),
            'groups': self.hi.load_groups(file=os.path.join(start_dir, 'groups')),
            'run': False,
            'argv': ['command'],
        }
        self.hi.run(**kwargs)
        mock_log.assert_called_once_with('ssh command')
        #print([call[0] for call in mock_log.call_args_list])

