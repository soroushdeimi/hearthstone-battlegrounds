#include"Board.h"
#include<iostream>
#include<algorithm>
using namespace std;



void Board::addMinion(Minion *m){

    if(minions.size()< maxMinions){
        minions.push_back(m);
        cout<<m->name<<" added to the board "<<endl;
    
    }

    else{

        cout<<"Board is full! Cannot add more minions."<<endl;
    }

}



// برای این تابع اومدم یه وکتور دیگه درست کردم و زنده ها رو ریختم توش و با وکتور قبلی جایگزین کردم
void Board::removeDead() {
    vector<Minion*> alive;

    for(int i=0;i<minions.size(); i++){
        if(minions[i]->health>0){
            alive.push_back(minions[i]);
        }

    }

    minions = alive;
}


//اولین مینیون زنده رو برمیگردونه برای نبرد
Minion *Board::getNextAttacker(){

    for(int i=0;i<minions.size();i++){
        if(minions[i]->health>0){
            return minions[i];
        }
    }

return nullptr; //     برای حالتی هست که هیچ مینیون زنده ای نبود
}



//این تابع صرفا مشخصات بورد رو چاپ میکنه کمک برای دیباگ هم هست
void Board::printBoard(){

    cout<<"Board: ";
        for (auto m : minions) {
        cout << m->name << "(" << m->attack << "/" << m->health << ") ";
    }
    cout << endl;
}
