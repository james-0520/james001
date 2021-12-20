import pygame 
import os
#初始化and建視窗

pygame.init()
Width,Length=900,600
screen = pygame.display.set_mode((Width,Length))
pygame.display.set_caption("test1")
Running=True

#圖
background_img = pygame.image.load(os.path.join("zero.jpg")).convert()
background_img = pygame.transform.scale(background_img, (900,600))
button_img = pygame.image.load(os.path.join("ball.png")).convert()
WHITE = 0,0,0
button_img.set_colorkey(WHITE)


#FPS
clock = pygame.time.Clock()
FPS = 10

Background = 255,50,163
Button_c = 0,62,150
#255,62,150
Button_R=Button_c[0]

class Button(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(button_img,(120,80))
        self.rect = self.image.get_rect()
        self.rect.center = (Width/2,Length/2)

    def update(self):
        self.image.fill(ButtonColor)


all_sprites = pygame.sprite.Group()
Buttons = Button()
all_sprites.add(Buttons)

#遊戲迴圈
while Running:
    clock.tick(FPS)
    #輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.KEYDOWN:
            pass

    #更新
    Button_R +=10
    Button_R = Button_R %200
    ButtonColor = Button_R,Button_c[1],Button_c[2]
    all_sprites.update()

    #顯示
    screen.fill((Background))
    all_sprites.draw(screen)
    pygame.display.update()