#ifndef PLAYER_H
#define PLAYER_H

#include "Hero.h"
#include "Board.h"
#include<iostream>
#include<string>
using namespace std;

class Player{
    public:
    string name;
    Hero *hero;
    Board board;
    int gold;

    Player(string n, Hero* h) : name(n), hero(h), gold(3){}

    void showBoard() {
        cout << name << "'s Board:" << endl;
        board.printBoard();
    }


};



#endif