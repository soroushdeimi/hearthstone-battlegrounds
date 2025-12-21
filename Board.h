#ifndef BOARD_H
#define BOARD_H


#include <iostream>
#include "minion.h"
using namespace std;
#include<vector>

class Board{
    public:
    vector<Minion*> minions;
    const int maxMinions=7;


    void addMinion(Minion *m);
    void removeDead();
    Minion *getNextAttacker();
    void printBoard();
    

};



#endif