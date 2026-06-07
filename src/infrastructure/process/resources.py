
import os

from common.utils.file_reader import FileReader
from common.utils.metadata import Metadata

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
        
        memory_ratio = getenv("MEMORY_RELOAD_RATIO")

        memory_ratio_as_float = float(memory_ratio) if memory_ratio is not None else None

        if memory_ratio_as_float is None:
            raise ValueError("Invalid MEMORY_RELOAD_RATIO environment variable")
        
        return memory_usage >= int(memory_limit * memory_ratio_as_float)
    
    @staticmethod
    def bytes_to_mb(value: int) -> int:
        return int(value / (1024 * 1024))

    @staticmethod
    def get_memory_usage_as_bytes() -> int | None:
        is_v2 = os.path.exists("/sys/fs/cgroup/memory.current")
            
        if is_v2:
            try:
                with open("/sys/fs/cgroup/memory.current", "r") as f:
                    total_memory = int(f.read().strip())
                    
                stats = {}
                with open("/sys/fs/cgroup/memory.stat", "r") as f:
                    for line in f:
                        key, val = line.strip().split()
                        stats[key] = int(val)
                    
                inactive_file = stats.get("inactive_file", 0)
                
                return total_memory - inactive_file
                    
            except (IOError, ValueError):
                return None
        else:
            try:
                with open("/sys/fs/cgroup/memory/memory.usage_in_bytes", "r") as f:
                    total_memory = int(f.read().strip())
                    
                stats = {}
                with open("/sys/fs/cgroup/memory/memory.stat", "r") as f:
                    for line in f:
                        key, val = line.strip().split()
                        stats[key] = int(val)
                    
                cache = stats.get("total_cache", 0)
                return total_memory - cache
                    
            except (IOError, ValueError):
                return None
        
    @staticmethod
    def get_memory_limit_as_bytes() -> int | None:
        if Resources.__memory_limit_as_bytes is not None:
            return Resources.__memory_limit_as_bytes

        memory_limit_env = getenv("MEMORY_LIMIT_MB")

        if memory_limit_env is not None:
            return int(memory_limit_env) * 1024 * 1024

        return Resources.__read_cgroup_value(
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
