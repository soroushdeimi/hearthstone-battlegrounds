#ifndef GAME_STATE_H
#define GAME_STATE_H


#include<vector>
#include"Player.h"
#include"Shop.h"
#include "Action.h"

#include<mutex>
#include<condition_variable>

// اینجا داریم فاز های بازی رو مشخص میکنیم - تیکه بانمک
enum class Phase{
    Buy,
    Combat
};


class GameState{
    public:
        int round =1;
        Phase phase = Phase::Buy;

        vector<Player*> players;
        vector<Shop*> shops;

        // پسرک اینجا داریم یه صف اکشن درست میکنیم برای هر بازیکن - سرور کلاینت میتواند پوش کنند
        std::vector<std::vector<Action>> pendingActions; // این صف اکسن ها برای هر بازیکن هست


                // Discover offers: برای هر بازیکن یک لیست از Minion* گزینه‌ها که وقتی discover رخ دهد پر می‌شود
       
        std::vector<std::vector<Minion*>> discoverOffers;
        std::vector<bool> discoverPending;


//        // synchronization for pendingActions/discoverOffers
        std::mutex actionMutex;
        std::condition_variable actionCv;
        
                GameState(); // اینم از کانستراکتورش


                void pushAction(int playerIndex , const Action &a);// پسرگ اینجا دارم زور میزنم thread-safe access درست کنم
                bool popAction(int playerIndex , Action &out);// ترو بر میگردونه اگر پاپ شد
};



#endif