#!/usr/bin/env python3

from typing import Any
import data_processor


class DataStream:
    def __init__(self) -> None:
        self.processors: list[data_processor.DataProcessor] = []

    def register_processor(self, proc: data_processor.DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            handled = False

            for proc in self.processors:
                if proc.validate(item):
                    proc.ingest(item)
                    handled = True
                    break

            if not handled:
                print("DataStream error - Can't process element "
                      f"in stream: {item}")

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data\n")

        for proc in self.processors:
            class_name = type(proc).__name__
            name = class_name.removesuffix("Processor") + " Processor"
            total = proc.total_processed
            remaining = proc.remaining

            print(f"{name}: total {total} items processed,", end=" ")
            print(f"remaining {remaining} on processor")


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Numeric Processor\n")
    numeric = data_processor.NumericProcessor()
    stream.register_processor(numeric)

    batch: list[Any] = [
        "Hello world", [3.14, -1, 2.71],
        [{"log_level": "WARNING", "log_message": "Telnet access! "
          "Use ssh instead"},
         {"log_level": "INFO", "log_message": "User wil is connected"}],
        42, ["Hi", "five"],
    ]

    print(f"Sending first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    text = data_processor.TextProcessor()
    stream.register_processor(text)

    logs = data_processor.LogProcessor()
    stream.register_processor(logs)

    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nConsume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for processor, count in [(numeric, 3), (text, 2), (logs, 1)]:
        for _ in range(count):
            processor.output()
    print("\nAfter consuming values:")
    stream.print_processors_stats()
