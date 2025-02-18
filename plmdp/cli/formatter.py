from dataclasses import asdict
from typing import Literal, Callable
import json
import yaml

from plmdp.models.output import ProfilerOutput


class FormatterFactory:
    FORMATTERS = {
        "raw": lambda data: repr(data),
        "json": lambda data: json.dumps(asdict(data), default=str, indent=2),
        "yaml": lambda data: yaml.dump(asdict(data)),
    }

    @staticmethod
    def get_formatter(
        print_format: Literal["raw", "yaml", "json"] = "raw",
    ) -> Callable[[ProfilerOutput], str]:
        try:
            return FormatterFactory.FORMATTERS[print_format]
        except KeyError:
            raise ValueError("Unsupported format. Use 'raw', 'json', or 'yaml'.")
