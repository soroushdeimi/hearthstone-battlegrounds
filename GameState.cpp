#include"GameState.h"


GameState::GameState(){
    round =1;
    phase = Phase::Buy;



    // پسر حواست باشه اینجا میتونی HERO ها رو اضافه کنی

    Hero *hero1 = new Hero("Hero 1");
    Hero *hero2 = new Hero("Hero 2");


    //پسرک حواست باشه اینجا بازیکن ها رو اضافه میکنی ها!

    Player *player1 = new Player("Player 1", hero1);
    Player *player2 = new Player("Player 2" ,hero2);

    players.push_back(player1);// حواسته که این وکتور بود دیگه
    players.push_back(player2);

    // حواست باشه پسرک اینجا داریم برای هر بازیکن shop ایجاد میکنم

    Shop *shop1 = new Shop();
    Shop *shop2= new Shop();


    shops.push_back(shop1);
    shops.push_back(shop2);// حواسته که این وکتور بود دیگه

}