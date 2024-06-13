
#匯入模組
import pygame, os , random ,time

#初始化 建視窗 
pygame.init()
Width,Length = 900,600
screen = pygame.display.set_mode((Width,Length))
pygame.display.set_caption("little game")


#顏色、文字
Background = 255,62,150
#255,62,150
WHITE = 255,255,255
BLACK = 0,0,0
font_name = os.path.join("TaipeiSans.ttf")
#大小
Line_size = Width,20
ball_big = 50,50
showlife_size = 200,100
balllife_size = 45,45
background_size = Width, Length


#運作
Running=True
init_rectx = random.randint(0,Width)
new_rectx = init_rectx+random.randint(int(-Width/4),int(Width/4))
button_left,button_right,button_top,button_bottom=0,0,0,0
score = 0
show_score = 0,0
button_pressed = 0
LINELENGTH = int(Length *2 /3)
SPEED_LEVEL = [8.6,9.3,10.2,11.5,13,19]
Speed = SPEED_LEVEL[0]
SCORERANGE = 100
fallcount = -1
lifeleft = 3
play_again = False

#圖片
line_img = pygame.image.load("Line.png").convert()
line_img = pygame.transform.scale(line_img, (Line_size))
line_img.set_colorkey(BLACK)
button_img = pygame.image.load("ball.png").convert()
button_img = pygame.transform.scale(button_img, (ball_big))
button_img.set_colorkey(WHITE)
balllife_img = pygame.transform.scale(button_img, (balllife_size))
show_life_img = pygame.image.load(os.path.join("show life.png")).convert()
background_img = pygame.image.load(os.path.join("background.jpg")).convert()
background_img = pygame.transform.scale(background_img, (background_size))
pygame.display.set_icon(balllife_img)
pressed_sound = pygame.mixer.Sound(os.path.join("Sound","pressed_300.wav"))
pygame.mixer.music.load(os.path.join("Sound","background.mp3"))

#FPS
clock = pygame.time.Clock()
FPS = 40

################################################

#Button
class Button(pygame.sprite.Sprite):

    def __init__(self):
        global new_rectx
        pygame.sprite.Sprite.__init__(self)
        self.image = button_img
        self.rect = self.image.get_rect()
        self.rect.center = new_rectx, random.randint(-50, int(Length/8-ball_big[0]))
    #update
    def update(self):
        global Speed,score,button_pressed,show_score,fallcount,lifeleft,new_rectx
        global button_left,button_right,button_top,button_bottom
        #move
        self.rect.y +=Speed
        button_left = self.rect.left
        button_right = self.rect.right
        button_top = self.rect.top
        button_bottom = self.rect.bottom

        # speed change
        if 500 <= score:
            Speed = SPEED_LEVEL[0]
        if 500 < score <= 1000:
            Speed = SPEED_LEVEL[1]
        if 1000 < score <= 2100:
            Speed = SPEED_LEVEL[2]
        if 2100 < score <= 3500:
            Speed = SPEED_LEVEL[3] 
        if 3500 < score <= 5000:
           Speed = SPEED_LEVEL[4]
        if score > 5000:
           Speed = SPEED_LEVEL[5]           

        #touch bottom
        if self.rect.top >= Length:
            self.rect.top -= self.rect.top
            fallcount += 1
            if fallcount == 1:
                lifeleft -= 1
                fallcount = 0
        #pressed
        if button_pressed == 1:  
            add_score = 0
            #score
            if self.rect.top <= LINELENGTH:
                add_score = int ( SCORERANGE + self.rect.top - LINELENGTH)
            if self.rect.top > LINELENGTH:
                add_score = int ( SCORERANGE - self.rect.top + LINELENGTH)

            if  0 < add_score <= SCORERANGE:
                pressed_sound.play()
                add_score = add_score + 300
                score += add_score   
                show_score = score,add_score

                #create new
                self.kill()
                button_pressed = 0
                time.sleep(0.1)
                buttons = Button()
                All_sprites.add(buttons)
                fallcount = -1
                new_rectx = new_rectx + random.randint(int(-Width/4),int(Width/4))
                if new_rectx > Width-ball_big[0]:
                    new_rectx = new_rectx -Width/2
                if new_rectx < 0+ball_big[1]:
                    new_rectx = new_rectx + Width/2
            else:
                button_pressed = 0
#text function
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

#init text
def draw_init():
    global play_again,show_score
    screen.blit(background_img,(0,0))
    if play_again:
        draw_text(screen, "score:", 40,Width/2,Length/15)
        draw_text(screen, str(show_score[0]), 40,Width/2,Length/15+40)
        show_score = 0,0
    draw_text(screen,'反應力小遊戲',64,Width /2,Length/4)
    draw_text(screen, '在一定的範圍內點擊畫面中移動的球來得分，點到會讓球重新回到上方',24,Width/2,Length*3/7)
    draw_text(screen, '在越接近判定線的位置點到，就有越高的分數',24,Width/2,Length*3/7+60)
    draw_text(screen,'但如果球落到螢幕底部，會消耗一次護盾，再掉一次就減少一條生命',24,Width/2,Length*3/7+120)
    draw_text(screen,'Tips:隨著分數變高，球的移動速度也會增加喔，目標5000分，加油!',24,Width/2,Length*3/7+180)
    draw_text(screen,'按一下任意鍵以開始遊戲',18,Width/2,Length*7/8)

    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        #輸入
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                play_again = True
                return False


#物件
show_init = True
All_sprites = pygame.sprite.Group()
Buttons = Button()
All_sprites.add(Buttons)
pygame.mixer.music.play(-1)

#game loop
while Running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
    clock.tick(FPS)

    #input
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_xy = pygame.mouse.get_pos()       
            if button_left-10 < mouse_xy[0] < button_right+10 and button_top-5 < mouse_xy[1] < button_bottom+5:
                print("YES")
                button_pressed = 1     
        if event.type == pygame.QUIT:
            Running = False 

    #update
    All_sprites.update()

    #show
    
    #life=0
    if lifeleft == 0:
        screen.blit(background_img,(0,0))
        show_init = True
        score = 0
        button_pressed = 0
        Speed = SPEED_LEVEL[0]
        fallcount = -1
        lifeleft = 3
        All_sprites = pygame.sprite.Group()
        Buttons = Button()
        All_sprites.add(Buttons)

    #draw
    else:
        screen.blit(background_img,(0,0))
        All_sprites.draw(screen)
        screen.blit(show_life_img,(0, 500))
        screen.blit(line_img,(0, LINELENGTH+10))
        for i in range(lifeleft):
            screen.blit(balllife_img,(i*60+10, 525))
        draw_text(screen,str(show_score),18,Width/2,5)

    pygame.display.update()
