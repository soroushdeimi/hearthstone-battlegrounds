#include "GameController.h"
#include "Combat.h"
#include <iostream>
#include <chrono>
#include<random>
#include<thread>// ترد ایجاد شده حواست باشه
#include "Action.h"
using namespace std;
using namespace chrono;



#include <thread>

GameController::GameController()
  : seed(static_cast<uint32_t>(std::chrono::steady_clock::now().time_since_epoch().count() & 0xffffffff)),
    rng(seed)
{
    // nada
}


void GameController::run(GameState &state){// تابع اجرایی بسیار مهم حتما تسلط روی کار با این رو داشته باش
cout << "Match seed: " << seed << endl;

    while(true){
        // ------پسرک حتما توجه کن به اینجا
        //فاز خرید بازی
        state.phase = Phase::Buy;
        cout<<"\n-=-=-Round "<<state.round<<" | BUY PHASE -=-=\n";
        
        for (int i = 0; i < (int)state.players.size(); ++i) {
            cout << "\n---" << state.players[i]->name << " TURN --(Health: " << state.players[i]->hero->health << ")\n";
            buyPhase(state, i);
            
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

//برای فاز سرور ما بعدها seed را از سرور برمی‌داریم (در پیام combat_start)، ولی برای تست محلی فعلاً یک seed بر اساس زمان ایجاد می‌کنیم و آن را چاپ می‌کنیم تا هر زمان خواستیم یک seed خاص را جایگزین کنیم و replay بگیریم
    cout<<"\n"<<A->name<<" VS "<<B->name<<endl;
    uint32_t combat_seed = rng(); // یک عدد 32 بیتی از RNG مرکزی
    std::mt19937 combat_rng(combat_seed);
    cout << "Combat seed: " << combat_seed << endl;
    Combat::fight(*A, *B, combat_rng);


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
           // اینجا دارم برد رو پاک میکنم
            A->board.clear();
            B->board.clear();


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
            A->board.clear();// بازم دارم برد پاک میکنم
            B->board.clear();
        if(A->hero->health<=0){
            cout<<A->name<<" has been eliminated! \n";


            state.players.erase(state.players.begin()+i);
            state.shops.erase(state.shops.begin()+i);

        }

        else{
            i+=2;

        }

        }

        else{
            cout << "It's a draw. No damage dealt.\n";

            // آخرین باری که برد پاک میکنم
            A->board.clear();
            B->board.clear();
            i += 2;        
        }

}

}








#include <thread> // اگر قبلاً نبود
// ... سایر includes (Action.h هم لازم است)
#include "Action.h"

void GameController::buyPhase(GameState &state, int playerIndex) {
    Player &p = *state.players[playerIndex];
    Shop &shop = *state.shops[playerIndex];

    // roll اولیه
    shop.roll(rng);
    auto start = steady_clock::now();
    const int TIMER = 120;

    while (true) {
        auto now = steady_clock::now();
        int elapsed = duration_cast<seconds>(now - start).count();

        if (elapsed >= TIMER) {
            cout << "\nTime's Up!\n";
            break;
        }

        // نمایش فروشگاه (برای debug / client-side احتمالی)
        shop.show();
        cout << "\nGold: " << p.gold << " | Time left: " << (TIMER - elapsed) << "s\n";

        //  تلاش برای گرفتن یک اکشن از صف به صورت thread-safe ---
        Action act;
        bool gotAction = false;

        {   // scope lock
            std::unique_lock<std::mutex> lk(state.actionMutex);
            // اگر صف خالیه، تا یک بازه کوتاه یا تا زمان کلی timeout صبر کن
            if (state.pendingActions[playerIndex].empty()) {
                // محاسبه زمان باقیمانده و حداقل یک interval منتظر شدن
                int remaining_ms = (TIMER - elapsed) * 1000;
                int wait_ms = std::min(remaining_ms, 500); // تا 500ms هر بار بیدار میشیم
                if (wait_ms <= 0) {
                    // اگر وقتی نمونده، شکسته و پایان بدیم
                    break;
                }
                state.actionCv.wait_for(lk, std::chrono::milliseconds(wait_ms), [&state, playerIndex](){
                    return !state.pendingActions[playerIndex].empty();
                });
            }

            // پس از بیداری، چک کن اگر اکشن هست آن را بگیر
            if (!state.pendingActions[playerIndex].empty()) {
                act = state.pendingActions[playerIndex].front();
                state.pendingActions[playerIndex].erase(state.pendingActions[playerIndex].begin());
                gotAction = true;
            }
        } // unlock mutex

        if (!gotAction) {
            // هیچ اکششنی در بازهٔ منتظر وجود نداشت — loop را ادامه می‌دهیم تا timer بررسی شود
            continue;
        }

        // --- حالا act را پردازش کن ---
        if (act.type == ActionType::Buy) {
            shop.buy(p, act.slotIndex);
            // بعد از خرید، بررسی triple
            int discoverTier = p.checkForTriple();
            if (discoverTier > 0) {
                // آماده‌سازی گزینه‌ها
                {
                    std::lock_guard<std::mutex> lg(state.actionMutex);
                    state.discoverOffers[playerIndex] = p.getDiscoverOptions(discoverTier);
                    state.discoverPending[playerIndex] = true;
                }
                cout << "Discover offered to player " << playerIndex << " (options: " << state.discoverOffers[playerIndex].size() << ")\n";

                // منتظر DiscoverChoice
                while (true) {
                    Action a2;
                    bool got = false;
                    {
                        std::unique_lock<std::mutex> lk(state.actionMutex);
                        state.actionCv.wait(lk, [&state, playerIndex](){
                            return !state.pendingActions[playerIndex].empty();
                        });
                        if (!state.pendingActions[playerIndex].empty()) {
                            a2 = state.pendingActions[playerIndex].front();
                            state.pendingActions[playerIndex].erase(state.pendingActions[playerIndex].begin());
                            got = true;
                        }
                    }

                    if (!got) continue;

                    if (a2.type == ActionType::DiscoverChoice) {
                        int choice = a2.choice;
                        auto &opts = state.discoverOffers[playerIndex];
                        if (choice < 0 || choice >= (int)opts.size()) choice = 0;
                        p.board.addMinion(opts[choice]);
                        // پاک کردن بقیه‌ی گزینه‌ها
                        for (int k = 0; k < (int)opts.size(); ++k) {
                            if (k != choice) delete opts[k];
                        }
                        opts.clear();
                        {
                            std::lock_guard<std::mutex> lg(state.actionMutex);
                            state.discoverPending[playerIndex] = false;
                        }
                        break;
                    } else {
                        // اگر اکشن غیر discover آمد، می‌توانیم آن را یا اجرا کنیم یا push back کنیم.
                        // راحت‌ترین کار این است که آن را push_back کنیم تا بعداً پردازش شود:
                        {
                            std::lock_guard<std::mutex> lg(state.actionMutex);
                            state.pendingActions[playerIndex].push_back(a2);
                        }
                        // کمی صبر کن و دوباره loop
                    }
                } // end waiting for discover
            } // end if discoverTier > 0
        } // end Buy

        else if (act.type == ActionType::Roll) {
            if (p.gold >= 1) {
                p.gold--;
                shop.roll(rng);
            } else {
                cout << "Not enough gold to roll\n";
            }
        }
        else if (act.type == ActionType::ToggleFreeze) {
            shop.toggleFreeze(p);
        }
        else if (act.type == ActionType::Sell) {
            shop.sell(p, act.slotIndex);
        }
        else if (act.type == ActionType::Upgrade) {
            shop.upgrade(p);
        }
        else if (act.type == ActionType::HeroPower) {


            if (p.hero->name == "George") {// پسرک حواست باشه اینجا هیرو پاور ها رو پیاده کردی
                int idx = act.slotIndex;
                if (p.gold < 2) {//قدرت جورج
                    cout << "Not enough gold to use hero power\n";
                } else if (p.board.minions.empty()) {
                    cout << "No minions on board\n";
                } else if (idx >= 0 && idx < (int)p.board.minions.size()) {
                    p.board.minions[idx]->divineShield = true;
                    p.gold -= 2;
                    cout << "Divine Shield granted to " << p.board.minions[idx]->name << endl;
                }
            } else if (p.hero->name == "Reno") {// قدرت رنو
                int idx = act.slotIndex;
                if (p.heroPowerUsed) cout << "Hero power already used\n";
                else if (p.board.minions.empty()) cout << "No minions on board\n";
                else if (idx >= 0 && idx < (int)p.board.minions.size()) {
                    Minion *m = p.board.minions[idx];
                    m->attack *= 2;
                    m->health *= 2;
                    m->name += " (Golden)";
                    p.heroPowerUsed = true;
                    cout << m->name << " is now Golden!\n";
                }
            } else if (p.hero->name == "Sylvanas") {// قدرت سیلواناس
                int idx = act.slotIndex;
                if (p.gold < 1) cout << "Not enough gold to use hero power\n";
                else if (p.board.minions.empty()) cout << "No minions on the board\n";
                else if (idx >= 0 && idx < (int)p.board.minions.size()) {
                    Minion *m = p.board.minions[idx];
                    m->attack += 1;
                    m->health += 1;
                    p.gold -= 1;
                    cout << m->name << " now has " << m->attack << "/" << m->health << endl;
                }
            } else {
                cout << "Hero power not implemented for " << p.hero->name << "\n";
            }
        }
        else if (act.type == ActionType::EndTurn) {
            break;
        }
    } // end while(timer)

    if (shop.frozen) {
        cout << "\nShop will remain frozen for next turn\n";
    }
}










// void GameController::buyPhase(GameState &state, int playerIndex) {
//     Player &p = *state.players[playerIndex];
//     Shop &shop = *state.shops[playerIndex];

//     // roll اولیه
//     shop.roll(rng);
//     auto start = steady_clock::now();
//     const int TIMER = 120;

//     while (true) {
//         auto now = steady_clock::now();
//         int elapsed = duration_cast<seconds>(now - start).count();

//         if (elapsed >= TIMER) {
//             cout << "\nTime's Up!\n";
//             break;
//         }

//         // نمایش فروشگاه
//         shop.show();
//         cout << "\nGold: " << p.gold << " | Time left: " << (TIMER - elapsed) << "s\n";

//         // اگر اکشن در صف وجود داشت، آن را پردازش کن
//         if (!state.pendingActions[playerIndex].empty()) {
//             Action act = state.pendingActions[playerIndex].front();
//             // pop_front-like:
//             state.pendingActions[playerIndex].erase(state.pendingActions[playerIndex].begin());

//             if (act.type == ActionType::Buy) {
//                 shop.buy(p, act.slotIndex);
//                 // بعد از خرید، بررسی triple
//                 int discoverTier = p.checkForTriple();
//                 if (discoverTier > 0) {
//                     // آماده‌سازی گزینه‌ها
//                     state.discoverOffers[playerIndex] = p.getDiscoverOptions(discoverTier);
//                     state.discoverPending[playerIndex] = true;

//                     cout << "Discover offered to player " << playerIndex << " (options: " << state.discoverOffers[playerIndex].size() << ")\n";
//                     // منتظر انتخاب discover_choice از صف باش
//                     while (state.discoverPending[playerIndex]) {
//                         if (!state.pendingActions[playerIndex].empty()) {
//                             Action a2 = state.pendingActions[playerIndex].front();
//                             state.pendingActions[playerIndex].erase(state.pendingActions[playerIndex].begin());
//                             if (a2.type == ActionType::DiscoverChoice) {
//                                 int choice = a2.choice;
//                                 auto &opts = state.discoverOffers[playerIndex];
//                                 if (choice < 0 || choice >= (int)opts.size()) choice = 0;
//                                 p.board.addMinion(opts[choice]);
//                                 // پاک کردن بقیه‌ی گزینه‌ها
//                                 for (int k = 0; k < (int)opts.size(); ++k) {
//                                     if (k != choice) delete opts[k];
//                                 }
//                                 opts.clear();
//                                 state.discoverPending[playerIndex] = false;
//                                 break;
//                             } else {
//                                 // اگر اکشن غیر discover آمد، به انتها منتقلش کن (تا بعداً پردازش شود)
//                                 state.pendingActions[playerIndex].push_back(a2);
//                             }
//                         } else {
//                             std::this_thread::sleep_for(std::chrono::milliseconds(50));
//                         }
//                     } // while waiting discover
//                 } // if discoverTier>0
//             } // if Buy

//             else if (act.type == ActionType::Roll) {
//                 if (p.gold >= 1) {
//                     p.gold--;
//                     shop.roll(rng);
//                 } else {
//                     cout << "Not enough gold to roll\n";
//                 }
//             }
//             else if (act.type == ActionType::ToggleFreeze) {
//                 shop.toggleFreeze(p);
//             }
//             else if (act.type == ActionType::Sell) {
//                 shop.sell(p, act.slotIndex);
//             }
//             else if (act.type == ActionType::Upgrade) {
//                 shop.upgrade(p);
//             }
//             else if (act.type == ActionType::HeroPower) {
//                 // استفاده از hero power با act.slotIndex به عنوان هدف
//                 if (p.hero->name == "George") {
//                     int idx = act.slotIndex;
//                     if (p.gold < 2) {
//                         cout << "Not enough gold to use hero power\n";
//                     } else if (p.board.minions.empty()) {
//                         cout << "No minions on board\n";
//                     } else if (idx >= 0 && idx < (int)p.board.minions.size()) {
//                         p.board.minions[idx]->divineShield = true;
//                         p.gold -= 2;
//                         cout << "Divine Shield granted to " << p.board.minions[idx]->name << endl;
//                     }
//                 } else if (p.hero->name == "Reno") {
//                     int idx = act.slotIndex;
//                     if (p.heroPowerUsed) cout << "Hero power already used\n";
//                     else if (p.board.minions.empty()) cout << "No minions on board\n";
//                     else if (idx >= 0 && idx < (int)p.board.minions.size()) {
//                         Minion *m = p.board.minions[idx];
//                         m->attack *= 2;
//                         m->health *= 2;
//                         m->name += " (Golden)";
//                         p.heroPowerUsed = true;
//                         cout << m->name << " is now Golden!\n";
//                     }
//                 } else if (p.hero->name == "Sylvanas") {
//                     int idx = act.slotIndex;
//                     if (p.gold < 1) cout << "Not enough gold to use hero power\n";
//                     else if (p.board.minions.empty()) cout << "No minions on the board\n";
//                     else if (idx >= 0 && idx < (int)p.board.minions.size()) {
//                         Minion *m = p.board.minions[idx];
//                         m->attack += 1;
//                         m->health += 1;
//                         p.gold -= 1;
//                         cout << m->name << " now has " << m->attack << "/" << m->health << endl;
//                     }
//                 } else {
//                     cout << "Hero power not implemented for " << p.hero->name << "\n";
//                 }
//             }
//             else if (act.type == ActionType::EndTurn) {
//                 break;
//             }
//         }
//         else {
//             // fallback تعاملی (CLI) — فقط برای تسهیلات تستِ محلی
//             cout << "0=Buy 1=Roll 2=Toggle Freeze 3=Sell 4=Upgrade 5=Hero Power 9=End\n";
//             cout << "Enter command: ";
//             int cmd;
//             if(!(cin >> cmd)){
//                 // اگر ورودی معتبر نبود، صبر کن و ادامه بده
//                 cin.clear();
//                 std::this_thread::sleep_for(std::chrono::milliseconds(100));
//                 continue;
//             }
//             if (cmd == 0) {
//                 cout << "Enter slot index: ";
//                 int i; cin >> i;
//                 shop.buy(p, i);
//                 int discoverTier = p.checkForTriple();
//                 if (discoverTier > 0) {
//                     state.discoverOffers[playerIndex] = p.getDiscoverOptions(discoverTier);
//                     state.discoverPending[playerIndex] = true;
//                     cout << "Choose discover option: \n";
//                     for (int j=0;j<(int)state.discoverOffers[playerIndex].size();++j){
//                         cout << j << ") " << state.discoverOffers[playerIndex][j]->name << "\n";
//                     }
//                     int choice; cin >> choice;
//                     if(choice<0 || choice >= (int)state.discoverOffers[playerIndex].size()) choice = 0;
//                     p.board.addMinion(state.discoverOffers[playerIndex][choice]);
//                     // پاک کردن بقیه
//                     for (int k=0;k<(int)state.discoverOffers[playerIndex].size();++k){
//                         if(k!=choice) delete state.discoverOffers[playerIndex][k];
//                     }
//                     state.discoverOffers[playerIndex].clear();
//                     state.discoverPending[playerIndex]=false;
//                 }
//             }
//             else if (cmd == 1 && p.gold >= 1) {
//                 p.gold--;
//                 shop.roll(rng);
//             }
//             else if (cmd == 2) {
//                 shop.toggleFreeze(p);
//             }
//             else if (cmd == 3) {
//                 cout << "Enter minion index to sell: ";
//                 int i; cin >> i;
//                 shop.sell(p, i);
//             }
//             else if (cmd == 4) {
//                 shop.upgrade(p);
//             }
//             else if (cmd == 5) {
//                 // hero power interactive (همان کد قبلی ولی بدون تغییر)
//                 // ... (می‌توانی کد قبلی را همینجا بگذاری؛ برای خلاصه از آن استفاده شد)
//                 cout << "Interactive hero power not shown here for brevity.\n";
//             }
//             else if (cmd == 9) {
//                 break;
//             }
//             else {
//                 cout << "Invalid command or not enough gold\n";
//             }
//         } // end else (no pendingActions)

//         // جلوگیری از busy loop سنگین
//         std::this_thread::sleep_for(std::chrono::milliseconds(20));
//     } // end while(timer)
//     if (shop.frozen) {
//         cout << "\nShop will remain frozen for next turn\n";
//     }
// }

