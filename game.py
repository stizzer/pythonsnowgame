#Ого! Вам правда интересен код?
#Тогда вот вам кот!
'''
*******%%%#(/,*,,,&&&@@(..  *&@@&&&&&&@@@@@@@@@@@@@&&&&&%%%@&%%####%%&/.....,,,*
*******/%%%%%(#/*/,.    .    /@@&&&&&&@@@@@@@@@@@@&&&&&%#&%&&%%####%&&#%&&*.....
*******,*#%%%&%((#(*.....    .#&&&&&&&&&&&&&@@@@&&&&%#/%%&&%%%##%%%%%%%%%%%%&&(.
*////*,,.*%%%%%&%(###(/*.     .%&%%%%%%%%&&&&%&&&&%(/#&&%%%%%##(##%%%##%##%#%%%&
..*.,....,/#%%&&%%%%((#%#/*,,,*&&%%%%%%%%&%%&%%%(//%&%&&&&%%%%(####(##%####%#%%%
..........,%%#%%%&&&&%((((((//**/////****//((#(((%%&&&&&%&&&&&&&%%##/%#%#%%%%%%&
..........,#%#%%#&&%%&&&%%%##///((/,*#######%%%&%%%&&&&&&@&@#&&&&##(#%%%%%%%&&&&
         ..,*%%%%%#%&%%%%%%%#((#%(**/#((%%##%#%&%%&%&&@%&&&&&%%%%&&#%%&&&%%%&&%#
  ...,**/#%#/#%(&%&&#%(%(%/##((/*,,.,(*#%%%##%%%#%&%#%%%&%&%%&%&&&%#%&####%&@@@@
,,/######(//((##%%####(%%#(***/,.....**#(%%%%&&#&%(&%%%&%&&&&&&&%#%%%&@@@@@&%#(/
%###(#(///(/(####%(/#(#%&/*..  .   ..,*/(%#%%%#&##%#&#%&&&%%%##%#(#((##%%&&%(/(#
%##(#*,*/(######((#((#/#/,...  .   ...,*(#%%%&%##%%%%#%%%%##%(#(##(((/(%&&&&@@@@
%%##*,*###%%%%#%%%##%#//,.............,*/%%%&%&%%%%&&%%%%&%###%%(/((((/,.,,/@@@@
###*,*(##%%%%%&&@@@@@@&#**,,,,........,,/#%%%%&&@@@@@&&%&&&&&%%###/(((/*,,,,,,*%
%#(,,*##%%%%%%&&@@&&&@&@&%/**,,......,,,/(#%@@@@@%@@&@@@&&%%%#%%%%&((#(**,,,,,*,
&%(*,*////(/#%((%@@@@@@&&&&*,,.......,,*(#&@&@@@@&@@@@%(%%%##%%#%%(#(//*****,***
&&#*,****/***,*,,(%@&&&&&&@,..... .....,##&@%&&@@@@@%((####%%%%%%####(/***/*****
%%%*,,,,,,.,....   ...  ..,....... .....(%##%,////*,,**#((##%%%%#%((##/***///***
%%%/,,,,,,,,......        ...  .........,.,..     ...,,*/#(%%%%#(/###/***////***
&%#(/,,,,,,..,,,....... ............,.,,...   .......,,*****/((%(###/**////////*
@@@@/********,,,,,,,,,...,,*/**********,.......,,,,,,,,*****/#%###(**/(((///////
@@@#***//************,.....*(%@&@@@@@(,,...,,,,,,,,,*****************/((((//////
@@@/*,**/((//******,*,,,,,,,,,(@@@@/*,,,,,,,,,*,,,,,,,,*****,,,,,,,***(#((((////
@%**,,,,*/###/***************//(#&((****,*,*****,,,,**,*/((*****/*****/#####((//
,*,,,,,,,*/(*,,,,,,**//(/****/((##((//**********/**,,,,,,,,*(//**,,,,**(####((((
,,,,,,,,,,**,........,,***(/**************((//,,...........,(***,,,,****/###((((
,***,,,,,,,.          ...,,,*/*/***,,,*///,.......  ........****,,,,******#####(
//******,,,..            ....,,,*#&&&#,,.........   ........****,,,,********/###
#(///*****,.......   ......... ...*/,.    ... .. .  ........****,,,,,*********(#
%##(//////*,...........          .,.            . .........,****,,,,,,,,*******/
/#(((((((/(//,,........      .  ...              .........,,****,,,*,,********//
/((((((((((##(/,.,.......... ........           .......,,,***************///((((
*/(((((((((#####*,.......................... .........,,*/////////////((((((####
//((((((((((##%%#/*,,,..........,..................,,,*/#((((((((((########%%###
/(#((((((((((######/,*,,.,,,..,,...............,,,,,*####(((((###%%%%######%%###
(##((((((((((((##%####(//*******,........,,,,,,,,/##%####((((####%%#####%%#%####
(##(((((((((((((#####%%%####(#((*,,,,,***,*****(%%%####(((((###########%%%%%####
##(((/////////(((##%%%%%%%%%%%(/////(((((##%##%%%######((############%%%%%######
'''




# Setup Python
import pygame,random,time,math



#Settings

#Display settings
image_scale=3
win_size = (1200, 800)
display_size=(win_size[0]//image_scale,
              win_size[1]//image_scale)


#Images
all_sprites_size=16

#Player movement
player_speed=[2,2] 

#Map
chunksize=8

#Camera
drawdistace=[5,4]
camera_position=[300,900]
camera_position_float=[0,0]
camera_smooth_multiplier=10
camera_indent=[win_size[0]//image_scale//2-8,
               win_size[1]//image_scale//2-8]
camerastatic=[-1,-1]


#FPS
FPS_show=False

#HUD
health=64
beartimer=150


#Player 
playerrotate=False
playerrun=False
eatedbybear=False

#Snow
SnowOnScreenCount=200

#Engine*******************************************************************************************************


animation_database={}
#Static stuff

class Tile:
    def __init__(self,size,permeability):
        self.permeability=permeability
        self.sprite=None
    def set_sprite(self,sprite):
        self.sprite=sprite

#Phisics objects
def collidetest(rect,tiles):
    collidelist=[]
    for i in tiles:
        if rect.colliderect(i):
            collidelist.append(i)
    return collidelist


class Obj_2d(object):
    def __init__(self,x,y,x_size,y_size):
        self.x=x
        self.y=y
        self.width=x_size
        self.height=y_size
        self.rect=pygame.Rect((x,y,x_size,y_size))
    def move(self,movement,platforms=[]):
        self.x+=movement[0]
        self.rect.x=int(self.x)
        collidelist=collidetest(self.rect,platforms)
        collidetypes={'top':False,'bottom':False,'left':False,'right':False}
        for tile in collidelist:
            if movement[0]>0:
                self.rect.right=tile.left
                collidetypes['right']=True
            elif movement[0]<0:
                self.rect.left=tile.right
                collidetypes['left']=True
            self.x=self.rect.x
        self.y+=movement[1]
        self.rect.y=int(self.y)
        collidelist=collidetest(self.rect,platforms)
        for tile in collidelist:
            if movement[1]>0:
                self.rect.bottom=tile.top
                collidetypes['bottom']=True
            elif movement[1]<0:
                self.rect.top=tile.bottom
                collidetypes['top']=True
            self.y=self.rect.y
        return collidetypes

#Entity
class Entity(object):
    def __init__(self,x,y,x_size,y_size,type):
        self.x=x
        self.y=y
        self.x_size=x_size
        self.y_size=y_size
        self.obj=Obj_2d(x,y,x_size,y_size)
        self.type=type
        self.action=None
        self.frame=0
        
    
    def setpos(self,x,y):
        self.x=x
        self.y=y
        self.obj.x=x
        self.obj.y=y
        self.obj.rect.x=x
        self.obj.rect.y=y
        
    def move(self,movement,platforms=[]):
        collisions=self.obj.move(movement,platforms)
        self.x=self.obj.x
        self.y=self.obj.y
        return collisions
    
    def rect(self):
        return pygame.Rect((self.x,self.y,self.x_size,self.y_size))
    
    def set_action(self,action):
        self.action=action
    
    def change_frame(self):
        animation_list=(global_animations_list[self.type][self.action][0])
        animation_mode=(global_animations_list[self.type][self.action][1])
        if animation_mode=='loop':
            if self.frame<len(animation_list)-1:
                self.frame+=1
            else:
                self.frame=0
        if animation_mode=='only':
            if self.frame<len(animation_list)-1:
                self.frame+=1
    
    def display(self,display,scroll,playerrotate):
        
        display.blit(pygame.transform.flip(global_animations_list[self.type][self.action][0][self.frame],playerrotate,False),(self.x-scroll[0],self.y-scroll[1]))
        

        
#Animations & Sprites
global_animations_list={}



def load_sprite(path):
    sprite=pygame.image.load(path)#.convert()
    #sprite.set_colorkey((255,255,255))
    return sprite
    
    

def load_animation(path):
    global global_animations_list
    path=path.split('\\')
    file=open(path[0]+'/'+path[1]+'/'+path[2]+'.txt','r')
    animation_durations=file.read().split(' ')
    file.close()
    if global_animations_list.get(path[1])==None:
        global_animations_list[path[1]]=dict()
    if global_animations_list[path[1]].get(path[2])==None:
        global_animations_list[path[1]][path[2]]=[[],animation_durations[-1]]
    n=0
    for duration in animation_durations[0:-1]:
        n+=1
        animation=load_sprite(path[0]+'/'+path[1]+'/'+path[2]+'/'+str(n)+'.png')
        for i in range(int(animation_durations[n-1])):
            global_animations_list[path[1]][path[2]][0].append(animation)
        



#Game**************************************************************************************************
# Setup pygame/window 
pygame.init()  
title = "Snow Night by Egor Medvedev"
window = pygame.display.set_mode(win_size)  
display=pygame.Surface(display_size)
hud=pygame.Surface(display_size)
pygame.display.set_caption(title)  
clock = pygame.time.Clock()  
pygame.display.set_icon(load_sprite('sprites\\logo.png'))


#Pre Game
window.fill((107,99,143))



# Animations
#e.load_animation('sprites\\character\\idle')
load_animation('sprites\\character\\leftright')
load_animation('sprites\\character\\hold')
load_animation('sprites\\bear\\sleep')
load_animation('sprites\\gift\\blue')
load_animation('sprites\\gift\\red')
load_animation('sprites\\gift\\green')
load_animation('sprites\\streetlight\\idle')
load_animation('sprites\\snow\\idle')
load_animation('sprites\\tree\\idle')
         

# Map
def loadmap(path,startpos,campos):
    f=open(path,'r')
    rawmap=f.read().split('\n')
    f.close()
    width=0
    for line in rawmap:
        if len(line)>width:
            width=len(line)
    width+=(chunksize-width%chunksize)
    for line_index in range(len(rawmap)):
        rawmap[line_index]+='0'*(width-len(rawmap[line_index]))
    for i in range(chunksize-len(rawmap)%chunksize):
        rawmap.append('0'*width)
    chunks={}
    height=len(rawmap)
    for chunk_y in range(height//chunksize): 
        for chunk_x in range(width//chunksize):
            chunk=[[0 for i in range(chunksize)] for j in range(chunksize)]
            for y in range(chunksize):
                for x in range(chunksize):
                    chunk[y][x]=rawmap[chunk_y*chunksize+y][chunk_x*chunksize+x]
            
            chunks[str(chunk_x)+';'+str(chunk_y)]=chunk
    return chunks,startpos,campos


map=loadmap('levels\maps\map.txt',[300,990],False)


def changemap(map):
    return map[0],map[1],map[2]




# Images
lightmap=load_sprite('sprites/map/light.png')
lightmap.set_alpha(95)    
backmap=load_sprite('sprites/map/back.png')
#nightmap=load_sprite('sprites/map/night.png')
#nightmap.set_alpha(80    )    


# Player
player=Entity(50,50,16,16,'character')
player.set_action('leftright')
keyboardinput={'up':False,'down':False,'left':False,'right':False}



# FPS
lasttime=time.time()
fpsk=0

actualmap,spawnpos,staticcampos=changemap(map)
player.setpos(spawnpos[0],spawnpos[1])


# Objects
bear=Entity(1030,160,30,25,'bear')
bear.set_action('sleep')
gifts=[]
gifts.append(Entity(1000,180,7,10,'gift'))
gifts.append(Entity(1415,1055,7,10,'gift'))
gifts.append(Entity(1420,1040,7,10,'gift'))
gifts[0].set_action('red')
gifts[1].set_action('blue')
gifts[2].set_action('green')
streetlights=[]
streetlights.append(Entity(1040,650,7,45,'streetlight'))
streetlights.append(Entity(1322,650,7,45,'streetlight'))
streetlights.append(Entity(1445,650,7,45,'streetlight'))
streetlights.append(Entity(1640,650,7,45,'streetlight'))
for i in range(len(streetlights)):
    streetlights[i].set_action('idle')

# Tree
tree=Entity(1427,1016,40,53,'tree')
tree.set_action('idle')

# Snow
def GenerateSnow(): 
    return ([random.randint(-200,win_size[0]//image_scale),-10],(random.randint(150,200)/100,random.randint(2,3)),5,5,random.randint(0,4))

Snows=[]
for i in range(5):
    size=5
    Snows.append(GenerateSnow())
for a in range(200):
    newSnows=[]
    for i in range(len(Snows)):
        Snows[i][0][0]+=Snows[i][1][0]
        Snows[i][0][1]+=Snows[i][1][1]
        display.blit(global_animations_list['snow']['idle'][0][Snows[i][4]-1],(Snows[i][0][0],Snows[i][0][1]))
        if  Snows[i][0][0]>win_size[0]//image_scale:
            continue
        newSnows.append(Snows[i])
    Snows=newSnows
    while len(Snows)<SnowOnScreenCount:
        Snows.append(GenerateSnow())

# Player Gift Holding
Hold=False

# Text and Menu stuff
def drawText(text,Surface,pos,color,font,size):
    apples = pygame.font.SysFont('arial', size)
    #apples = pygame.font.Font(font, size)
    applest = apples.render(text, 2, color)
    Surface.blit(applest, pos)


# Menu

#Tunel
class Snowflake:
    def __init__(self):
        self.pos3=self.GenPos3()
        self.speed=random.randint(50,100)/1000
        self.size=0.25
        
        
    def GenPos3(self):
        return [random.randint(1,win_size[0]),random.randint(1,win_size[1] ),-100.01]
    
    
    def Update(self):
        self.pos3[2]+=self.speed
        if self.pos3[2]>=0:
            self.pos3=self.GenPos3()
        
    def Draw(self,window):
        a=self.size/(-  self.pos3[2])*100
        pygame.draw.rect(window, (255,255,255),(self.pos3[0]/(-self.pos3[2])  ,self.pos3[1]/(-self.pos3[2]) ,a,a),0)
        
        
class Snow:
    def __init__(self,snowCount):
        self.snow=[Snowflake() for i in range(snowCount)]
    def Update(self):
        [snowflake.Update() for snowflake in self.snow]
     
    def Run(self,window):
        [snowflake.Update() for snowflake in self.snow]
        [snowflake.Draw(window) for snowflake in self.snow]

def F(x,y,z):
    return(x/z,y/z)

class Button:
    def __init__(self, x,y,sx,sy,sprite,csprite,action):
        self.x=x
        self.y=y
        self.sx=sx
        self.sy=sy
        self.sprite=sprite
        self.clicksprite=csprite
        self.clicked=0
        self.action=action
    def Update(self,pos,press):
        mouserect=pygame.Rect(pos[0],pos[1],1,1)
        buttrect=pygame.Rect(self.x,self.y,self.sx,self.sy)
        if self.clicked==1 and not press[0] and mouserect.colliderect(buttrect):
            self.action()
        if mouserect.colliderect(buttrect) and press[0]:
            self.clicked=1
        else:
            self.clicked=0       
    def ShowRect(self,window):
        c=100*(self.clicked+0.3)
        pygame.draw.rect(window,(c,c,c),(self.x,self.y,self.sx,self.sy),0)
start=False
def stt():
    global start
    start=True
snow=Snow(1000)   
for i in range(1000):
    snow.Update()


def Menu():
    Start=Button(100,100+200,400,100,None,None,stt)
    Exit=Button(100,300+200,400,100,None,None,exit)
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    return False
        pos = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()
        window.fill((107,99,143))
        snow.Run(window)
        Start.ShowRect(window)
        Start.Update(pos,press)
        drawText('Играть',window,(120,100+200),(100,255,200),'calibri',70)
        Exit.ShowRect(window)
        Exit.Update(pos,press)
        drawText('Выход',window,(120,300+200),(255,100,100),'calibri',70)
        if start:
            return True
        clock.tick(60)
        pygame.display.flip() 













GameRun=Menu()
# Loop
while GameRun:
    #Background
    display.fill((107,99,143))
    
    
    #FPS
    fpsk+=1
    if time.time()-lasttime>1:
        if FPS_show:  print('FPS: ',int(fpsk/1))
        fpsk=0
        lasttime=time.time()
   
    #Camera
    camera_position_float[0]+=(player.x-camera_position_float[0]-camera_indent[0])/camera_smooth_multiplier
    camera_position_float[1]+=(player.y-camera_position_float[1]-camera_indent[1])/camera_smooth_multiplier
    
    camera_position[0]=int(camera_position_float[0])
    camera_position[1]=int(camera_position_float[1])
    
    if staticcampos:
        camera_position=[16,16]
     

  
    #Player movement
    player_movement_vector=[0,0]
    if keyboardinput['up']:
        player_movement_vector[1]-=player_speed[1]
    if keyboardinput['down']:
        player_movement_vector[1]+=player_speed[1]
    if keyboardinput['left']:
        player_movement_vector[0]-=player_speed[0]
    if keyboardinput['right']:
        player_movement_vector[0]+=player_speed[0]
    
    
    if (player_movement_vector[0]!=0 or player_movement_vector[1]!=0):
        playerrun=True
        player.set_action('leftright')
    else:
        playerrun=False
        
    #    player.set_action('idle')
    if player_movement_vector[0]<0:
        playerrotate=False
    if player_movement_vector[0]>0:
        playerrotate=True
    
    #Keyboard input
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                pygame.quit()
                quit()
            if event.key==pygame.K_RIGHT:
                keyboardinput['right']=True
            if event.key==pygame.K_LEFT:
                keyboardinput['left']=True
            if event.key==pygame.K_UP:
                keyboardinput['up']=True
            if event.key==pygame.K_DOWN:
                keyboardinput['down']=True
            
            if event.key==pygame.K_KP6:
                player.setpos(player.x+100,player.y)
            if event.key==pygame.K_KP4:
                player.setpos(player.x-100,player.y)
            if event.key==pygame.K_KP8:
                player.setpos(player.x,player.y-100)
            if event.key==pygame.K_KP2:
                player.setpos(player.x,player.y+100)
            
            
            '''
            if event.key==pygame.K_w:
                actualmap,spawnpos,staticcampos=changemap(lobbymap)
                player.setpos(spawnpos[0],spawnpos[1])
            if event.key==pygame.K_a:
                actualmap,spawnpos,staticcampos=changemap(map1)
                player.setpos(spawnpos[0],spawnpos[1])
            '''
            if event.key==pygame.K_c:
                Hold=True
            if event.key==pygame.K_v:
                Hold=False

                    
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT:
                keyboardinput['right']=False
            if event.key==pygame.K_LEFT:
                keyboardinput['left']=False
            if event.key==pygame.K_UP:
                keyboardinput['up']=False
            if event.key==pygame.K_DOWN:
                keyboardinput['down']=False
    #Tiles
    tiles=[]
    for y in range(drawdistace[1]):
        targety=y-1+int(round(camera_position[1]/(8*16)))
        for x in range(drawdistace[0]):
            targetx=x-1+int(round(camera_position[0]/(8*16)))   
            targetchunk=str(targetx)+';'+str(targety)
            if targetchunk not in actualmap:
                chunk=[[0 for j in range(chunksize)] for i in range(chunksize)]
            else:
                chunk=actualmap[targetchunk]
            for tile_y in range(chunksize):
                for tile_x in range(chunksize):
                    if str(chunk[tile_y][tile_x])=='1':
                        tiles.append(pygame.Rect((tile_x*16+targetx*16*8,tile_y*16+targety*8*16,16,15)))


    #Eating 
    if eatedbybear==0:
        eatedbybear=-1
    if player.rect().colliderect(bear.rect()):
        print("Ваc съел медведь")
        eatedbybear=beartimer
        player.setpos(spawnpos[0],spawnpos[1])
        camera_position_float[0]+=(player.x-camera_position_float[0]-camera_indent[0])
        camera_position_float[1]+=(player.y-camera_position_float[1]-camera_indent[1])
        if Hold==True:
            Hold=False
            gifts[0].setpos(1072,165)
    
    #Map
    display.blit(backmap,(-camera_position[0],-camera_position[1]-16))
    
    #Objects Collide
    for i in streetlights:
        tiles.append(i.rect())
    if Hold==False:
        for i in gifts:
            tiles.append(i.rect())
    tiles.append(tree.rect())
    
    #Main game script
    if Hold==False and gifts[0].rect().colliderect(pygame.Rect(player.x-1,player.y-1,player.x_size+2,player.y_size+2)):
        Hold=True
        #print('lets go')
    if Hold==True:
        gifts[0].setpos(player.x+(15 if playerrotate else -6),player.y-5)
    if Hold==True and player.rect().colliderect(pygame.Rect(tree.x-1,tree.y-1,tree.x_size+2,tree.y_size+2)):
        #print('ok')
        Hold="Done"
    if Hold=="Done":
        gifts[0].setpos(1467+5,1050+3)
        print('End')
    
    #Player
    if Hold==True:
        player.set_action('hold')
    else:
        player.set_action('leftright')
    if playerrun:
        player.change_frame()
    else:
        player.frame=0
    player.display(display,(camera_position[0],camera_position[1]+4),playerrotate)
    player.move(player_movement_vector,tiles)

    #Objects
    bear.display(display,(camera_position[0],camera_position[1]),False)
    bear.change_frame()

    for i in gifts:
        i.display(display,(camera_position[0],camera_position[1]),False)
    

    for i in streetlights:
        i.display(display,(camera_position[0],camera_position[1]),False)
    
    #Tree
    tree.change_frame()
    tree.display(display,camera_position,False)
    
    # Snow
    
    newSnows=[]
    for i in range(len(Snows)):
        Snows[i][0][0]+=Snows[i][1][0]
        Snows[i][0][1]+=Snows[i][1][1]
        
        display.blit(global_animations_list['snow']['idle'][0][Snows[i][4]-1],(Snows[i][0][0],Snows[i][0][1]))
        
        if  Snows[i][0][0]>win_size[0]//image_scale:
            continue
        newSnows.append(Snows[i])
    Snows=newSnows
    while len(Snows)<SnowOnScreenCount:
        Snows.append(GenerateSnow())
    

    #Post Processing
    #display.blit(nightmap,(-camera_position[0],-camera_position[1]-16))
    display.blit(lightmap,(-camera_position[0],-camera_position[1]-16))
    
    
    
    #Rendering
    window.blit(pygame.transform.scale(display,win_size),(0,0))
    #window.blit(hud,(0,0))
    
    #pygame.time.delay(10)  
    # Hud
    fontsize=70
    fontcolor=(232,191,102)
    if eatedbybear>0:
        eatedbybear-=1
        drawText('Вас съел медведь',window,(100,100),(255,255,255),'calibri',70)
    else:
        if Hold==False:
            drawText('Найдите подарок',window,(100,100),fontcolor,'calibri',fontsize)
            drawText('(красный)',window,(100,170),(255,100,100),'calibri',fontsize-30)
        if Hold==True:
            drawText('Отнесите подарок к ёлке',window,(100,100),fontcolor,'calibri',fontsize)
        if Hold=='Done':
            drawText('Спасибо за игру!',window,(100,100),fontcolor,'calibri',fontsize)

    
    clock.tick(60)
    pygame.display.flip() 

  
