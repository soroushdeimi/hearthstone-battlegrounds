#include"GameState.h"
#include "HeroPool.h"
#include<iostream>

GameState::GameState(){
    round =1;
    phase = Phase::Buy;



    std::vector<Hero*> heroes = HeroPool::getHeroes();

    int numPlayers = 4;  //تعداد کل بازیکنانی که قراره تو لابی باشن



for(int i=0;i<numPlayers;i++){// همون اولی رو به هر کدوم میدیم
    // باید اینجا رو ادیت کنم با توجه به اکشن ها کار کنه
    // اینجا سیستم فعلا اتوماتیک هیرو انتخاب میکنه
    Player *player = new Player("Player" + std::to_string(i+1), heroes[0]);
    players.push_back(player);
    heroes.erase(heroes.begin()+0);
    Shop *shop = new Shop();
    shops.push_back(shop);
}


    // اینجا داریم از کاربر هیرو میگیریم که اگه وارد فاز سرور شیم اذیته 
    // for(int i=0; i< numPlayers; i++){
    //     std::cout<<"Player "<<(i+1)<<"choose your hero:\n";
    //     for(int j=0;j<heroes.size(); ++j){
    //         std::cout<<j<<") "<<heroes[j]->name<<std::endl;
    //     }
    //     int choice;
    //     std::cin>>choice;
    //     if (choice < 0 || choice >= (int)heroes.size()) {
    //         choice = 0;
    //     }

    //     Player* player = new Player("Player " + std::to_string(i + 1), heroes[choice]);
    //     players.push_back(player);
    //     heroes.erase(heroes.begin() + choice);
    //     Shop* shop = new Shop();
    //     shops.push_back(shop);
    // }



    pendingActions.resize(numPlayers);
    discoverOffers.resize(numPlayers);    // مقداردهی ساختارهای pending / discover
    discoverPending.resize(numPlayers ,false);





    // پسر حواست باشه اینجا میتونی HERO ها رو اضافه کنی

    // Hero *hero1 = new Hero("Hero 1");
    // Hero *hero2 = new Hero("Hero 2");


    //پسرک حواست باشه اینجا بازیکن ها رو اضافه میکنی ها!

    // Player *player1 = new Player("Player 1", hero1);
    // Player *player2 = new Player("Player 2" ,hero2);

    // players.push_back(player1);// حواسته که این وکتور بود دیگه
    // players.push_back(player2);

    // حواست باشه پسرک اینجا داریم برای هر بازیکن shop ایجاد میکنم

    // Shop *shop1 = new Shop();
    // Shop *shop2= new Shop();


    // shops.push_back(shop1);
    // shops.push_back(shop2);// حواسته که این وکتور بود دیگه



}

void GameState::pushAction(int playerIndex ,const Action &a){//مطالعه شود
    {
        std::lock_guard<std::mutex> lg(actionMutex);
        if (playerIndex >= 0 && playerIndex < (int)pendingActions.size()) {
            pendingActions[playerIndex].push_back(a);
        }
    }
    actionCv.notify_all();
}

bool GameState::popAction(int playerIndex , Action &out){// you should read this bro
        std::lock_guard<std::mutex> lg(actionMutex);
    if (playerIndex >= 0 && playerIndex < (int)pendingActions.size() && !pendingActions[playerIndex].empty()) {
        out = pendingActions[playerIndex].front();
        pendingActions[playerIndex].erase(pendingActions[playerIndex].begin());
        return true;
    }
    return false;

}