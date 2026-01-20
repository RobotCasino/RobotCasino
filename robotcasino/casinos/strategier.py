from pathlib import Path
import json

class Strategier:

    @staticmethod
    def is_strategy(game: str, strategy: str):
        path = Path(f"./robotcasino/casinos/games/{game.lower()}/strategies/{strategy.lower()}.json")

        return path.is_file()
    
    def __get_strategy_as_dict(self, game: str, strategy: str) -> dict:
        path = Path(f"./robotcasino/casinos/games/{game.lower()}/strategies/{strategy.lower()}.json")

        if not path.is_file():
            raise FileNotFoundError(f"Strategy file not found: {path}")

        with path.open("r") as f:
            text = f.read()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON strategy file")

        return data

