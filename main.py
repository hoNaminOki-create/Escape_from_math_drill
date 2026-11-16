"""MainProgram"""
import asyncio
import pygame
from pygame.locals import *
import math
import random

# 色の定義
B, W, R, BACK = (0,0,0), (255,255,255), (255,0,0), (150,0,5)

# 変数の定義
screenSize = (960,640)  # game size
keyTime, titleTime, gameTime = 0, 0, 0  # time definition

playerAreaX, playerAreaY, playerAreaWidth, playerAreaHeight, playerAreaLine = 0, 0, 960, 640, 1  # play size

index, stage = 1, 0
d = 0

# リスト
enemy_bullet = []
enemy_laser = []

# 三角関数の定義
def sin(x):
    return round(math.sin(math.radians(x)),3)
def cos(x):
    return round(math.cos(math.radians(x)),3)
def arctan(x1, y1, x2, y2):
    return round(math.degrees(math.atan((x2-x1)/(y1-y2))),1) if y1-y2<0 else round(math.degrees(math.atan((x2-x1)/(y1-y2))),1) + 180 if y1 - y2 > 0 else 90 if y1-y2== 0 and x1-x2 > 0 else -90

# objectクラスの定義
class object:
    def __init__(self, posX, posY, objectW, objectH):
        self.posX, self.posY, self.objectW ,self.objectH = posX, posY, objectW, objectH

# playerクラスの定義
class playerClass(object):
    def __init__(self, posX, posY, objectW, objectH, moveSpeedMax, moveSpeedMin ,playerHp, hitCollision, img):
        super().__init__(posX, posY, objectW, objectH)
        self.startX, self.startY = posX, posY

        self.moveSpeed, self.moveSpeedMax, self.moveSpeedMin = moveSpeedMax, moveSpeedMax, moveSpeedMin

        self.playerHp, self.playerMaxHp = playerHp, playerHp

        self.hitCollision, self.damageTrriger = hitCollision, 0
        self.img = img

    def playerMove(self,screen,key):
        if key[pygame.K_UP] == True and key[pygame.K_DOWN] == False and playerAreaY < self.posY - self.moveSpeed - self.objectH/2:
            self.posY -= self.moveSpeed
        elif key[pygame.K_DOWN] == True and key[pygame.K_UP] == False and self.posY + self.moveSpeed + self.objectH/2 < playerAreaY + playerAreaHeight:
            self.posY += self.moveSpeed
        if key[pygame.K_LEFT] == True and key[pygame.K_RIGHT] == False and playerAreaX < self.posX - self.moveSpeed - self.objectW/2:
            self.posX -= self.moveSpeed
        elif key[pygame.K_RIGHT] == True and key[pygame.K_LEFT] == False and self.posX + self.moveSpeed + self.objectW/2 < playerAreaX + playerAreaWidth:
            self.posX += self.moveSpeed

        self.playerImg = pygame.transform.scale(self.img,[40,40])
        screen.blit(self.playerImg,[self.posX - 40/2,self.posY - 40/2])

        if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
            self.moveSpeed = self.moveSpeedMin
        else:
            self.moveSpeed = self.moveSpeedMax

    def playerDamage(self):
        if 0 < self.damageTrriger:
            self.damageTrriger = 0
            self.playerHp -= 1

    def playerDeath(self):
        global index
        if self.playerHp <= 0:
            index = 4

    def playerReset(self):
        enemy_bullet.clear()
        enemy_laser.clear()
        self.posX, self.posY = self.startX, self.startY
        self.moveSpeed = self.moveSpeedMax
        self.damageTrriger = 0
        self.playerHp = self.playerMaxHp

# playerクラスの制御
def playerBehave(a,key,screen):
    a.playerMove(screen,key)
    a.playerDamage()
    a.playerDeath()

# enemyBulletクラスの定義
class enemyBullet():
    def __init__(self, posX, posY, objectW, objectH, Time, stayTime1, moveTime1, stayTime2, moveTime2, size1, size2, size3, size4, speed1, speedA1, track1, direction1, directionA1, speed2, speedA2, track2, direction2, directionA2, hitCollision, image):
        self.posX, self.posY, self.objectW, self.objectH = posX, posY, objectW, objectH

        self.actionTime0, self.actionTime1, self.actionTime2, self.actionTime3, self.actionTime4 = Time + gameTime, Time + gameTime + stayTime1, Time + gameTime + stayTime1 + moveTime1, Time + gameTime + stayTime1 + moveTime1 + stayTime2, Time + gameTime + stayTime1 + moveTime1 + stayTime2 + moveTime2

        self.speed1, self.speedA1, self.track1, self.direction1, self.directionA1 = speed1, speedA1, track1, direction1, directionA1
        self.speed2, self.speedA2, self.track2, self.direction2, self.directionA2 = speed2, speedA2, track2,  direction2, directionA2

        self.hitCollision = hitCollision
        self.image, self.image1, self.image2, self.image3, self.image4 =image.subsurface(size1), image.subsurface(size1), image.subsurface(size2), image.subsurface(size3), image.subsurface(size4)

    def enemyBulletMove(self,screen,a):
        if gameTime == self.actionTime0 and self.track1 == 1:
            self.direction1 = -1 * arctan(self.posX,self.posY,a.posX,a.posY)
        elif gameTime == self.actionTime2 and self.track2 == 1:
            self.direction2 = -1 * arctan(self.posX,self.posY,a.posX,a.posY)

        if self.actionTime0 <= gameTime < self.actionTime1:
            self.image = pygame.transform.rotozoom(self.image1,self.direction1,1)
        elif self.actionTime1 <= gameTime < self.actionTime2:
            self.image = pygame.transform.rotozoom(self.image2,self.direction1,1)
            self.speed1, self.direction1 = self.speed1 + self.speedA1, self.direction1 + self.directionA1
            self.posX += self.speed1 * sin(self.direction1)
            self.posY += self.speed1 * cos(self.direction1)

        elif self.actionTime2 <= gameTime < self.actionTime3:
            self.image = pygame.transform.rotozoom(self.image3,self.direction2,1)
        elif self.actionTime3 <= gameTime < self.actionTime4:
            self.image = pygame.transform.rotozoom(self.image4,self.direction2,1)
            self.speed2, self.direction2 = self.speed2 + self.speedA2, self.direction2 + self.directionA2
            self.posX += self.speed2 * sin(self.direction2)
            self.posY += self.speed2 * cos(self.direction2)

        self.objectW, self.objectH = self.image.get_width(), self.image.get_height()

        if self.actionTime0 <= gameTime:
            screen.blit(self.image,self.image.get_rect(center=self.image.get_rect(center=(self.posX, self.posY)).center))
            pygame.draw.circle(screen,R,[self.posX,self.posY],self.hitCollision*0)

    def enemyBulletDamage(self,player):
        if (self.posX - player.posX)**2 + (self.posY - player.posY)**2 < (self.hitCollision + player.hitCollision)**2:
            player.damageTrriger  += 1

    def enemyBulletDel(self,num):
        if self.actionTime4 <= gameTime:
            del enemy_bullet[num]

# enemyBulletクラスの制御
def enemyBulletBehave(screen,player):
    for i in range(len(enemy_bullet)-1,-1,-1):
        enemy_bullet[i].enemyBulletMove(screen,player)
        enemy_bullet[i].enemyBulletDamage(player)
        enemy_bullet[i].enemyBulletDel(i)

# enemyBulletを生成する
def makeEnemyBullet1(startTime,period,phase,num,centerX,centerY,r,dphase, degree, Bnum, width, height, T, sT1, mT1, sT2, mT2, si1,si2,si3,si4, s1, sA1, t1, d1, dA1, s2, sA2, t2, d2,dA2, cR, img):
    if (gameTime - startTime) % period == phase and 0 <= gameTime - startTime < period * num:
        for i in range(Bnum):
            enemy_bullet.append(enemyBullet(centerX + r * sin(dphase + degree * i),centerY + r * cos(dphase + degree * i),width,height,T * i,sT1,mT1,sT2,mT2,si1,si2,si3,si4,s1,sA1,t1,dphase + degree * i + d1,dA1,s2,sA2,t2,dphase + degree * i + d2,dA2,cR,img))

def makeEnemyBullet2(startTime,period,phase,num,x1,y1,x2,y2, Bnum, width, height, T, sT1, mT1, sT2, mT2, si1,si2,si3,si4, s1, sA1, t1, d1, dA1, s2, sA2, t2, d2,dA2, cR, img):
    if (gameTime - startTime) % period == phase and 0 <= gameTime - startTime < period * num:
        for i in range(Bnum):
            enemy_bullet.append(enemyBullet(x1 + (x2-x1)*i/(Bnum-1),y1 + (y2-y1)*i/(Bnum-1),width,height,T * i,sT1,mT1,sT2,mT2,si1,si2,si3,si4,s1,sA1,t1,d1,dA1,s2,sA2,t2,d2,dA2,cR,img))

def C(centerX,centerY,r,dphase, degree, Bnum, width, height, T, sT1, mT1, sT2, mT2, si1,si2,si3,si4, s1, sA1, t1, d1, dA1, s2, sA2, t2, d2,dA2, cR, img):
    for i in range(Bnum):
        enemy_bullet.append(enemyBullet(centerX + r * sin(dphase + degree * i),centerY + r * cos(dphase + degree * i),width,height,T * i,sT1,mT1,sT2,mT2,si1,si2,si3,si4, s1,sA1,t1,dphase + degree * i + d1,dA1,s2,sA2,t2,dphase + degree * i + d2,dA2,cR,img))

def L(x1,y1,x2,y2, Bnum, width, height, T, sT1, mT1, sT2, mT2, si1,si2,si3,si4, s1, sA1, t1, d1, dA1, s2, sA2, t2, d2,dA2, cR, img):
    for i in range(Bnum):
            enemy_bullet.append(enemyBullet(x1 + (x2-x1)*i/(Bnum),y1 + (y2-y1)*i/(Bnum),width,height,T * i,sT1,mT1,sT2,mT2,si1,si2,si3,si4,s1,sA1,t1,d1,dA1,s2,sA2,t2,d2,dA2,cR,img))


def CL(startTime,period,phase,num,centerX,centerY,r,dphase, degree, Cnum, Bnum, T, sT1, mT1, sT2, mT2, si1,si2,si3,si4, s1, sA1, t1, d1, dA1, s2, sA2, t2, d2,dA2, cR, img):
    if (gameTime - startTime) % period == phase and 0 <= gameTime - startTime < period * num:
        for i in range(Cnum):
            L(centerX+r*sin(dphase+degree*i),centerY+r*cos(dphase+degree*i),centerX+r*sin(dphase+degree*(i+1)),centerY+r*cos(dphase+degree*(i+1)),Bnum,0,0,T*i,sT1,mT1,sT2,mT2,si1[i],si2[i],si3[i],si4[i],s1,sA1,t1,d1-dphase+degree/2+degree*i,dA1,s2,sA2,t2,d2-dphase+degree/2+degree*i,dA2,cR,img)

def CC(startTime,period,phase,num,centerX,centerY,r,phaseD,degreeD,numD,Cr,CphaseD,Cdegree,CnumD,T,sT1,mT1,sT2,mT2,si1,si2,si3,si4,s1,sA1,t1,d1,dA1,s2,sA2,t2,d2,dA2,cR,img):
    if (gameTime - startTime) % period == phase and 0 <= gameTime - startTime < period * num:
        for i in range(numD):
            C(centerX+r*sin(phaseD+degreeD*i),centerY+r*cos(phaseD+degreeD*i),Cr,CphaseD,Cdegree,CnumD,0,0,T,sT1,mT1,sT2,mT2,si1[i],si2[i],si3[i],si4[i],s1,sA1,t1,d1,dA1,s2,sA2,t2,d2,dA2,cR,img)

def draw_hud(screen, hud_font, stage, gameTime, chara, stage_clear_times, left_panel, right_panel):
    """Draw compact semi-transparent phase/time and HP bar HUDs."""
    total_phases = (4, 5, 6)[stage]
    current_phase = min(total_phases, gameTime // (60 * 30) + 1)
    remain_sec = max(0, (stage_clear_times[stage] - gameTime + 59) // 60)

    screen.blit(left_panel, (16, 596))
    phase_text = hud_font.render(f"WAVE {current_phase}/{total_phases}   {remain_sec}s", True, W)
    screen.blit(phase_text, phase_text.get_rect(midleft=(28, 612)))

    screen.blit(right_panel, (714, 596))
    hp = max(0, chara.playerHp)
    hp_ratio = max(0.0, min(1.0, hp / chara.playerMaxHp))
    if hp_ratio > 0.5:
        bar_color = (80, 220, 140)
    elif hp_ratio > 0.25:
        bar_color = (245, 190, 60)
    else:
        bar_color = (235, 70, 80)

    hp_text = hud_font.render(f"HP {hp:>3}", True, W)
    screen.blit(hp_text, hp_text.get_rect(midleft=(726, 612)))

    bar_x, bar_y, bar_w, bar_h = 804, 607, 128, 10
    pygame.draw.rect(screen, (35, 35, 45), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
    fill_w = int(bar_w * hp_ratio)
    if fill_w > 0:
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_w, bar_h), border_radius=5)
    pygame.draw.rect(screen, (200, 200, 215), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=5)


# mainの関数
async def main():
    global index, keyTime, titleTime, gameTime, stage, d
    pygame.init()
    pygame.display.set_caption("Escape from Math Drill")
    screen = pygame.display.set_mode(screenSize)
    clock = pygame.time.Clock()

# Load image
    title = pygame.image.load("Title.png")
    select = pygame.image.load("Select.png")

    player = pygame.image.load("Player1.png")
    chara = playerClass(480,600,85,85,6,3,100,20,player)

    Bullet = pygame.image.load("Bullet.png")

    Back = pygame.image.load("Back.png")
    Lose = pygame.image.load("Lose.png")
    Win = pygame.image.load("Win.png")
    WinBack = pygame.image.load("WinBack.png")

    small_font = pygame.font.Font(None, 28)
    hud_font = pygame.font.Font(None, 26)
    stage_clear_times = [60 * 123, 60 * 153, 60 * 183]

    left_panel = pygame.Surface((190, 32), pygame.SRCALPHA)
    pygame.draw.rect(left_panel, (15, 15, 25, 145), left_panel.get_rect(), border_radius=8)
    right_panel = pygame.Surface((230, 32), pygame.SRCALPHA)
    pygame.draw.rect(right_panel, (15, 15, 25, 145), right_panel.get_rect(), border_radius=8)

    running = True

    while running:
        # ゲームの終了処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
 
        # index 1 -- Choose Stage --
        if index == 1:
            screen.fill(BACK)
            screen.blit(title,[180,30])

            if key[pygame.K_DOWN] == True and 10 <= keyTime:
                stage = (stage + 1) % 3
                keyTime = 0
            elif key[pygame.K_UP] == True and 10 <= keyTime:
                stage = (stage - 1) % 3
                keyTime = 0

            elif key[pygame.K_SPACE] == True and 10 <= keyTime:
                chara.playerReset()
                gameTime = 0
                index = 3
                keyTime = 0

            for i in range(3):
                screen.blit(select,[270 if i==stage else 292,300+i*70],[0,60*i,375,60])

            guide = small_font.render("UP / DOWN: Select   SPACE: Start   SHIFT: Slow", True, W)
            screen.blit(guide, guide.get_rect(center=(480, 580)))

        # index 3 -- Play Game --
        elif index == 3:
            screen.blit(Back,(0,0))
            draw_hud(screen, hud_font, stage, gameTime, chara, stage_clear_times, left_panel, right_panel)

            if stage == 0:
                CC(0,90,  0,20,  480,80, 30,random.randint(0,71),72,5,30,random.randint(0,29),30,12, 0,0,0,0,120,[[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56]],[[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56]],[[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56]],[[0, 0,40,56],[0, 0,40,56],[0, 0,40,56],[0, 0,40,56],[0, 0,40,56]], 0,0,0,0,0,6,0,0,random.randint(-45,45),random.uniform(-0.4,0.4),15,Bullet)
                CC(0,90, 45,20,  480,80, 50,random.randint(0,71),72,5,30,random.randint(0,29),30,12, 0,0,0,0,120,[[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56]],[[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56]],[[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56],[0,0,40,56]],[[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44]], 0,0,0,0,0,6,0,1,-20,0,10,Bullet)
                
                CL(60*30,120,0,15,480,100, 90,0,144,5,5,0,0,40,30,150,[[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44]],[[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44]],[[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44]],[[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44]],3,0,0,0,0,0,0.2,1,0,0,10,Bullet)
                CC(60*30,60,10,30,480,100,0,0,0,1,80,random.randint(0,14),15,24,0,0,0,0,240,[[0,100,20,28]],[[0,100,20,28]],[[0,100,20,28]],[[0,100,20,28]],0,0,0,0,0,6,0,0,0,0,6,Bullet)

                CL(60*60,120, 0,14,480+random.randint(-20,20,),  -20,480,90,180,1,10,10,0,0,0,420,[[0,56,32,44]],[[0,56,32,44]],[[0,56,32,44]],[[0,56,32,44]],0,0,0,0,0,2,0,0,0,0,10,Bullet)
                CL(60*60,120,60,14,480+random.randint(-20,20,),  -20,480,90,180,1,10,10,0,0,0,240,[[0,56,32,44]],[[0,56,32,44]],[[0,56,32,44]],[[0,56,32,44]],0,0,0,0,0,4,0,0,0,0,10,Bullet)

                CC(60*90,40,0,45,random.randint(0,960),random.randint(0,100),100,random.randint(0,119),120,3,40,random.randint(0,35),45,8,0,0,0,0,360,[[0,100,20,28],[0,100,20,28],[0,100,20,28]],[[0,100,20,28],[0,100,20,28],[0,100,20,28]],[[0,100,20,28],[0,100,20,28],[0,100,20,28]],[[0,100,20,28],[0,100,20,28],[0,100,20,28]],0,0,0,0,0,0,0.05,0,0,random.uniform(-0.2,0.2),6,Bullet)

                if gameTime >= 60*123:
                    index = 5

            elif stage == 1:
                CC(0,40,  0,45, 480,80, 50,0,0,1,0,random.randint(0,17),20,18, 0,0,20,0,120,[[0,56,32,44]],[[0,56,32,44]],[[0,56,32,44]],[[0,56,32,44]], 8,0,0,0,0,2,0.05,0, random.randint(-20,20),0,10,Bullet)
                CC(0,180, 0,10,  80,60, 50,0,0,1,10,0,30,12, 0,0,20,0,120,[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]], 5,0,0,0,0,7,0,1,0,0,6,Bullet)
                CC(0,180,90,10, 880,60, 50,0,0,1,10,0,30,12, 0,0,20,0,120,[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]], 5,0,0,0,0,7,0,1,0,0,6,Bullet)

                CL(60*30,60,0,30,480,140,130,0,144,5,5,0,30,0,0,200,[[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44],[0,56,32,44]],[[0,56,32,44],[0,56,32,44],[0,56,32,44],[32,56,32,44],[32,56,32,44]],[[0,56,32,44],[0,56,32,44],[0,56,32,44],[32,56,32,44],[32,56,32,44]],[[32,56,32,44],[32,56,32,44],[32,56,32,44],[32,56,32,44],[32,56,32,44]],0,0,0,0,0,6,0,1,0,0,10,Bullet)
                CC(60*30,60,10,29,480,100,0,0,0,1,80,random.randint(0,14),15,24,0,0,40,30,300,[[0,100,20,28]],[[0,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],5,0,0,0,0,6,0,0,180,0,6,Bullet)

                CL(60*60,120, 0,15,480+random.randint(-30,30,), -20,520, 90,180,1,10,10,0,0,0,420,[[0,56,32,44]],[[0,56,32,44]],[[0,56,32,44]],[[0,56,32,44]],0,0,0,0,0,3,0,0,0,0,10,Bullet)
                CL(60*60,180, 0,10,-20, 300+random.randint(-30,30),520,0,180,1,10,10,0,0,0,480,[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],0,0,0,0,0,random.randint(2,4),0,0,0,0,6,Bullet)
                CL(60*60,180,90, 9,980, 300+random.randint(-30,30),520,0,180,1,10,10,0,0,0,480,[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],0,0,0,0,0,random.randint(2,4),0,0,180,0,6,Bullet)

                CC(60*90,120,0,14,random.randint(0,960),random.randint(0,100),30,random.randint(0,119),72,5,20,random.randint(0,29),30,12,0,0,90,0,360,[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],4,0,0,0,0,3,0.02,0,random.randint(140,220),random.uniform(-0.1,0.1),6,Bullet)
                CC(60*90, 60,0,28,480,100,0,0,0,1,80,random.randint(0,23),24,15,0,0,0,0,300,[[0,0,40,56]],[[0,0,40,56]],[[0,0,40,56]],[[0,0,40,56]],0,0,0,0,0,6,0,0,180,0,6,Bullet)

                CL(60*120,180, 0,10,480,400,800,0,72,5,20,0,0,0,0,360,[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],0,0,0,0,0,10,-0.1,0,180,0,6,Bullet)
                CC(60*117,180,90,10,480,400,0,0,0,1, 0,random.randint(0,35),18,20,0,0,30,150,300,[[0,100,20,28]],[[0,100,20,28]],[[0,100,20,28]],[[0,100,20,28]],1,0,0,0,0,0,0.03,0,0,0,6,Bullet)

                if gameTime >= 60 * 153:
                    index = 5

            elif stage == 2:
                CC(0, 40,  0,44, 380,80, 50,0,0,1,0,random.randint(0,29),30,12, 0,0,20,0,120,[[40,100,20,28]],[[40,100,20,28]],[[40,100,20,28]],[[40,100,20,28]], 8,0,0,0,0,2,0.04,0, random.randint(-20,20),0,10,Bullet)
                CC(0, 40, 20,44, 580,80, 50,0,0,1,0,random.randint(0,29),30,12, 0,0,20,0,120,[[40,100,20,28]],[[40,100,20,28]],[[40,100,20,28]],[[40,100,20,28]], 8,0,0,0,0,2,0.04,0, random.randint(-20,20),0,10,Bullet)
                CC(0,180, 0,9,  80,60, 50,0,0,1,10,0,30,12, 0,0,10,0,180,[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]], 5,0,0,0,0,7,0,1,0,0,6,Bullet)
                CC(0,180,90,9, 880,60, 50,0,0,1,10,0,30,12, 0,0,10,0,180,[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]], 5,0,0,0,0,7,0,1,0,0,6,Bullet)

                CL(60*30,60,0,29,480,320, 90,0,144,5,5,0,30,0,0,200,[[32,56,32,44],[32,56,32,44],[32,56,32,44],[32,56,32,44],[32,56,32,44]],[[32,56,32,44],[32,56,32,44],[32,56,32,44],[32,56,32,44],[32,56,32,44]],[[32,56,32,44],[32,56,32,44],[32,56,32,44],[32,56,32,44],[32,56,32,44]],[[32,56,32,44],[32,56,32,44],[32,56,32,44],[32,56,32,44],[32,56,32,44]],0,0,0,0,0,6,0,1,0,0,10,Bullet)
                CL(60*30,60,0,29,480,320,120,0,144,5,5,0, 0,0,0,200,[[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44]],[[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44]],[[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44]],[[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44]],0,0,0,0,0,6,0,1,0,0,10,Bullet)
                CC(60*30,60,0,29,480,320,0,0,0,1,80,0,18,20,0,0,0,0,300,[[0,100,20,28]],[[0,100,20,28]],[[0,100,20,28]],[[0,100,20,28]],5,0,0,0,0,6,0,0,180,0,6,Bullet)

                CC(60*60,60, 0,29,480,100,0,0,0,1,80,random.randint(0,17),18,20,0,0,0,0,300,[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],5,0,0,0,0,6,0,0,180,0,6,Bullet)
                CL(60*60,90, 0,19,-20, 300+random.randint(-40,40),520,0,180,1,10,10,0,0,0,480,[[40,100,20,28]],[[40,100,20,28]],[[40,100,20,28]],[[40,100,20,28]],0,0,0,0,0,random.randint(4,6),0,0,0,0,6,Bullet)
                CL(60*60,90,45,19,980, 300+random.randint(-40,40),520,0,180,1,10,10,0,0,0,480,[[40,100,20,28]],[[40,100,20,28]],[[40,100,20,28]],[[40,100,20,28]],0,0,0,0,0,random.randint(4,6),0,0,180,0,6,Bullet)

                CC(60*90,90, 0,19,random.randint(0,960),random.randint(0,100),30,random.randint(0,71),72,5,20,random.randint(0,29),30,12,0,0,90,0,360,[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],[[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28],[20,100,20,28]],4,0,0,0,0,3,0.02,0,random.randint(140,220),random.uniform(-0.1,0.1),6,Bullet)
                CC(60*90,90,45,19,random.randint(0,960),random.randint(0,100),30,random.randint(0,71),72,5,20,random.randint(0,29),30,12,0,0,90,0,360,[[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28]],[[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28]],[[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28]],[[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28]],4,0,0,0,0,3,0.02,0,random.randint(140,220),random.uniform(-0.1,0.1),6,Bullet)

                CL(60*120,180, 0, 9,480,400,800,0,72,5,6,0,0,0,0,360,[[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28]],[[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28]],[[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28]],[[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28],[40,100,20,28]],0,0,0,0,0,4,0,0,180,0,6,Bullet)
                CL(60*120,120, 0,14,480,110,100,0,144,5,5,0,30,0,0,200,[[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44]],[[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44]],[[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44]],[[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44],[64,56,32,44]],0,0,0,0,0,6,0,1,0,0,10,Bullet)

                CC(60*150,12,0,150,480,130,0,0,0,1,80, gameTime/9,18,20,0,0,0,30,100,[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],[[20,100,20,28]],0,0,0,0,0,6,0,0,0,0,6,Bullet)
                CC(60*150,12,0,150,480,130,0,0,0,1,80,-gameTime/9,18,20,0,0,0,30,100,[[40,100,20,28]],[[40,100,20,28]],[[40,100,20,28]],[[40,100,20,28]],0,0,0,0,0,6,0,0,0,0,6,Bullet)

                if gameTime >= 60 * 183:
                    index = 5

            playerBehave(chara,key,screen)
            enemyBulletBehave(screen,chara)
            gameTime += 1

        elif index == 4:
            screen.blit(Lose.subsurface(0,360 * stage,720,360),(120,270))
            retry = small_font.render("SPACE: Back to Title", True, W)
            screen.blit(retry, retry.get_rect(center=(480, 610)))
            if key[pygame.K_SPACE] == True and 10 <= keyTime:
                index = 1
                keyTime = 0

        elif index == 5:
            screen.blit(WinBack,(0,0))
            screen.blit(Win.subsurface(0,220*stage,630,210),(165,300))
            retry = small_font.render("SPACE: Back to Title", True, W)
            screen.blit(retry, retry.get_rect(center=(480, 610)))
            if key[pygame.K_SPACE] == True and 10 <= keyTime:
                index = 1
                keyTime = 0

        keyTime += 1
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == '__main__':
    asyncio.run(main())
