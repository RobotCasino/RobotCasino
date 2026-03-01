from pathlib import Path
import json
from src.constants import BASE_DIR

class Strategier:

    @staticmethod
    def _get_strategy_json_path(game: str, strategy: str) -> Path:

        return BASE_DIR / "casinos" / "games" / game.lower() / f"{strategy.lower()}.json"

    @staticmethod
    def _get_strategy_script_path(game: str, strategy: str) -> Path:
        return BASE_DIR / "casinos" / "games" / game.lower() / f"{strategy.lower()}.js"

    @staticmethod
    def is_strategy(game: str, strategy: str):
        path = Strategier._get_strategy_json_path(game, strategy)

        return path.is_file()
    
    @staticmethod
    def get_strategy_as_dict(game: str, strategy: str) -> dict:
        path = Strategier._get_strategy_json_path(game, strategy)

        if not path.is_file():
            raise FileNotFoundError(f"Strategy file not found: {path}")

        with path.open("r") as f:
            text = f.read()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON strategy file")

        return data

    @staticmethod
    def get_strategy_as_string(game: str, strategy: str) -> str:
        path = Strategier._get_strategy_json_path(game, strategy)
        
        if not path.is_file():
            raise FileNotFoundError(f"Strategy file not found: {path}")

        with path.open("r") as f:
            text = f.read()
        
        return json.dumps(text)

    @staticmethod
    def get_strategy_script(game: str, strategy: str) -> str:
        path = Strategier._get_strategy_script_path(game, strategy)

        if not path.is_file():
            raise FileNotFoundError(f"Strategy script file not found: {path}")

        return path.read_text(encoding='utf-8')

    @staticmethod
    def build_strategy_with_user(game: str, strategy: str, user_data: dict | None = None) -> dict:
        strategy_data = Strategier.get_strategy_as_dict(game, strategy)
        safe_user_data = user_data or {}

        strategy_data['user'] = {
            'betAmount': safe_user_data.get('amount', '3.0'),
            'autoWithdrawal': safe_user_data.get('auto', '1.5')
        }

        return strategy_data

    @staticmethod
    def get_strategy_script_with_payload(game: str, strategy: str, user_data: dict | None = None) -> str:
        script = Strategier.get_strategy_script(game, strategy)
        strategy_data = Strategier.build_strategy_with_user(game, strategy, user_data)

        json_str = json.dumps(strategy_data)
        
        escaped_for_js = json.dumps(json_str)[1:-1]
        return script.replace('[strategy]', escaped_for_js)