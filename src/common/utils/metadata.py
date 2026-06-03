class Metadata:
    _metadata: dict[str, str] = {}

    @classmethod
    def set(cls, key: str, value: str) -> None:
        cls._metadata[key] = value

    @classmethod
    def get(cls, key: str) -> str | None:
        return cls._metadata.get(key)

    @classmethod
    def get_or_fail(cls, key: str) -> str:
        if key not in cls._metadata:
            raise ValueError(f"Metadata key '{key}' not found")
        return cls._metadata[key]
    
    @classmethod
    def remove(cls, key: str) -> None:
        if key in cls._metadata:
            del cls._metadata[key]

    @classmethod
    def set_dictionary(cls, metadata: dict[str, str]) -> None:
        cls._metadata.update(metadata)
