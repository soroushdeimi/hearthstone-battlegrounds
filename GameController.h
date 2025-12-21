#ifndef GAME_CONTROLLER_H
#define GAME_CONTROLLER_H
#include "Shop.h"
#include "Player.h"
#include"GameState.h"


class GameController{
    public:
        void run(GameState &state);
        void combatPhase(GameState &state);
        void buyPhase(Player &p, Shop &shop);
    
};


#endif
