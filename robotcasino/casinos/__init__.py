from .game import Game
from .one_win import Aviator as OneWinAviator

OneWinGames = {
    'aviator': OneWinAviator,
}

Games = {
    'aviator': OneWinAviator,
}

__ALL__ = ['Game', 'OneWinGames']