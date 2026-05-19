from src.application import App
from src.infrastructure.config import init as config_init


def main():
    config_init()
    App()

if __name__ == "__main__":
    main()