from common.minion import Minion

class GameState:

    def __init__(self):
        self.board=[]
        self.max_board=7

    def add_to_board(self,minion,position=None):

        if len(self.board)>=self.max_board:
            print("Board is full, cannot summon:", minion.name)
            return False
        
        if position is None or position>=len(self.board):
            self.board.append(minion)

        else:
            self.board.insert(position,minion)
        
        print("Summoned on board:", minion)
        return True
    
    def summon_minion(self,card_id,position=None):

        from common.minion import BeetleToken, BuzzingVermin

        if card_id=="BEETLE_TOKEN":
            minion=BeetleToken()

        elif card_id=="BUZZING_VERMIN":
            minion=BuzzingVermin()

        else:
            print("Unknown card_id:", card_id)
            return False
        
        return self.add_to_board(minion, position)
    
    def debug_print_board(self):
        print("=== BOARD STATE ===")
        if not self.board:
            print("Board is empty.")
        else:
            for i, m in enumerate(self.board):
                print(f"{i}: {m}")
        print("===================")