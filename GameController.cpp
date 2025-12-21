#include "GameController.h"
#include "Combat.h"
#include <iostream>
#include <chrono>

using namespace std;
using namespace chrono;



void GameController::run(GameState &state){// تابع اجرایی بسیار مهم حتما تسلط روی کار با این رو داشته باش

    while(true){
        // ------پسرک حتما توجه کن به اینجا
        //فاز خرید بازی
        state.phase = Phase::Buy;
        cout<<"\n-=-=-Round "<<state.round<<" | BUY PHASE -=-=\n";
        for (int i=0;i<state.players.size();i++){
            Player *p = state.players[i];
            Shop *s = state.shops[i];


            cout<<"\n---"<<p->name<<"TURN --\n";
            buyPhase(*p , *s);


        }
        // ------پسرک حتما توجه کن به اینجا
        //فاز Combat بازی

        state.phase = Phase::Combat;
        cout<<"\n----COMBAT PHASE ---\n";
        combatPhase(state);

        state.round++;
    }
}



void GameController::combatPhase(GameState &state){// نیاز به بررسی مجدد دارم  - پیاده سازی فاز مبارزه

for(int i=0; i+1<state.players.size();i+=2){
    Player *A = state.players[i];
    Player *B = state.players[i+1];

    cout<<"\n"<<A->name<<" VS "<<B->name<<endl;
    Combat::fight(*A ,*B);
}

}


void GameController::buyPhase(Player &p, Shop &shop) {

    // شروع فاز خرید (دقیقاً مثل قبل)
    shop.roll();
    auto start = steady_clock::now();

    const int TIMER = 120; // پسرک تایمر رو اینجا ست کردی حواست باشه

    while (true) {
        auto now = steady_clock::now();
        int elapsed = duration_cast<seconds>(now - start).count();

        // پایان زمان
        if (elapsed >= TIMER) {
            cout << "\nTime's Up!\n";
            break;
        }

        // نمایش فروشگاه
        shop.show();

        cout << "\nGold: " << p.gold
             << " | Time left: " << (TIMER - elapsed) << "s\n";

        cout << "0=Buy 1=Roll 2=Toggle Freeze 3=Sell 4=Upgrade 9=End\n";
        cout << "Enter command: ";

        int cmd;
        cin >> cmd;

        if (cmd == 0) {
            cout << "Enter slot index: ";
            int i;
            cin >> i;
            shop.buy(p, i);
        }
        else if (cmd == 1 && p.gold >= 1) {
            p.gold--;
            shop.roll();
        }
        else if (cmd == 2) {
            shop.toggleFreeze(p);
        }
        else if (cmd == 3) {
            cout << "Enter minion index to sell: ";
            int i;
            cin >> i;
            shop.sell(p, i);
        }
        else if (cmd == 4) {
            shop.upgrade(p);
        }
        else if (cmd == 9) {
            break;
        }
        else {
            cout << "Invalid command or not enough gold\n";
        }
    }

    // پایان فاز خرید
    if (shop.frozen) {
        cout << "\nShop will remain frozen for next turn\n";
    }
}
