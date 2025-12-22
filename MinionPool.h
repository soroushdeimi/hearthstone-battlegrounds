#ifndef MINION_POOL_H
#define MINION_POOL_H
// اینها به عنوان مثال اومدم یسری مینیون خیالی دادم
// برای بازی اصلی میتوان هر چقدر که میخوام مینیون اضافه کنم و توی این موردی نیست


#include<vector>
#include"minion.h"
#include<memory>

using namespace std;

class MinionPool{

    public:
    static vector<Minion*> getByTier(int tier){

        vector <Minion*> result;

        if(tier>=1){
            result.push_back(new Minion("Alleycat", 1, 1, 1));
            Minion* scally = new Minion("Scallywag", 1, 2, 1);
            scally->poisonous = true;      // اینجا مینیون زهر دار و سمی ایجاد کردم
            result.push_back(scally);
        }
        if (tier >= 2) {
            Minion *golem = new Minion("Harvest Golem", 2, 2, 3); // برای مینیون گولم اومدم دف رتل نوشتم
            golem->deathrattle = true;
            result.push_back(golem);
        }

        if (tier >= 3) {
            result.push_back(new Minion("Deflect-o-Bot", 3, 3, 2));
        }

        return result;

    }
};


#endif