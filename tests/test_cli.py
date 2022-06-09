import subprocess

from tests import HiTest


class CLITest(HiTest):
    def test_exit_default(self):
        subprocess.check_call(["python", "-mhicli", "--hosts-file", self.hosts_file])

    def test_exit_norun(self):
        subprocess.check_call(
            [
                "python",
                "-mhicli",
                "--hosts-file",
                self.hosts_file,
                "--no-run",
                "exit_norun",
            ]
        )

    def test_exit_child_success(self):
        subprocess.check_call(
            ["python", "-mhicli", "--hosts-file", self.hosts_file, "exit_success"]
        )

    def test_exit_child_failure(self):
        try:
            subprocess.check_call(
                ["python", "-mhicli", "--hosts-file", self.hosts_file, "exit_failure"]
            )
            self.fail("received success exit code when error expected")
        except subprocess.CalledProcessError:
            pass

    def test_exit_hi_failure(self):
        try:
            subprocess.check_call(
                [
                    "python",
                    "-mhicli",
                    "--hosts-file",
                    self.hosts_file,
                    "undefined_group",
                ]
            )
            self.fail("received success exit code when error expected")
        except subprocess.CalledProcessError:
            pass
