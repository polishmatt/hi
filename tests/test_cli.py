import subprocess
import os

from tests import HiTest

class CLITest(HiTest):

    def test_exit_default(self):
        with open(os.devnull, 'w') as FNULL:
            subprocess.check_call(
                ['python', '-mhicli', '--hosts-file', self.hosts_file],
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT
            )

    def test_exit_norun(self):
        with open(os.devnull, 'w') as FNULL:
            subprocess.check_call(
                ['python', '-mhicli', '--hosts-file', self.hosts_file, '--no-run', 'exit_norun'],
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT
            )

    def test_exit_child_success(self):
        with open(os.devnull, 'w') as FNULL:
            subprocess.check_call(
                ['python', '-mhicli', '--hosts-file', self.hosts_file, 'exit_success'],
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT
            )

    def test_exit_child_failure(self):
        try:
            with open(os.devnull, 'w') as FNULL:
                subprocess.check_call(
                    ['python', '-mhicli', '--hosts-file', self.hosts_file, 'exit_failure'],
                    stdout=subprocess.STDOUT,
                    stderr=subprocess.STDOUT
                )
            self.fail('received success exit code when error expected')
        except subprocess.CalledProcessError:
            pass

    def test_exit_hi_failure(self):
        try:
            with open(os.devnull, 'w') as FNULL:
                subprocess.check_call(
                    ['python', '-mhicli', '--hosts-file', self.hosts_file, 'undefined_group'],
                    stdout=subprocess.STDOUT,
                    stderr=subprocess.STDOUT
                )
            self.fail('received success exit code when error expected')
        except subprocess.CalledProcessError:
            pass

