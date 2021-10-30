import logging
import subprocess


class Result:
    def __init__(self, return_code: int, outputs: tuple):
        self.return_code: int = return_code
        self.stdout: str = str(outputs[0].decode('utf-8', errors='ignore')).strip() if outputs[0] else ''
        self.stderr: str = str(outputs[1].decode('utf-8', errors='ignore')).strip() if outputs[1] else ''


class OS:
    """Implements OS dependent calls"""
    @staticmethod
    def run(cmd: list) -> Result:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        outputs = process.communicate()
        return Result(process.returncode, outputs)

    @staticmethod
    def is_running(process: str) -> bool:
        return process in OS.run(['ps', '-A']).stdout

    @staticmethod
    def get_user_name() -> str:
        return OS.run(['hostname']).stdout

    @staticmethod
    def pop_up(message: str) -> None:
        logger.info(f'warning pop-ed: {message}')
        # TODO

    @staticmethod
    def kill(process: str, message: str='') -> Result:
        logger.info(f'killing {process} ({message})')
        # TODO pop some sorry message
        result = OS.run(['pkill', process])
        logger.error(f'pkill {process} failed: {result}') if result.return_code else logger.info('Killing successful')
        return result


logger = logging.getLogger(__name__)


# just UNIT TESTs
if __name__ == '__main__':
    assert not OS.is_running('not_running_process')
    assert OS.is_running('system')
    print(OS.get_user_name())
    OS.pop_up(message='test message')
    OS.kill('chromium-browse')
