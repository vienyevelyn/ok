from pygame import *

window = display.set_mode((700, 500)) #lebar, tinggi
back = (119, 210, 223) #rgb
display.set_caption("Maze")

class character(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect() 
        self.rect.x =player_x
        self.rect.y =player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class player(character):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        character.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    
    def update(self):
        #gerakan horizontal(kiri atau kanan)
        if pemain.rect.x <= 700 - 80 and pemain.x_speed > 0 or pemain.rect.x >= 0 and pemain.x_speed < 0:
            self.rect.x += self.x_speed

        #biar nggak bentrok dinding maze
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: #pergi ke sebelah kanan
            for p in platform_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platform_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        #gerakan vertical (atas dan bawah)
        if pemain.rect.y <= 500 - 80 and pemain.y_speed > 0 or pemain.rect.y >= 0 and pemain.y_speed < 0:
            self.rect.y += self.y_speed
            platform_touched = sprite.spritecollide(self, barriers, False)

        if self.y_speed > 0: #pergi ke sebelah bawah
            for p in platform_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)

        elif self.y_speed < 0: #atas
            for p in platform_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class enemy(character):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        character.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= 700 - 85:
            self.side = "left"

        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(character):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        character.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 700 + 10:
            self.kill()


barriers = sprite.Group()

bullets = sprite.Group()

monsters = sprite.Group()

pemain = player("player.png", 5, 500 - 80, 80, 80, 0, 0)
w1 = character('w1.png',500 / 2 - 500 / 3, 700 / 2, 500, 50)
w2 = character('w2.png', 370, 100, 50, 350)

monster = enemy("enemy.png", 700 - 80, 180, 80, 80, 5)
treasure = character("treasure.png", 700 - 85, 500 - 100, 80, 80)

monsters.add(monster)

barriers.add(w1)
barriers.add(w2)

finish = False
run = True
while run:
    time.delay(50) #mili seoncd, 0.05 sec
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                pemain.x_speed = -5
            elif e.key == K_RIGHT:
                pemain.x_speed = 5
            elif e.key == K_UP:
                pemain.y_speed = -5  
            elif e.key == K_DOWN:
                pemain.y_speed = 5
            elif e.key == K_SPACE:
                pemain.fire()

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                pemain.x_speed =  0
            elif e.key == K_RIGHT:
                pemain.x_speed = 0
            elif e.key == K_UP:
                pemain.y_speed =  0  
            elif e.key == K_DOWN:
                pemain.y_speed = 0

    if not finish:
        window.fill(back)
        w1.reset()
        w2.reset()

        barriers.draw(window)
        bullets.draw(window)

        pemain.update()
        bullets.update()

        pemain.reset()
        monster.reset()
        treasure.reset()
        
        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, True)


        if sprite.collide_rect(pemain, monster):
            finish = True
            img = image.load("game_over.jpg")
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (500 * d, 500)), (90, 0))
        if sprite.collide_rect(pemain, treasure):
            finish = True
            img = image.load("you_win.jpg")
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (500 * d, 500)), (90, 0))
    display.update()




