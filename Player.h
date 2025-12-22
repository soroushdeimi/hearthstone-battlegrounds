#ifndef PLAYER_H
#define PLAYER_H

#include "Hero.h"
#include "Board.h"
#include "MinionPool.h"
#include<algorithm>
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

    bool heroPowerUsed; // اینو اضافه کردم که بتونیم چک کنیم آیا هیرو قبلا از قدرتش استفاده کرده یا نه؟

    Player(string n, Hero* h) : name(n), hero(h), gold(3) , heroPowerUsed(false){}

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


                int nextTier = tier+1;
                discover(nextTier);
                break;
                
            }
        }

    }


    void discover(int tier){

        std::vector<Minion*> options = MinionPool::getByTier(tier);


            if(options.empty()){
                std::cout<<"No minions available for discover.\n";
                return;
            }

            int numOptions = std::min(3,(int)options.size());
            std::cout<<"Discover from Tier "<<tier<<":\n";
            for(int i=0;i<numOptions;i++){
                std::cout<<i<<") "<<options[i]->name<<" "<<options[i]->attack<<"/"<<options[i]->health<<std::endl;
            }
            std::cout<<"Enter your choice: ";
            int choice;
            std::cin>>choice;
            if(choice<0||choice>=numOptions){

                std::cout<<"Invalid choice, defaulting to 0\n";
                choice =0;
            }


            // اینجا دارم مینیون انتخاب شده رو به برد بازی اضافه میکنم
            Minion *chosen =options[choice];
            board.addMinion(chosen);

            for(int i=0;i<options.size();i++){
                if(i != choice){
                    delete options[i];
                }
            }
    }

};



#endif