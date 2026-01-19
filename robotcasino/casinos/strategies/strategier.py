from pathlib import Path
import json

class Strategier:

    @staticmethod
    def is_strategy(casino: str, game: str, strategy: str):
        path = Path(f"./robotcasino/casinos/{casino.lower()}/strategies/{game.lower()}/{strategy.lower()}.json")

        return path.is_file()
    
    @staticmethod
    def get_strategy_as_dict(casino: str, game: str, strategy: str) -> dict:
        path = Path(f"./robotcasino/casinos/{casino.lower()}/strategies/{game.lower()}/{strategy.lower()}.json")


        if not path.is_file():
            raise FileNotFoundError(f"Strategy file not found: {path}")

        with path.open("r") as f:
            text = f.read()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON strategy file")

        return data

