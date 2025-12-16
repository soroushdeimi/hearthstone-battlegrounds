from common.game_state import GameState
from common.minion import BuzzingVermin

if __name__ == "__main__":
    gs = GameState()

    gs.add_to_board(BuzzingVermin())
    gs.debug_print_board()

    print("\n--- Deal huge damage to slot 0 ---")
    gs.deal_damage_to_slot(0, 999)

    gs.debug_print_board()


