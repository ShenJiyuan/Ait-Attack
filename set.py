# -*- coding: cp936 -*-

# bullet
   
import pygame
import random

class Bullet():
    #�����ӵ���
    def __init__(self,x,y,d):
        self.poslist = [[x,y]]
        #�ӵ�λ��
        self.delta = d
        #�ӵ�ÿ���ƶ�����
    def getpos(self):
        for pos in self.poslist:
            pos[1] = pos[1]+self.delta
            if pos[1] < 0:
                self.poslist.remove(pos)
                #���ӵ��ɳ�����֮��ʱ���ӵ���ʧ
        return self.poslist
    def setpos(self,x,y):
        self.poslist.append([x,y])
        #����λ�ü����б�

class Player():
    #���������
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = self.x - 20
        self.right = self.x + 20
        #�����ҷɻ��ķɻ������Ҷ˵�
        self.bullet = Bullet(self.x,self.y,-10)
        #����ҷɻ��������ӵ����
        self.bulletnum = 0
        #Ϊ�ӵ��������ó�ʼֵ

    def move(self,direction):
        #�ɻ�ǰ�����ҵ��ƶ�����
        if direction is  "U":
            self.y = self.y - 15
            if self.y < 0:
                self.y = 0

        if direction is "D":
            self.y = self.y+15
            if self.y + 15 > self.height:
                self.y = self.height - 15
                #���ɻ����������½�ʱ���ɻ������ƶ�

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
               #����������ҷɻ�����������������

    def getbulletpos(self):
        return self.bullet.getpos()
        #����ӵ������б�

    def setbulletpos(self,shoot):
        self.bulletnum = self.bulletnum + 1
        if self.bulletnum % 10 == 0:
            self.bullet.setpos(self.x,self.y)
            #�ӵ���Ŀ��10�������¶�λ�ӵ�

class Enemy():
    #����л���
    def __init__(self,x,y,d,height):
        self.x = x
        self.y = y
        self.size = random.randint(2,4)
        #���Ƶл������ֲ�ͬ��С
        self.big = 10 * self.size
        self.left = self.x - self.big
        self.right = self.x + self.big
        self.delta = d
        self.height = height
        self.score = 100 * (self.size-1)
        #ÿ�ֵл��ķ�ֵ��ͬ

    def getpos(self):
        self.y = self.y + self.delta
        #�л����ƶ�
        if self.y > self.height:
            self.x = random.randint(100,700)
            self.y = 0
            #�ɳ����ں����³���
            self.left = self.x - self.big
            self.right = self.x + self.big
        return [[self.x,self.y],[self.left,self.y-self.big],[self.right,self.y-self.big]]
                #����л������ε���������


def screen():
    #������Ļ��С������
    global screen,width,height,background
    width = 800
    height = 600
    screen = pygame.display.set_mode([width,height])
    background = pygame.image.load("Background.jpg")
    width = screen.get_width()
    height = screen.get_height()
    pygame.display.set_caption("Flight Attack")

def loadaudio():
    #������Ƶ
    global hit,shoot,enemy
    #��������
    #pygame.mixer.music.load("backgroundmusic.mp3")
    #pygame.mixer.music.play(-1)
    ##ѭ������
    pygame.mixer.music.set_volume(0.3)
    ##��������
    #��Ч
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
    #��������

    clock = pygame.time.Clock()
    #���ƶ���֡����

    moveup  = False
    movedown = False
    moveleft = False
    moveright = False
    #Ϊ�жϷ�������boolֵ

    player = Player(width/2,height-20,width,height)
    #��ҷɻ�ʵ�廯

    plane = []
    for i in range(0,5):
        plane.append(Enemy(random.randint(100,700),0,random.randint(1,5),height))
        #���õл��ɻ�λ�á�����

    done = True
    #Ϊ��Ϸ��ʼ����������boolֵ

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
##    ��ʼҳ��ʧ�ܣ�

    while done:
        screen.blit(background,[0,0])
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               exit()
            #�˳���

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
            #���¼��̺��ɿ�����ʱ��ҷɻ����ƶ�����

        enemyrect = []
        for posl in plane:
           poslist = posl.getpos()
           enemyrect.append(pygame.draw.polygon(screen,[219,142,113],poslist,0))
        #�����л�

        playerlist = player.getpos()
        playerrect = pygame.draw.polygon(screen,[112,100,154],playerlist,0)
        #������ҷɻ�
        if moveup:
            playerlist = player.move("U")
        if movedown :
            playerlist = player.move("D")
        if moveleft:
            playerlist = player.move("L")
        if moveright:
            playerlist = player.move("R")
        player.setbulletpos(shoot)
        #ʵʩ�ƶ�

        bulletlist = player.getbulletpos()
        j = 0
        for bulletpos in bulletlist:
            i = 0
            for enemyrt in enemyrect:
                if enemyrt.collidepoint(bulletpos):
                    #�л����ӵ���ײ���
                    shoot.play()
                    plane[i].size =plane[i].size - 1
                    #���ֵл���ʧ����ı����еĴ�����ͬ
                    player.bullet.poslist.pop(j)
                    if plane[i].size <= 0:
                        score = score + plane[i].score
                        plane.pop(i)
                        plane.append(Enemy(random.randint(100,700),0,random.randint(1,5),height))
                    #�л���ʧ�󣬷������ӣ������µĵл�
                    break
                if enemyrt.colliderect(playerrect):
                    #�л��������ײ���
                    hit.play()
                    done = False
                    #��Ϸ����
                    break
                pygame.draw.circle(screen,[247,217,76],bulletpos,5)
                #�����ӵ�
                i = i+1
            if not done:
                break
            j = j
        if not done:
            break

        score_text = "score:"+str(score)
        text = font.render(score_text,1,[255,255,255])
        screen.blit(text,(20,20))
        #��ʾ��ʱ����
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
        #����Game Over�����ı�

        pygame.display.update()

if __name__=="__main__":
    main()
