#ifndef SHOP_H
#define SHOP_H
#include<vector>
#include<iostream>
#include<cstdlib>
#include<ctime>
#include<chrono>
#include "Player.h"
#include "MinionPool.h"
using namespace std;
using namespace chrono;

class Shop{
public: 
    int tavernTier = 1; //سطح فروشگاه
    bool frozen = false; // بررسی فریز بودن فروشگاه
    vector<Minion*> slots; // نشون میده چه مینیون هایی داخل فروشگاه داریم 
    


    const int MAX_SLOTS = 3; // ماکزیمم میزان خانه های فروشگاه
    const int BUY_COST = 3; // قیمت خرید هر مینیون
    const int SELL_GAIN = 1; // قیمت فروش هر مینیون
    const int MAX_TIER = 6; // ماکزیمم 
    // const int TIMER = 120;       توجه کن پسر - انتقال دادم به کنترلر
    const int FREEZE_COST = 0; // هزینه فریز (در Hearthstone Battlegrounds رایگان است)
    
    // این تابع فروشگاه رو پر میکنه
    void roll();//{
        // if(frozen){
        //     cout << "Shop is frozen - skipping roll\n";
        //     return;
        // }
        // slots.clear();
        // vector<Minion*> pool = MinionPool::getByTier(tavernTier);
        // for(int i = 0; i < MAX_SLOTS; i++){
        //     int r = rand() % pool.size();
        //     slots.push_back(pool[r]);
        // }
    //}
    
    //این تابع برای نمایش هست
    void show();//{           //این موقت اینجاست باید بره توی کنترلر -------------پسر توجه کن رد نشو
        // cout << "\n--- TAVERN (Tier " << tavernTier << ") ---\n";
        // for(int i = 0; i < slots.size(); i++){
        //     cout << i << ") " << slots[i]->name << " " << slots[i]->attack << "/" << slots[i]->health << endl;
        // }
        // cout << "Frozen: " << (frozen ? "YES" : "NO") << endl;
    //}
    
    void buy(Player &p, int index);//{// تابع خرید 
        // if(p.gold < BUY_COST){
        //     cout << "NOT enough gold\n";
        //     return; 
        // }
        // if(index < 0 || index >= slots.size()){
        //     cout << "Invalid slot index\n";
        //     return;
        // }
        // if(p.board.minions.size() >= p.board.maxMinions){
        //     cout << "Board is full\n";
        //     return;
        // }
        // p.gold -= BUY_COST;
        // p.board.addMinion(slots[index]);
        // slots.erase(slots.begin() + index);
        // cout << "Minion bought\n";
    //}
    
    void sell(Player &p, int index);//{
        // if(index < 0 || index >= p.board.minions.size()){
        //     cout << "Invalid minion index\n";
        //     return;
        // }
        // delete p.board.minions[index];
        // p.board.minions.erase(p.board.minions.begin() + index);
        // p.gold += SELL_GAIN;
        // cout << "Minion sold (+1 gold)\n";
   // }
    
    // فریز و آنفریز کردن
    void toggleFreeze(Player &p);//{
        // if(!frozen && p.gold < FREEZE_COST){
        //     cout << "Not enough gold to freeze\n";
        //     return;
        // }
        
        // if(!frozen){
        //     p.gold -= FREEZE_COST;
        //     frozen = true;
        //     cout << "Shop FROZEN\n";
        // } else {
        //     frozen = false;
        //     cout << "Shop UNFROZEN\n";
        // }
    //}
    
    void upgrade(Player &p);//{
        // int cost = tavernTier + 4;
        // if(tavernTier >= MAX_TIER){
        //     cout << "Max Tier reached\n";
        //     return;
        // }
        // if(p.gold < cost){
        //     cout << "Not enough gold to upgrade\n";
        //     return;
        // }
        // p.gold -= cost;
        // tavernTier++;
        // cout << "Tavern upgraded to Tier " << tavernTier << endl;
    //}
    
    // اینجا مهم هست حواستو جمع کن 
    // این همون فاز خرید بازی هست که توی بازی وای میسته که همه خریدارو کنیم این اونجاست
    // void buyPhase(Player &p){.                 اینو میبریم توی کنترلر پیاده میکنیم ----------------توجه کن پسر ---رد نکن توروخدا
    //     roll();
    //     auto start = steady_clock::now();
        
    //     while(true){
    //         auto now = steady_clock::now();
    //         int elapsed = duration_cast<seconds>(now - start).count();
            
    //         if(elapsed >= TIMER){ // اینجا تنظیم کردم که دو دقیقه طول بکشه این فرآیند
    //             cout << "\nTime's Up!\n";
    //             break;
    //         }
            
    //         show();
    //         cout << "\nGold: " << p.gold << " | Time left: " << TIMER - elapsed << "s\n";
    //         cout << "0=Buy 1=Roll 2=Toggle Freeze 3=Sell 4=Upgrade 9=End\n";
    //         cout << "Enter command: ";
            
    //         int cmd;
    //         cin >> cmd;
            
    //         if(cmd == 0){
    //             cout << "Enter slot index: ";
    //             int i;
    //             cin >> i;
    //             buy(p, i);
    //         }
    //         else if(cmd == 1 && p.gold >= 1){
    //             p.gold--;
    //             roll();
    //         }
    //         else if(cmd == 2){
    //             toggleFreeze(p);
    //         }
    //         else if(cmd == 3){
    //             cout << "Enter minion index to sell: ";
    //             int i;
    //             cin >> i;
    //             sell(p, i);
    //         }
    //         else if(cmd == 4){
    //             upgrade(p);
    //         }
    //         else if(cmd == 9){
    //             break;
    //         }
    //         else {
    //             cout << "Invalid command or not enough gold\n";
    //         }
    //     }
        
    //     // بعد از اتمام فاز خرید، اگر frozen نبود، unfreeze میکنیم
    //     if(frozen){
    //         cout << "\nShop will remain frozen for next turn\n";
    //     }
    // }
};

#endif