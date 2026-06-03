class ArgsParser:
    @staticmethod
    def parse_args(args: list[str]) -> dict[str, str]:
        idx = 0
        extra_params: dict[str, str] = {}
        for arg in args:
            if arg.startswith("--"):
                key_value = arg[2:]
                
                if idx < len(args) - 1 and not args[idx + 1].startswith("--"):
                    extra_params[key_value] = args[idx + 1]
                
            idx += 1

        return extra_params

__ALL__ = ['ArgsParser']