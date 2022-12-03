import pyxel

class Actor:
    def __init__(self, e_x, e_y):
        self.posx = e_x
        self.posy = e_y
        
    def update(self):
        pass

    def draw(self):
        pass

class KEY:
    def __init__(self):
        self.flag = 0

    def button(self, key):
        if pyxel.btnp(key):
            self.flag = 1
        if pyxel.btnr(key):
            self.flag = 0

        return self.flag

class Player(Actor):
    def __init__(self, app):
        self.app = app
        self.pl_x = (app.screen.right + app.screen.left) // 2
        self.pl_y = app.screen.bottom - 10
        self.pl_speed = 3
        self.pl_hp = 10
        self.pl_radius = 5
        self.shot_maneger = Player_Shot_Manager(app)

    def shot(self):
        self.shot_maneger.spawn_shot(self.pl_x, self.pl_y, -90, 5, 0)
        pass

    
    def update(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            self.shot()
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.pl_x = min(self.pl_x + self.pl_speed, self.app.screen.right)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.pl_x = max(self.pl_x - self.pl_speed, self.app.screen.left)
        if pyxel.btn(pyxel.KEY_UP):
            self.pl_y = max(self.pl_y - self.pl_speed, self.app.screen.top)
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.pl_y = min(self.pl_y + self.pl_speed, self.app.screen.bottom)


    def draw(self):
        pyxel.circ(self.pl_x, self.pl_y, self.pl_radius, 0)

class Player_Shot_Manager:
    def __init__(self, app):
        self.app = app

    def spawn_shot(self, pox, poy, angle, speed, mode):
        self.app.attacks.append(Player_Attack(pox, poy, angle, speed, 3))
    

class Attack_Base:
    def __init__(self, a_x, a_y, angle, speed, radius, col):
        self.a_x = a_x
        self.a_y = a_y
        self.angle = angle
        self.a_vx = pyxel.cos(self.angle)
        self.a_vy = pyxel.sin(self.angle)
        self.a_speed = speed
        self.a_radius = radius
        self.a_color = col
        #print(f"{self.a_vx, self.a_vy}")

    def update(self):
        self.a_x += self.a_vx * float(self.a_speed)
        self.a_y += self.a_vy * float(self.a_speed)

    def draw(self):
        #print("Attack_Base_draw")
        pyxel.circ(self.a_x, self.a_y, self.a_radius, self.a_color)


class Player_Attack(Attack_Base):
    def __init__(self, a_x, a_y, angle, speed, radius):
        super().__init__(a_x, a_y, angle, speed, radius, 1)

class Player_Attack_ver1(Player_Attack):
    def __init__(self):
        self.a1_speed = -10
        self.a1_color = 14
        super().positon()

class Enemy:
    def __init__(self, app):
        self.app = app
        self.en_hp = 1000
        self.en_x = pyxel.rndi(10, 790)
        self.en_y = 100
        self.ea_attack_area = 200
        self.en_radius = 10

    def update(self):
        if self.app.player.pl_x - self.ea_attack_area <= self.app.screen.left:
            self.ea_x = pyxel.rndi(self.app.screen.left, self.app.player.pl_x + self.ea_attack_area)
        elif self.app.player.pl_x + self.ea_attack_area <= self.app.screen.right:
            self.ea_x = pyxel.rndi(self.app.player.pl_x - self.ea_attack_area, self.app.player.pl_x + self.ea_attack_area)
        else:
            self.ea_x = pyxel.rndi(self.app.player.pl_x - self.ea_attack_area, self.app.screen.right)
        #if  pyxel.frame_count % 60 == 0:
        #    self.app.enemy_attacks.append(Enemy_attack(self.ea_x, self.en_y, 90, 3, 8))
        self.app.enemy_attacks.append(Enemy_attack(self.ea_x, self.en_y, 90, 3, 8))
        pass

    def draw(self):
        pyxel.circ(self.en_x, self.en_y, self.en_radius, 0)
        pass

class Enemy_attack(Attack_Base):
    def __init__(self, a_x, a_y, angle, speed, radius):
        super().__init__(a_x, a_y, angle, speed, radius, 8)
        

class Game_Screen:
    def __init__(self):
        self.top = 100
        self.bottom = 700
        self.left = 100
        self.right = 700
    
    def contain(self, is_x, is_y):
        return is_y <= self.bottom and is_y >= self.top and is_x <= self.right and is_x >= self.left

class App: 
    def __init__(self):
        pyxel.init(1200,800)
        self.screen = Game_Screen()
        self.key = KEY()
        self.player = Player(self)
        self.enemies = [Enemy(self)]
        self.attacks = []
        self.enemy_attacks =[]
        self.gamestatus = 0
        pyxel.run(self.update, self.draw)

    #def make_attacks(self):
    #    attack = Player_Attack_ver1()
    #    self.attacks.append(attack)

    def update(self):
        #global player, attacks, enemy, enemy_attacks, gamestatus, screen

        if self.player.pl_hp <= 0:
            self.gamestatus = 1
            return
        #elif self.enemy.en_hp <= 0:
        #    self.gamestatus = 2
        #    return
        else:
            #self.enemy_attacks.append(Enemy_attack())
            self.player.update()

            for enemy in self.enemies:
                enemy.update()

            #for atk in self.attacks:
            #    if not self.screen.contain(atk.a_x, atk.a_y):
            #        self.attacks.remove(atk)            

            for atk in self.attacks:
                atk.update()

            self.attacks = list(filter(lambda atk: self.screen.contain(atk.a_x, atk.a_y) , self.attacks))

            for eatk in self.enemy_attacks:
                eatk.update()

            def enemy_attacks_filter(eatk):
                if not self.screen.contain(eatk.a_x, eatk.a_y):
                    return False
                if ((eatk.a_x - self.player.pl_x) ** 2 + (eatk.a_y - self.player.pl_y) ** 2) ** (1/2) <= eatk.a_radius:
                    self.player.pl_hp -= 1
                    return False
                #特定のアイテムを取ることで、敵の攻撃が栄養（HP回復）になる。

                return True
            self.enemy_attacks = list(filter(enemy_attacks_filter, self.enemy_attacks))
            # self.enemy_attacks = list(filter(lambda eatk: self.screen.contain(eatk.a_x, eatk.a_y) , self.enemy_attacks))



            #i = 0
            #while i < len(self.attacks):
            #    print(i)
            #    atk = self.attacks[i]
            #    atk.update()
            #    if not self.screen.contain(atk.a_x, atk.a_y):
            #        self.attacks.remove(atk)
            #        i -= 1
            #    else:
            #        i += 1

                #atk.po_y += atk.a1_speed
                #if atk.po_y <= self.screen.top:
                #    self.attacks.remove(atk)
            
            #for eatk in enemy_attacks:
            #    eatk.ea_y += eatk.ea_speed
            #    if eatk.ea_y + eatk.ea_diameter >= self.player.pl_y - self.player.pl_diameter and eatk.ea_y - eatk.ea_diameter <= self.player.pl_y + self.player.pl_diameter:
            #        if eatk.ea_x - eatk.ea_diameter <= self.player.pl_x + self.player.pl_diameter and eatk.ea_x + eatk.ea_diameter >= self.player.pl_x - self.player.pl_diameter:
            #          self.player.pl_hp -= 1
            #          self.enemy_attacks.remove(eatk)
            #    elif eatk.ea_y > self.screen.bottom + eatk.ea_diameter + self.player.pl_diameter:
            #        self.enemy_attacks.remove(eatk) 


    def draw(self):
        #global player, attacks, enemy, gamestatus, screen
        pyxel.cls(7)
        if self.gamestatus == 1:
            pyxel.text(self.screen.right + 100, self.screen.top + 40, "GameOver",0)
        elif self.gamestatus == 2:
            pyxel.text(self.screen.right + 100, self.screen.top + 40, "GameClear",0)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
            pyxel.text(self.screen.right + 100, self.screen.top, f"EnemyHP:{enemy.en_hp}", 0)
        pyxel.rectb(self.screen.left, self.screen.top, self.screen.right - self.screen.left, self.screen.bottom - self.screen.top, 0)
        pyxel.text((self.screen.left + self.screen.right)/2, self.screen.top - 50, "Enemy", 0)
        pyxel.text((self.screen.left + self.screen.right)/2, self.screen.bottom + 50, "Player", 0)      
        pyxel.text(self.screen.right + 100, self.screen.top + 20, f"PlayerHP:{self.player.pl_hp}", 0)
        for atk in self.attacks:
            atk.draw()
        for eatk in self.enemy_attacks:
            eatk.draw()

App()