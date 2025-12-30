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


            cout<<"\n---"<<p->name<<"TURN --(Health: "<<p->hero->health<<")\n";
            buyPhase(*p , *s);


        }
            // چک دارم میگنم اگه فقط یه بازیکن مونده باشه بازی تموم باشه
        if(state.players.size()<=1){
            cout<<state.players[0]->name<<"is the last player standing! Game Over.\n";
            break;
        }


        // ------پسرک حتما توجه کن به اینجا
        //فاز Combat بازی


        state.phase = Phase::Combat;
        cout<<"\n----COMBAT PHASE ---\n";
        combatPhase(state);

        state.round++;

            // نیازه دوباره چک کنم ببینم یه بازیکن اگر مونده بازی تمومه
                if(state.players.size()<=1){
            cout<<state.players[0]->name<<"is the last player standing! Game Over.\n";
            break;
        }

    }
}



void GameController::combatPhase(GameState &state){// نیاز به بررسی مجدد دارم  - پیاده سازی فاز مبارزه

int i=0;
while(i+1<state.players.size()){
    Player *A = state.players[i];
    Player *B = state.players[i+1];


    cout<<"\n"<<A->name<<" VS "<<B->name<<endl;
    Combat::fight(*A,*B);


    //اینجا دارم بازنده و برنده رو مشخص میکنم
    bool aHasMinions = (A->board.minions.size()>0);
    bool bHasMinions = (B->board.minions.size()>0);
    
    if(aHasMinions && !bHasMinions){

        int damage = state.shops[i]->tavernTier;
        for(Minion *m :A->board.minions){
            damage +=m->tier;
        }

        B->hero->health -= damage;
        
        cout << B->name << " takes " << damage << " damage! (Health: " << B->hero->health << ")\n";
        if(B->hero->health<=0){
            cout<<B->name<<"has been eliminated!\n";
            state.players.erase(state.players.begin()+ (i+1));
            state.shops.erase(state.shops.begin() + (i+1));

        }
        else{
            i+=2;
        }


    }       
     else if(bHasMinions && !aHasMinions){
        int damage = state.shops[i+1]->tavernTier;
        for(Minion *m : B->board.minions){
            damage +=m->tier;
        }
        
        A->hero->health -=damage;
            cout << A->name << " takes " << damage << " damage! (Health: " << A->hero->health << ")\n";
        if(A->hero->health<=0){
            cout<<A->name<<" has been eliminated! \n";


            state.players.erase(state.players.begin()+i);
            state.shops.erase(state.shops.begin()+i);

        }

        else{
            i+2;

        }

        }

        else{
            cout << "It's a draw. No damage dealt.\n";
            i += 2;        
        }

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

        cout << "0=Buy 1=Roll 2=Toggle Freeze 3=Sell 4=Upgrade 5=Hero Power 9=End\n";
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
        else if(cmd == 5){
            if(p.hero->name =="George"){
                // اینجا دارم توانایی های هیرو ها رو ست میکنم 
                // جرج قدرتش اینه سپر الهی بده
                if(p.gold<2){
                    cout<<"Not enough gold to use hero power\n";

                }
                else if(p.board.minions.empty()){
                    cout<<"No minions on board\n";
                }
                else{
                    cout<<"Select minion index to give Divine Shiled: ";
                    int idx;
                    cin>>idx;
                    if(idx>=0 && idx<p.board.minions.size()){
                        p.board.minions[idx]->divineShield = true;
                        p.gold -= 2;
                        cout<<"Divine Shiled grantd to "<<p.board.minions[idx]->name<<endl;

                    }
                    else{
                        cout<<"invalid index\n";
                    }
                }

            }
            else if(p.hero->name == "Reno"){
                // پسرک اینجا دارم قدرت رنو رو تعیین میکنم میتونه یه مینیون رو فقط یکبار طلایی کنه
                if(p.heroPowerUsed){
                    cout<<"Hero power already used\n";

                }
                else if(p.board.minions.empty()){
                    cout<<"No minions on board\n";
                }
                else{
                    cout<<"Select minion index to make Golden: ";
                    int idx;
                    cin >>idx;
                    if(idx>=0 && idx<p.board.minions.size()){
                        Minion *m = p.board.minions[idx];
                        m->attack *=2;
                        m->health *=2;
                        m->name +=" (Golden)";
                        p.heroPowerUsed =true;
                        cout<<m->name<<" is now Golden!\n";
                    }
                    else{
                        cout<<"Invalid index\n";
                    }
                }
            }
            else if(p.hero->name == "Millhouse"){
                // این هیرو قدرت فعال ندارد
                cout << "Millhouse has a passive power; no active hero power to use.\n";
            }
            else{// هیرو های دیگه که بعدا اضافه میکنیم
        cout << "Hero power not implemented for " << p.hero->name << "\n";
                }
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
