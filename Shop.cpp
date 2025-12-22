#include "Shop.h"
#include <iostream>
//توضیحات تک تک کد ها رو توی شاپ دات اچ دادم
// ببین اول کلا شاپ دات اچ بود بعدا اومدم این شاپ دات سی پ پ رو اضافه کردم 
// تلاش بر این بود که بتونم مدل رو از کنترلر جدا کنم چون توی حالت قبلی اینا توی هم بودن

using namespace std;

// پر کردن فروشگاه
void Shop::roll() {
    if (frozen) {
        cout << "Shop is frozen - skipping roll\n";
        return;
    }

    slots.clear();
    vector<Minion*> pool = MinionPool::getByTier(tavernTier);

    for (int i = 0; i < MAX_SLOTS; i++) {
        int r = rand() % pool.size();
        slots.push_back(pool[r]);
    }
}

// نمایش فروشگاه (فعلاً CLI)
void Shop::show() {
    cout << "\n--- TAVERN (Tier " << tavernTier << ") ---\n";
    for (int i = 0; i < slots.size(); i++) {
        cout << i << ") "
             << slots[i]->name << " "
             << slots[i]->attack << "/"
             << slots[i]->health << endl;
    }
    cout << "Frozen: " << (frozen ? "YES" : "NO") << endl;
}

// خرید مینیون
void Shop::buy(Player &p, int index) {

    int cost = BUY_COST;
    if(p.hero->name =="Millhouse"){ // اگر هیرو ما میلهاوز بود یه سکه ارزونتر باهاش تا میکنیم
        cost = BUY_COST -1;
        if(cost <1){
            cost =1;
        }
    }


    if (p.gold < cost) {
        cout << "Not enough gold\n";
        return;
    }

    if (index < 0 || index >= slots.size()) {
        cout << "Invalid slot index\n";
        return;
    }

    if (p.board.minions.size() >= p.board.maxMinions) {
        cout << "Board is full\n";
        return;
    }

    p.gold -= cost;
    p.board.addMinion(slots[index]);
    slots.erase(slots.begin() + index);

    p.checkForTriple();   // پسرک اینو اضافه کردم که حواست باشه و یادت باشه که یه قانون داریم که میتونی توش اگر سه تا از یه مینیون بخری نسخه طلایی اش رو فعال کنی

    cout << "Minion bought\n";
}

// فروش مینیون
void Shop::sell(Player &p, int index) {
    if (index < 0 || index >= p.board.minions.size()) {
        cout << "Invalid minion index\n";
        return;
    }

    delete p.board.minions[index];
    p.board.minions.erase(p.board.minions.begin() + index);
    p.gold += SELL_GAIN;

    cout << "Minion sold (+1 gold)\n";
}

// فریز / آنفریز
void Shop::toggleFreeze(Player &p) {
    if (!frozen && p.gold < FREEZE_COST) {
        cout << "Not enough gold to freeze\n";
        return;
    }

    if (!frozen) {
        p.gold -= FREEZE_COST;
        frozen = true;
        cout << "Shop FROZEN\n";
    } else {
        frozen = false;
        cout << "Shop UNFROZEN\n";
    }
}

// آپگرید Tavern
void Shop::upgrade(Player &p) {
    int cost = tavernTier + 4;

    if(p.hero->name == "Millhouse"){// میلهاوس هزینه کمتری میده
        cost -=2;
        if(cost<1){
            cost =1;
        }
    }
    if (tavernTier >= MAX_TIER) {
        cout << "Max Tier reached\n";
        return;
    }

    if (p.gold < cost) {
        cout << "Not enough gold to upgrade\n";
        return;
    }

    p.gold -= cost;
    tavernTier++;

    cout << "Tavern upgraded to Tier " << tavernTier << endl;
}
