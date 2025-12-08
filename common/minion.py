class Minion:

    def __init__(self,card_id,name,tier,attack,health,tribe=None,keywords=None):
        self.card_id=card_id
        self.name=name
        self.tier=tier
        self.attack=attack
        self.health=health
        self.tribe=tribe
        self.keywords=keywords

        if keywords is None:
            self.keywords = set()
        else:
            self.keywords = set(keywords)
        
        self.is_golden = False   # بعداً برای Triple
        self.dead = False        # بعداً وقتی Health<=0 شد True میشه

    def is_alive(self):

        return self.health >0    

    def take_damage(self,damage):

        self.health-=damage

        if self.health<=0:
            self.dead=True
        
        return self.dead


    def buff(self,attack=0,health=0):
        #تقویت امار کارت
        self.attack+=attack
        self.health+=health

    def add_keyword(self,keyword):

        self.keywords.add(keyword)

    def remove_keyword(self,keyword):

        if keyword in self.keywords:
            self.keywords.remove(keyword)


    #بعدا override میشن

    def on_play(self, game_state):
    
        pass

    def on_deathrattle(self, game_state):

        pass

    def on_start_of_combat(self, game_state):
    
        pass

    def on_end_of_turn(self, game_state):
    
        pass

    def after_attack(self, game_state):

        pass

    def __repr__(self):
        #برای دیباگ راحت تر
        return f"<Minion {self.name} {self.attack}/{self.health} keywords={self.keywords}>"



class BeetleToken(Minion):
    def __init__(self):
        super().__init__(
            card_id="BEETLE_TOKEN",
            name="Beetle",
            tier=1,
            attack=1,
            health=1,
            tribe="Beast",
            keywords=None
        )


class BuzzingVermin(Minion):
    def __init__(self):
        super().__init__(
            card_id="BUZZING_VERMIN",
            name="Buzzing Vermin",
            tier=1,
            attack=2,      # مثال
            health=3,
            tribe="Beast",
            keywords={"Taunt", "Deathrattle"}
        )

    def on_deathrattle(self, game_state):
    
        print("Buzzing Vermin died, summoning a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


