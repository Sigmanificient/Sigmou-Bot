import os
from datetime import datetime
from typing import NoReturn, List

import colorama
from termcolor import colored

colorama.init()

MAX_LOG_SIZE: int = 8 * 1024 * 1024
LOGS_DIR: str = 'app/logs/'


class Logger:

    def __init__(self):
        log_files: List[str] = [
            f for f in os.listdir(LOGS_DIR) if f.endswith('.log')
        ]

        self._actual_log_file_path = (
            sorted(log_files)[-1] if log_files else self.new_file
        )

    def __call__(self, color, log_type: str, message: str) -> NoReturn:
        date: str = datetime.now().strftime("%d/%b/%Y-%Hh:%Mm:%Ss")

        with open(self.log_file_path, 'a+') as f:
            f.write(f"[{date}] [{log_type}] {message}\n")

        print(
            f"[{colored(date, 'magenta')}]",
            f"[{colored(log_type, color=color)}]",
            message, flush=True
        )

    @property
    def new_file(self) -> str:
        return f'{datetime.now():%Y%b%d-%H%M%S}.log'

    @property
    def log_file_path(self) -> str:
        file_path: str = f'{LOGS_DIR}{self._actual_log_file_path}'

        if not os.path.exists(file_path):
            return file_path

        if os.path.getsize(file_path) < MAX_LOG_SIZE:
            return file_path

        return self.new_file

    def success(self, message: str) -> None:
        self('green', 'Success', message)

    def inform(self, message: str) -> None:
        self('blue', 'Info', message)

    def warn(self, message: str) -> None:
        self('yellow', 'Warning', message)

    def error(self, message: str) -> None:
        self('red', 'Error', message)


log = Logger()
