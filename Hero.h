#ifndef HERO_H
#define HERO_H
#include<string>
#include<iostream>
#include "Card.h"
using namespace std;


class Hero : public Card{
        public:
        int health;

        Hero(string n)
        : Card(n, 1, CardType::Hero), health(40)
        {}

        void play() override{
            cout<< name<< " is your hero!"<<endl;
        }


};



#endif