#ifndef MINION_H
#define MINION_H

#include "Card.h"
#include <iostream>
using namespace std;

class Minion : public Card {
public:
    int attack;
    int health;
    bool taunt;
    bool divineShield;
    bool deathrattle;
    bool poisonous;

    Minion(string n, int t, int atk, int hp)
        : Card(n, t, CardType::Minion),
          attack(atk),
          health(hp),
          taunt(false),
          divineShield(false),
          deathrattle(false),
          poisonous(false)
    {}

    void play() override {
        cout << name << " entered the board!" << endl;
    }
};


#endif
