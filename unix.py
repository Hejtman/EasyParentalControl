import logging
import subprocess


class Result:
    def __init__(self, return_code: int, outputs: tuple, strip=True):
        self.return_code: int = return_code
        self.stdout: str = str(outputs[0].decode('utf-8', errors='ignore')) if outputs[0] else ''
        self.stderr: str = str(outputs[1].decode('utf-8', errors='ignore')) if outputs[1] else ''

        if strip:
            self.stdout = self.stdout.strip()
            self.stderr = self.stderr.strip()

    def __str__(self):
        s = str(self.return_code)
        s += '\n' + self.stdout if self.stdout else ''
        s += '\n' + self.stderr if self.stderr else ''
        return s


class Unix:
    """Implements OS dependent calls"""
    @staticmethod
    def run(cmd: list) -> Result:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        outputs = process.communicate()
        return Result(process.returncode, outputs)

    @staticmethod
    def is_running(process: str) -> bool:
        return process in Unix.run(['ps', '-A']).stdout

    @staticmethod
    def get_user_name() -> str:
        return Unix.run(['hostname']).stdout

    @staticmethod
    def kill(process: str) -> Result:
        logger.info(f'killing {process}')
        result = Unix.run(['pkill', process])
        logger.error(f'pkill {process} failed: {result}') if result.return_code else logger.info('Killing successful')
        return result


logger = logging.getLogger(__name__)


# just UNIT TESTs
if __name__ == '__main__':
    assert not Unix.is_running('not_running_process')
    assert Unix.is_running('system')
    print(Unix.get_user_name())
    Unix.kill('chromium-browse')
