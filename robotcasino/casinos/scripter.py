from robotcasino.constants import BASE_DIR

class Scripter:

    @staticmethod
    def get_general_game_script(casino: str, game: str) -> str:
        return (BASE_DIR / "casinos" / casino / "scripts" / f"{game}.js").read_text(encoding='utf-8')
    
    @staticmethod
    def get_game_utils_script() -> str:
        return (BASE_DIR / "casinos" / "games" / "utils.js").read_text(encoding='utf-8')

    @staticmethod
    def get_game_domain_script(game: str) -> str:
        return (BASE_DIR / "casinos" / "games" / f"{game}-domain.js").read_text(encoding='utf-8')