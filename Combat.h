#ifndef COMBAT_H
#define COMBAT_H


#include<ctime>
#include<vector>
#include<cstdlib>
#include<iostream>

#include "Player.h"
using namespace std;

class Combat{

    public:

    static vector<Minion*> getTaunts(Board &board){  //   این تابع کارش این هست که بره داخل برد حریف بگرده ببینه کدوم میمنیون ها تاونت دارن که بهشون اتک بزنیم اول
        vector<Minion*> taunts;
        for(int i=0 ; i<board.minions.size(); i++){
            if(board.minions[i]->taunt && board.minions[i]->health>0){
                taunts.push_back(board.minions[i]);
            }
        }

        return taunts;

    }


    static Minion* chooseTarget(Board &board){// انتخاب هدف برای حمله با این تابع انجام میشود

        vector<Minion*> taunts = getTaunts(board);

        if(taunts.size()>0){
            int r = rand() % taunts.size();
            return taunts[r];       
        }


        if(board.minions.size() ==0){
            return nullptr;
        }

        int index = rand() % board.minions.size();
        return board.minions[index];
    }



    static void deaalDamage(Minion *attacker, Minion *defender){// بررسی و ضربه زدن به مینیون حریف با توجه به دارا بودن دیواین شیلد
        if (defender->divineShield){
            defender->divineShield = false;

        }

        else{
            defender->health -= attacker->attack;    
        }
    
        if(attacker->divineShield){
            attacker->divineShield = false;
        }

        else{
            attacker->health -= defender->attack;
        }
    
    
    }



static void runDeathrattle(Board &board , Minion *m){// تابعی برای اجرا کردن دفرتل درصورت وجود بودن
    if(!m->deathrattle){
        return;
    }

    cout<<m->name<< " deathrattle triggered!\n";


     if (board.minions.size() < board.maxMinions) {
            board.addMinion(new Minion("Deathrattle Token", 1, 1, 1));
        }
}

static void handleDeaths(Board &board){ //پاک کردن مینیون های مرده از برد با دفرتل

    vector<Minion*> alive;
    for(int i=0 ;i<board.minions.size();i++){
        Minion *m = board.minions[i];


        if(m->health<=0){
            runDeathrattle(board , m);
        }
        else{
            alive.push_back(m);
        }
    }
board.minions = alive;

}


static void fight(Player &A ,Player &B){

    srand(time(NULL));

    cout<<"-=-=-= Combat Started! =-=-=-\n";

    int attackerIndexA = 0;
    int attackerIndexB = 0;

    while(A.board.minions.size()>0 && B.board.minions.size()>0){


        // نوبت بازیکن آ
        if(A.board.minions.size()>0){
            if(attackerIndexA >= A.board.minions.size()){
                attackerIndexA =0;
            }


            Minion *attacker = A.board.minions[attackerIndexA];
            Minion *target = chooseTarget(B.board);

            if(target ==nullptr){
                break;
            }

            cout << "[A] " << attacker->name << " attacks " << target->name << endl;  //مناسب برای لاگ گیری


            deaalDamage(attacker , target);
            handleDeaths(A.board);
            handleDeaths(B.board);



            attackerIndexA++;
        }

        if (A.board.minions.size() == 0 || B.board.minions.size() == 0){
                break;
            }


            //نوبت بازی ب

           if(B.board.minions.size()>0){


                if(attackerIndexB>=B.board.minions.size()){
                    attackerIndexB =0;
                }

                Minion *attacker = B.board.minions[attackerIndexB];
                Minion *target = chooseTarget(A.board);


                if(target==nullptr){
                    break;
                }

                cout << "[B] " << attacker->name << " attacks " << target->name << endl;

                deaalDamage(attacker ,target);
                handleDeaths(A.board);
                handleDeaths(B.board);



                attackerIndexB++;
           } 
    }


    cout<<"~~~ Combat Ended! ~~~\n";


    if(A.board.minions.size()>0 && B.board.minions.size() ==0){
        cout<<A.name<<" wins!\n";
    }
    else if(B.board.minions.size()>0 && A.board.minions.size() ==0){
        cout<<B.name<<" wins!\n";
    }
    else{
        cout<<"Draw!\n";
    }

}


};




#endif