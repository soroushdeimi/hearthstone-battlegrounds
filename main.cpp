// #include<iostream>
// using namespace std;
// #include "GameState.h"
// #include "GameController.h"
// #include<ctime>
// #include<cstdlib>
// #include"Action.h"


// int main(){
//     // srand(time(NULL));

//     // پسرک اینجا دارم حالت اولیه بازی رو پیاده میکنم از جمله بازیکن ها هیرو ها و فروشگاه ها
//     GameState state;


//     // اینجا کنترلر بازی رو ساختم
//     GameController controller;

//     controller.run(state);
    


// }





#include <iostream>
#include "GameState.h"
#include "GameController.h"
#include "Action.h"

int main(){// اینجا اومدیم تست درست کردیم
    
    // ساختِ state (ممکنه ازت بخواد هیرو انتخاب کنی؛ این مرحله interactive است)
    GameState state;

    // ======= تست خودکار: اضافه کردن اکشن‌ها برای player0 =========
    // player0: Roll, Buy slot 0, EndTurn
    Action a;
    a.type = ActionType::Roll;
    state.pendingActions[0].push_back(a);

    Action b;
    b.type = ActionType::Buy;
    b.slotIndex = 0; // خرید از اسلات 0 (اگر خالی یا نامعتبر بود، shop.buy آن را رد خواهد کرد)
    state.pendingActions[0].push_back(b);

    Action e;
    e.type = ActionType::EndTurn;
    state.pendingActions[0].push_back(e);

    // برای بقیه بازیکنان هم EndTurn بفرست تا سریع عبور کنند
    for(int i = 1; i < (int)state.players.size(); ++i){
        Action end;
        end.type = ActionType::EndTurn;
        state.pendingActions[i].push_back(end);
    }
    // ================================================================

    GameController controller;
    controller.run(state);
    return 0;
}
