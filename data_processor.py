#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


NumericData = int | float | list[int | float]
TextData = str | list[str]
LogData = dict[str, str] | list[dict[str, str]]


class DataProcessor(ABC):
    """Hold separate values and assign a permanent rank as each one arrives."""

    def __init__(self) -> None:
        self._pending: list[tuple[int, str]] = []
        self._total_processed = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Return whether this processor accepts the entire input."""

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Validate and add all values in the input."""

    def _store(self, values: list[str]) -> None:
        for value in values:
            self._pending.append((self._total_processed, value))
            self._total_processed += 1

    def output(self) -> tuple[int, str]:
        """Remove and return the oldest value and its original rank."""
        if not self._pending:
            raise IndexError("No data to output")
        return self._pending.pop(0)

    def _restore_output(self, data: list[tuple[int, str]]) -> None:
        """Put an unsuccessful export back at the front of the queue."""
        self._pending[:0] = data

    @property
    def total_processed(self) -> int:
        return self._total_processed

    @property
    def remaining(self) -> int:
        return len(self._pending)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return bool(data) and all(
                isinstance(item, (int, float)) and not isinstance(item, bool)
                for item in data
            )
        return isinstance(data, (int, float)) and not isinstance(data, bool)

    def ingest(self, data: NumericData) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        values = data if isinstance(data, list) else [data]
        self._store([str(value) for value in values])


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return bool(data) and all(isinstance(item, str) for item in data)
        return isinstance(data, str)

    def ingest(self, data: TextData) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        values = data if isinstance(data, list) else [data]
        self._store(values)


class LogProcessor(DataProcessor):
    @staticmethod
    def _valid_entry(data: Any) -> bool:
        return (isinstance(data, dict) and bool(data)
                and all(isinstance(key, str) and isinstance(value, str)
                        for key, value in data.items()))

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return bool(data) and all(self._valid_entry(item) for item in data)
        return self._valid_entry(data)

    @staticmethod
    def _format_entry(entry: dict[str, str]) -> str:
        if "log_level" in entry and "log_message" in entry:
            return f"{entry['log_level']}: {entry['log_message']}"
        return ", ".join(f"{key}={value}" for key, value in entry.items())

    def ingest(self, data: LogData) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        values = data if isinstance(data, list) else [data]
        self._store([self._format_entry(entry) for entry in values])


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")
    numeric = NumericProcessor()
    print("\nTesting Numeric Processor...")
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    try:
        numeric.ingest("foo")  # Intentional mypy error: invalid input demo.
    except ValueError as error:
        print(f"Got exception: {error}")
    numeric.ingest([1, 2, 3, 4, 5])
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    text = TextProcessor()
    print("\nTesting Text Processor...")
    print(f"Trying to validate input '42': {text.validate(42)}")
    print(f"Trying to validate input 'Hello': {text.validate('Hello')}")
    text.ingest(["Hello", "Nexus", "World"])
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    logs = LogProcessor()
    print("\nTesting Log Processor...")
    print(f"Trying to validate input 'Hello': {logs.validate('Hello')}")
    valid_log = {"log_level": "NOTICE", "log_message": "Connected"}
    print(f"Trying to validate a log entry: {logs.validate(valid_log)}")
    logs.ingest([
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ])
    for _ in range(2):
        rank, value = logs.output()
        print(f"Log entry {rank}: {value}")
