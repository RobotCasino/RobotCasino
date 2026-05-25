
from src.utils.file_reader import FileReader
from os import getenv

class Resources:

    __memory_limit_as_bytes: int | None = None

    def __init__(self):
        Resources.__memory_limit_as_bytes = Resources.get_memory_limit_as_bytes()

    @staticmethod
    def is_memory_limit_reached() -> bool:
        memory_usage = Resources.get_memory_usage_as_bytes()
        memory_limit = Resources.get_memory_limit_as_bytes()

        if memory_usage is None or memory_limit is None:
            return False

        memory_ratio = float(getenv("MEMORY_RELOAD_RATIO", "0.95"))
        
        return memory_usage >= int(memory_limit * memory_ratio)
    
    @staticmethod
    def bytes_to_mb(value: int) -> int:
        return int(value / (1024 * 1024))

    @staticmethod
    def get_memory_usage_as_bytes() -> int | None:
        return Resources.__read_cgroup_value(
            (
                "/sys/fs/cgroup/memory.current",
                "/sys/fs/cgroup/memory/memory.usage_in_bytes",
            )
        )
    
    @staticmethod
    def get_memory_limit_as_bytes() -> int | None:
        return Resources.__memory_limit_as_bytes or Resources.__read_cgroup_value(
            (
                "/sys/fs/cgroup/memory.max",
                "/sys/fs/cgroup/memory/memory.limit_in_bytes",
            )
        )
    
    @staticmethod
    def get_memory_usage_as_bytes_or_fail() -> int:
        bytes = Resources.get_memory_usage_as_bytes()

        if bytes is None:
            raise ValueError("Failed to read memory usage")
        return bytes
    
    @staticmethod
    def get_memory_limit_as_bytes_or_fail() -> int:
        bytes = Resources.__memory_limit_as_bytes or Resources.get_memory_limit_as_bytes()

        if bytes is None:
            raise ValueError("Failed to read memory limit")
        return bytes
    
    @staticmethod
    def __read_cgroup_value(paths: tuple[str, ...]) -> int | None:
        for path in paths:
            try:
                raw_value = FileReader.read(path)

                if raw_value == "max":
                    return None

                value = int(raw_value)
                if value > (1 << 60):
                    return None

                return value
            except (FileNotFoundError, ValueError, OSError):
                continue

        return None
