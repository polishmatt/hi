import subprocess
import os

from tests import HiTest

class CLITest(HiTest):

    def test_exit_default(self):
        with open(os.devnull, 'w') as FNULL:
            subprocess.check_call(
                ['python', '-mhi', '--hosts-file', 'tests/fixtures/hosts'],
                stdout=FNULL,
                stderr=subprocess.STDOUT
            )

    def test_exit_norun(self):
        with open(os.devnull, 'w') as FNULL:
            subprocess.check_call(
                ['python', '-mhi', '--hosts-file', 'tests/fixtures/hosts', '--no-run', 'exit_norun'],
                stdout=FNULL,
                stderr=subprocess.STDOUT
            )

    def test_exit_success(self):
        with open(os.devnull, 'w') as FNULL:
            subprocess.check_call(
                ['python', '-mhi', '--hosts-file', 'tests/fixtures/hosts', 'exit_success'],
                stdout=FNULL,
                stderr=subprocess.STDOUT
            )

    def test_exit_failure(self):
        try:
            with open(os.devnull, 'w') as FNULL:
                subprocess.check_call(
                    ['python', '-mhi', '--hosts-file', 'tests/fixtures/hosts', 'exit_failure'],
                    stdout=FNULL,
                    stderr=subprocess.STDOUT
                )
            self.fail('received success exit code when error expected')
        except subprocess.CalledProcessError:
            pass

