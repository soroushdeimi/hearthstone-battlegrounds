from core.app import GameManager
from config import *

def main() -> None:
    game_manager = GameManager(width=WIDTH, height=HEIGHT, caption=CAPTION, fps=FPS)
    game_manager.run()

if __name__ == "__main__":
    main()