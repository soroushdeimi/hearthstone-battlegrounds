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
// سطح Tier 1  رو داریم اینجا

        if(tier>=1){
            result.push_back(new Minion("Alleycat", 1, 1, 1));
            Minion* scally = new Minion("Scallywag", 1, 2, 1);
            // scally->poisonous = true;      // اینجا مینیون زهر دار و سمی ایجاد کردم
            result.push_back(scally);
            result.push_back(new Minion("Scavenger", 1, 1, 2));
            result.push_back(new Minion("Murloc Scout", 1, 1, 2));
            result.push_back(new Minion("Pterrordax Hatchling", 1, 2, 2));
            result.push_back(new Minion("Righteous Squire", 1, 1, 3)); // تانک کوچک
            result.push_back(new Minion("Rat", 1, 1, 1));
            result.push_back(new Minion("Squirrel", 1, 1, 2));
            result.push_back(new Minion("Fledgling", 1, 2, 1));
            result.push_back(new Minion("Wisp", 1, 1, 1));
        }
        if (tier >= 2) {
            Minion *golem = new Minion("Harvest Golem", 2, 2, 3); // برای مینیون گولم اومدم دف رتل نوشتم
            golem->deathrattle = true;
            result.push_back(golem);
        
           Minion *defender = new Minion("Stonehill Defender", 2, 1, 4);
            defender->taunt = true;
            result.push_back(defender);

            result.push_back(new Minion("River Crocolisk", 2, 2, 4));
            result.push_back(new Minion("Frog Tosser", 2, 3, 2));
            result.push_back(new Minion("Murloc Tidecaller", 2, 2, 2));
            result.push_back(new Minion("Bristleback Protector", 2, 2, 5)); // دفاعی
            result.push_back(new Minion("Harvest Golem (2)", 2, 3, 3));
            result.push_back(new Minion("Reef Walker", 2, 2, 3));
            result.push_back(new Minion("Tavern Guard", 2, 1, 5));
            result.push_back(new Minion("Goblin Tinkerer", 2, 3, 3));

        }

        if (tier >= 3) {
            Minion *bot = new Minion("Deflect-o-Bot", 3, 3, 2); // اینجا اومدم یه مینیون با قابلیت ریبورن ساختم
            bot->reborn =true;
            result.push_back(bot);

            Minion *grizzly = new Minion("Ironfur Grizzly", 3, 3, 5);
            grizzly->taunt = true;
            result.push_back(grizzly);

            Minion *knight = new Minion("Sunborne Knight", 3, 2, 4);
            knight->divineShield = true;
            result.push_back(knight);

            result.push_back(new Minion("Arcane Ooze", 3, 4, 3));
            result.push_back(new Minion("Wispcaller", 3, 2, 4));
            Minion *scarab = new Minion("Scarabsmith", 3, 2, 3);
            scarab->deathrattle = true;
            result.push_back(scarab);
            result.push_back(new Minion("Blade Fencer", 3, 4, 2));
            result.push_back(new Minion("Shieldbearer", 3, 2, 6));
            result.push_back(new Minion("Tidehunter", 3, 3, 4));
            result.push_back(new Minion("Skyhunter", 3, 4, 3));

        }
               if (tier >= 4) {
            Minion *colossus = new Minion("Stone Colossus", 4, 5, 8);
            colossus->taunt = true;
            result.push_back(colossus);

            Minion *phoenix = new Minion("Ashwing Phoenix", 4, 4, 4);
            phoenix->reborn = true;
            result.push_back(phoenix);

            Minion *slayer = new Minion("Iron Slasher", 4, 6, 5);
            result.push_back(slayer);

            Minion *warden = new Minion("Tavern Warden", 4, 3, 7);
            warden->taunt = true;
            result.push_back(warden);

            Minion *saboteur = new Minion("Saboteur", 4, 3, 3);
            saboteur->deathrattle = true;
            result.push_back(saboteur);

            result.push_back(new Minion("Stormcaller", 4, 4, 5));
            result.push_back(new Minion("Night Prowler", 4, 5, 4));
            result.push_back(new Minion("Gargantuan Beetle", 4, 4, 6));
            result.push_back(new Minion("Blightfang", 4, 3, 5));
            result.push_back(new Minion("Arc Warden", 4, 5, 5));
        }

        if (tier >= 5) {
            Minion *titan = new Minion("Tavern Titan", 5, 7, 9);
            titan->taunt = true;
            result.push_back(titan);

            Minion *nemesis = new Minion("Nemesis Hunter", 5, 8, 6);
            result.push_back(nemesis);

            Minion *warden2 = new Minion("Bulwark Sentinel", 5, 4, 10);
            warden2->taunt = true;
            result.push_back(warden2);

            Minion *lich = new Minion("Frost Lich", 5, 6, 7);
            lich->deathrattle = true;
            result.push_back(lich);

            Minion *divine = new Minion("Paladin of the Maw", 5, 5, 8);
            divine->divineShield = true;
            result.push_back(divine);

            result.push_back(new Minion("Rending Beast", 5, 6, 6));
            result.push_back(new Minion("Voidcaller", 5, 7, 5));
            result.push_back(new Minion("Skullcrusher", 5, 8, 6));
            result.push_back(new Minion("Spiritbinder", 5, 4, 9));
            result.push_back(new Minion("Elder Guardian", 5, 3, 12));
        }

        if (tier >= 6) {
            Minion *colossus2 = new Minion("Worldbreaker Colossus", 6, 10, 12);
            colossus2->taunt = true;
            result.push_back(colossus2);

            Minion *reaper = new Minion("Reaper of Realms", 6, 9, 10);
            reaper->deathrattle = true;
            result.push_back(reaper);

            Minion *archon = new Minion("Archon of Light", 6, 6, 14);
            archon->divineShield = true;
            result.push_back(archon);

            Minion *phoenix2 = new Minion("Eternal Phoenix", 6, 8, 8);
            phoenix2->reborn = true;
            result.push_back(phoenix2);

            Minion *titan2 = new Minion("Aegis Titan", 6, 7, 15);
            titan2->taunt = true;
            result.push_back(titan2);

            result.push_back(new Minion("Void Overlord", 6, 12, 9));
            result.push_back(new Minion("Soul Harvester", 6, 9, 12));
            result.push_back(new Minion("Dragonlord", 6, 10, 10));
            result.push_back(new Minion("Ancient Warden", 6, 8, 14));
            result.push_back(new Minion("Obsidian Colossus", 6, 11, 11));
        }


        return result;

    }
};


#endif