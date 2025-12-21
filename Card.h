#ifndef CARD_H
#define CARD_H


#include <string>
#include<iostream>

using namespace std;


enum class CardType{
Hero,
Minion

};

class Card{

    public:
        CardType type;
        string name;
        int tier;
        // int cost;   in battleground the cost of each minion is always 3 coins 
        string description;

        //constructors are here
        Card() : type(CardType::Minion), name(""), tier(1), description("") {}
        Card(string n, int t, CardType tp, string desc = "")
            : name(n), tier(t), type(tp), description(desc) {}

        virtual void play() {} // override in child classes
        virtual ~Card() {}
};



#endif