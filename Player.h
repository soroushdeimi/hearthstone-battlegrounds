#ifndef PLAYER_H
#define PLAYER_H

#include "Hero.h"
#include "Board.h"
#include<iostream>
#include<string>
#include <unordered_map> // این چیز باحالیه شبیه دیکشنری ها توی پایتون هست 
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
    void checkForTriple(){// درواقع شمارش تعداد مینیون ها بر اساس نام رو انجام میده
        unordered_map<string, int> count; // اینجا یه دیکشنری ساختم که ببینیم از هر مینیون چند تا داریم 
        for(Minion *m : board.minions){
            count[m->name]++;
        }
        for(auto &entry : count){
            if(entry.second >= 3){
                std::string targetName= entry.first;
                int removed =0;
                int baseAttack =0;
                int baseHealth = 0;
                int tier =0;


                // اینجا اطلاعات مینیون رو جمع میکنیم و سه نسخه رو حذف میکنیم
                for(auto it = board.minions.begin(); it != board.minions.end() && removed <3;){
                    if((*it)->name == targetName){
                        if(removed ==0){
                            baseAttack =(*it)->attack;
                            baseHealth= (*it)->health;
                            tier = (*it)->tier;
                        }
                        delete *it;
                        it = board.minions.erase(it);
                        removed ++;

                    }
                    else{
                        ++it;
                    }
                }
    Minion* golden = new Minion(targetName + " (Golden)",
                            tier,
                            baseAttack * 2,
                            baseHealth * 2);
                board.addMinion(golden);
                break;
                
            }
        }

    }


};



#endif