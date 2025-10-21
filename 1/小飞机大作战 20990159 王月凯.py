#20990159 王月凯 期末大作业 游戏制作：小飞机大作战
import pygame #使用pygame模块制作游戏
import random #使用随机性模块
import math #引入数学模块

# 游戏初始界面的制作  
pygame.init() #初始化
screen=pygame.display.set_mode((800,600)) #设置游戏窗口的大小
pygame.display.set_caption('20990159王月凯 小飞机大作战') #设置游戏的标题
icon=pygame.image.load('wyk ufo.png') #导入ufo图片
pygame.display.set_icon(icon) #导入图标
bgImg=pygame.image.load('wyk bg.png') #导入游戏的背景图

#添加游戏背景音乐
pygame.mixer.music.load('wyk bg.wav') #导入游戏背景音乐
pygame.mixer.music.play(-1) #让游戏背景音乐循环播放

#添加击中攻击对象的音乐
jizhong_sound = pygame.mixer.Sound('wyk jizhong.wav') #导入击中攻击对象时播放的音乐

#小飞机设置
playerImg=pygame.image.load('wyk player.png') #导入飞机模型图标
playerX = 400 #设置小飞机的初始横坐标
playerY = 500 #设置小飞机的初始纵坐标
playerStep =0 #设置小飞机的移动速度

#设置玩家的得分
score = 0 #玩家的初始得分为0
font = pygame.font.Font('freesansbold.ttf',32) #设置字体和大小

#显示玩家的得分
def show_score():
    text = f"Score:{score}" #设置窗口左上角的玩家得分情况
    score_render = font.render(text, True, (0,255,0)) #设置字体颜色 绿色
    screen.blit(score_render,(10,10)) #设置得分展示的位置

#游戏结束
is_over = False
over_font = pygame.font.Font('freesansbold.ttf',64) #设置 Game Over 的字体和大小

#游戏结束提示信息的设置
def check_is_over():
    if is_over:  #如果游戏结束了
        text = f"Game Over" #设置游戏结束的提示信息
        render = over_font.render(text, True, (255,0,0)) #设置 Game Over 的字体颜色 红色
        screen.blit(render,(200,250)) #设置 Game Over 的显示位置

#攻击对象数量的设置
number_of_enemies = 7  #设置攻击对象的个数

#创建攻击对象类
class Enemy: #创建类
    def __init__(self):
        self.img = pygame.image.load('wyk enemy.png') #导入攻击对象的图片
        self.x = random.randint(200,600) #设置7个攻击对象的随机横坐标
        self.y = random.randint(50,250) #设置7个攻击对象的随机纵坐标
        self.step = random.randint(1,2) #设置7个攻击对象的随机性移动速度

    #当攻击对象被击中时，重置它的位置  复活攻击对象
    def reset(self):
        self.x = random.randint(200,600) #被击中的攻击对象的复活位置 随机横坐标
        self.y = random.randint(50,200) #被击中的攻击对象的复活位置 随机纵坐标

enemies = [] #保存所有的攻击对象
for i in range(number_of_enemies):  #如果游戏窗口内的攻击对象数量小于我们初始设置的数量
    enemies.append(Enemy())  #添加攻击对象

def distance(bx,by,ex,ey): #计算子弹和攻击对象之间的距离
    a = bx - ex #它们的横坐标相减
    b = by - ey #它们的纵坐标相减
    return math.sqrt(a*a + b*b) #开根号，算直线距离
print(distance(3,6,9,14))  #输出（3,6）和（9,14）两点之间的距离 这是游戏制作过程中的功能测试

#创建子弹类
class Bullet: #创建类
    def __init__(self):
        self.img = pygame.image.load('wyk bullet.png') #导入子弹的图片
        self.x = playerX + 16 #设置子弹的横坐标 与小飞机挂钩
        self.y = playerY + 10 #设置子弹的纵坐标 与小飞机挂钩
        self.step = 10 #设置子弹的移动速度

      #子弹击中攻击对象
    def hit(self):
        global score #引用全局变量
        for e in enemies:
            if distance(self.x, self.y, e.x, e.y)< 30:  #距离小于30 认为子弹已经击中目标
                jizhong_sound.play() #播放击中攻击对象的音乐
                bullets.remove(self) #将子弹移除
                e.reset() #调用复活攻击对象的方法
                score += 1 #每击中一个攻击对象 得分加一
                print(score) #输出得分

bullets = [] #保存现有的子弹

#子弹的显示和移动
def show_bullets():
    for b in bullets:
        screen.blit(b.img,(b.x,b.y)) #设置子弹的位置
        b.hit()  #调用子弹击中攻击对象的方法
        b.y -= b.step #设置子弹的移动
        if b.y < 0:  #如果子弹的位置超出了游戏窗口的边界
            bullets.remove(b) #移除子弹

#显示攻击对象，并且实现攻击对象的上下左右移动
def show_enemy():
    global is_over #调用全局变量
    for e in enemies:
        screen.blit(e.img,(e.x,e.y)) #设置攻击对象的位置 
        e.x += e.step #设置攻击对象的移动
        if e.x > 736 or e.x <0: #控制攻击对象在显示窗口里运动
            e.step *= -1 #攻击对象向反方向横向移动
            e.y += 40 #攻击对象向下移动
            if e.y > 420 : #设置游戏结束的条件 玩家失败
                is_over = True  #游戏结束
                print("游戏结束") #输出游戏结束
                enemies.clear() #清空攻击对象 游戏结束`12

def move_player(): #设置小飞机的移动
    global playerX #调用全局变量
    playerX += playerStep  # 设置小飞机的移动

 # 控制小飞机保持在显示窗口界面里运动
    if playerX > 736:  # 如果即将向右出界
        playerX = 736  # 让它不再向右移动
    if playerX < 0:  # 如果即将向左出界
        playerX = 0  # 让它不再向左移动

# 游戏主体的制作
running = True
while running:
    screen.blit(bgImg,(0,0)) #设置背景图片的位置
    show_score() #显示玩家的得分
    for event in pygame.event.get():
        if event.type==pygame.QUIT:  #设置游戏结束
             running = False  #设置程序结束
#用键盘事件控制小飞机的移动
        if event.type ==pygame.KEYDOWN: #设置用键盘按下来操作
            if event.key == pygame.K_RIGHT: #设置按右键的操作
                playerStep = 3 #设置向右移动的速度
            elif event.key == pygame.K_LEFT: #设置按左键的操作
                playerStep = -3 #设置向左移动的速度 //向右移动为正方向
            elif event.key == pygame.K_SPACE: #设置按空格键的操作
                print('发射子弹。。。') #输出 发射子弹。。。
                #创建一颗子弹
                bullets.append(Bullet()) #把子弹加入数组
        if event.type == pygame.KEYUP: #设置松开键盘的操作
            playerStep = 0 #小飞机停止移动

    screen.blit(playerImg,(playerX,playerY)) #设置小飞机初始位置
    move_player() #玩家操控小飞机的移动
    show_enemy() #攻击对象的显示和移动
    show_bullets() #显示子弹
    check_is_over() #显示游戏结束的提示信息
    pygame.display.update()