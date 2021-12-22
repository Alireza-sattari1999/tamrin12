import math
import random
import arcade
from arcade.sprite_list.spatial_hash import check_for_collision
import time
from arcade.key import END

S_W=900

S_H=700


######ship######
class ship(arcade.Sprite):

    def __init__(self):

       super().__init__(':resources:images/space_shooter/playerShip1_blue.png')

       self.center_x = S_W // 2

       self.center_y = 32

       self.width = 40

       self.height = 18

       self.angle = 0

       self.change_angle = 0

       self.speed = 6

       self.change_x = 0

       self.change_y = 0

       self.tir_list = []

       self.score = 0

       self.health = 3
     
       
    def charkhesh(self):

        self.angle += self.change_angle * self.speed
    def harkat(self):

        self.center_x += self.change_x * self.speed

        self.center_y += self.change_y * self.speed

    def fire(self):

       self.tir_list.append(Tir(self))


       arcade.play_sound(arcade.sound.Sound(':resources:sounds/upgrade2.wav'))
    

#########doshman#######
class Doshman(arcade.Sprite):

    def __init__(self,s):

       super().__init__(':resources:images/space_shooter/playerShip1_green.png')

       self.center_x = random.randint(0,S_W)

       self.center_y = S_H + 2

       self.speed = s

       self.angle = 180

       self.width = 50

       self.height = 40
       
    def harkat(self):

        self.center_y -= self.speed 


#########tir########
class Tir(arcade.Sprite):

     def __init__(self,host):

       super().__init__(':resources:images/space_shooter/laserRed01.png')

       self.center_x = host.center_x

       self.center_y = host.center_y

       self.speed = 7

       self.angle = host.angle
      

     def harkat(self):

        i = math.radians(self.angle)

        self.center_x -= self.speed * math.sin(i)

        self.center_y += self.speed * math.cos(i)

#######bazi#######
class Bazi(arcade.Window):

    def __init__(self):

        super().__init__(S_W , S_H , 'welcome to airplane Game!')

        arcade.set_background_color(arcade.color.BLUE)

        self.background_image=arcade.load_texture(':resources:images/backgrounds/stars.png')

        self.me=ship()

        self.doshman_list = []
        
        self.num_doshman = 0

        self.start_time = time.time()

    def on_draw(self):

        arcade.start_render()

        if self.me.health <= 0:

            arcade.set_background_color(arcade.color.BLUE)

            arcade.draw_text('Game Over!',350,S_H//2,arcade.color.PURPLE,30)
        else:
            arcade.draw_lrwh_rectangle_textured(0,0,S_W,S_H,self.background_image)

            self.me.draw()
        for tir in self.me.tir_list:
    
                tir.draw()

        for doshman in self.doshman_list:
            doshman.draw()

        for health in range(self.me.health):

            health_image = arcade.load_texture('health.png')
            arcade.draw_lrwh_rectangle_textured(5 + health * 21 , 12 , 22 , 22 , health_image)

        arcade.draw_text(f'Score= {self.me.score}',790, 18 , arcade.color.BLACK , 18)

        
       
    
    def on_update(self, delta_time):

        self.end_time = time.time()

        time_doshman = random.randrange(2,8,2)

        if self.end_time - self.start_time >= time_doshman:

          self.num_doshman += 1
        
          self.doshman_list.append(Doshman(3 + self.num_doshman//10))

          self.start_time = time.time()

        self.me.harkat()

        self.me.charkhesh()
        
        for tir in self.me.tir_list:

            tir.harkat()

        for doshman in self.doshman_list:

            doshman.harkat()


        for doshman in self.doshman_list:

            for tir in self.me.tir_list:

                if check_for_collision(doshman , tir):

                    arcade.play_sound(arcade.sound.Sound(':resources:sounds/explosion2.wav'))

                    self.me.tir_list.remove(tir)

                    self.doshman_list.remove(doshman)

                    self.me.score += 1

        for tir in self.me.tir_list:
    
            if tir.center_y >= S_H or S_W <= tir.center_x <=0 or tir.center_y <= 0:
                
                self.me.tir_list.remove(tir)

        for doshman in self.doshman_list:

            if doshman.center_y <= 0:

                self.doshman_list.remove(doshman)

                self.me.health -= 1

        
########key#########
    def on_key_press(self, key, modifiers: int):

        if key == arcade.key.DOWN:

            self.me.change_y = -1

        elif key == arcade.key.UP:

            self.me.change_y = 1

        elif key == arcade.key.RIGHT:

            self.me.change_x = +1

        elif key == arcade.key.LEFT:

            self.me.change_x = -1

        if key == arcade.key.D:

            self.me.change_angle = -1

        if key == arcade.key.A:

            self.me.change_angle = 1
        
        elif key == arcade.key.SPACE:
            self.me.fire()   

    def on_key_release(self, symbol: int, modifiers: int):

        return super().on_key_release(symbol, modifiers)

    def on_key_release(self, key, modifiers: int):

        self.me.change_angle = 0

        self.me.change_x = 0

        self.me.change_y = 0


game=Bazi()

arcade.run()
######End######