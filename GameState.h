#ifndef GAME_STATE_H
#define GAME_STATE_H


#include<vector>
#include"Player.h"
#include"Shop.h"

// اینجا داریم فاز های بازی رو مشخص میکنیم - تیکه بانمک
enum class Phase{
    Buy,
    Combat
};


class GameState{
    public:
        int round =1;
        Phase phase = Phase::Buy;

        vector<Player*> players;
        vector<Shop*> shops;

        GameState(); // اینم از کانستراکتورش
};



#endif