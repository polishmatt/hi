import subprocess
import os

from tests import HiTest

class CLITest(HiTest):

    def test_exit_norun(self):
        with open(os.devnull, 'w') as FNULL:
            subprocess.check_call(
                ['python', '-mhi', '--no-run', 'exit_norun'],
                stdout=FNULL,
                stderr=subprocess.STDOUT
            )

    def test_exit_success(self):
        with open(os.devnull, 'w') as FNULL:
            subprocess.check_call(
                ['python', '-mhi', 'exit_success'],
                stdout=FNULL,
                stderr=subprocess.STDOUT
            )

    def test_exit_failure(self):
        try:
            with open(os.devnull, 'w') as FNULL:
                subprocess.check_call(
                    ['python', '-mhi', 'exit_failure'],
                    stdout=FNULL,
                    stderr=subprocess.STDOUT
                )
            self.fail('received success exit code when error expected')
        except subprocess.CalledProcessError:
            pass
