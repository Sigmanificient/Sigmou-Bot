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

    def __call__(self, message: str, color: str = 'green') -> NoReturn:
        date: str = f"[{datetime.now():%d/%b/%Y:%Hh %Mm %Ss}]"
        print(colored(date, color='blue'), colored(message, color=color))

        with open(self.log_file_path, 'a+') as f:
            f.write(f"{date} {message}\n")


def temp_print(message: str) -> NoReturn:
    print(
        colored('->', color='magenta'),
        colored(message.ljust(80, ' '), color='green'), end='\r'
    )


def warn(message: str) -> NoReturn:
    print(colored('[Warning]', color='red'), colored(message, 'yellow'))
