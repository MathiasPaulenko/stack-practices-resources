"""Template Method Pattern — data import pipeline.

The base class owns the algorithm skeleton (import_data); subclasses
implement only the steps that vary. Run with: python template_method.py
"""

from abc import ABC, abstractmethod


class DataImporter(ABC):
    def import_data(self, source: str) -> None:
        """The template method defining the algorithm skeleton."""
        raw = self._fetch(source)
        parsed = self._parse(raw)
        validated = self._validate(parsed)
        self._save(validated)
        self._on_complete()

    @abstractmethod
    def _fetch(self, source: str) -> str:
        pass

    @abstractmethod
    def _parse(self, raw: str) -> dict:
        pass

    def _validate(self, data: dict) -> dict:
        """Default step; can be overridden."""
        if "id" not in data:
            raise ValueError("Missing required field: id")
        return data

    def _save(self, data: dict) -> None:
        """Default step; can be overridden."""
        print(f"Saving: {data}")

    def _on_complete(self) -> None:
        """Hook method — subclasses may override or ignore."""
        pass


class CSVImporter(DataImporter):
    def _fetch(self, source: str) -> str:
        return f"CSV content from {source}"

    def _parse(self, raw: str) -> dict:
        return {"id": 1, "format": "csv", "content": raw}


class JSONImporter(DataImporter):
    def _fetch(self, source: str) -> str:
        return f"JSON content from {source}"

    def _parse(self, raw: str) -> dict:
        return {"id": 2, "format": "json", "content": raw}

    def _on_complete(self) -> None:
        print("JSON import completed!")


if __name__ == "__main__":
    CSVImporter().import_data("users.csv")
    JSONImporter().import_data("users.json")
