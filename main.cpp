#include<iostream>
using namespace std;
#include "GameState.h"
#include "GameController.h"
#include<ctime>
#include<cstdlib>

int main(){
    srand(time(NULL));

    // پسرک اینجا دارم حالت اولیه بازی رو پیاده میکنم از جمله بازیکن ها هیرو ها و فروشگاه ها
    GameState state;


    // اینجا کنترلر بازی رو ساختم
    GameController controller;

    controller.run(state);
    


}