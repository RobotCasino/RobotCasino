import re
from typing import Optional, Tuple

class BrowserConsole:
    @staticmethod
    def parse_message(message: object) -> Optional[Tuple[str, str]]:
        if not isinstance(message, dict):
            return None

        params = message.get("params")
        if not isinstance(params, dict):
            return None
        
        args = params.get("args")
        if not isinstance(args, list) or not args:
            return None

        first_arg = args[0]
        if not isinstance(first_arg, dict):
            return None

        msg = first_arg.get("value")
        if not isinstance(msg, str):
            return None
            
        match = re.search(r'\[([^\]]+)\]', msg)
        if not match:
            return None

        command = match.group(1)
        payload = msg[len(match.group(0)):].strip()

        return command, payload
