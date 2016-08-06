# -*- coding: cp936 -*-

# bullet
   
import pygame
import random

class Bullet():
    #定义子弹类
    def __init__(self,x,y,d):
        self.poslist = [[x,y]]
        #子弹位置
        self.delta = d
        #子弹每次移动距离
    def getpos(self):
        for pos in self.poslist:
            pos[1] = pos[1]+self.delta
            if pos[1] < 0:
                self.poslist.remove(pos)
                #当子弹飞出窗口之外时，子弹消失
        return self.poslist
    def setpos(self,x,y):
        self.poslist.append([x,y])
        #将新位置加入列表

class Player():
    #定义玩家类
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = self.x - 20
        self.right = self.x + 20
        #标出玩家飞机的飞机的左右端点
        self.bullet = Bullet(self.x,self.y,-10)
        #将玩家飞机坐标与子弹结合
        self.bulletnum = 0
        #为子弹数量设置初始值

    def move(self,direction):
        #飞机前后左右的移动函数
        if direction is  "U":
            self.y = self.y - 15
            if self.y < 0:
                self.y = 0

        if direction is "D":
            self.y = self.y+15
            if self.y + 15 > self.height:
                self.y = self.height - 15
                #当飞机超出窗口下界时，飞机不再移动

        if direction is "L":
            self.x = self.x - 20
            self.left = self.x + 20
            self.right =self.x - 20

        if direction is "R":
            self.x = self.x + 20
            self.left = self.left + 20
            self.right = self.right + 20
        return [[self.x,self.y],[self.left,self.y+20],[self.right,self.y+20]]

    def getpos(self):
        return [[self.x,self.y],[self.left,self.y+20],[self.right,self.y+20]]
               #给出代表玩家飞机的三角形三点坐标

    def getbulletpos(self):
        return self.bullet.getpos()
        #获得子弹坐标列表

    def setbulletpos(self,shoot):
        self.bulletnum = self.bulletnum + 1
        if self.bulletnum % 10 == 0:
            self.bullet.setpos(self.x,self.y)
            #子弹数目满10个后，重新定位子弹

class Enemy():
    #定义敌机类
    def __init__(self,x,y,d,height):
        self.x = x
        self.y = y
        self.size = random.randint(2,4)
        #控制敌机的三种不同大小
        self.big = 10 * self.size
        self.left = self.x - self.big
        self.right = self.x + self.big
        self.delta = d
        self.height = height
        self.score = 100 * (self.size-1)
        #每种敌机的分值不同

    def getpos(self):
        self.y = self.y + self.delta
        #敌机的移动
        if self.y > self.height:
            self.x = random.randint(100,700)
            self.y = 0
            #飞出窗口后重新出现
            self.left = self.x - self.big
            self.right = self.x + self.big
        return [[self.x,self.y],[self.left,self.y-self.big],[self.right,self.y-self.big]]
                #代表敌机三角形的三点坐标


def screen():
    #设置屏幕大小、背景
    global screen,width,height,background
    width = 800
    height = 600
    screen = pygame.display.set_mode([width,height])
    background = pygame.image.load("Background.jpg")
    width = screen.get_width()
    height = screen.get_height()
    pygame.display.set_caption("Flight Attack")

def loadaudio():
    #设置音频
    global hit,shoot,enemy
    #背景音乐
    #pygame.mixer.music.load("backgroundmusic.mp3")
    #pygame.mixer.music.play(-1)
    ##循环播放
    pygame.mixer.music.set_volume(0.3)
    ##设置音量
    #音效
    hit = pygame.mixer.Sound("explode.wav")
    enemy = pygame.mixer.Sound("enemy.wav")
    shoot = pygame.mixer.Sound("shoot.wav")
    hit.set_volume(0.1)
    enemy.set_volume(0.1)
    shoot.set_volume(0.1)

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    screen()
    loadaudio()

    score = 0
    font = pygame.font.Font(None,20)
    #字体设置

    clock = pygame.time.Clock()
    #控制动画帧速率

    moveup  = False
    movedown = False
    moveleft = False
    moveright = False
    #为判断方向设置bool值

    player = Player(width/2,height-20,width,height)
    #玩家飞机实体化

    plane = []
    for i in range(0,5):
        plane.append(Enemy(random.randint(100,700),0,random.randint(1,5),height))
        #设置敌机飞机位置、数量

    done = True
    #为游戏开始及结束设置bool值

##    while 1:
##       background1=pygame.image.load("background1.jpg")
##       screen.blit(background1,[0,0])
##       
##       for event in pygame.event.get():
##          if event.type == pygame.QUIT:
##               exit()
##          if event.type == pygame.KEYDOWN:
##            if event.type == pygame.K_SPACE:
##               done=True
##    开始页（失败）

    while done:
        screen.blit(background,[0,0])
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               exit()
            #退出键

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                moveup = True
            elif event.key == pygame.K_DOWN:
                movedown = True
            elif event.key == pygame.K_LEFT:
                moveleft = True
            elif event.key == pygame.K_RIGHT:
                moveright = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                moveup = False
            elif event.key == pygame.K_DOWN:
                movedown = False
            elif event.key == pygame.K_LEFT:
                moveleft = False
            elif event.key == pygame.K_RIGHT:
                moveright = False
            #按下键盘和松开键盘时玩家飞机的移动方向

        enemyrect = []
        for posl in plane:
           poslist = posl.getpos()
           enemyrect.append(pygame.draw.polygon(screen,[219,142,113],poslist,0))
        #画出敌机

        playerlist = player.getpos()
        playerrect = pygame.draw.polygon(screen,[112,100,154],playerlist,0)
        #画出玩家飞机
        if moveup:
            playerlist = player.move("U")
        if movedown :
            playerlist = player.move("D")
        if moveleft:
            playerlist = player.move("L")
        if moveright:
            playerlist = player.move("R")
        player.setbulletpos(shoot)
        #实施移动

        bulletlist = player.getbulletpos()
        j = 0
        for bulletpos in bulletlist:
            i = 0
            for enemyrt in enemyrect:
                if enemyrt.collidepoint(bulletpos):
                    #敌机与子弹碰撞检测
                    shoot.play()
                    plane[i].size =plane[i].size - 1
                    #三种敌机消失所需的被击中的次数不同
                    player.bullet.poslist.pop(j)
                    if plane[i].size <= 0:
                        score = score + plane[i].score
                        plane.pop(i)
                        plane.append(Enemy(random.randint(100,700),0,random.randint(1,5),height))
                    #敌机消失后，分数增加，出现新的敌机
                    break
                if enemyrt.colliderect(playerrect):
                    #敌机与玩家碰撞检测
                    hit.play()
                    done = False
                    #游戏结束
                    break
                pygame.draw.circle(screen,[247,217,76],bulletpos,5)
                #画出子弹
                i = i+1
            if not done:
                break
            j = j
        if not done:
            break

        score_text = "score:"+str(score)
        text = font.render(score_text,1,[255,255,255])
        screen.blit(text,(20,20))
        #显示当时分数
        pygame.display.update()

    while 1:
        background2=pygame.image.load("background2.png")
        screen.blit(background2,[0,0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit(0)

        final_text1 = "Game Over!"
        final_text2 = "Your final score is:" + str(score)
        final_text3 = "Please press Esc to quit."
        ft1_font = pygame.font.Font(None,200)
        ft1_surf = font.render(final_text1,1,[232,48,21])
        ft2_font = pygame.font.Font(None,100)
        ft2_surf = font.render(final_text2,1,[232,48,21])
        ft3_font = pygame.font.Font(None,100)
        ft3_surf = font.render(final_text3,1,[232,48,21])

        screen.blit(ft1_surf,(width/5,height/4))
        screen.blit(ft2_surf,(width/5,height/4 + 15))
        screen.blit(ft3_surf,(width/5,height/4 + 30))
        #设置Game Over界面文本

        pygame.display.update()

if __name__=="__main__":
    main()
