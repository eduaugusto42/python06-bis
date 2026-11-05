#!/usr/bin/env python3

from typing import Any, Protocol
from data_stream import DataStream as BaseDataStream
import data_processor


class CSVExportPlugin:
    @staticmethod
    def _csv_field(value: str) -> str:
        if any(char in value for char in ',"\n\r'):
            return '"' + value.replace('"', '""') + '"'
        return value

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        values = [self._csv_field(value) for _, value in data]
        print(",".join(values))


class JSONExportPlugin:
    @staticmethod
    def _json_escape(value: str) -> str:
        return (value.replace("\\", "\\\\")
                     .replace('"', '\\"')
                     .replace("\n", "\\n")
                     .replace("\r", "\\r")
                     .replace("\t", "\\t"))

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        items = [f'"item_{rank}": "{self._json_escape(value)}"'
                 for rank, value in data]
        print("{" + ", ".join(items) + "}")


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class DataStream(BaseDataStream):
    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        if nb < 0:
            raise ValueError("nb must be non-negative")

        for proc in self.processors:
            data: list[tuple[int, str]] = []

            count = min(nb, proc.remaining)

            for _ in range(count):
                data.append(proc.output())

            if data:
                plugin.process_output(data)


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Processors\n")
    numeric = data_processor.NumericProcessor()
    text = data_processor.TextProcessor()
    logs = data_processor.LogProcessor()
    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(logs)

    first_batch: list[Any] = [
        "Hello world", [3.14, -1, 2.71],
        [{"log_level": "WARNING", "log_message": "Telnet access! "
          "Use ssh instead"},
         {"log_level": "INFO", "log_message": "User wil is connected"}],
        42, ["Hi", "five"],
    ]

    print(f"Send first batch of data on stream: {first_batch}")
    stream.process_stream(first_batch)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())
    stream.print_processors_stats()

    second_batch: list[Any] = [
        21, ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [{"log_level": "ERROR", "log_message": "500 server crash"},
         {"log_level": "NOTICE",
          "log_message": "Certificate expires in 10 days"}],
        [32, 42, 64, 84, 128, 168], "World hello",
    ]

    print(f"\nSend another batch of data: {second_batch}")
    stream.process_stream(second_batch)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExportPlugin())
    stream.print_processors_stats()
