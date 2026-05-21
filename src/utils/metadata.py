from typing import Any

class Metadata:
    _metadata: dict[str, str] = {}

    @classmethod
    def set(cls, key: str, value: str) -> None:
        cls._metadata[key] = value

    @classmethod
    def get(cls, key: str) -> str | None:
        return cls._metadata.get(key)
    
    @classmethod
    def remove(cls, key: str) -> None:
        if key in cls._metadata:
            del cls._metadata[key]
