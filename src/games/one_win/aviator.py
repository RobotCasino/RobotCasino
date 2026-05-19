from src.domain import Game
from src.web import Tab, Element

class Aviator(Game):

    def __init__(self):
        super().__init__("OneWin", "https://1win.com", 'aviator')

    async def play(self, tab: Tab):
        if not self.is_strategy_loaded():
            raise ValueError('Strategy not loaded')

        await tab.go_to(self.get_url())

    async def _load_strategy(self, iframe: Element):
        pass
        # utils_script = ScriptLoader.get_game_utils_script()
        # general_script = ScriptLoader.get_general_game_script(self.get_casino(), self.get_name())
        # domain_script = ScriptLoader.get_game_domain_script(self.get_name())
        # observer_script = ScriptLoader.get_game_observer_script()
        # strategy_script = StrategyLoader.get_strategy_script_with_payload(
        #     self.get_name(),
        #     self.get_strategy(),
        #     self.get_user_data()
        # )

        # await iframe.execute_script(utils_script)
        # await iframe.execute_script(domain_script)
        # await iframe.execute_script(observer_script)
        # await iframe.execute_script(strategy_script)
        # await iframe.execute_script(general_script)
        
    async def __select_and_init_game(self, tab: Tab): # pyright: ignore
        play_btn = await tab.find_element('')

        return

        if isinstance(play_btn, WebElement):
            await play_btn.click()

    async def __get_iframe(self, tab: Tab) -> Element | bool: # pyright: ignore
        iframe_element = await tab.find_element('iframe')

        return False

        if not isinstance(iframe_element, WebElement):
            raise ValueError('Aviator iframe element not found')
    
        return iframe_element

__ALL__ = ['Aviator']