#ifndef HERO_POOL_H
#define HERO_POOL_H

#include<vector>
#include "Hero.h"
// اینجا هیرو های مختلف حضور دارن که باید بینشون کاربر ها انتخاب کنن
// خاطرت باشه هر هیرو قدرت جداگانه باید میداشت که جلوشون پیشنهادات رو نوشتم
class HeroPool{
    public: 

    // این تابعی که نوشتم لیستی از هیرو های در دسترس رو بر میگردونه
    static std::vector<Hero*> getHeroes(){

        std::vector<Hero*> heroes;

        heroes.push_back(new Hero("Sylvanas")); // سیلواناس برای مثال میتونه آمار دائمی مینیون های مرده رو افزایش بده
        heroes.push_back(new Hero("Millhouse")); //مثلا قیمت این میتونه کمتر باشه برای افزایش تاورن
        heroes.push_back(new Hero("George")); // میتونه دیواین شیلد اعطا کنه
        heroes.push_back(new Hero("Reno"));// میتونه مثلا یه مینیون رو طلایی کنه
        return heroes;
    }

};



#endif