from core.app import GameManager

def main() -> None:
    game_manager = GameManager(width=800, height=500, caption="STUNNERS GAME", fps=60)
    game_manager.run()

if __name__ == "__main__":
    main()