from datetime import datetime
import sys


class Logger:
    def __init__(self, level: str, name: str = "logger"):
        self.min_level = level
        self.name = name
        self._level = {
            "DEBUG": {"value": 10, "label": "\033[36m DEBUG \033[0m"},
            "INFO": {"value": 20, "label": "\033[32m INFO \033[0m"},
            "WARNING": {"value": 30, "label": "\033[33m WARNING \033[0m"},
            "ERROR": {"value": 40, "label": "\033[31m ERROR \033[0m"},
            "CRITICAL": {"value": 50, "label": "\033[1;31m CRITICAL \033[0m"},
        }

    def _format_msg(self, level_name: str, messaje: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        label = self._level[level_name.upper()]["label"]

        return f"[{timestamp}] [{self.name}] [{label}] [{messaje}]"

    def _log(self, level_name, messaje):

        if self._level[level_name]["value"] >= self.min_level:
            formated_msg = self._format_msg(level_name, messaje)
            print(formated_msg, file=sys.stdout, flush=True)

    def debug(self, messaje):
        return self._log("DEBUG", messaje)

    def info(self, messaje):
        return self._log("INFO", messaje)

    def warning(self, messaje):
        return self._log("WARNING", messaje)

    def error(self, messaje):
        return self._log("ERROR", messaje)

    def critical(self, messaje):
        return self._log("CRITICAL", messaje)
