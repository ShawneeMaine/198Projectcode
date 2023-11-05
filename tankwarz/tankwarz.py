
import wx,random,string,os,pygame,math
import  wx.html as  html
import  wx.lib.wxpTag
import  wx.lib.mixins.listctrl  as  listmix
import sys
from time import gmtime, strftime






global mineexp,mineimg,trackerimg,heshot,grapeshot,silvershot,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
pygame.init()
inf=pygame.display.Info()
width= int(inf.current_w)
height =int(inf.current_h)
startdir=os.getcwd()
size = width, height


screen = pygame.display.set_mode((1,1))
maxwidth=5000
maxheight=5000
pork3 = pygame.Surface((maxwidth,maxheight),flags = 0, )
pork5 = pygame.Surface((maxwidth,maxheight),flags = 0, ).convert_alpha()
road = pygame.image.load(startdir+"/images/road.png")
notroad = pygame.image.load(startdir+"/images/notroad1.png")
notroadrock = pygame.image.load(startdir+"/images/notroadwithrock.png")
road_notroad = []
rectroad_rectnotroad = []
input=open(startdir+"/images/roadmap1.txt","r+",1000000)
roadmap=input.readlines()
counta=-1
countb=-1
countc=0
tanks=0
deekson=False
gason=False
maxmoney=0
editon=True

missimg=pygame.image.load(startdir+"/images/missile.png")
trackerimg=pygame.image.load(startdir+"/images/trackermiss.png")
heshot=pygame.image.load(startdir+"/images/hemiss.png")
grapeshot=pygame.image.load(startdir+"/images/grapemiss.png")
silvershot=pygame.image.load(startdir+"/images/silvermiss.png")
missexp=pygame.image.load(startdir+"/images/explode.png")
mineimg=pygame.image.load(startdir+"/images/mine.png")
mineexp=pygame.image.load(startdir+"/images/explode.png")


for a in roadmap:
    counta=counta+1
    countb=0
    for b in a:
        if b == " ":
            road_notroad.append(notroad)
        if b == "1":
            road_notroad.append(road)
        if b == "0":
            road_notroad.append(notroadrock)
        countb=countb+1
for a in range (0,counta):
    for b in range (0,countb):
        rectroad_rectnotroad.append(road_notroad[a*countb+b].get_rect())
        rectroad_rectnotroad[a*countb+b].left = (b*20)
        rectroad_rectnotroad[a*countb+b].top = (a*20)
        pork3.blit(road_notroad[a*countb+b],rectroad_rectnotroad[a*countb+b])
maxwidth=countb*20
maxheight=counta*20
#ghost map MUAHAHAHAHA
pork4=pork3.copy()
#sounds
pygame.mixer.init()
exp=pygame.mixer.Sound(startdir+"/audio/explode.ogg")
fire=pygame.mixer.Sound(startdir+"/audio/fire.ogg")
eng=pygame.mixer.Sound(startdir+"/audio/engine.ogg")


backmusic=[pygame.mixer.Sound(startdir+"/audio/back1.ogg"),pygame.mixer.Sound(startdir+"/audio/back2.ogg"),pygame.mixer.Sound(startdir+"/audio/back3.ogg")]
backmusic=random.sample(backmusic,1)[0]

OriginalTanks=[]
#build the screen for viewing here


TankCount=0
TankIndex=[]
MissileIndex=[]
MineIndex=[]
GameRun=False
mastererror=0

#name,weight,destruction,area,cost,speed,type,targetable,range
ammodata={  'Standard HE':["Standard HE",2000,1000,30,800,14,0,False,450],
            'Silver Bullet':["Silver Bullet",2500,2000,15,1200,18,1,False,550],
            'Tracker':["Tracker",5000,1500,30,3200,12,3,True,600],
            'Grapeshot':["Grapeshot",1500,750,45,400,9,2,False,250]}
#name,weight,destruction,range,area,cost,type,targetable,speed
minedata={  'Dumb':["Dumb",1000,2000,50,30,500,0,False,20],
            'HE Dumb':["HE Dumb",1500,4000,80,40,1000,1,False,20],
            'Proximity':["Proximity",2500,2000,50,30,1500,2,True,30],
            'High Proximity':["High Proximity",3000,4000,80,40,2000,3,True,30]}
#name,weight,strength,damage,cost
armordata={ 'Steel':["Steel",2000,2000,100,1500],
            'Aluminum':["Aluminum",1000,1500,100,2000],
            'Titanium':["Titanium",1250,3000,100,2500],
            'Ceramic':["Ceramic",750,3500,100,3000]}
#name,weight,accuracy,rateoffire,cost,loaded,count,range
gunnerydata={'Standard':["Standard",3500,8,70,1600,True,0,300],
            'Short Range':["Short Range",2500,20,50,1200,True,0,200],
            'Long Range':["Long Range",4500,3,100,2000,True,0,500],
            'German Made':["German Made",4000,3,40,2500,True,0,400],
            'Mini Gun':["Mini Gun",4000,2,15,5000,True,0,400],
            'GMC':["GMC",2000,25,110,800,True,0,250]}
#name,weight,capacity,strength,damage,cost
chassisdata={'Light':["Light",10000,5,2000,100,800],
            'Medium':["Medium",15000,7,3000,100,1600],
            'Composite':["Composite",3000,10,4000,100,3200],
            'Heavy':["Heavy",20000,10,4000,100,2400]}
#name,weight,horsepower,cost
enginedata={"Johnson":["Johnson",5000,1000,1500],
            "Toyota":["Toyota",6500,500,750],
            "Cummings":["Cummings",10000,1500,2250],
            "Rolls-Royce":["Rolls-Royce",10000,2000,3000]}
#name,weight,strength,duration,damage,cost
decoydata={ 'Low-Grade':["Low-Grade",150,10,20,100,500],
            'Mid-Grade':["Mid-Grade",250,20,40,100,800],
            'High-Grade':["High-Grade",400,40,80,100,1200],
            'High-Tech':["High-Tech",300,100,120,100,1500]}
#name,weight,capacity,cost
fueldata={  'Cheap':["Cheap",1000,500,500],
            'Mediocre':["Mediocre",2000,1000,2000],
            'Nice':["Nice",3000,1500,4000]}
#name,weight,fixed,maxrange,range,arc,maxarc,cost
scannerdata={'Standard':["Standard",200,False,30,30,35,35,1000],
            'Short Range':["Short Range",100,False,15,15,60,60,600],
            'Long Range':["Long Range",400,False,50,50,20,20,1400],
            'High-End Model':["High-End Model",300,False,50,50,25,25,1800]}


#AI DICTIONARIES
keyword_list={"switch":0,"set":1,"call":2,"eval":3,"function":4}
arg_list={"variable":0,"constant":1,"function":2,"eval":3,"canned":4,"double":5,"single":6}
function_list={}
variable_list={}
statement_list={"switch":0,"set":1,"call":2,"exit":3,"return":4,"canned":5,"loop":6}
operator_list={"+":5,"-":6,"*":2,"/":3,"^":1,"%":4}
sep_list=["+","-","*","/","^","%","(",")"]
operator_list2={6:"+",5:"-",2:"*",3:"/",1:"^",4:"%"}
operators=range(0,6)
comp_list1={"==":0,">=":1,"<=":2,">":3,"<":4,"!=":5}
comp_list2={0:"==",1:">=",2:"<=",3:">",4:"<",5:"!="}
#term can be any arg_list type, or a combination of them based on an operator
keywords_list={"if":0,"else":1,"endif":2,"while":3,"endwhile":4,"call":5,"set":6,"return":7,"break":8,"continue":9,"exit":10}

def get_money(self):
    money=self.Money
    for mc in self.ammo.amlist:
        money=money+mc.cost
    for mc in self.mine.mmlist:
        money=money+mc.cost
    for mc in self.armor.alist:
        money=money+mc.cost
    for mc in self.chassis.chaslist:
        money=money+mc.cost
    for mc in self.engine.elist:
        money=money+mc.cost
    for mc in self.scanner.slist:
        money=money+mc.cost
    for mc in self.gunnery.glist:
        money=money+mc.cost
    return money
    
    
def puttext(surf,pos,text,font,size,color,flag):
    fontrend=pygame.font.Font(font,size)
    textrend=fontrend.render(text,1,color)
    if flag=="center":
        textpos=textrend.get_rect()
        textpos.centerx=surf.get_rect().centerx
    elif flag == "left":
        textpos=(surf.get_rect().left+2,surf.get_rect().top)
    elif flag=="right":
        textpos=(surf.get_rect().right-textrend.get_rect().width-2,surf.get_rect().top)
    else:
        textpos=pos
    surf.blit(textrend,textpos)


class can_print():
    def __init__(self,parent,terms):
        self.terms=terms
    def execute(self):
        #args is a list of arguments
        app.frame.Output.AppendText(str(self.terms[0].evaluate())+"\n")
        print (self.terms[0].evaluate())

def can_scan_tank(tank,sc_tank_id):
    #check to see if tank id tank is in range of scanners
    #return True if it is
    #return false if it isn't
    distlow=1000000
#    print "Target ID" , sc_tank_id
    targid=sc_tank_id.PlayerIdent
    to180=180-tank.scanner.slist[0].angle
    lowangle=(180-int(tank.scanner.slist[0].arc/2))%360
    highangle=(180+int(tank.scanner.slist[0].arc/2))%360
    if not sc_tank_id.Dead:
        dist=math.sqrt((sc_tank_id.xpos-tank.xpos)*(sc_tank_id.xpos-tank.xpos)+(sc_tank_id.ypos-tank.ypos)*(sc_tank_id.ypos-tank.ypos))
        angle=(get_angle(tank.xpos,sc_tank_id.xpos,tank.ypos,sc_tank_id.ypos)+to180)%360
        if dist<tank.scanner.slist[0].range and angle<highangle and angle>lowangle and dist<distlow:
            dist=distlow
            return True
    return False

def get_angle(x1,x2,y1,y2):
    #returns an angle from object 1 to object2
    difx=x2-x1
    dify=y2-y1
    angle=0
    if int(difx) == 0:
        delx = 0
    elif difx>0:
        delx=1
    else:
        delx=-1
    if int(dify) == 0:
        dely = 0
    elif dify>0:
        dely=1
    else:
        dely=-1
    if delx == -1 and dely == -1:
    #up left
        angle=(90+abs(90-180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14))
    if delx == -1 and dely == 1:
    #down left
        angle=(180+abs(180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14))
    if delx == 1 and dely == -1:
    #up right
       angle=(180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14)
    if delx == 1 and dely == 1:
    #down right
       angle=(270+(abs(90-180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14)))
    if delx==0 and dely==1:
        angle=270
    if delx==0 and dely==-1:
        angle=90
    if delx==1 and dely==0:
        angle=0
    if delx==-1 and dely==0:
        angle=180
    return angle

def set_angle(x1,y1,x2,y2,angle2):
    #returns an angle from object 1 to object2
    difx=x2-x1
    dify=y2-y1
    angle=0
    if int(difx) == 0:
        delx = 0
    elif difx>0:
        delx=1
    else:
        delx=-1
    if int(dify) == 0:
        dely = 0
    elif dify>0:
        dely=1
    else:
        dely=-1
    if delx == -1 and dely == 1:
    #up left
        angle=(90+abs(90-180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14))
    if delx == -1 and dely == -1:
    #down left
        angle=(180+abs(180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14))
    if delx == 1 and dely == 1:
    #up right
       angle=(180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14)
    if delx == 1 and dely == -1:
    #down right
       angle=(270+(abs(90-180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14)))
    if delx==0 and dely==-1:
        angle=270
    if delx==0 and dely==1:
        angle=90
    if delx==1 and dely==0:
        angle=0
    if delx==-1 and dely==0:
        angle=180
    angle=(angle+angle2)%360
    y3=y1+math.sqrt(difx*difx+dify*dify)*math.sin(angle*3.14159/180)
    x3=x1+math.sqrt(difx*difx+dify*dify)*math.cos(angle*3.14159/180)
    
    return (x3,y3)

class can_fire():
    def __init__(self,parent,terms):
        # holds all of the canned functions\
        # first index is always the parent the rest are the arguments passed to this function
        #create missile object here, and give it a destination and a position and a velocity
        #terms index    meaning
        #       0 xpos destination 
        #       1 ypos destination
        self.terms=terms
        self.parent=parent
        if len(terms)<2:
            self.terms=[0,0]
    def execute(self):
        if self.parent.tank.currentammo!=None:
            dist=math.sqrt((self.parent.tank.xpos-self.terms[0].evaluate())*(self.parent.tank.xpos-self.terms[0].evaluate())+(self.parent.tank.ypos-self.terms[1].evaluate())*(self.parent.tank.ypos-self.terms[1].evaluate()))
            if self.parent.tank.gunnery.glist[0].loaded==True and dist<self.parent.tank.gunnery.glist[0].range:
                tup=set_angle(self.parent.tank.xpos,self.parent.tank.ypos,self.terms[0].evaluate(),self.terms[1].evaluate(),random.randint(-1*self.parent.tank.gunnery.glist[0].accuracy,self.parent.tank.gunnery.glist[0].accuracy))
                newmiss=Missile(self.parent.tank)
                MissileIndex.append(newmiss)
                indx=len(MissileIndex)-1
                newmiss.xpos=self.parent.tank.xpos
                newmiss.ypos=self.parent.tank.ypos
                newmiss.index=indx
                newmiss.range=self.parent.tank.gunnery.glist[0].range
#                newmiss.range=self.parent.tank.currentammo.range
                newmiss.destx=tup[0]+(self.parent.tank.tankwidth/2)
                newmiss.desty=tup[1]+(self.parent.tank.tankheight/2)
                newmiss.speed=self.parent.tank.currentammo.speed 
                newmiss.type=self.parent.tank.currentammo
                self.parent.tank.gunnery.glist[0].loaded=False
                self.parent.tank.gunnery.glist[0].reloadtime=0
                #fire weapon function call here.
                fire.play()
                return 0
            else:
                return 1
        else:
            return 1

class can_firetrack():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.target=int(terms[0].evaluate())
        self.parent=parent
    def execute(self):
        if self.parent.tank.currentammo!=None:
            if self.target<=len(TankIndex) and self.target>=0 and can_scan_tank(self.parent.tank,TankIndex[self.target]) and self.parent.tank.gunnery.glist[0].loaded==True:
                #find future point of intersection
                vx=TankIndex[self.target].velox
                vy=TankIndex[self.target].veloy
                x2=TankIndex[self.target].xpos
                y2=TankIndex[self.target].ypos
                x1=self.parent.tank.xpos
                y1=self.parent.tank.ypos
                speed=self.parent.tank.currentammo.speed
                dist=math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
                time=0
                x2a=x2+vx*time
                y2a=y2+vy*time
                time=dist/speed
                x2b=0
                y2b=0
                ddist1=0
                ddist1a=100000000000
                while abs(x2a-x2b)>abs(vx) and abs(y2a-y2b)>abs(vy):
                    x2b=x2a
                    y2b=y2a
                    x2a=x2+vx*time
                    y2a=y2+vy*time
                   # print x1,x2a,y1,y2a,dist,time
                    dist=math.sqrt((x1-x2a)*(x1-x2a)+(y1-y2a)*(y1-y2a))
                    time=dist/speed
                    ddist1=abs(math.sqrt((x2-x2a)*(x2-x2a)+(y2-y2a)*(y2-y2a))-math.sqrt((x2-x2b)*(x2-x2b)+(y2-y2b)*(y2-y2b)))
                   # print ddist1,ddist1a
                    if ddist1>=ddist1a:
                        break
                    else:
                        ddist1a=ddist1
                    if x2a > 1000 or y2a > 1000:
                        break
                if dist<self.parent.tank.gunnery.glist[0].range:
                    tup=set_angle(x1,y1,x2a,y2a,random.randint(-1*self.parent.tank.gunnery.glist[0].accuracy,self.parent.tank.gunnery.glist[0].accuracy))
                    newmiss=Missile(self.parent.tank)
                    MissileIndex.append(newmiss)
                    indx=len(MissileIndex)-1
                    newmiss.xpos=self.parent.tank.xpos
                    newmiss.ypos=self.parent.tank.ypos
                    newmiss.index=indx
                    newmiss.destx=tup[0]
                    newmiss.desty=tup[1]
##                    newmiss.desty=tup[1]+(self.parent.tank.tankheight/2)
                    newmiss.speed=self.parent.tank.currentammo.speed 
                    newmiss.range=self.parent.tank.gunnery.glist[0].range
                    newmiss.type=self.parent.tank.currentammo
                    self.parent.tank.gunnery.glist[0].loaded=False
                    self.parent.tank.gunnery.glist[0].reloadtime=0
                    #fire weapon function call here.
                    fire.play()
                    return 0
                else:
                    return 1
            else:
                return 1
        else:
            return 1
            

class can_firetarget():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.target=int(terms[0].evaluate())
        self.parent=parent
    def execute(self):
        if self.parent.tank.currentammo!=None:
            dist=math.sqrt((TankIndex[self.target].xpos-self.parent.tank.xpos)*(TankIndex[self.target].xpos-self.parent.tank.xpos)+(TankIndex[self.target].ypos-self.parent.tank.ypos)*(TankIndex[self.target].ypos-self.parent.tank.ypos))
            if self.target<=len(TankIndex) and self.target>=0 and can_scan_tank(self.parent.tank,TankIndex[self.target]) and self.parent.tank.gunnery.glist[0].loaded==True and self.parent.tank.gunnery.glist[0].range>=dist and self.parent.tank.currentammo.track and self.target!=self.parent.tank.PlayerIdent:
                newmiss=Missile(self.parent.tank)
                MissileIndex.append(newmiss)
                indx=len(MissileIndex)-1
                newmiss.xpos=self.parent.tank.xpos
                newmiss.ypos=self.parent.tank.ypos
                newmiss.index=indx
                newmiss.destx=500
                newmiss.desty=500
                newmiss.speed=self.parent.tank.currentammo.speed 
                newmiss.range=self.parent.tank.gunnery.glist[0].range
                #newmiss.range=self.parent.tank.currentammo.range
#                print "Ammo Range: ",range
#                print "Target: ",self.target
                
                newmiss.type=self.parent.tank.currentammo
                newmiss.offsetx1=random.randint(-1*self.parent.tank.gunnery.glist[0].accuracy,self.parent.tank.gunnery.glist[0].accuracy)
                newmiss.offsety1=random.randint(-1*self.parent.tank.gunnery.glist[0].accuracy,self.parent.tank.gunnery.glist[0].accuracy)
                self.parent.tank.gunnery.glist[0].loaded=False
                self.parent.tank.gunnery.glist[0].reloadtime=0
                newmiss.targetid=self.target
                #fire weapon function call here.
                fire.play()
                return 0
            else:
                return 1
        else:
            return 1

class can_minedrop():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.parent=parent
    def execute(self):
        if self.parent.tank.currentmine!=None:
            if self.parent.tank.currentmine.loaded:
                newmine=LandMine(self.parent.tank)
                MineIndex.append(newmine)
                indx=len(MineIndex)-1
                newmine.xpos=self.parent.tank.xpos-(self.parent.tank.velox/abs(self.parent.tank.velox+.000000001))*(1.1*(self.parent.tank.currentmine.proximity+30))
                newmine.ypos=self.parent.tank.ypos-(self.parent.tank.veloy/abs(self.parent.tank.veloy+.000000001))*(1.1*(self.parent.tank.currentmine.proximity+30))
                newmine.index=indx
                newmine.type=self.parent.tank.currentmine
                if self.parent.tank.currentmine.track:
                    newmine.targetid=self.parent.tank.currentmine.target
                newmine.proximity=self.parent.tank.currentmine.proximity
                self.parent.tank.currentmine.loaded=False
                self.parent.tank.currentmine.loading=0
                #fire weapon function call here.
                fire.play()


class can_ammoset():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.parent=parent
    def execute(self):
        #args is a list of arguments
        #set the scanner parameters here 
        #terms index    meaning
        #       0 ammoindex
        if self.parent.tank.currentammo!=None:
            if self.terms[0].evaluate()>=len(self.parent.tank.ammo.amlist) or self.terms[0].evaluate()<0:
                self.parent.tank.currentammo=self.parent.tank.ammo.amlist[0]
                return 0
            else:
                self.parent.tank.currentammo=self.parent.tank.ammo.amlist[int(self.terms[0].evaluate())]
                return self.terms[0].evaluate()

class can_mineset():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.parent=parent
    def execute(self):
        #args is a list of arguments
        #set the scanner parameters here 
        #terms index    meaning
        #       0 ammoindex
        if self.parent.tank.currentmine!=None:
            if self.terms[0].evaluate()>=len(self.parent.tank.mine.mmlist) or self.terms[0].evaluate()<0:
                self.parent.tank.currentmine=self.parent.tank.mine.mmlist[0]
                return 0
            else:
                self.parent.tank.currentmine=self.parent.tank.mine.mmlist[int(self.terms[0].evaluate())]
                return self.terms[0].evaluate()

class can_minesettarget():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.target=int(terms[0].evaluate())
        self.parent=parent
    def execute(self):
        #args is a list of arguments
        #set the scanner parameters here 
        #terms index    meaning
        #       0 ammoindex
        if self.parent.tank.currentmine!=None:
            self.target=int(self.terms[0].evaluate())
            if self.target<0 or self.target>len(TankIndex)-1 or not self.parent.tank.currentmine.track:
                return -1
            if self.target<=len(TankIndex) and self.target>=0:
                self.parent.tank.currentmine.target=self.target
                return 0
            else:
                return -1

class can_minesetproximity():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.parent=parent
    def execute(self):
        #args is a list of arguments
        #set the scanner parameters here 
        #terms index    meaning
        #       0 ammoindex
        if self.parent.tank.currentmine!=None:
            if self.terms[0].evaluate()>self.parent.tank.currentmine.range:
                self.parent.tank.currentmine.proximity=self.parent.tank.currentmine.range
                return self.parent.tank.currentmine.range
            elif self.terms[0].evaluate()<=0:
                self.parent.tank.currentmine.proximity=0
                return 0
            else:
                self.parent.tank.currentmine.proximity=self.terms[0].evaluate()
                return self.terms[0].evaluate()

class can_scansetarc():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.parent=parent
    def execute(self):
        #args is a list of arguments
        #set the scanner parameters here 
        #terms index    meaning
        #       0 arc(if over max, then set to max, if under 1 set to 1
#        if not self.parent.tank.scanner.slist[0].fixed:
#        self.parent.tank.scancircle.fill((0,0,0,0))
        self.parent.tank.scanner.slist[0].arc=self.terms[0].evaluate()
        if self.parent.tank.scanner.slist[0].arc>359:
            self.parent.tank.scanner.slist[0].arc=359
        self.parent.tank.scanner.slist[0].range=int(math.sqrt(self.parent.tank.scanner.slist[0].area*360/(3.14*self.parent.tank.scanner.slist[0].arc)))
        self.parent.tank.scancircle=pygame.Surface((self.parent.tank.scanner.slist[0].range*2,self.parent.tank.scanner.slist[0].range*2)).convert_alpha()
        self.parent.tank.scancircle.fill((0,0,0,0))
        pygame.draw.arc(self.parent.tank.scancircle, (30,30,220,55), pygame.Rect((0,0),(self.parent.tank.scanner.slist[0].range*2,self.parent.tank.scanner.slist[0].range*2)), 6.28*(self.parent.tank.scanner.slist[0].angle-self.parent.tank.scanner.slist[0].arc/2)/360, 6.28*(self.parent.tank.scanner.slist[0].angle+self.parent.tank.scanner.slist[0].arc/2)/360,self.parent.tank.scanner.slist[0].range)
        return self.parent.tank.scanner.slist[0].arc

class can_scansetrange():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.parent=parent
    def execute(self):
        #args is a list of arguments
        #set the scanner parameters here 
        #terms index    meaning
        #       0 arc(if over max, then set to max, if under 1 set to 1
#        self.parent.tank.scancircle.fill((0,0,0,0))
        if int(self.terms[0].evaluate())*int(self.terms[0].evaluate())>=self.parent.tank.scanner.slist[0].area/3.14:
            self.parent.tank.scanner.slist[0].range=int(self.terms[0].evaluate())
        else:
            self.parent.tank.scanner.slist[0].range=int(math.sqrt(self.parent.tank.scanner.slist[0].area/3.14))
        self.parent.tank.scanner.slist[0].arc=int(360*self.parent.tank.scanner.slist[0].area/(3.14*self.parent.tank.scanner.slist[0].range*self.parent.tank.scanner.slist[0].range))
        if self.parent.tank.scanner.slist[0].arc>359:
            self.parent.tank.scanner.slist[0].arc=359
        self.parent.tank.scancircle=pygame.Surface((self.parent.tank.scanner.slist[0].range*2,self.parent.tank.scanner.slist[0].range*2)).convert_alpha()
        self.parent.tank.scancircle.fill((0,0,0,0))
        pygame.draw.arc(self.parent.tank.scancircle, (30,30,220,55), pygame.Rect((0,0),(self.parent.tank.scanner.slist[0].range*2,self.parent.tank.scanner.slist[0].range*2)), 6.28*(self.parent.tank.scanner.slist[0].angle-self.parent.tank.scanner.slist[0].arc/2)/360, 6.28*(self.parent.tank.scanner.slist[0].angle+self.parent.tank.scanner.slist[0].arc/2)/360,self.parent.tank.scanner.slist[0].range)
        return self.parent.tank.scanner.slist[0].arc

class can_scanresetarc():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.parent=parent
    def execute(self):
        #args is a list of arguments
        #set the scanner parameters here 
        #terms index    meaning
        #       0 arc(if over max, then set to max, if under 1 set to 1
#        if not self.parent.tank.scanner.slist[0].fixed:
#        self.parent.tank.scancircle.fill((0,0,0,0))
        self.parent.tank.scanner.slist[0].arc=self.parent.tank.scanner.slist[0].maxarc
        self.parent.tank.scanner.slist[0].range=self.parent.tank.scanner.slist[0].maxrange
        self.parent.tank.scancircle=pygame.Surface((self.parent.tank.scanner.slist[0].range*2,self.parent.tank.scanner.slist[0].range*2)).convert_alpha()
        self.parent.tank.scancircle.fill((0,0,0,0))
        pygame.draw.arc(self.parent.tank.scancircle, (30,30,220,55), pygame.Rect((0,0),(self.parent.tank.scanner.slist[0].range*2,self.parent.tank.scanner.slist[0].range*2)), 6.28*(self.parent.tank.scanner.slist[0].angle-self.parent.tank.scanner.slist[0].arc/2)/360, 6.28*(self.parent.tank.scanner.slist[0].angle+self.parent.tank.scanner.slist[0].arc/2)/360,self.parent.tank.scanner.slist[0].range)
        return self.parent.tank.scanner.slist[0].range

class can_scansetangle():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.parent=parent
    def execute(self):
        #args is a list of arguments
        #set the scanner parameters here 
        #terms index    meaning
        #       0 angle to set the scanner to
        self.parent.tank.scancircle.fill((0,0,0,0))
#        pygame.draw.circle(self.parent.tank.scancircle, (0,0,0,0), pygame.Rect((0,0),(self.parent.tank.scanner.slist[0].range*2,self.parent.tank.scanner.slist[0].range*2)), 6.28*(self.parent.tank.scanner.slist[0].angle-self.parent.tank.scanner.slist[0].arc/2)/360, 6.28*(self.parent.tank.scanner.slist[0].angle+self.parent.tank.scanner.slist[0].arc/2)/360,self.parent.tank.scanner.slist[0].range)
        self.parent.tank.scanner.slist[0].angle=self.terms[0].evaluate()
        pygame.draw.arc(self.parent.tank.scancircle, (30,30,220,55), pygame.Rect((0,0),(self.parent.tank.scanner.slist[0].range*2,self.parent.tank.scanner.slist[0].range*2)), 6.28*(self.parent.tank.scanner.slist[0].angle-self.parent.tank.scanner.slist[0].arc/2)/360, 6.28*(self.parent.tank.scanner.slist[0].angle+self.parent.tank.scanner.slist[0].arc/2)/360,self.parent.tank.scanner.slist[0].range)
        return self.terms[0].evaluate()

class can_scansetdest():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.parent=parent
        self.destx=terms[0].evaluate()
        self.desty=terms[1].evaluate()
    def execute(self):
        #args is a list of arguments
        #set the ammo choice here 
        #terms index    meaning
        self.xpos=self.parent.tank.xpos
        self.ypos=self.parent.tank.ypos
        self.parent.tank.scancircle.fill((0,0,0,0))
        self.angle=get_angle(self.xpos,self.destx,self.ypos,self.desty)
        pygame.draw.arc(self.parent.tank.scancircle, (30,30,220,55), pygame.Rect((0,0),(self.parent.tank.scanner.slist[0].range*2,self.parent.tank.scanner.slist[0].range*2)), 6.28*(self.parent.tank.scanner.slist[0].angle-self.parent.tank.scanner.slist[0].arc/2)/360, 6.28*(self.parent.tank.scanner.slist[0].angle+self.parent.tank.scanner.slist[0].arc/2)/360,self.parent.tank.scanner.slist[0].range)
        self.parent.tank.scanner.slist[0].angle=self.angle
        return self.angle

class can_scanclosest():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.parent=parent
    def execute(self):
        #args is a list of arguments
        #set the scanner parameters here 
        #terms index    meaning
        distlow=1000000
        targid=self.parent.tank.PlayerIdent
        to180=180-self.parent.tank.scanner.slist[0].angle
        lowangle=(180-int(self.parent.tank.scanner.slist[0].arc/2))%360
        highangle=(180+int(self.parent.tank.scanner.slist[0].arc/2))%360
        for x in TankIndex:
            if x!=self.parent.tank and not x.Dead:
                dist=math.sqrt((x.xpos-self.parent.tank.xpos)*(x.xpos-self.parent.tank.xpos)+(x.ypos-self.parent.tank.ypos)*(x.ypos-self.parent.tank.ypos))
                angle=(get_angle(self.parent.tank.xpos,x.xpos,self.parent.tank.ypos,x.ypos)+to180)%360
                if dist<self.parent.tank.scanner.slist[0].range and angle<highangle and angle>lowangle and dist<distlow:
                    distlow=dist
                    targid=x.PlayerIdent
        return targid

class can_iamscanned():
    def __init__(self,parent,terms):
        self.terms=terms
        self.parent=parent
    def execute(self):
        for x in TankIndex:
            if x!=self.parent.tank:
                if can_scan_tank(x,self.parent.tank):
                    return 0
        return 1
class can_followtarget():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.target=int(terms[0].evaluate())
        self.parent=parent
        self.xpos=TankIndex[self.target].xpos
        self.ypos=TankIndex[self.target].ypos
    def execute(self):
        if self.target<=len(TankIndex) and self.target>=0 and can_scan_tank(self.parent.tank,TankIndex[self.target]):
            self.parent.tank.destx=self.xpos
            self.parent.tank.desty=self.ypos
            return self.target
        else:
            return self.parent.tank.PlayerIdent


class can_inrange():
    def __init__(self,parent,terms):
        # Is the target in range of current weapon or not?
        self.target=int(terms[0].evaluate())
        self.parent=parent
        self.xpos=TankIndex[self.target].xpos
        self.ypos=TankIndex[self.target].ypos
    def execute(self):
        x1=self.parent.tank.xpos
        y1=self.parent.tank.ypos
        x2=self.xpos
        y2=self.ypos
        dist=math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
        if self.target<=len(TankIndex) and self.target>=0 and can_scan_tank(self.parent.tank,TankIndex[self.target]) and self.parent.tank.gunnery.glist[0].range>dist:
            return 1
        else:
            return 0




class can_godest():
    def __init__(self,parent,terms):
        # sets a new destination and returns True on success False on a failure
        # holds all of the canned functions
        # first index is always the parent the rest are the arguments passed to this function
        self.parent=parent
        self.xpos=terms[0].evaluate()
        self.ypos=terms[1].evaluate()
    def execute(self):
        #args is a list of arguments
        #set the ammo choice here 
        #terms index    meaning
##        print "xpos",self.parent.tank.xpos,"destx",self.xpos,"SPEED",self.parent.tank.speed
##
##        print "ypos",self.parent.tank.ypos,"desty",self.ypos
##        print "compare1",self.parent.tank.xpos, "vs",self.xpos-self.parent.tank.speed
##        print "compare2",self.parent.tank.xpos, "vs",self.xpos+self.parent.tank.speed
##        print "compare3",self.parent.tank.ypos, "vs",self.ypos-self.parent.tank.speed
##        print "compare4",self.parent.tank.ypos, "vs",self.ypos+self.parent.tank.speed
        if self.xpos>maxwidth-self.parent.tank.tankwidth or self.xpos<0 or self.ypos>maxheight-self.parent.tank.tankheight or self.ypos<0:
##            print "return 1"
            return 1
        elif self.parent.tank.xpos>self.xpos-self.parent.tank.speed and self.parent.tank.xpos<self.xpos+self.parent.tank.speed and self.parent.tank.ypos>self.ypos-self.parent.tank.speed and self.parent.tank.ypos<self.ypos+self.parent.tank.speed:
##            print "return 2"
            return 2
        else:
            self.parent.tank.destx=self.xpos
            self.parent.tank.desty=self.ypos
            return 0
class can_getgunrange():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return self.parent.tank.gunnery.glist[0].range

class can_getscanarc():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return self.parent.tank.scanner.slist[0].arc
class can_getxpos():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
        self.PlayerIdent=int(self.terms[0].evaluate())
    def execute(self):
        if self.PlayerIdent<=len(TankIndex) and self.PlayerIdent>=0 and can_scan_tank(self.parent.tank,TankIndex[self.PlayerIdent]):
            return TankIndex[self.PlayerIdent].xpos
        else:
            return self.parent.tank.xpos
class can_getypos():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
        self.PlayerIdent=int(self.terms[0].evaluate())
    def execute(self):
        if self.PlayerIdent<=len(TankIndex) and self.PlayerIdent>=0 and can_scan_tank(self.parent.tank,TankIndex[self.PlayerIdent]):
            return TankIndex[self.PlayerIdent].ypos
        else:
            return self.parent.tank.ypos
class can_getid():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return self.parent.tank.PlayerIdent
        
class can_getarmorstrength():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
        self.PlayerIdent=int(self.terms[0].evaluate())
    def execute(self):
        if self.PlayerIdent==self.parent.tank.PlayerIdent or (self.PlayerIdent<=len(TankIndex) and self.PlayerIdent>=0 and can_scan_tank(self.parent.tank,TankIndex[self.PlayerIdent])):
            tank=TankIndex[self.PlayerIdent]
            strength=0
            for x in TankIndex[self.PlayerIdent].armor.alist:
                strength=strength+x.damage*x.strength/100
            return strength
        else:
            return -1
class can_getarmordamage():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
        self.PlayerIdent=int(self.terms[0].evaluate())
    def execute(self):
        if self.PlayerIdent==self.parent.tank.PlayerIdent or (self.PlayerIdent<=len(TankIndex) and self.PlayerIdent>=0 and can_scan_tank(self.parent.tank,TankIndex[self.PlayerIdent])):
            strength=0
            strength2=0
            for x in TankIndex[self.PlayerIdent].armor.alist:
                strength=strength+x.damage*x.strength/100
            for x in TankIndex[self.PlayerIdent].armor.alist:
                strength2=strength2+x.strength
            if strength2>0:
                return 100*strength/strength2
            else:
                return 0
        else:
            return -1
class can_getchassisstrength():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
        self.PlayerIdent=int(self.terms[0].evaluate())
    def execute(self):
        if self.PlayerIdent==self.parent.tank.PlayerIdent or (self.PlayerIdent<=len(TankIndex) and self.PlayerIdent>=0 and can_scan_tank(self.parent.tank,TankIndex[self.PlayerIdent])):
            return TankIndex[self.PlayerIdent].chassis.chaslist[0].damage*TankIndex[self.PlayerIdent].chassis.chaslist[0].strength/100
        else:
            return -1
class can_getchassisdamage():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
        self.PlayerIdent=int(self.terms[0].evaluate())
    def execute(self):
        if self.PlayerIdent==self.parent.tank.PlayerIdent or (self.PlayerIdent<=len(TankIndex) and self.PlayerIdent>=0 and can_scan_tank(self.parent.tank,TankIndex[self.PlayerIdent])):
            if TankIndex[self.PlayerIdent].chassis.chaslist[0].strength>0:
                return 100*(TankIndex[self.PlayerIdent].chassis.chaslist[0].damage*TankIndex[self.PlayerIdent].chassis.chaslist[0].strength/100)/TankIndex[self.PlayerIdent].chassis.chaslist[0].strength
            else:
                return 0
        else:
            return -1
class can_gettag():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
        self.PlayerIdent=int(self.terms[0].evaluate())
    def execute(self):
        return TankIndex[self.PlayerIdent].TagID
        
class can_settag():
    def __init__(self,parent,terms):
        # holds all of the canned functions
        self.terms=terms
        self.parent=parent
        self.tagid=terms[0].evaluate()
    def execute(self):
        #args is a list of arguments
        #set the tag id
        #terms index    meaning
        self.parent.tank.TagID=self.tagid
        return 0
        
class can_maxy():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return maxheight-self.parent.tank.tankheight
        
class can_maxx():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return maxwidth-self.parent.tank.tankwidth
        
class can_sin():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return math.sin(self.terms[0].evaluate()*3.14159/180)
class can_cos():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return math.cos(self.terms[0].evaluate()*3.14159/180)
class can_tan():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        if self.terms[0].evaluate()==90 or self.terms[0].evaluate()==270:
            return 9999999999999999
        else:
            return math.tan(self.terms[0].evaluate()*3.14159/180)
class can_asin():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return 180*math.asin(self.terms[0].evaluate())/3.14159
class can_acos():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return 180*math.acos(self.terms[0].evaluate())/3.14159
class can_random():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        #returns random number from 0 to 100
        return random.randint(0,100)
class can_atan():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return 180*math.atan(self.terms[0].evaluate())/3.14159
class can_sqrt():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return math.sqrt(self.terms[0].evaluate())
class can_dist():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        #0 = x1
        #1 = y1
        #2 = x2
        #3 = y2
        return math.sqrt((self.terms[0].evaluate()-self.terms[2].evaluate())*(self.terms[0].evaluate()-self.terms[2].evaluate())+(self.terms[1].evaluate()-self.terms[3].evaluate())*(self.terms[1].evaluate()-self.terms[3].evaluate()))
class can_abs():
    def __init__(self,parent,terms):
        self.parent=parent
        self.terms=terms
    def execute(self):
        return abs((self.terms[0].evaluate()-self.terms[2].evaluate())*(self.terms[0].evaluate()-self.terms[2].evaluate())+(self.terms[1].evaluate()-self.terms[3].evaluate())*(self.terms[1].evaluate()-self.terms[3].evaluate()))
        
canned_list={   "scansetdest":can_scansetdest,
                "scansetarc":can_scansetarc,
                "scanresetarc":can_scanresetarc,
                "scansetrange":can_scansetrange,
                "scansetangle":can_scansetangle,
                "scanclosest":can_scanclosest,
                "ammoset":can_ammoset,
                "mineset":can_mineset,
                "minesetproximity":can_minesetproximity,
                "minesettarget":can_minesettarget,
                "fire":can_fire,
                "firetrack":can_firetrack,
                "minedrop":can_minedrop,
                "followtarget":can_followtarget,
                "print":can_print,
                "godest":can_godest,
                "getscanarc":can_getscanarc,
                "getchassisstrength":can_getchassisstrength,
                "getarmorstrength":can_getarmorstrength,
                "getchassisdamage":can_getchassisdamage,
                "getarmordamage":can_getarmordamage,
                "getxpos":can_getxpos,
                "getgunrange":can_getgunrange,
                "iamscanned":can_iamscanned,
                "inrange":can_inrange,
                "getypos":can_getypos,
                "getid":can_getid,
                "gettag":can_gettag,
                "settag":can_settag,
                "maxx":can_maxx,
                "maxy":can_maxy,
                "sin":can_sin,
                "random":can_random,
                "cos":can_cos,
                "asin":can_asin,
                "tan":can_tan,
                "atan":can_atan,
                "dist":can_dist,
                "sqrt":can_sqrt,
                "firetarget":can_firetarget}

#THERE ARE NO GLOBAL VARIABLES
class statement():
    def __init__(self,parent,statement_type,eval,variable,terms,call_list,call,fparent):
            #parent is the statement block to which this statement bleongs(parent line( like an if or a while))
            #statement_type tells which type of statement it is
            #fparent is the parent function for the statement.
            #eval is an truefalse object, none if not a switch type statement
            #variable is a named index to a list of variable objects for set type statements in the current function 
            #term is an object type terms holding two terms connected by an operator or a single function call that returns a result
            # call_list is a list of function arguments
            # call is a functions or a canned type object that is the entry point for a function 
            self.type="statement"
            self.statement_type=statement_type
            self.next_step=0 # use this to set the next step for linear steps also the step after a block 
            self.true_switch=0 # used for conditionals next step
            self.false_switch=0 # used for conditionals next step
            self.eval=eval
            self.variable=variable
            self.term=terms
            self.call=call
            self.code="NONE"
            self.parent=parent
            self.call_list=call_list # structured as [[type,value/object],[type,value/object],etc]
 #           print "call_list",statement_type,parent,call_list
            self.fparent=fparent
    def evaluate(self):
        if self.statement_type==0 or self.statement_type==6:
            if self.eval.evaluate():
                return [self.true_switch,self.fparent]
            else:
                return [self.false_switch,self.fparent]
        elif self.statement_type==1:
            self.fparent.local_list[self.variable]=self.term.evaluate()
            return [self.next_step,self.fparent]
        elif self.statement_type==2:
            self.call.execute(self.call_list)
            return [self.call.current,self.call]
            # returns the aiprog that is currently in focus
#        elif self.statement_type==3:
#            exit() # a hard exit from the program  Shouldn't be used by the programmer
        elif self.statement_type==5:
            can=self.call(self.fparent,self.call_list)
            can.execute()
            return [self.next_step,self.fparent]
##        else:
##            app.frame.Output.AppendText("ERROR 1")
            

class truefalse():
    def __init__(self,parent,left,right,comparator):
        self.left=left # left part of the true false evaluation must be a term
        self.right=right # right part of the true false evaluation must be a term
        self.comparator=comparator # comparison value 0 - == 1 <= 2>= 3 < 4 > 5 !=
    def evaluate(self):
        if self.comparator==0:
            if self.left.evaluate()==self.right.evaluate():
                return True
            else:
                return False
        elif self.comparator==1:
            if self.left.evaluate()<=self.right.evaluate():
                return True
            else:
                return False
        elif self.comparator==2:
            if self.left.evaluate()>=self.right.evaluate():
                return True
            else:
                return False
        elif self.comparator==3:
            if self.left.evaluate()>self.right.evaluate():
                return True
            else:
                return False
        elif self.comparator==4:
            if self.left.evaluate()<self.right.evaluate():
                return True
            else:
                return False
        elif self.comparator==5:
#            print self.left.evaluate(), self.right.evaluate()
            if self.left.evaluate()!=self.right.evaluate():
                return True
            else:
                return False
        else:
            app.frame.Output.AppendText("ERROR - TRUEFALSE"+str(self.comparator))
    
class term():
    def __init__(self,parent,single,type,left,right,operator,call_list,function,value):
        #single is a boolean indicating if this is a singular term or if it is a combination action
        #type indicates the type of term for a single
        #left and right are the terms that are combined, only left is used if a single
        #value is used to hold the value of the term 
        #function and call_list are used to hold information for a function call
        #parent is the ai obj or function that is parent for local variable list
        self.single=single
        self.type=type
        self.right=right
        self.left=left
        self.operator=operator
        self.call_list=call_list
        self.value=value
        self.function=function
        self.parent=parent
    def evaluate(self):
        self.lresult=0
        self.rresult=0
        if self.single: # here we return actual values to the calling functions/methods
            #includes all canned functions 
            if self.type==4:
                #canned function
                x=self.function(self.parent,self.call_list)
                return x.execute()
            elif self.type==0:
                #variable
                return self.parent.local_list[self.left]
            elif self.type==1:
                #constant
                return self.value
            else:
                app.frame.Output.AppendText("ERROR TERMS SINGLE")
        else:#here we call for evaluation of individual terms and return a combined result based on operator
            # combine terms
            self.lresult=self.left.evaluate()
            self.rresult=self.right.evaluate()
            if self.operator==5:
                return self.lresult+self.rresult
            elif self.operator==6:
                return self.lresult-self.rresult
            elif self.operator==2:
                return self.lresult*self.rresult
            elif self.operator==3:
                return self.lresult/self.rresult
            elif self.operator==1:
                return self.lresult**self.rresult
            elif self.operator==4:
                return self.lresult%self.rresult
            
class ai_prog():
    # this class reads a block and converts it into structural code above.
    # it also creates sub sections of the same class(sub blocks) that it processes.
    def __init__(self,tank,parent,var_list):
        #lines is a list of text lines
        self.type="function"
        self.tank=tank
        self.program="Main"
        if parent==None:
            parent=self
        self.parent=parent # contains the object that acts as a parent for this function set( it will be an ai_prog object)
        self.local_list={}# a list of local variables Dictionary Name:value
        self.local_order={}# a list of local variables Dictionary order:name
        cnt=0
        for x in var_list:
            self.local_order.update({cnt:x})
            self.local_list.update({x:self.getterm("0")}) # build list for variables at outset
            cnt=cnt+1
        self.came_from=[]
        self.last_step=None
    def build(self,lines):
#        for b in lines:
#            print self.tank.PlayerIdent,b
#        print self.tank.PlayerIdent, "****",self.tank.Code
        self.success=True
        lines2=[]
        # remove all balnk and commented lines from program
        for line in lines:
            if len(line.lstrip().rstrip())!=0:
                if line.lstrip()[0]!="#":
                    lines2.append(line)
        lines=lines2
        self.start=self.process_line(self.parent,lines)
##        print "************"
##        print "************"
##        print "compiled"
##        print "************"
##        print "************"
        return self.success
    def execute(self,call_list):
        self.current=self.start
        cnt=0
#        print call_list
        for x in call_list:
        #set variables
            if x!=None:
                self.local_list[self.local_order[cnt]]=x.evaluate()  # each of these are terms
                cnt=cnt+1
    def next_step(self):
#print line for diagnostics when running program
#        print self.parent.tank.PlayerName+" - "+self.program+" - "+self.current.code
        if self.current==self.last_step or self.current.statement_type==4:#return or last step in fucntion
            if self.parent!=self:
                self.parent.current=self.parent.current.next_step#returns the next statement
                return self.parent
            else:
                self.current=self.start
                return self
        elif self.current.statement_type==2:
            next=self.current.evaluate()#returns the next statement
            next[1].current=next[0] # this is the next step in line
            return next[1]            
        else:
            next=self.current.evaluate()#returns the next statement
            if next==None:
                self.current=self.start
                return self
            else:
                self.current=next[0] # this is the next step in line
                return next[1]            
    def process_line(self,parent,lineblock):
        # returns a statement object for this linestructure of the line
        # first line in the block will return a statement object as a reference
        # parent is used to tell the statement which statement is the parent block for this statement, so when we get to the end of the block, we know which parent statement block to get the next statement from.
#       print lineblock
        if len(lineblock)==0:
            if parent.type=="function":
                outcome=statement(parent,statement_list["exit"],None,None,None,None,None,self)
            elif parent.type=="statement" and parent.statement_type==6:
                outcome=parent
            else:
                outcome=parent.next_step
            return outcome
        #clear comment lines
        line=lineblock[0]
        self.line=line
        command=line.lstrip().split()[0]
        # identify command
        #begin is a special entry point command no parents given
        if command=="if":
            # new block 
            outcome=statement(parent,statement_list["switch"],self.get_condition(line.lstrip().rstrip().partition(" ")[2]),None,None,None,None,self)
            outcome.code=line
            #find end on block 
            inif=1
            inelse=0
            ifs=1
            linecnt=1
            marker=0
            #it is an if statement, get me the condition and build the initial statement
            #get the blocks and build parts of the statement
            while True:
#               print linecnt,"ifs",ifs,inif,lineblock[linecnt]
                if lineblock[linecnt].lstrip().split()[0]=="if":
                    #extra if block inside so increment counter
                    ifs=ifs+1
                elif lineblock[linecnt].lstrip().split()[0]=="else" and ifs==1:
                    #found the else
                    inif=0
                    inelse=1
                    # get the block for the if
                elif lineblock[linecnt].lstrip().split()[0]=="endif" and ifs==1:
#                    print "ENDIF HIT"
                    #found the end of the list build the next_step statement
                    outcome.next_step=self.process_line(parent,lineblock[linecnt+1:len(lineblock)])
                    break
                elif lineblock[linecnt].lstrip().split()[0]=="endif" and ifs>1:
                    ifs=ifs-1
                    #if there is an else, then right step = block return here
                    #else the left step 
                linecnt=linecnt+1

            #find end on block and start of else
            inif=1
            inelse=0
            ifs=1
            linecnt=1
            marker=0
            #it is an if statement, get me the condition and build the initial statement
            #get the blocks and build parts of the statement
            while True:
                if lineblock[linecnt].lstrip().split()[0]=="if":
                    #extra if block inside so increment counter
                    ifs=ifs+1
                elif lineblock[linecnt].lstrip().split()[0]=="else" and ifs==1:
                    #found the else
                    inif=0
                    inelse=1
                    outcome.true_switch=self.process_line(outcome,lineblock[marker+1:linecnt])
                    marker=linecnt
                    # get the block for the if
                elif lineblock[linecnt].lstrip().split()[0]=="endif" and ifs==1:
                    #found the end of the list
                    if inif==0:
                        # there is an else
                        outcome.false_switch=self.process_line(outcome,lineblock[marker+1:linecnt])
                        marker=linecnt
                        inelse=0
                    else:
                        outcome.true_switch=self.process_line(outcome,lineblock[marker+1:linecnt])
                        outcome.false_switch=outcome.next_step
                        marker=linecnt
                        inif=0
                    return outcome
                elif lineblock[linecnt].lstrip().partition(" ")[0]=="endif" and ifs>1:
                    ifs=ifs-1
                    #if there is an else, then right step = block return here
                    #else the left step 
                linecnt=linecnt+1
        elif command=="while":
            # new block 
            whiles=1
            linecnt=1
            marker=0
            endmark=0
            #it is an if statement, get me the condition and build the initial statement
            outcome=statement(parent,statement_list["loop"],self.get_condition(line.lstrip().rstrip().partition(" ")[2]),None,None,None,None,self)
            outcome.code=line
            #it is an if statement, get me the condition and build the initial statement
            #get the blocks and build parts of the statement
            #find the end of the while first for early exits
            while True:
 #               print linecnt,"while",whiles,lineblock[linecnt]
                if lineblock[linecnt].lstrip().split()[0]=="while":
                    #extra while block inside so increment counter
                    whiles=whiles+1
                elif lineblock[linecnt].lstrip().split()[0]=="endwhile" and whiles==1:
                    #found the end of the list
                    endmark=linecnt
                    linecnt=0
                    whiles=1
                    break
                elif lineblock[linecnt].lstrip().split()[0]=="endwhile" and whiles>1:
                    whiles=whiles-1
                linecnt=linecnt+1
            #now build the block
            outcome.false_switch=self.process_line(parent,lineblock[endmark+1:len(lineblock)])#use parent here because we are back out in the main block
            outcome.next_step=outcome.false_switch # they are the same
            outcome.true_switch=self.process_line(outcome,lineblock[1:endmark])            
            return outcome
        elif command=="function":
            # new block 
            #find end on block and build new ai_prog putting it in function list
            funs=1
            linecnt=1
            marker=0
            endmark=0
            call=line.lstrip().rstrip().partition(" ")[2]
            fun=call.lstrip().rstrip().partition("(")[0]
            if call.rstrip().lstrip().partition("(")[2].lstrip().rstrip()==")":
                args=[]
            else:
                args=call.rstrip().partition("(")[2].partition(")")[0]
                args=args.split(",")
            #get the blocks and build parts of the statement
            #find the end of the while first for early exits
            while True:
                if lineblock[linecnt].lstrip().split()[0]=="function":
                    #extra while block inside so increment counter
                    funs=funs+1
                elif lineblock[linecnt].lstrip().split()[0]=="endfunction" and funs==1:
                    #found the end of the list
                    endmark=linecnt
                    linecnt=0
                    break
                elif lineblock[linecnt].lstrip().split()[0]=="endfunction" and funs>1:
                    funs=funs-1
                linecnt=linecnt+1
            #now build the new ai_prog
            function_list.update({fun:ai_prog(self.tank,self.parent,args)})
            function_list[fun].program=line
            function_list[fun].build(lineblock[1:endmark]) # build new statement list
            return self.process_line(parent,lineblock[endmark+1:len(lineblock)])# return next line after function definition
        elif command=="break":
            return parent.next_step
        elif command=="continue":
            return parent
        elif command=="set":
            var=line.lstrip().rstrip().split()[1].rstrip().lstrip().partition("=")[0]
            val=self.getterm(line.lstrip().rstrip().partition(" ")[2].rstrip().lstrip().partition("=")[2])
            if not var in self.local_list:
                self.local_list.update({var:val})
            outcome=statement(parent,statement_list["set"],None,var,val,None,None,self)
            outcome.code=line
            outcome.next_step=self.process_line(parent,lineblock[1:len(lineblock)])
            return outcome
        elif command=="call":
            call=line.lstrip().rstrip().partition(" ")[2]
            fun=call.lstrip().rstrip().partition("(")[0].lstrip().rstrip()

            if fun in canned_list:
                # this is a canned function a singular action not a value returned
                outcome=statement(parent,
                                    statement_list["canned"],
                                    None,
                                    None,
                                    None,
                                    self.getargs(self.getparens("("+call.partition("(")[2]),self),
                                    canned_list[fun],
                                    self)
            elif fun in function_list:
#                print "getargs in"
                outcome=statement(parent,
                                    statement_list["call"],
                                    None,
                                    None,
                                    None,
                                    self.getargs(self.getparens("("+call.partition("(")[2]),function_list[fun]),
                                    function_list[fun],
                                    self)
#                print "getargs out",self.getparens("("+call.partition("(")[2]),self.getargs(self.getparens("("+call.partition("(")[2]),function_list[fun])
            else:
                app.frame.Output.AppendText("ERROR unrecognized command: "+command+" Line: "  +str(line))
            outcome.code=line
            outcome.next_step=self.process_line(parent,lineblock[1:len(lineblock)])
            return outcome
#        elif command=="exit":
#            outcome=statement(parent,statement_list["exit"],None,None,None,None,None,self)
#            return outcome
        elif command=="return":
            # here is where the aiprog ends and reverts controlto the parent function which ever that is.
            outcome=statement(parent,statement_list["return"],None,None,self.getterm(line.lstrip().rstrip().partition(" ")[2]),None,None,self.parent)
            outcome.code=line
            outcome.next_step=self.parent.next_step
            #Question.... When a function returns a value, how does that value find its way back to where it belongs????  Answer only canned functions return values and they are only used in terms
            return outcome
        else:
            app.frame.Output.AppendText("ERROR unrecognized command: "+command+" Line: "  +str(line))
    def getparens(self,termline):
        #gets the contents of a parentheses and returns it
        pcount=0
        pos=-1
        for x in termline:
            pos=pos+1
            if x=="(":
                pcount=pcount+1
            elif x==")":
                pcount=pcount-1
            if pcount==0:
                return termline[1:pos]
    def gettype(self,line,sep):
        #returns the type of term at the beginning of this line and the term
        #sep is a list of separators  
        #check for canned functions first
        item=line
        for x in sep:
            item=item.replace(x," ")
        item=item.split()
        if item[0] in canned_list.keys():
            item[0]=line[0:len(item[0])+2+len(self.getparens(line[len(item[0]):len(line)]))]
            return ["canned",item[0]]
        elif item[0] in self.local_list:
            return ["variable",item[0]]
        else:
            try:
                x=float(item[0])
                return ["constant",item[0]]
            except ValueError:
                return ["unknown",None]
##    def gettype(self,line,sep):
##        #returns the type of term at the beginning of this line and the term
##        #sep is a list of separators  
##        #check for canned functions first
##        item=line
##        for x in sep:
##            item=item.replace(x," ")
##        item=item.split()
##        if item[0] in canned_list.keys():
##            #canned function, get the arguments and return the complete entry
##            if line[len(item[0])+1+len(getparens(line[len(item[0])])):len(line)].lstrip() == "," or  line[len(item[0])+1+len(getparens(line[len(item[0])])):len(line)].lstrip() == ")":
##                #end of argument
##                return["canned",line[0:len(item[0])+2+len(getparens(line[len(item[0])]))]]
##            else:
##                
##                return item[0]+"("+self.getparens(line[len(item[0]):len(line)"("+item[1].partition("(")[2]),self)+")"
####            item[0]=line[0:len(item[0])+2+len(self.getparens(line[len(item[0]):len(line)]))]
####            return ["canned",item[0]]
####        elif item[0] in self.local_list:
####            return ["variable",item[0]]
##        else:
##            try:
##                x=float(item[0])
##                return ["constant",item[0]]
##            except ValueError:
##                return ["unknown",None]
##        return item[0]
##       
    def getargs(self,arglist,fun):
        #walk through looking for comma separators and getting next terms
        #first check on type of term
        args=[]
        argsep=[]
        inparens=0
        line=""
        for st in arglist:
            if st=="(":
                inparens=inparens+1
            if st==")":
                inparens=inparens-1
            if st==","and inparens==0:
                #found a separator
                args.append(self.getterm(line))
                line=""
            else:
                line=line+st
        args.append(self.getterm(line))
        line=""
        
        return args
    def getterm(self,termline):
        #returns a term object
        #termline holds the term expession to be evaluated  Evaluate it here and return a term object
        #strip off leading and trailing spaces if they exist and parentheses
        termline=termline.rstrip().lstrip()
        #PEMDAS in effect find all terms in statement the determine order of operations
        terms=[]
        #terms holds the terms in the line at level 1
        ops=[]
        #ops holds all operators in the line
        last="NONE"
        while len(termline)>0:
            #find what is first
            if termline[0]=="(":
                #we have a parens
                terms.append(self.getterm(self.getparens(termline)))
                termline=termline[len(self.getparens(termline))+2:len(termline)].lstrip()
                last="TERM"
            elif termline[0] in operator_list.keys() and last=="TERM":
                #we have an operator
                ops.append(operator_list[termline[0]])
                termline=termline[1:len(termline)].lstrip()
                last="OP"
            elif termline[0] =="-":
                #we have a negative number
                item=self.gettype(termline[1:len(termline)].lstrip(),[",","(",")","+","-","/","*","%","^"])
#                print item
                terms.append(term(self,True,arg_list["constant"],None,None,None,None,None,(-1)*float(item[1])))
                last="TERM"
                termline=termline[len(item[1])+1:len(termline)]
            else:
                #it is a function, value, or variable figure out which
                item=self.gettype(termline,[",","(",")","+","-","/","*","%","^"])
                if item[0] == "canned":
                    terms.append(term(self,
                                            True,
                                            arg_list["canned"],
                                            None,
                                            None,
                                            None,
                                            self.getargs(self.getparens("("+item[1].partition("(")[2]),self),
                                            canned_list[item[1].partition("(")[0]],None))
                elif item[0] == "variable":
                    terms.append(term(self,True,arg_list["variable"],item[1],None,None,None,None,None))
                elif item[0] == "constant":
                    terms.append(term(self,True,arg_list["constant"],None,None,None,None,None,float(item[1])))
                    
                else:
                    app.frame.Output.AppendText("ERROR: unknown argument in "+termline)
                termline=termline[len(item[1]):len(termline)]
                last="TERM"

        #okay now we have built the terms and ops for the line, so lets combine them
        #find the highest order in the op list first, perform it and replace it witha single term object
        while len(ops)>0:#when we get to 1 term end it
            indx=0
            cnt=0
            while cnt<len(ops):
                if ops[cnt]<ops[indx]:
                    indx=cnt 
                cnt=cnt+1
            #found next order combine and reduce
            terms[indx]=term(self,False,arg_list["double"],terms[indx],terms[indx+1],ops[indx],None,None,None)
            del ops[indx]
            del terms[indx+1]
        if len(terms)>0:
            return terms[0]
        else:
            return None    
    def get_condition(self,condition):
        # get conditional portion of the line and process the remainder
        for x in range(0,6,1):
            if condition.partition(comp_list2[x])[1]!="":
                #found a condition
                return truefalse(self,self.getterm(condition.partition(comp_list2[x])[0]),self.getterm(condition.partition(comp_list2[x])[2]),x)
        app.frame.Output.AppendText("ERROR Invalid condtion: " +condition + " Line: "+str(self.line))
                
####HERE IS A SAMPLE LOAD####    
#progfile="test.program"
#input=open(progfile,"r+",1000000)
#lines=input.readlines()
#ailist=[]
#ailist.append(ai_prog(None,None,[]))
####COMPILE LIKE THIS#####
#for y in ailist:
#    y.build(lines)
####THIS IS THE EXECUTE LINE CALL AT START OF GAME####
#    y.execute([])
####EXECUTE IN ROUND ROBIN LIKE THIS####
#while True:
####ALL THREE LINES ARE NECESSARY####

#        y=ailist[0].next_step()            
#        if y!=None:
#            ailist[0]=y
########## WHY THE HECK ARE THERE SO MANY COMMENTS????? ##########

class LandMine():
    def __init__(self,parent):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.active=True
        self.exploding=False
        self.mine=mineimg
        self.explode=mineexp
        self.index=-1
        self.xpos=0
        self.ypos=0
        self.playindex=0
        self.tank=parent
        self.shotsquare=pygame.Surface((125,120)).convert_alpha()
        self.eraseblank=pygame.Surface((8,8)).convert_alpha()
        self.shotsquare.fill((0,0,0,0))
        self.shotsquare.blit(self.mine,(0,0))
        self.shotsquare=pygame.transform.scale(self.shotsquare,(8,8))
        self.expsquare=pygame.Surface((400,400)).convert_alpha()
        self.expsquare.fill((0,0,0,0))
        self.expsquare.blit(self.explode,(0,0))
        self.targetid=-1
        self.proximity=10
        self.tankwidth=8
        self.tankheight=8
        self.offsetx=15  # used for offset with missile for contact
        self.offsety=15  # used for offset with missile for contact
        self.type=-1
        self.cycles=8
        
    def Move(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        if self.exploding:
            xpos=self.xpos-50
            ypos=self.ypos-50
            if xpos<0:
                xpos=0
            if ypos<0:
                ypos=0
            pork3.blit(pork4.subsurface(pygame.Rect(xpos,ypos,100,100)),(xpos,ypos))
            if self.cycles<-8:
                self.active=False
                pork3.blit(pork4.subsurface(pygame.Rect(xpos,ypos,100,100)),(xpos,ypos))
            else:
                pork3.blit(pygame.transform.scale(self.expsquare,(int((8-abs(self.cycles)+1)*self.type.area/9),int((8-abs(self.cycles)+1)*self.type.area/9))), (self.xpos+10-int((8-abs(self.cycles)+1)*self.type.area/18),self.ypos+10-int((8-abs(self.cycles)+1)*self.type.area/18)))
            self.cycles=self.cycles-1
        else:
            if self.targetid!=-1:
                #check to see if selected target is near
                if math.sqrt((self.xpos-TankIndex[self.targetid].xpos)**2 + (self.ypos-TankIndex[self.targetid].ypos)**2)<=self.proximity+TankIndex[self.targetid].tankwidth/2:
                    #time to blow
                    exp.play()
                    for self.z in TankIndex:
                        if self.z!=self.tank and not self.z.Dead:
                            dist=math.sqrt((self.z.xpos-self.xpos+self.offsetx)*(self.z.xpos-self.xpos+self.offsetx)+(self.z.ypos-self.ypos+self.offsety)*(self.z.ypos-self.ypos+self.offsety))
                            if dist<self.type.area:
                                damage=self.type.destruction*(1-dist/self.type.area)
                                self.z.TakeDamage(damage)
                                self.tank.score=self.tank.score+damage
                                if self.z.Dead:
                                    self.tank.score=self.tank.score+3000
                    self.exploding=True
            else:
                for z in TankIndex:
                    dist=math.sqrt((z.xpos-self.xpos+self.offsetx)**2+(z.ypos-self.ypos+self.offsety)**2)
                    if dist<self.proximity+TankIndex[self.targetid].tankwidth/2:
                        exp.play()
                        for self.z in TankIndex:
                            if self.z!=self.tank and not self.z.Dead:
                                dist=math.sqrt((self.z.xpos-self.xpos+self.offsetx)*(self.z.xpos-self.xpos+self.offsetx)+(self.z.ypos-self.ypos+self.offsety)*(self.z.ypos-self.ypos+self.offsety))
                                if dist<self.type.area:
                                    damage=self.type.destruction*(1-dist/self.type.area)
                                    self.z.TakeDamage(damage)
                                    self.tank.score=self.tank.score+damage
                                    if self.z.Dead:
                                        self.tank.score=self.tank.score+3000
                        self.exploding=True
    def Draw(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        pork3.blit(self.shotsquare, (self.xpos,self.ypos))
    
class Missile():
    def __init__(self,parent):
        global mineexp,mineimg,trackerimg,heshot,grapeshot,silvershot,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.active=True
        self.tank=parent
        self.exploding=False
        self.missile=missimg
        self.explode=missexp
        self.index=-1
        self.xpos=0
        self.ypos=0
        self.destx=10000
        self.desty=10000
        self.angle=0
        self.distance=0
        self.range=0
        self.velox=0
        self.veloy=0
        self.speed=2
        self.delx=0
        self.dely=0
        self.currentxpos=0
        self.currentypos=0        
        self.playindex=0
        self.ammoname=self.tank.currentammo.name
        if self.tank.currentammo.type==3:
            self.missile=pygame.transform.scale(trackerimg,(20,10))
        elif self.tank.currentammo.type==2: # grapeshot
            self.missile=pygame.transform.scale(grapeshot,(20,10))
        elif self.tank.currentammo.type==1: # silver bullet
            self.missile=pygame.transform.scale(silvershot,(20,10))
        elif self.tank.currentammo.type==2: # High Exp
            self.missile=pygame.transform.scale(heshot,(20,10))

        self.shotsquare=pygame.Surface((20,10)).convert_alpha()
        self.eraseblank=pygame.Surface((20,10)).convert_alpha()
        self.shotsquare.fill((0,0,0,0))
        self.shotsquare.blit(self.missile,(0,0))
        self.expsquare=pygame.Surface((400,400)).convert_alpha()
        self.expsquare.fill((0,0,0,0))
        self.expsquare.blit(self.explode,(0,0))
        self.dify=0
        self.difx=0
        self.targetid=-1
        self.tankwidth=20
        self.tankheight=10
        self.offsetx=0  # used for offset with missile for contact
        self.offsety=0  # used for offset with missile for contact
        self.type=-1
        self.cycles=8
        self.offsetx1=0
        self.offsety1=0
        
    def Move(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        if self.exploding:
            xpos=self.xpos-50
            ypos=self.ypos-50
            if xpos<0:
                xpos=0
            if ypos<0:
                ypos=0
            pork3.blit(pork4.subsurface(pygame.Rect(xpos,ypos,100,100)),(xpos,ypos))
            if self.cycles<-8:
                self.active=False
                pork3.blit(pork4.subsurface(pygame.Rect(xpos,ypos,100,100)),(xpos,ypos))
            else:
                pork3.blit(pygame.transform.scale(self.expsquare,(int((8-abs(self.cycles)+1)*self.type.area/9),int((8-abs(self.cycles)+1)*self.type.area/9))), (self.xpos+10-int((8-abs(self.cycles)+1)*self.type.area/18),self.ypos+10-int((8-abs(self.cycles)+1)*self.type.area/18)))
            self.cycles=self.cycles-1
        else:
            if self.targetid!=-1:
                self.destx=TankIndex[self.targetid].xpos+self.offsetx1
                self.desty=TankIndex[self.targetid].ypos+self.offsety1
            xpos=self.xpos-50
            ypos=self.ypos-50
            if xpos<0:
                xpos=0
            if ypos<0:
                ypos=0
            pork3.blit(pork4.subsurface(pygame.Rect(xpos,ypos,100,100)),(xpos,ypos))
            difx=self.destx-self.xpos
            dify=self.desty-self.ypos
            if int(difx) == 0:
                self.delx = 0
            elif difx>0:
                self.delx=1
            else:
                self.delx=-1
            if int(dify) == 0:
                self.dely = 0
            elif dify>0:
                self.dely=1
            else:
                self.dely=-1
            mult=1

            self.velox=mult*self.speed*self.delx*math.cos(abs(math.asin(dify/(math.sqrt(difx*difx+dify*dify+.00001)))))
            self.veloy=mult*self.speed*self.dely*math.sin(abs(math.asin(dify/(math.sqrt(difx*difx+dify*dify+.00001)))))

            if self.delx==0:
                self.velox=0
            if self.dely==0:
                self.veloy=0
                
            if self.delx == -1 and self.dely == -1:
            #up left
                self.angle=(90+abs(90-180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14))
            if self.delx == -1 and self.dely == 1:
            #down left
                self.angle=(180+abs(180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14))
            if self.delx == 1 and self.dely == -1:
            #up right
               self.angle=(180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14)
            if self.delx == 1 and self.dely == 1:
            #down right
               self.angle=(270+(abs(90-180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.00001))))/3.14)))
            if self.delx==0 and self.dely==1:
                self.angle=270
            if self.delx==0 and self.dely==-1:
                self.angle=90
            if self.delx==1 and self.dely==0:
                self.angle=0
            if self.delx==-1 and self.dely==0:
                self.angle=180
            self.xpos=self.xpos+self.velox
            self.ypos=self.ypos+self.veloy
            self.distance=self.distance+math.sqrt(self.velox*self.velox+self.veloy*self.veloy)
            if self.active:
                if self.xpos-self.offsetx<=1 or self.ypos-self.offsety<=1 or self.xpos-self.offsetx+self.tankwidth>=maxwidth or self.ypos-self.offsety+self.tankheight>=maxheight:
                    #out of bounds destroy the missile
                    self.active=False

                elif (self.xpos>self.destx-self.speed and self.xpos<self.destx+self.speed and self.ypos>self.desty-self.speed and self.ypos<self.desty+self.speed) or self.distance>self.range:
                    #target reached  Destroy missile, and damage any tanks in the blast radius
                    exp.play()
                    if self.distance<=self.range:
                        self.xpos=self.destx
                        self.ypos=self.desty
                    else:
                        self.destx=self.xpos
                        self.desty=self.ypos
                    for self.z in TankIndex:
                        if self.z!=self.tank and not self.z.Dead:
                            dist=math.sqrt((self.z.xpos-self.destx+self.offsetx)*(self.z.xpos-self.destx+self.offsetx)+(self.z.ypos-self.desty+self.offsety)*(self.z.ypos-self.desty+self.offsety))
                            if dist<self.type.area:
                                damage=self.type.destruction*(1-dist/self.type.area)
                                
                                self.z.TakeDamage(damage)
                                self.tank.score=self.tank.score+damage
                                if self.z.Dead:  # give extra points for each kill.
                                    self.tank.score=self.tank.score+3000
                    self.exploding=True
            # location in the screen
    def Draw(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        pork3.blit(pygame.transform.rotate(self.shotsquare, self.angle), (self.xpos,self.ypos))
class Tank():
    def __init__(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,deekson,gason,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.PlayerIdent=0
        self.title="TankObject"
        self.PlayerName=""
        self.Money=7050
        self.Weight=0
        self.Dead=False
        self.Loading=False
        self.arch=0
        self.Code="# Enter your code here.\n\n"
        self.xpos=0
        self.ypos=0
        self.destx=0
        self.desty=0
        self.delx=0
        self.dely=0
        self.angle=0
        self.velox=0
        self.veloy=0
        self.width=width
        self.height=height
        self.tankwidth=30
        self.tankheight=30
        self.score=0
        self.TagID=0
        self.screenx = self.xpos-int(self.width/2)+int(self.tankwidth/2)
        
        self.screeny = self.ypos-int(self.height/2)+int(self.tankheight/2)

## TANK GRAPHICS HERE

        self.tanksquare = pygame.Surface((self.tankwidth,self.tankheight)).convert_alpha()
        self.tanksquare.fill((0,0,0,0))
        self.tankcolor = pygame.Surface((10,20)).convert_alpha()
        nums=random.randint(0,13)
        self.tankcolor.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255),255))
        self.turretback = pygame.Surface((int(self.tankwidth/3),int(self.tankheight/3))).convert_alpha()
        self.turretback.fill((0,0,0,0))
        self.turret = pygame.image.load(startdir+"/images/turret.png")
        self.chassis = pygame.image.load(startdir+"/images/chassis.png")
        self.tanksquare.blit(self.tankcolor,(10,5))
        self.tanksquare.blit(self.chassis,(6,2))
        self.tanksquare.blit(self.turret,(8,5))
        self.tanksquare=pygame.transform.rotate(self.tanksquare,270)

        #calculate speed based on...
        self.speed=1
        self.speedfact=1.25
        #calculate speed based on...
        #Mr. Murph's Stuff
        self.ai_prog=0
        self.ai_code=""
        #
        self.armor=Armor(self)
        self.ammo=Ammo(self)
        self.mine=Mine(self)
        self.chassis=Chassis(self)
        self.chassis.chaslist.append(ChassisType(chassisdata['Light'][0],chassisdata['Light'][1],chassisdata['Light'][2],chassisdata['Light'][3],chassisdata['Light'][4],chassisdata['Light'][5]))
        self.decoy=Decoy(self)
        self.engine=Engine(self)
        self.engine.elist.append(EngineType(enginedata['Toyota'][0],enginedata['Toyota'][1],enginedata['Toyota'][2],enginedata['Toyota'][3]))
        self.fuel=Fuel(self)
        self.fuel.flist.append(FuelType(fueldata['Cheap'][0],fueldata['Cheap'][1],fueldata['Cheap'][2],fueldata['Cheap'][3]))
        self.scanner=Scanner(self)
        self.scanner.slist.append(ScannerType(scannerdata['Short Range'][0],scannerdata['Short Range'][1],scannerdata['Short Range'][2],scannerdata['Short Range'][3],scannerdata['Short Range'][4],scannerdata['Short Range'][5],scannerdata['Short Range'][6],scannerdata['Short Range'][7]))
        self.gunnery=Gunnery(self)
        self.gunnery.glist.append(GunneryType(gunnerydata['GMC'][0],gunnerydata['GMC'][1],gunnerydata['GMC'][2],gunnerydata['GMC'][3],gunnerydata['GMC'][4],gunnerydata['GMC'][5],gunnerydata['GMC'][6],gunnerydata['GMC'][7]))
        
        self.ArmorList=armordata.keys()
        self.AmmoList=ammodata.keys()
        self.MineList=minedata.keys()
        self.GunneryList=gunnerydata.keys()
        self.ChassisList=chassisdata.keys()
        self.EngineList=enginedata.keys()
        self.DecoyList=decoydata.keys()
        self.FuelList=fueldata.keys()
        self.ScannerList=scannerdata.keys()
        self.data={"Armor":[self.ArmorList,self.armor.alist,self.armor,self.armor.AddArmor],"Decoy":[self.DecoyList,self.decoy.dlist,self.decoy,self.decoy.AddDecoy],"Ammo":[self.AmmoList,self.ammo.amlist,self.ammo,self.ammo.AddAmmo],"Mine":[self.MineList,self.mine.mmlist,self.mine,self.mine.AddMine],"Fuel":[self.FuelList,self.fuel.flist,self.fuel,self.fuel.ChangeFuel],"Scanner":[self.ScannerList,self.scanner.slist,self.scanner,self.scanner.ChangeScanner],
                    "Engine":[self.EngineList,self.engine.elist,self.engine,self.engine.ChangeEngine],"Chassis":[self.ChassisList,self.chassis.chaslist,self.chassis,self.chassis.ChangeChassis],"Gunnery":[self.GunneryList,self.gunnery.glist,self.gunnery,self.gunnery.ChangeGunnery]}
        self.nameplate=nameplate(self)
        maxmoney=get_money(self)
        self.guncircle=pygame.Surface((self.gunnery.glist[0].range*2,self.gunnery.glist[0].range*2)).convert_alpha()
        self.guncircle.fill((0,0,0,0))
        pygame.draw.circle(self.guncircle, (220,30,50,200), (self.gunnery.glist[0].range-2,self.gunnery.glist[0].range-2), self.gunnery.glist[0].range, 5)
        self.scancircle=pygame.Surface((self.scanner.slist[0].range*2,self.scanner.slist[0].range*2)).convert_alpha()
        self.scancircle.fill((0,0,0,0))
        pygame.draw.arc(self.scancircle, (30,30,220,30), pygame.Rect((0,0),(self.scanner.slist[0].range*2,self.scanner.slist[0].range*2)), 6.28*(self.scanner.slist[0].angle-self.scanner.slist[0].arc/2)/360, 6.28*(self.scanner.slist[0].angle+self.scanner.slist[0].arc/2)/360,self.scanner.slist[0].range)

        self.namex=self.xpos+5-self.tankwidth/2
        self.namey=self.ypos-10-self.tankheight/2


    def viewtank(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        return pork3.subsurface(pygame.Rect(self.screenx,self.screeny,width,height))
    def movetank(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        #update gun
        self.gunnery.glist[0].reloadtime=self.gunnery.glist[0].reloadtime+1
        if self.currentmine!=None:
            self.currentmine.loading=self.currentmine.loading+1
        if self.gunnery.glist[0].reloadtime>=self.gunnery.glist[0].rateoffire:
            self.gunnery.glist[0].reloadtime=self.gunnery.glist[0].rateoffire
            self.gunnery.glist[0].loaded=True
        if self.currentmine!=None:
            if self.currentmine.loading>=self.currentmine.timer:
                self.currentmine.loading=self.currentmine.timer
                self.currentmine.loaded=True
        # Check collisions, handle movement, get rid of "graphics"
        if self.xpos>self.destx-self.speed and self.xpos<self.destx+self.speed and self.ypos>self.desty-self.speed and self.ypos<self.desty+self.speed:
            #we are just about there
            self.destx=self.xpos
            self.desty=self.ypos
        xpos=self.xpos-50
        ypos=self.ypos-50
        if xpos<0:
            xpos=0
        if ypos<0:
            ypos=0
        pork3.blit(pork4.subsurface(pygame.Rect(xpos,ypos,150,150)),(xpos,ypos))
        try:
            pork3.blit(pork4.subsurface(pygame.Rect(self.namex,self.namey,100,50)),(self.namex,self.namey))
        except ValueError:
            xvcx=1
        difx=self.destx-self.xpos
        dify=self.desty-self.ypos
        if int(difx) == 0:
            self.delx = 0
        elif difx>0:
            self.delx=1
        else:
            self.delx=-1
        if int(dify) == 0:
            self.dely = 0
        elif dify>0:
            self.dely=1
        else:
            self.dely=-1
        mult=1
        if roadmap[(int((self.ypos+int(self.tankheight/2))/20))][(int((self.xpos+int(self.tankwidth/2))/20))] == "1":
            mult=2

        self.velox=mult*self.speed*self.delx*math.cos(abs(math.asin(dify/(math.sqrt(difx*difx+dify*dify+.000000001)))))
        self.veloy=mult*self.speed*self.dely*math.sin(abs(math.asin(dify/(math.sqrt(difx*difx+dify*dify+.000000001)))))

        if self.delx==0:
            self.velox=0
        if self.dely==0:
            self.veloy=0
            
        if self.delx == -1 and self.dely == -1:
        #up left
            self.angle=(90+abs(90-180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.000000001))))/3.14))
        if self.delx == -1 and self.dely == 1:
        #down left
            self.angle=(180+abs(180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.000000001))))/3.14))
        if self.delx == 1 and self.dely == -1:
        #up right
           self.angle=(180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.000000001))))/3.14)
        if self.delx == 1 and self.dely == 1:
        #down right
           self.angle=(270+(abs(90-180*math.asin(abs(dify/(math.sqrt(difx*difx+dify*dify+.0000000001))))/3.14)))
        if self.delx==0 and self.dely==1:
            self.angle=270
        if self.delx==0 and self.dely==-1:
            self.angle=90
        if self.delx==1 and self.dely==0:
            self.angle=0
        if self.delx==-1 and self.dely==0:
            self.angle=180
           


        self.xpos=self.xpos+self.velox
        self.ypos=self.ypos+self.veloy
        if self.xpos<0:
            self.xpos=0
            self.xpos=self.xpos-self.velox
            self.ypos=self.ypos-self.veloy
        if self.ypos<0:
            self.ypos=0
            self.xpos=self.xpos-self.velox
            self.ypos=self.ypos-self.veloy
        if self.xpos+self.tankwidth>=maxwidth:
            self.xpos=maxwidth-1-self.tankwidth
            self.xpos=self.xpos-self.velox
            self.ypos=self.ypos-self.veloy
        if self.ypos+self.tankheight>=maxheight:
            self.ypos=maxheight-1-self.tankheight
            self.xpos=self.xpos-self.velox
            self.ypos=self.ypos-self.veloy
        z=0
        for z in TankIndex:
            if z!=self and not z.Dead:
                dist=math.sqrt((z.xpos-self.xpos)*(z.xpos-self.xpos)+(z.ypos-self.ypos)*(z.ypos-self.ypos))
                if dist<self.tankwidth:
                    self.xpos=self.xpos-self.velox
                    self.ypos=self.ypos-self.veloy
        self.screenx = self.xpos-int(self.width/2)+int(self.tankwidth/2)
        self.screeny = self.ypos-int(self.height/2)+int(self.tankheight/2)
        if self.screenx<0:
            self.screenx=0
        if self.screeny<0:
            self.screeny=0
        if self.screenx+self.width>maxwidth:
            self.screenx=maxwidth-self.width
        if self.screeny+self.height>maxheight:
            self.screeny=maxheight-self.height
    def drawtank(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        temp=pygame.transform.rotate(self.tanksquare, self.angle)
        pork3.blit(temp, (self.xpos-temp.get_width()/2,self.ypos-temp.get_height()/2))


        x1=TankIndex[app.frame.Current].screenx
        y1=TankIndex[app.frame.Current].screeny
        x2=self.xpos
        y2=self.ypos
        self.namex=self.xpos+5-self.tankwidth/2
        self.namey=self.ypos-10-self.tankheight/2

        if x2-x1+80>width:  #off the right
            self.namex=x1+width-80
        if x1-x2>0: #off the left
            self.namex=x1
        if y2+20-y1>height: #off the bottom
            self.namey=y1+height-20
        if y1-y2>0: #off the top
            self.namey=y1
            
            
#        pork3.blit(self.nameplate.update(), (self.xpos+5-self.tankwidth/2,self.ypos-10-self.tankheight/2))
        pork3.blit(self.nameplate.update(), (self.namex,self.namey))
        
    def TakeDamage(self,impact):
        lefty=impact
        z=0
        while lefty>0:
            while z<len(self.armor.alist):
                if self.armor.alist[z].damage>0:
                    break
                z=z+1
            if z==len(self.armor.alist):
                lefty=self.chassis.chaslist[0].CalcDamage(lefty)
                if self.chassis.chaslist[0].damage<=0:
                    self.Dead=True
                    break
            else:
                lefty=self.armor.alist[z].CalcDamage(lefty)
class Armor():
    level=1
#    global TankIndex
    def __init__(self,parent):
        self.parent=parent
        self.alist=[]
    def AddArmor(self,name):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        mastererror=0
        if name in armordata:
            if TankIndex[app.frame.Current].Loading:
                self.alist.append(ArmorType(armordata[name][0],armordata[name][1],armordata[name][2],armordata[name][3],armordata[name][4]))
            elif armordata[name][4]<=TankIndex[app.frame.Current].Money:
                self.alist.append(ArmorType(armordata[name][0],armordata[name][1],armordata[name][2],armordata[name][3],armordata[name][4]))
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money-armordata[name][4]
                return 0
            else:
                mastererror=1
                dlg = wx.MessageDialog(app.frame, "You're broke. Tough Luck","Money Error",
                                    wx.CANCEL
                                   )
                dlg.ShowModal()
                dlg.Destroy()
                return 1
        elif name=="Tiger":
            if app.frame.RebootCall("Ivan"):
                self.alist.append(ArmorType("WtfHaxxor",0,1000000000,100,0))
    def DelArmor(self,id):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        cnt=0
        for c in self.alist:
            if c.id==id:
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money+c.cost
                app.frame.cashpan.Destroy()
                app.frame.cashpan=CashPanel(app.frame)
                del self.alist[cnt:cnt+1]
                app.frame.weightpan.Destroy()
                app.frame.weightpan=WeightPanel(app.frame)
            cnt=cnt+1
class ArmorType():
    name="None"
    weight=0
    strength=1
    damage=100
    cost=0
    id=None
    def __init__(self,name,weight,strength,damage,cost):
        self.name=name
        self.weight=weight
        self.strength=strength
        self.damage=damage
        self.cost=cost
    def CalcDamage(self,hit):
        perclost=100*hit/self.strength
        if perclost>self.damage:
            temp=perclost-self.damage
            self.damage=0
            return (temp/100)*self.strength
        else:
            self.damage-=perclost
            return 0
class Ammo():
    level=1
#    global TankIndex
    def __init__(self,parent):
        self.parent=parent
        self.amlist=[]
    def AddAmmo(self,name):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        mastererror=0
        c=0
        error=0
        for c in TankIndex[app.frame.Current].ammo.amlist:
            if name==c.name:
                error=1
        if error==0:
            if name in ammodata:
                if TankIndex[app.frame.Current].Loading:
                    self.amlist.append(AmmoType(ammodata[name][0],ammodata[name][1],ammodata[name][2],ammodata[name][3],ammodata[name][4],ammodata[name][5],ammodata[name][6],ammodata[name][7],ammodata[name][8]))
                elif ammodata[name][4]<=TankIndex[app.frame.Current].Money: 
                    self.amlist.append(AmmoType(ammodata[name][0],ammodata[name][1],ammodata[name][2],ammodata[name][3],ammodata[name][4],ammodata[name][5],ammodata[name][6],ammodata[name][7],ammodata[name][8]))
                    TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money-ammodata[name][4]
                    return 0
                else:
                    mastererror=1
                    dlg = wx.MessageDialog(app.frame, "You're broke. Tough Luck","Money Error",
                                    wx.CANCEL
                                   )
                    dlg.ShowModal()
                    dlg.Destroy()
                    return 1
            if name=="Panther":
                if app.frame.RebootCall("Feodor"):
                    self.amlist.append(AmmoType("Napalm",0,1000000,50,0,5,10,False,500))
    def DelAmmo(self,id):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        cnt=0
        for c in self.amlist:
            if c.id==id:
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money+c.cost
                app.frame.cashpan.Destroy()
                app.frame.cashpan=CashPanel(app.frame)
                del self.amlist[cnt:cnt+1]
                app.frame.weightpan.Destroy()
                app.frame.weightpan=WeightPanel(app.frame)
            cnt=cnt+1
class AmmoType():
    name="None"
    weight=0
    destruction=0
    area=0
    range=0
    cost=0
    id=None
    def __init__(self,name,weight,destruction,area,cost,speed,type,track,range):
        self.name=name
        self.weight=weight
        self.destruction=destruction
        self.area=area
        self.cost=cost
        self.speed=speed
        self.type=type
        self.track=track
        self.range=range
class Mine():
    level=1
#    global TankIndex
    def __init__(self,parent):
        self.parent=parent
        self.mmlist=[]
    def AddMine(self,name):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        mastererror=0
        if name in minedata:
            if TankIndex[app.frame.Current].Loading:
                self.mmlist.append(MineType(minedata[name][0],minedata[name][1],minedata[name][2],minedata[name][3],minedata[name][4],minedata[name][5],minedata[name][6],minedata[name][7],minedata[name][8]))
            elif minedata[name][5]<=TankIndex[app.frame.Current].Money: 
                self.mmlist.append(MineType(minedata[name][0],minedata[name][1],minedata[name][2],minedata[name][3],minedata[name][4],minedata[name][5],minedata[name][6],minedata[name][7],minedata[name][8]))
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money-minedata[name][5]
                return 0
            else:
                mastererror=1
                dlg = wx.MessageDialog(app.frame, "You're broke. Tough Luck","Money Error",
                                wx.CANCEL
                               )
                dlg.ShowModal()
                dlg.Destroy()
                return 1
    def DelMine(self,id):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        cnt=0
        for c in self.mmlist:
            if c.id==id:
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money+c.cost
                app.frame.cashpan.Destroy()
                app.frame.cashpan=CashPanel(app.frame)
                del self.mmlist[cnt:cnt+1]
                app.frame.weightpan.Destroy()
                app.frame.weightpan=WeightPanel(app.frame)
            cnt=cnt+1
class MineType():
    name="None"
    weight=0
    destruction=0
    area=0
    range=0
    cost=0
    type=-1
    track=False
    id=None
    target=-1
    proximity=0
    timer=100
    loaded=False
    loading=0
    def __init__(self,name,weight,destruction,area,range,cost,type,track,timer):
        self.name=name
        self.weight=weight
        self.destruction=destruction
        self.area=area
        self.range=range
        self.cost=cost
        self.type=type
        self.track=track
        self.timer=timer
class Gunnery():
    level=1
#    global TankIndex
    def __init__(self,parent):
        self.parent=parent
        self.glist=[]
    def ChangeGunnery(self,name):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        mastererror=0
        if name in gunnerydata:
            if TankIndex[app.frame.Current].Loading:
                self.glist[0]=(GunneryType(gunnerydata[name][0],gunnerydata[name][1],gunnerydata[name][2],gunnerydata[name][3],gunnerydata[name][4],gunnerydata[name][5],gunnerydata[name][6],gunnerydata[name][7]))
            elif gunnerydata[name][4]<=TankIndex[app.frame.Current].Money+self.glist[0].cost:
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money-gunnerydata[name][4]+self.glist[0].cost
                self.glist[0]=(GunneryType(gunnerydata[name][0],gunnerydata[name][1],gunnerydata[name][2],gunnerydata[name][3],gunnerydata[name][4],gunnerydata[name][5],gunnerydata[name][6],gunnerydata[name][7]))
                return 0
            else:
                mastererror=1
                dlg = wx.MessageDialog(app.frame, "You're broke. Tough Luck","Money Error",
                                    wx.CANCEL
                                   )
                dlg.ShowModal()
                dlg.Destroy()
                return 1
        elif name=="Abrams":
            if app.frame.RebootCall("Godunov"):
                self.glist[0]=(GunneryType("Hand of God",0,0,1,0,True,0,50000))
class GunneryType():
    name="None"
    weight=0
    accuracy=1
    rateoffire=100
    cost=0
    def __init__(self,name,weight,accuracy,rateoffire,cost,loaded,count,range):
        self.name=name
        self.weight=weight
        self.accuracy=accuracy
        self.rateoffire=rateoffire
        self.cost=cost
        self.loaded=loaded
        self.count=count
        self.reloadtime=rateoffire
        self.range=range
class Chassis():
    level=1
#    global TankIndex
    def __init__(self,parent):
        self.parent=parent
        self.chaslist=[]
    def ChangeChassis(self,name):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        mastererror=0
        if name in chassisdata:
            if TankIndex[app.frame.Current].Loading:
                self.chaslist[0]=(ChassisType(chassisdata[name][0],chassisdata[name][1],chassisdata[name][2],chassisdata[name][3],chassisdata[name][4],chassisdata[name][5]))
            elif chassisdata[name][5]<=TankIndex[app.frame.Current].Money+self.chaslist[0].cost:
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money-chassisdata[name][5]+self.chaslist[0].cost
                self.chaslist[0]=(ChassisType(chassisdata[name][0],chassisdata[name][1],chassisdata[name][2],chassisdata[name][3],chassisdata[name][4],chassisdata[name][5]))
                return 0
            else:
                mastererror=1
                dlg = wx.MessageDialog(app.frame, "You're broke. Tough Luck","Money Error",
                                    wx.CANCEL
                                   )
                dlg.ShowModal()
                dlg.Destroy()
                return 1
        elif name=="Leopard":
            if app.frame.RebootCall("Dmitri"):
                self.chaslist[0]=(ChassisType("Chariot of Fire",1,100,10000,100,0))
class ChassisType():
    name="None"
    weight=1
    capacity=1
    strength=1
    damage=100
    cost=0
    def __init__(self,name,weight,capacity,strength,damage,cost):
        self.name=name
        self.weight=weight
        self.capacity=capacity
        self.strength=strength
        self.damage=damage
        self.cost=cost
    def CalcDamage(self,hit):
        perclost=100*hit/self.strength
        if perclost>self.damage:
            temp=perclost-self.damage
            self.damage=0
            return (temp/100)*self.strength
        else:
            self.damage-=perclost
            return 0
class Engine():
    level=1
#    global TankIndex
    global enginedata
    def __init__(self,parent):
        self.parent=parent
        self.elist=[]
    def ChangeEngine(self,name):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        mastererror=0
        if name in enginedata:
            if TankIndex[app.frame.Current].Loading:
                self.elist[0]=(EngineType(enginedata[name][0],enginedata[name][1],enginedata[name][2],enginedata[name][3]))
            elif enginedata[name][3]<=TankIndex[app.frame.Current].Money+self.elist[0].cost:
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money-enginedata[name][3]+self.elist[0].cost
                self.elist[0]=(EngineType(enginedata[name][0],enginedata[name][1],enginedata[name][2],enginedata[name][3]))
                return 0
            else:
                mastererror=1
                dlg = wx.MessageDialog(app.frame, "You're broke. Tough Luck","Money Error",
                                    wx.CANCEL
                                   )
                dlg.ShowModal()
                dlg.Destroy()
                return 1
        elif name=="Whippet":
            if app.frame.RebootCall("Vasili"):
                self.elist[0]=(EngineType("Anti-Matter",0,10000,0))
class EngineType():
    global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,enginedata
    name="None"
    weight=0
    horsepower=0
    cost=0
    def __init__(self,name,weight,horsepower,cost):
        self.name=name
        self.weight=weight
        self.horsepower=horsepower
        self.cost=cost
class Decoy():
    level=1
#    global TankIndex
    def __init__(self,parent):
        self.parent=parent
        self.dlist=[]
    def AddDecoy(self,name):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        mastererror=0
        if name in decoydata:
            if TankIndex[app.frame.Current].Loading:
                self.dlist.append(DecoyType(decoydata[name][0],decoydata[name][1],decoydata[name][2],decoydata[name][3],decoydata[name][4],decoydata[name][5]))
            elif decoydata[name][5]<=TankIndex[app.frame.Current].Money:
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money-decoydata[name][5]
                self.dlist.append(DecoyType(decoydata[name][0],decoydata[name][1],decoydata[name][2],decoydata[name][3],decoydata[name][4],decoydata[name][5]))
                return 0
            else:
                mastererror=1
                dlg = wx.MessageDialog(app.frame, "You're broke. Tough Luck","Money Error",
                                    wx.CANCEL
                                   )
                dlg.ShowModal()
                dlg.Destroy()
                return 1
        elif name=="Sherman":
            if app.frame.RebootCall("Vasa"):
                self.dlist.append(DecoyType("Ultimate",0,1000000000,3000,100,0))
    def DelDecoy(self,id):
        cnt=0
        for c in self.dlist:
            if c.id==id:
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money+c.cost
                app.frame.cashpan.Destroy()
                app.frame.cashpan=CashPanel(app.frame)
                del self.dlist[cnt:cnt+1]
                app.frame.weightpan.Destroy()
                app.frame.weightpan=WeightPanel(app.frame)
            cnt=cnt+1
class DecoyType():
    name="None"
    weight=0
    strength=1
    duration=0
    damage=100
    cost=0
    id=None
    def __init__(self,name,weight,strength,duration,damage,cost):
        self.name=name
        self.weight=weight
        self.strength=strength
        self.duration=duration
        self.damage=damage
        self.cost=cost
    def CalcDamage(self,hit):
        perclost=hit/self.strength
        if perclost>self.damage:
            self.damage=0
            return (perclost-self.damage)*self.strength
        else:
            self.damage-=perclost
            return 0
class Fuel():
    level=1
#    global TankIndex
    def __init__(self,parent):
        self.parent=parent
        self.flist=[]
    def ChangeFuel(self,name):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        mastererror=0
        if name in fueldata:
            if TankIndex[app.frame.Current].Loading:
                self.flist[0]=(FuelType(fueldata[name][0],fueldata[name][1],fueldata[name][2],fueldata[name][3]))
            elif fueldata[name][3]<=TankIndex[app.frame.Current].Money+self.flist[0].cost:
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money-fueldata[name][3]+self.flist[0].cost
                self.flist[0]=(FuelType(fueldata[name][0],fueldata[name][1],fueldata[name][2],fueldata[name][3]))
                return 0
            else:
                mastererror=1
                dlg = wx.MessageDialog(app.frame, "You're broke. Tough Luck","Money Error",
                                    wx.CANCEL
                                   )
                dlg.ShowModal()
                dlg.Destroy()
                return 1
        elif name=="Panzer":
            if app.frame.RebootCall("Aleksey"):
                self.flist[0]=(FuelType("Bottomless",5,9999999999,0))
class FuelType():
    name="None"
    weight=0
    capacity=0
    cost=0
    def __init__(self,name,weight,capacity,cost):
        self.name=name
        self.weight=weight
        self.capacity=capacity
        self.cost=cost
class Scanner():
    level=1
#    global TankIndex
    def __init__(self,parent):
        self.parent=parent
        self.slist=[]
    def ChangeScanner(self,name):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        mastererror=0
        if name in scannerdata:
            if TankIndex[app.frame.Current].Loading:
                self.slist[0]=(ScannerType(scannerdata[name][0],scannerdata[name][1],scannerdata[name][2],scannerdata[name][3],scannerdata[name][4],scannerdata[name][5],scannerdata[name][6],scannerdata[name][7]))
            elif scannerdata[name][7]<=TankIndex[app.frame.Current].Money+self.slist[0].cost:
                TankIndex[app.frame.Current].Money=TankIndex[app.frame.Current].Money-scannerdata[name][7]+self.slist[0].cost
                self.slist[0]=(ScannerType(scannerdata[name][0],scannerdata[name][1],scannerdata[name][2],scannerdata[name][3],scannerdata[name][4],scannerdata[name][5],scannerdata[name][6],scannerdata[name][7]))
                return 0
            else:
                mastererror=1
                dlg = wx.MessageDialog(app.frame, "You're broke. Tough Luck","Money Error",
                                    wx.CANCEL
                                   )
                dlg.ShowModal()
                dlg.Destroy()
                return 1
        elif name=="Vickers":
            if app.frame.RebootCall("Khrushchev"):
                self.slist[0]=(ScannerType("All-Seeing Eye",0,True,10000000,1,360,0,0))
class ScannerType():
    name="None"
    weight=0
    fixed=True
    range=1
    maxrange=1
    arc=15
    maxarc=15
    cost=0
    angle=0
    ["Standard",200,True,20,1,45,1,1000]
    def __init__(self,name,weight,fixed,maxrange,range,arc,maxarc,cost):
        self.name=name
        self.weight=weight
        self.fixed=fixed
        self.range=range*20 # in pixels
        self.maxrange=maxrange*20
        self.arc=arc
        self.maxarc=maxarc # in degrees
        self.cost=cost
        self.area=arc*3.14*self.range*self.range/360

class MyTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent, id, pos, size, style):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
#        self.SetOwnBackgroundColour((100,100,100,0)) 
        self.SetOwnBackgroundColour((100,100,100)) 
    def OnCompareItems(self, item1, item2):
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        if t1 < t2: return -1
        if t1 == t2: return 0
        return 1
class IndiTankCtrlPanel(wx.Panel):
    def __init__(self, parent,scrsize):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,deekson,gason,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        wx.Panel.__init__(self, parent, -1, style=wx.NO_BORDER)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetOwnBackgroundColour((100,100,100)) 
        self.tID = wx.NewId()
        self.parent=parent
        self.tree = MyTreeCtrl(parent.ilpanel, self.tID, (0,0), scrsize,
                               style=wx.NO_BORDER
                               | wx.TR_HAS_BUTTONS
                               )

        self.isz = (16,16)
        self.il = wx.ImageList(self.isz[0], self.isz[1])
        self.fldridx     = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, self.isz))
        self.fldropenidx = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, self.isz))
        self.fileidx     = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, self.isz))

        self.tree.SetImageList(self.il)
        
#        global TankCount,TankIndex
        self.TankId=self.parent.Current

        self.root = self.tree.AddRoot("Your Tank")
        self.tree.SetItemData(self.root, None)
        self.tree.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.ammo = self.tree.AppendItem(self.root, "Ammo" )
        self.tree.SetItemData(self.ammo, None)
        self.tree.SetItemImage(self.ammo, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.ammo, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.mine = self.tree.AppendItem(self.root, "Mine" )
        self.tree.SetItemData(self.mine, None)
        self.tree.SetItemImage(self.mine, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.mine, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.armor = self.tree.AppendItem(self.root, "Armor" )
        self.tree.SetItemData(self.armor, None)
        self.tree.SetItemImage(self.armor, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.armor, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.chassis = self.tree.AppendItem(self.root, "Chassis" )
        self.tree.SetItemData(self.chassis, None)
        self.tree.SetItemImage(self.chassis, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.chassis, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        if deekson==True:
            self.decoy = self.tree.AppendItem(self.root, "Decoys" )
            self.tree.SetItemData(self.decoy, None)
            self.tree.SetItemImage(self.decoy, self.fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(self.decoy, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.engine = self.tree.AppendItem(self.root, "Engine")
        self.tree.SetItemData(self.engine, None)
        self.tree.SetItemImage(self.engine, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.engine, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        if gason==True:
            self.fuel = self.tree.AppendItem(self.root, "Fuel")
            self.tree.SetItemData(self.fuel, None)
            self.tree.SetItemImage(self.fuel, self.fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(self.fuel, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.gunnery = self.tree.AppendItem(self.root, "Gunnery" )
        self.tree.SetItemData(self.gunnery, None)
        self.tree.SetItemImage(self.gunnery, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.gunnery, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.scanner = self.tree.AppendItem(self.root, "Scanner" )
        self.tree.SetItemData(self.scanner, None)
        self.tree.SetItemImage(self.scanner, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.scanner, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.Update()
        

        self.tree.Expand(self.root)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self.tree)

        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        #
        self.tree.Bind(wx.EVT_RIGHT_DCLICK, self.OnRightDClick)
#        self.tree.Bind(wx.EVT_MIDDLE_DOWN,self.OnMiddleClick)
        #
#        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
#        self.tree.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        
    def Update(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,deekson,gason,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.TankId=self.parent.Current
        y=0
        self.tree.DeleteChildren(self.ammo)
        for y in range(len(TankIndex[self.TankId].ammo.amlist)):
                TankIndex[self.TankId].ammo.amlist[y].id=self.tree.AppendItem(self.ammo, "Ammo %4.0d" % (y+1))
                last=TankIndex[self.TankId].ammo.amlist[y].id 
                self.tree.SetItemData(last, None)
                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                
                ##Creates Sub-Items for each category
                item = self.tree.AppendItem(last, "Name: %s" % TankIndex[self.TankId].ammo.amlist[y].name)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Weight: %d" % TankIndex[self.TankId].ammo.amlist[y].weight)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Destruction: %d" % TankIndex[self.TankId].ammo.amlist[y].destruction)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Area: %d" % TankIndex[self.TankId].ammo.amlist[y].area)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Range: %d" % TankIndex[self.TankId].ammo.amlist[y].range)
                self.tree.SetItemData(item, None)
                     
        y=0
        self.tree.DeleteChildren(self.mine)
        for y in range(len(TankIndex[self.TankId].mine.mmlist)):
                TankIndex[self.TankId].mine.mmlist[y].id=self.tree.AppendItem(self.mine, "Mine %4.0d" % (y+1))
                last=TankIndex[self.TankId].mine.mmlist[y].id 
                self.tree.SetItemData(last, None)
                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                
                ##Creates Sub-Items for each category
                item = self.tree.AppendItem(last, "Name: %s" % TankIndex[self.TankId].mine.mmlist[y].name)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Weight: %d" % TankIndex[self.TankId].mine.mmlist[y].weight)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Destruction: %d" % TankIndex[self.TankId].mine.mmlist[y].destruction)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Area: %d" % TankIndex[self.TankId].mine.mmlist[y].area)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Range: %d" % TankIndex[self.TankId].mine.mmlist[y].range)
                self.tree.SetItemData(item, None)
                
                if TankIndex[self.TankId].mine.mmlist[y].track:
                    item = self.tree.AppendItem(last, "Proximity Fuse: True")
                else:
                    item = self.tree.AppendItem(last, "Proximity Fuse: False")
                self.tree.SetItemData(item, None)
                
                
        y=0
        self.tree.DeleteChildren(self.armor)
        for y in range(len(TankIndex[self.TankId].armor.alist)):
                
                last = self.tree.AppendItem(self.armor, "Layer %4.0d" % (y+1))
                TankIndex[self.TankId].armor.alist[y].id=last
                self.tree.SetItemData(last, None)
                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                
                ##Creates Sub-Items for each category
                item = self.tree.AppendItem(last, "Name: %s" % TankIndex[self.TankId].armor.alist[y].name)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Weight: %d" % TankIndex[self.TankId].armor.alist[y].weight)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Strength: %d" % TankIndex[self.TankId].armor.alist[y].strength)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Damage: %d" % TankIndex[self.TankId].armor.alist[y].damage)
                self.tree.SetItemData(item, None)
                
        self.tree.DeleteChildren(self.gunnery)
        for y in range(len(TankIndex[self.TankId].gunnery.glist)):
                last = self.tree.AppendItem(self.gunnery, "Gun")
                self.tree.SetItemData(last, None)
                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                
                ##Creates Sub-Items for each category
                item = self.tree.AppendItem(last, "Name: %s" % TankIndex[self.TankId].gunnery.glist[y].name)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Weight: %d" % TankIndex[self.TankId].gunnery.glist[y].weight)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Margin of Error: %d" % TankIndex[self.TankId].gunnery.glist[y].accuracy)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Rate of Fire: %d" % TankIndex[self.TankId].gunnery.glist[y].rateoffire)
                self.tree.SetItemData(item, None)

                item = self.tree.AppendItem(last, "Range: %d" % TankIndex[self.TankId].gunnery.glist[y].range)
                self.tree.SetItemData(item, None)

        self.tree.DeleteChildren(self.chassis)
        for y in range(len(TankIndex[self.TankId].chassis.chaslist)):
                last = self.tree.AppendItem(self.chassis, "Chassis")
                self.tree.SetItemData(last, None)
                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                
                ##Creates Sub-Items for each category
                item = self.tree.AppendItem(last, "Name: %s" % TankIndex[self.TankId].chassis.chaslist[y].name)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Weight: %d" % TankIndex[self.TankId].chassis.chaslist[y].weight)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Strength: %d" % TankIndex[self.TankId].chassis.chaslist[y].strength)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Capacity: %d" % TankIndex[self.TankId].chassis.chaslist[y].capacity)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Damage: %d" % TankIndex[self.TankId].chassis.chaslist[y].damage)
                self.tree.SetItemData(item, None)
                
        self.tree.DeleteChildren(self.engine)
        for y in range(len(TankIndex[self.TankId].engine.elist)):
                last = self.tree.AppendItem(self.engine, "Engine")
                self.tree.SetItemData(last, None)
                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                
                ##Creates Sub-Items for each category
                item = self.tree.AppendItem(last, "Name: %s" % TankIndex[self.TankId].engine.elist[y].name)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Weight: %d" % TankIndex[self.TankId].engine.elist[y].weight)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Horsepower: %d" % TankIndex[self.TankId].engine.elist[y].horsepower)
                self.tree.SetItemData(item, None)
        
        if deekson==True:
            self.tree.DeleteChildren(self.decoy)
            for y in range(len(TankIndex[self.TankId].decoy.dlist)):
                    last = self.tree.AppendItem(self.decoy, "Decoy %4.0d" % (y+1))
                    TankIndex[self.TankId].decoy.dlist[y].id=last
                    self.tree.SetItemData(last, None)
                    self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                    
                    ##Creates Sub-Items for each category
                    item = self.tree.AppendItem(last, "Name: %s" % TankIndex[self.TankId].decoy.dlist[y].name)
                    self.tree.SetItemData(item, None)
                    
                    item = self.tree.AppendItem(last, "Weight: %d" % TankIndex[self.TankId].decoy.dlist[y].weight)
                    self.tree.SetItemData(item, None)
                    
                    item = self.tree.AppendItem(last, "Strength: %d" % TankIndex[self.TankId].decoy.dlist[y].strength)
                    self.tree.SetItemData(item, None)
                    
                    item = self.tree.AppendItem(last, "Duration: %d" % TankIndex[self.TankId].decoy.dlist[y].duration)
                    self.tree.SetItemData(item, None)
                    
                    item = self.tree.AppendItem(last, "Damage: %d" % TankIndex[self.TankId].decoy.dlist[y].damage)
                    self.tree.SetItemData(item, None)
        
        if gason==True:    
            self.tree.DeleteChildren(self.fuel)
            for y in range(len(TankIndex[self.TankId].fuel.flist)):
                    last = self.tree.AppendItem(self.fuel, "Fuel Tank")
                    self.tree.SetItemData(last, None)
                    self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                    
                    ##Creates Sub-Items for each category
                    item = self.tree.AppendItem(last, "Name: %s" % TankIndex[self.TankId].fuel.flist[y].name)
                    self.tree.SetItemData(item, None)
                    
                    item = self.tree.AppendItem(last, "Weight: %d" % TankIndex[self.TankId].fuel.flist[y].weight)
                    self.tree.SetItemData(item, None)
                    
                    item = self.tree.AppendItem(last, "Capacity: %d" % TankIndex[self.TankId].fuel.flist[y].capacity)
                    self.tree.SetItemData(item, None)
            
        self.tree.DeleteChildren(self.scanner)
        for y in range(len(TankIndex[self.TankId].scanner.slist)):
                last = self.tree.AppendItem(self.scanner, "Scanner")
                self.tree.SetItemData(last, None)
                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                
                ##Creates Sub-Items for each category
                item = self.tree.AppendItem(last, "Name: %s" % TankIndex[self.TankId].scanner.slist[y].name)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Weight: %d" % TankIndex[self.TankId].scanner.slist[y].weight)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Range: %d" % TankIndex[self.TankId].scanner.slist[y].range)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Arc: %d" % TankIndex[self.TankId].scanner.slist[y].arc)
                self.tree.SetItemData(item, None)
        y=0
        self.tree.DeleteChildren(self.ammo)
        for y in range(len(TankIndex[self.TankId].ammo.amlist)):
                TankIndex[self.TankId].ammo.amlist[y].id=self.tree.AppendItem(self.ammo, "Ammo %4.0d" % (y+1))
                last=TankIndex[self.TankId].ammo.amlist[y].id 
                self.tree.SetItemData(last, None)
                self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                
                ##Creates Sub-Items for each category
                item = self.tree.AppendItem(last, "Name: %s" % TankIndex[self.TankId].ammo.amlist[y].name)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Weight: %d" % TankIndex[self.TankId].ammo.amlist[y].weight)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Destruction: %d" % TankIndex[self.TankId].ammo.amlist[y].destruction)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Area: %d" % TankIndex[self.TankId].ammo.amlist[y].area)
                self.tree.SetItemData(item, None)
                
                item = self.tree.AppendItem(last, "Range: %d" % TankIndex[self.TankId].ammo.amlist[y].range)
                self.tree.SetItemData(item, None)
        self.tree.ExpandAll()        

                

    def OnLeftDClick(self,event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        if GameRun==False:
            selec=event.GetPosition()
            item, flags = self.tree.HitTest(selec)
            if self.tree.GetItemParent(item)==self.tree.GetRootItem():
                #add new item
                if self.tree.GetItemText(item)=="Armor":
                    self.parent.InTreeAdd("Armor","Edit Armor")
                if self.tree.GetItemText(item)=="Decoys":
                    self.parent.InTreeAdd("Decoy","Edit Decoys")
                if self.tree.GetItemText(item)=="Ammo":
                    self.parent.InTreeAdd("Ammo","Edit Ammo")
                if self.tree.GetItemText(item)=="Mine":
                    self.parent.InTreeAdd("Mine","Edit Mine")
                if self.tree.GetItemText(item)=="Gunnery":
                    self.parent.InTreeAdd("Gunnery","Edit Gunnery")
                if self.tree.GetItemText(item)=="Engine":
                    self.parent.InTreeAdd("Engine","Edit Engine")
                if self.tree.GetItemText(item)=="Scanner":
                    self.parent.InTreeAdd("Scanner","Edit Scanner")
                if self.tree.GetItemText(item)=="Chassis":
                    self.parent.InTreeAdd("Chassis","Edit Chassis")
                if self.tree.GetItemText(item)=="Fuel":
                    self.parent.InTreeAdd("Fuel","Edit Fuel")
            elif item==self.tree.GetRootItem():
                self.SaveTank()
    def SaveTank(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        dlg = wx.FileDialog(
        self, message="Save",
        defaultDir=startdir, 
        defaultFile="",
        style=wx.SAVE | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        self.select=dlg.GetFilename()
        dlg.Destroy()
        z=0
        out=open(self.select,"wb+",99999999)
        out.write("0!"+TankIndex[self.TankId].title+"\r\n")
        out.write("1!"+TankIndex[self.TankId].PlayerName+"\r\n")
        out.write("2!"+str(TankIndex[self.TankId].Money)+"\r\n")
        while z < len(TankIndex[self.TankId].armor.alist):
            out.write("3!"+TankIndex[self.TankId].armor.alist[z].name+"\r\n")
            z=z+1
        z=0
        while z < len(TankIndex[self.TankId].ammo.amlist):
            out.write("4!"+TankIndex[self.TankId].ammo.amlist[z].name+"\r\n")
            z=z+1
        out.write("5!"+TankIndex[self.TankId].chassis.chaslist[0].name+"\r\n")
        z=0
        while z < len(TankIndex[self.TankId].decoy.dlist):
            out.write("6!"+TankIndex[self.TankId].decoy.dlist[z].name+"\r\n")
            z=z+1
        out.write("7!"+TankIndex[self.TankId].engine.elist[0].name+"\r\n")
        out.write("8!"+TankIndex[self.TankId].fuel.flist[0].name+"\r\n")
        out.write("9!"+TankIndex[self.TankId].scanner.slist[0].name+"\r\n")
        out.write("10!"+TankIndex[self.TankId].gunnery.glist[0].name+"\r\n")
        while z < len(TankIndex[self.TankId].mine.mmlist):
            out.write("11!"+TankIndex[self.TankId].mine.mmlist[z].name+"\r\n")
            z=z+1
        for line in TankIndex[self.TankId].Code.splitlines(): 
#            print "writing line:  " + line  
            out.write("99!"+line+"\n")

#    def OnRightDown(self, event):
#        pt = event.GetPosition();
#        item, flags = self.tree.HitTest(pt)
#        if item:
#            self.tree.SelectItem(item)

#    def OnRightUp(self, event):
#        pt = event.GetPosition();
#        item, flags = self.tree.HitTest(pt)
#        if item:        
#            self.tree.EditLabel(item)

    def OnBeginEdit(self, event):
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.tree.GetItemText(item) == "The Root Item":
            wx.Bell()

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.tree.GetFirstChild(root)

            while child.IsOk():
                (child, cookie) = self.tree.GetNextChild(root, cookie)

            event.Veto()

    def OnEndEdit(self, event):
        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                event.Veto()
                return

#    def OnLeftDClick(self, event):
#        pt = event.GetPosition();
#        item, flags = self.tree.HitTest(pt)
#        if item:
#            parent = self.tree.GetItemParent(item)
#            if parent.IsOk():
#                self.tree.SortChildren(parent)
#        event.Skip()
    def OnRightDClick(self, event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        if GameRun==False:
            selec=event.GetPosition()
            item, flags = self.tree.HitTest(selec)
            if self.tree.GetItemText(self.tree.GetItemParent(item))=="Ammo":
                TankIndex[self.TankId].ammo.DelAmmo(item)
                self.Update()
            if self.tree.GetItemText(self.tree.GetItemParent(item))=="Mine":
                TankIndex[self.TankId].mine.DelMine(item)
                self.Update()
            if self.tree.GetItemText(self.tree.GetItemParent(item))=="Armor":
                TankIndex[self.TankId].armor.DelArmor(item)
                self.Update()
            if self.tree.GetItemText(self.tree.GetItemParent(item))=="Decoys":
                TankIndex[self.TankId].decoy.DelDecoy(item)
                self.Update()
    def OnSize(self, event):
        w,h = self.GetClientSizeTuple()
        self.tree.SetDimensions(0, 0, w, h)

    def OnItemExpanded(self, event):
        item = event.GetItem()

    def OnItemCollapsed(self, event):
        item = event.GetItem()
            
    def OnSelChanged(self, event):
        self.item = event.GetItem()
        event.Skip()
        
    def OnActivate(self, event):
        1==1



class TankListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=(0,0),
                 size=(200,300), style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class TankListPanel(wx.Panel):
    def __init__(self, parent,scrsize):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        wx.Panel.__init__(self, parent, -1, style=wx.NO_BORDER)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetOwnBackgroundColour((100,100,100)) 
        self.tID = wx.NewId()
        self.parent=parent
        self.tree = MyTreeCtrl(parent.tlpanel, self.tID, (0,0), scrsize,
                               style=wx.NO_BORDER
                               | wx.TR_HAS_BUTTONS
                               )

        self.isz = (16,16)
        self.il = wx.ImageList(self.isz[0], self.isz[1])
        self.fldridx     = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, self.isz))
        self.fldropenidx = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, self.isz))
        self.fileidx     = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, self.isz))

        self.tree.SetImageList(self.il)

        self.root = self.tree.AddRoot("Tank Index")
        self.tree.SetItemData(self.root, None)
        self.tree.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.Update()
        

        self.tree.Expand(self.root)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self.tree)

        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.tree.Bind(wx.EVT_LEFT_UP, self.OnLeftClick)
        #
        self.tree.Bind(wx.EVT_RIGHT_DCLICK, self.OnRightDClick)
        #self.tree.Bind(wx.EVT_MIDDLE_DOWN,self.OnMiddleClick)
        #
#        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
 #       self.tree.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
    def ResetTanks(self):
        editon=False                
        if GameRun==False:
            self.parent.Current=0
            y=0
            text=TankIndex[self.parent.Current].Code
            self.parent.CodeArea.Clear()
            self.parent.CodeArea.AppendText(text)
            
            y=0
            self.parent.Refresh()
            self.parent.cashpan.Destroy()
            self.parent.cashpan=CashPanel(self.parent)
            self.parent.weightpan.Destroy()
            self.parent.weightpan=WeightPanel(self.parent)
            self.parent.namepan.Destroy()
            self.parent.namepan=NamePanel(self.parent)
            self.parent.Refresh()
            self.parent.TankTree.Refresh()
            self.parent.TankTree.Update()
            y=0
        elif GameRun==True:
            self.parent.Current=0
            screen=pygame.display.set_mode((width,height))
            self.SetWindowStyle(wx.MAXIMIZE_BOX)
            pygame.display.set_caption(TankIndex[self.parent.Current].PlayerName)
        editon=True                
    def Update(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.tree.DeleteChildren(self.root)

        unsortedlist=[]
        sortedlist=[]
        for x in range(len(TankIndex)):
            score="0000000000"+str(int(TankIndex[x].score))
            score=score[len(score)-10:len(score)]
            unsortedlist.append(score+":"+str(x))
        unsortedlist.sort(key=None,reverse=True)
        for x in unsortedlist:
            sortedlist.append(int(x.partition(":")[2]))

        for y in sortedlist:
            TankIndex[y].arch = self.tree.AppendItem(self.root, "%s" % TankIndex[y].PlayerName)
            last = TankIndex[y].arch
            self.tree.SetItemData(last, None)
            self.tree.SetItemImage(last, self.fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(last, self.fldropenidx, wx.TreeItemIcon_Expanded)
                
            ##Creates Sub-Items for each category
            potato="Empty"
            if(TankIndex[y].ai_prog!=0):
                potato="Set"
            item = self.tree.AppendItem(last, "Name:  %s" % TankIndex[y].PlayerName)
            self.tree.SetItemData(item, None)
                
                
            item = self.tree.AppendItem(last, "Id:    %d" % TankIndex[y].PlayerIdent)
            self.tree.SetItemData(item, None)
               
            item = self.tree.AppendItem(last, "Cash:  %d" % TankIndex[y].Money)
            self.tree.SetItemData(item, None)
                
            item = self.tree.AppendItem(last, "Score: %s" % int(TankIndex[y].score))
            self.tree.SetItemData(item, None)
        self.tree.ExpandAll()

    def OnLeftDClick(self,event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        selec=event.GetPosition()
        item, flags = self.tree.HitTest(selec)
        if GameRun==False:
            if item==self.tree.GetRootItem():
                self.LoadTank()
    def LoadTank(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.parent.Output.AppendText("\nLoad Tank Initiated")
        dlg = wx.FileDialog( #filedialog is what bring up the file explorer to select a file
            self, message="Choose", #the message is what is prompted to the user in the button to select a file
            defaultDir=startdir, 
            defaultFile="",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST #| wx.CHANGE_DIR These check conditions to make sure the file will work okay
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        
#        self.select=dlg.GetFilename()
        self.select=paths[0]
        dlg.Destroy()


        text=open(self.select,"r+",99999999)
        text1=text.readlines()
        z=0
        self.sepline=[]
        while z < len(text1):
            click=text1[z].rstrip().lstrip().partition("!")
            self.sepline.append(click)
            z=z+1
        if self.sepline[0][2]=="TankObject":
            editon=False
            app.frame.CodeArea.Clear()
            editon=True
            TankIndex.append(Tank())
            app.frame.Current=len(TankIndex)-1
            NewTank=TankIndex[app.frame.Current]
            NewTank.Loading=True
            TankCount=TankCount+1
            NewTank.PlayerIdent=TankCount
            NewTank.Money=9999999999999
            z=0
            while z<len(self.sepline):
                
                if self.sepline[z][0]=='3':
                    NewTank.armor.AddArmor(self.sepline[z][2])
                if self.sepline[z][0]=='4':
                    NewTank.ammo.AddAmmo(self.sepline[z][2])
                if self.sepline[z][0]=='5':
                    NewTank.chassis.ChangeChassis(self.sepline[z][2])
                if self.sepline[z][0]=='6':
                    NewTank.decoy.AddDecoy(self.sepline[z][2])
                if self.sepline[z][0]=='7':
                    NewTank.engine.ChangeEngine(self.sepline[z][2])
                if self.sepline[z][0]=='8':
                    NewTank.fuel.ChangeFuel(self.sepline[z][2])
                if self.sepline[z][0]=='9':
                    NewTank.scanner.ChangeScanner(self.sepline[z][2])
                if self.sepline[z][0]=='10':
                    NewTank.gunnery.ChangeGunnery(self.sepline[z][2])
                if self.sepline[z][0]=='11':
                    NewTank.mine.AddMine(self.sepline[z][2])
                if self.sepline[z][0]=='99':
                    NewTank.Code=NewTank.Code+self.sepline[z][2]+"\r\n"
                z=z+1
            app.frame.CodeArea.AppendText(NewTank.Code)
            z=0
            while z<len(self.sepline):
                if self.sepline[z][0]=='2':
                    NewTank.Money=int(self.sepline[z][2])
                z=z+1
            if get_money(NewTank)!=maxmoney:
                del TankIndex[app.frame.Current]
                TankCount=TankCount-1
                app.frame.Current=app.frame.Current-1
                app.frame.Output.AppendText('\nError:  Not a valid Tank Profile')
                app.frame.IndexTree.Refresh()
                app.frame.IndexTree.Update()
                app.frame.TankTree.Update()
                return
            self.dlg = wx.TextEntryDialog(self, 'Please Enter Your Player Name:','Name', "Name",wx.OK)
            if self.dlg.ShowModal() == wx.ID_OK:
                NewTank.PlayerName=self.dlg.GetValue()
            self.dlg.Destroy()
            app.frame.cashpan.Destroy()
            app.frame.cashpan=CashPanel(app.frame)
            app.frame.weightpan.Destroy()
            app.frame.weightpan=WeightPanel(app.frame)
            NewTank.Loading=False
            app.frame.namepan.Destroy()
            app.frame.namepan=NamePanel(app.frame)
##            self.parent.namepan.PName.Destroy()
##            self.parent.Refresh()
##            self.parent.namepan.PName=wx.StaticText(self.parent, -1, TankIndex[self.parent.Current].PlayerName, (self.parent.namepan.PNameX,self.parent.namepan.PNameY), (100, 20))
##            self.parent.namepan.PNamefont = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL)
##            self.parent.namepan.PName.SetFont(self.parent.namepan.PNamefont)
            self.parent.Refresh()
            self.parent.TankTree.Refresh()
            self.parent.TankTree.Update()
        else:
            app.frame.Output.AppendText('\nError:  Not a Tank Profile')
        app.frame.IndexTree.Refresh()
        app.frame.IndexTree.Update()
        app.frame.TankTree.Update()
    def NewTank(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        TankIndex.append(Tank())
        app.frame.Current=len(TankIndex)-1
        NewTank=TankIndex[app.frame.Current]
        NewTank.Loading=True
        TankCount=TankCount+1
        NewTank.PlayerIdent=TankCount
        self.dlg = wx.TextEntryDialog(self, 'Please Enter Your Player Name:','Name', "Name",wx.OK)
        if self.dlg.ShowModal() == wx.ID_OK:
            NewTank.PlayerName=self.dlg.GetValue()
        self.dlg.Destroy()
        app.frame.cashpan.Destroy()
        app.frame.cashpan=CashPanel(app.frame)
        app.frame.weightpan.Destroy()
        app.frame.weightpan=WeightPanel(app.frame)
        NewTank.Loading=False

        app.frame.namepan.Destroy()
        app.frame.namepan=NamePanel(app.frame)
##            self.parent.namepan.PName.Destroy()
##            self.parent.Refresh()
##            self.parent.namepan.PName=wx.StaticText(self.parent, -1, TankIndex[self.parent.Current].PlayerName, (self.parent.namepan.PNameX,self.parent.namepan.PNameY), (100, 20))
##            self.parent.namepan.PNamefont = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL)
##            self.parent.namepan.PName.SetFont(self.parent.namepan.PNamefont)
        self.parent.Refresh()
        self.parent.TankTree.Refresh()
        self.parent.TankTree.Update()
        app.frame.IndexTree.Refresh()
        app.frame.IndexTree.Update()
        app.frame.TankTree.Update()

#    def OnRightDown(self, event):
#        pt = event.GetPosition();
#        item, flags = self.tree.HitTest(pt)
#        if item:
#            self.tree.SelectItem(item)

#    def OnRightUp(self, event):
#        pt = event.GetPosition();
#        item, flags = self.tree.HitTest(pt)
#        if item:        
#            self.tree.EditLabel(item)
            
    def OnRightDClick(self, event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        if GameRun==False:
            selec=event.GetPosition()
            item, flags = self.tree.HitTest(selec)
            if self.tree.GetItemText(self.tree.GetItemParent(item))=="Tank Index" and TankCount>=1:
                z=0
                while z<len(TankIndex):
                    if TankIndex[z].arch==item:
                        break
                    else:
                        z=z+1
                if z<len(TankIndex):
                    del TankIndex[z:z+1]
                    TankCount=TankCount-1
                    z=0
                    while z<len(TankIndex):
                        TankIndex[z].PlayerIdent=z
                        z=z+1
                    self.parent.Current=0
                    self.parent.IndexTree.Update()
                    self.parent.TankTree.Update()
    def OnBeginEdit(self, event):
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.tree.GetItemText(item) == "The Root Item":
            wx.Bell()

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.tree.GetFirstChild(root)

            while child.IsOk():
                (child, cookie) = self.tree.GetNextChild(root, cookie)

            event.Veto()

    def OnEndEdit(self, event):
        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                event.Veto()
                return

    def OnLeftClick(self, event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        editon=False                
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        c=0
        for c in TankIndex:
            if c.arch==item:
                break
        if GameRun==False:
            self.parent.Current=c.PlayerIdent
            y=0
            self.parent.CodeArea.Clear()
            self.parent.CodeArea.AppendText(TankIndex[self.parent.Current].Code)
            
            y=0
            self.parent.Refresh()
            self.parent.cashpan.Destroy()
            self.parent.cashpan=CashPanel(self.parent)
            self.parent.weightpan.Destroy()
            self.parent.weightpan=WeightPanel(self.parent)
            self.parent.namepan.Destroy()
            self.parent.namepan=NamePanel(self.parent)
            self.parent.Refresh()
            self.parent.TankTree.Refresh()
            self.parent.TankTree.Update()
            y=0
        elif GameRun==True:
            self.parent.Current=c.PlayerIdent
#            self.SetWindowStyle(wx.MAXIMIZE_BOX)
            screen=pygame.display.set_mode((width,height))
            self.SetWindowStyle(wx.MAXIMIZE_BOX)
            pygame.display.set_caption(TankIndex[self.parent.Current].PlayerName)
        editon=True                
#    def OnLeftClick(self, event):
#        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
#        editon=False                
#        pt = event.GetPosition();
#        item, flags = self.tree.HitTest(pt)
#        c=0
#        for c in TankIndex:
#            if c.arch==item:
#                break
#        if GameRun==False:
#            self.parent.Current=c.PlayerIdent
#            self.parent.CodeArea.Clear()
#            self.parent.CodeArea.AppendText(TankIndex[self.parent.Current].Code)
#            self.parent.Refresh()
#            self.parent.cashpan.Destroy()
#            self.parent.cashpan=CashPanel(self.parent)
#            self.parent.weightpan.Destroy()
#            self.parent.weightpan=WeightPanel(self.parent)
#            app.frame.namepan.Destroy()
#            app.frame.namepan=NamePanel(app.frame)
#            self.parent.Refresh()
#            self.parent.TankTree.Refresh()
#            self.parent.TankTree.Update()
#        elif GameRun==True:
#            self.parent.Current=c.PlayerIdent
#            screen=pygame.display.set_mode((width,height))
#            self.SetWindowStyle(wx.MAXIMIZE_BOX)
#            pygame.display.set_caption(TankIndex[self.parent.Current].PlayerName)
#        editon=True                
    def OnSize(self, event):
        w,h = self.GetClientSizeTuple()
        self.tree.SetDimensions(0, 0, w, h)

    def OnItemExpanded(self, event):
        item = event.GetItem()

    def OnItemCollapsed(self, event):
        item = event.GetItem()
            
    def OnSelChanged(self, event):
        self.item = event.GetItem()
        event.Skip()
        
    def OnActivate(self, event):
        1==1
class CashPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent, -1, (25,50), (100,15))
        self.parent=parent
        self.SetOwnBackgroundColour((200,220,40))  
        self.cashamount=wx.StaticText(self, -1, "Cash: $"+str(TankIndex[self.parent.Current].Money), (0,0), (100,25))
        self.cashamount.SetForegroundColour((50,50,50))
    def OnPaint(self,event):
        dc=wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.BeginDrawing()
        dc.DrawBitmap(self.exp,10,10,False)
        dc.DrawBitmap(self.exp,0,0,True)
        dc.EndDrawing()
    def destroy(self,event):
        self.Destroy() 
class NamePanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent, -1, (25,10), (150,25))
        self.parent=parent
        self.SetOwnBackgroundColour((20,200,20))  
        self.PName=wx.StaticText(self, -1, "Tank: "+TankIndex[self.parent.Current].PlayerName, (0,0), (150, 25))
        self.PNamefont = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.PName.SetFont(self.PNamefont)
        self.PName.SetForegroundColour((20,20,20))
    def OnPaint(self,event):
        dc=wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.BeginDrawing()
        dc.DrawBitmap(self.exp,10,10,False)
        dc.DrawBitmap(self.exp,0,0,True)
        dc.EndDrawing()
    def destroy(self,event):
        self.Destroy() 
class WeightPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent, -1, (25,65), (100,30))
        self.parent=parent
        self.SetOwnBackgroundColour((200,180,100))
        currtank=TankIndex[self.parent.Current]
        c=0
        Weight=0
        for c in currtank.armor.alist:
            Weight=Weight+c.weight
        if deekson:
            for c in currtank.decoy.dlist:
                Weight=Weight+c.weight
        for c in currtank.ammo.amlist:
            Weight=Weight+c.weight
        for c in currtank.mine.mmlist:
            Weight=Weight+c.weight
        Weight=Weight+currtank.chassis.chaslist[0].weight
        Weight=Weight+currtank.engine.elist[0].weight
        Weight=Weight+currtank.scanner.slist[0].weight
        if gason:
            Weight=Weight+currtank.fuel.flist[0].weight
        Weight=Weight+currtank.gunnery.glist[0].weight
        currtank.Weight=Weight
        currtank.speed=currtank.chassis.chaslist[0].damage*40*currtank.engine.elist[0].horsepower/(Weight*50) 
        self.weightread=wx.StaticText(self, -1, "Weight: "+str(Weight)+"\nSpeed:  "+str(currtank.speed), (0,0), (100,30))
        self.weightread.SetForegroundColour((50,50,50))
    def OnPaint(self,event):
        dc=wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.BeginDrawing()
        dc.DrawBitmap(self.exp,10,10,False)
        dc.DrawBitmap(self.exp,0,0,True)
        dc.EndDrawing()
    def destroy(self,event):
        self.Destroy() 
class TestDialog(wx.Dialog):
    def __init__(
            self, parent, ID, data,script,  
            style=wx.DEFAULT_DIALOG_STYLE
            ):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        wx.Dialog.__init__(self, parent, -1,script,wx.DefaultPosition,(200,200))
        self.parent=parent
        self.data=data
        self.tank=TankIndex[app.frame.Current]
        self.box=wx.ComboBox(self, 500, TankIndex[app.frame.Current].data[data][0][0], (42, 50), (115, -1), TankIndex[app.frame.Current].data[data][0], wx.CB_DROPDOWN)
        self.click=wx.Button(self,1,"Add",(67,100),(75,25))
        self.Bind(wx.EVT_BUTTON, self.clicked, id=1)
    def clicked(self,event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        z=0
        error=0
        c=0
        tick=0
        if self.data=="Armor" or self.data=="Decoy":
            error=0
            mastererror=TankIndex[app.frame.Current].data[self.data][3](self.box.GetValue()) 
        if self.data=="Ammo":
            for c in range(len(TankIndex[app.frame.Current].data[self.data][1])):
                if self.box.GetValue()==TankIndex[app.frame.Current].data[self.data][1][c].name:
                    error=1
            if error==0:
                mastererror=TankIndex[app.frame.Current].data[self.data][3](self.box.GetValue())
        if self.data=="Mine":
            error=0
            mastererror=TankIndex[app.frame.Current].data[self.data][3](self.box.GetValue())
        if self.data=="Scanner" or self.data=="Chassis" or self.data=="Engine" or self.data=="Gunnery" or self.data=="Fuel":
            tick=1
            c=0
            for c in range(len(TankIndex[app.frame.Current].data[self.data][1])):
                if self.box.GetValue()==TankIndex[app.frame.Current].data[self.data][1][c].name:
                    error=1
        if error==0:
            if tick==1:
                mastererror=TankIndex[app.frame.Current].data[self.data][3](self.box.GetValue())
            c=0
            for c in range(len(TankIndex[app.frame.Current].data[self.data][1])):
                    if TankIndex[app.frame.Current].data[self.data][1][c].name==self.box.GetValue():
                        break
            if mastererror==0:
                self.parent.cashpan.Destroy()
                self.parent.cashpan=CashPanel(self.parent)
                self.parent.weightpan.Destroy()
                self.parent.weightpan=WeightPanel(self.parent)
            self.parent.IndexTree.Update()
            self.parent.TankTree.Update()
class PopDialog(wx.Dialog):
    def __init__(self,statement,title):
        wx.Dialog.__init__(self,-1)
        self.text=statement
        popper = wx.MessageDialog(self, statement,
                       title,
                       wx.OK | wx.ICON_INFORMATION
                       )
        popper.ShowModal()
        popper.Destroy()
class EndGame(wx.Dialog):
    def __init__(self,parent,statement,title):
        wx.Dialog.__init__(self,parent,-1)
        self.text=statement
        popper = wx.MessageDialog(self, statement,
                       title,
                       wx.OK | wx.ICON_INFORMATION
                       )
        popper.ShowModal()
        popper.Destroy()
#----------------------------------------------------------------------

# This shows how to catch the OnLinkClicked non-event.  (It's a virtual
# method in the C++ code...)
class MyHtmlWindow(html.HtmlWindow):
    def __init__(self, parent, id):
        html.HtmlWindow.__init__(self, parent, id, style=wx.NO_FULL_REPAINT_ON_RESIZE|html.HW_SCROLLBAR_AUTO)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

class AboutBox(wx.Dialog):
    def __init__(self, parent):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        wx.Dialog.__init__(self, parent, -1, "Programming Instructions", wx.DefaultPosition, (520,480),style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.parent=parent

        self.html = MyHtmlWindow(self, -1)


        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.html, 1, wx.GROW)

        subbox = wx.BoxSizer(wx.HORIZONTAL)

        self.box.Add(subbox, 0, wx.GROW)
        self.SetSizer(self.box)
        self.SetAutoLayout(True)

        self.button = wx.Button(self, 2001, "OK", (250,420), (50,-1))
        self.button.Bind(wx.EVT_BUTTON, self.OnOK)
        self.OnShowDefault(None)

    def OnOK(self, event):
        self.EndModal(wx.ID_OK)

    def OnShowDefault(self, event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        name = os.path.join(startdir, "instr.html")
        self.html.LoadPage(name)


class MyFrame(wx.Frame):
    def __init__(self, parent):
#INitial tank object here
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        TankObj=Tank()
        TankIndex.append(TankObj)
        TankIndex[0].PlayerIdent=TankCount
        self.PNameX=25
        self.PNameY=23
        self.IndList=TankIndex
        wx.Frame.__init__(self, parent, -1, "Opening Screen", pos=(0,0),size=(width,height), style=wx.DEFAULT_FRAME_STYLE)
        self.SetOwnBackgroundColour((100,100,100))
        self.Current=0      
        self.newrun=True
        self.randstart=0
        OriginalTanks=[]
##        self.tlpanel=wx.Panel(self,900,(610,100),(200,550),style=wx.SUNKEN_BORDER)
##        self.ilpanel=wx.Panel(self,901,(10,100),(200,550),style=wx.SUNKEN_BORDER)
        self.tlpanel=wx.Panel(self,900,(int(width*.75-10),100),(int(width*.25),int(height*.8)-70),style=wx.SUNKEN_BORDER)
        self.ilpanel=wx.Panel(self,901,(10,100),(int(width*.25),int(height*.8)-70),style=wx.SUNKEN_BORDER)
        self.dlg = wx.TextEntryDialog(self, 'Please Enter Your Player Name:','Name', "Name",wx.OK)
        if self.dlg.ShowModal() == wx.ID_OK:
            TankIndex[self.Current].PlayerName=self.dlg.GetValue()
            self.namepan=NamePanel(self)
        self.dlg.Destroy()
        self.TankTree = IndiTankCtrlPanel(self,(int(width*.25),int(height*.8)-75))
        self.cashpan=CashPanel(self)
        self.weightpan=WeightPanel(self)
        self.Refresh()
        self.IndexTree=TankListPanel(self,(int(width*.25),int(height*.8)-75))
        self.sq=wx.BitmapButton(self,4001,wx.Bitmap("images/square.png"),(20,38),(5,5))
        self.Bind(wx.EVT_BUTTON,self.WindowAdjust,id=4001)
        self.CodeArea = wx.TextCtrl(self, 800,
                        TankIndex[self.Current].Code,
                       (int(width*.25+10), 100),(int(width*.5-20),int(height*.5)), style=wx.TE_MULTILINE|wx.SIZE_ALLOW_MINUS_ONE)
        self.Output=wx.TextCtrl(self,-1,"Welcome to TankWarz.  Load a tank and program to compete in the arena, or create your own.",(int(width*.25+10),100+int(height*.5)+5),(int(width*.5-20),int(height*.3)-75),style=wx.TE_MULTILINE|wx.SIZE_ALLOW_MINUS_ONE|wx.TE_READONLY)
        self.Output.SetBackgroundColour((150,150,150))
        self.Refresh()

        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menuBar = wx.MenuBar()
        menu1 = wx.Menu()

        # 1st menu from left
        menu1a = wx.Menu()
        menu1a.Append(151, "&Tank", "Create a new tank")
        menu1a.Append(152, "&Program", "Create a new program")
        menu1b = wx.Menu()
        menu1b.Append(161, "&Tank", "Load a tank")
        menu1b.Append(162, "&Program", "Load a program")
        menu1b.Append(163, "&Arena", "Load an arena")
        menu1b.Append(164, "&Replay", "Load a replay")
        menu1c = wx.Menu()
        menu1c.Append(171, "&Tank", "Save a tank")
        menu1c.Append(172, "&Program", "Save a program")
        menu1c.Append(173, "&Arena", "Save an arena")
        menu1.Append(101, "&New", menu1a)
        menu1.Append(102, "&Load", menu1b)
        menu1.Append(103, "&Save", menu1c)
        menu1.AppendSeparator()
        menu1.Append(104, "&Exit", "Close this frame")
        # Add menu to the menu bar
        menuBar.Append(menu1, "&File")

        # 2nd menu from left
        menu2 = wx.Menu()
        menu2.Append(201, "Compile Code")
        menu2.Append(202, "Enter Arena")
        menu2.Append(203, "Clear Scores")
        menuBar.Append(menu2, "&Run")
        menu3 = wx.Menu()
        menu3.Append(301, "Instructions")
        menuBar.Append(menu3, "&Help")


        self.SetMenuBar(menuBar)

        # Menu events
        self.Bind(wx.EVT_TEXT,self.updatecode,id=800)
        self.Bind(wx.EVT_MENU_HIGHLIGHT_ALL, self.OnMenuHighlight)

        self.Bind(wx.EVT_MENU, self.NewTank, id=151)
        self.Bind(wx.EVT_MENU, self.NewProgram, id=152)
        self.Bind(wx.EVT_MENU, self.LoadTank, id=161)
        self.Bind(wx.EVT_MENU, self.Load, id=162)
        self.Bind(wx.EVT_MENU, self.LoadArena, id=163)
        self.Bind(wx.EVT_MENU, self.LoadReplay, id=164)
        self.Bind(wx.EVT_MENU, self.SaveTank, id=171)
        self.Bind(wx.EVT_MENU, self.Save, id=172)
        self.Bind(wx.EVT_MENU, self.SaveArena, id=173)
        self.Bind(wx.EVT_MENU, self.CloseWindow, id=104)

        self.Bind(wx.EVT_MENU, self.Compile, id=201)
        self.Bind(wx.EVT_MENU, self.Start, id=202)
        self.Bind(wx.EVT_MENU, self.ClearScores, id=203)
        self.Bind(wx.EVT_MENU, self.instruct, id=301)


    # Methods

    def OnMenuHighlight(self, event):
        # Show how to get menu item info from this event handler
        id = event.GetMenuId()
        item = self.GetMenuBar().FindItemById(id) ##current compass
        if item:
            text = item.GetLabel()
            help = item.GetHelp()

        # but in this case just call Skip so the default is done
        event.Skip() 

    def updatecode(self, event):
        if editon:
            TankIndex[self.Current].Code=self.CodeArea.GetValue()

    def ClearScores(self, event):
        for z in TankIndex:
            z.score=0
            

    def CloseWindow(self, event):
        self.Close()




    def OnWindowClose(self, event):
        self.Destroy()
    def instruct(self, event):
        about = AboutBox(self)
        about.Show(True)
        about.ShowModal()
    def Compile(self,event):
####is this the right way to access the current tank in focus?####
        global width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.Output.AppendText("\nCompiling...\n")
        TankIndex[self.Current].ai_prog=ai_prog(TankIndex[self.Current],None,[])
        lines=TankIndex[self.Current].Code
        lines=lines.split("\n")
        TankIndex[self.Current].ai_prog.build(lines)
        TankIndex[self.Current].ai_prog.execute([])
        self.Output.AppendText("\nCompile Complete.\n")
    def LoadTank(self,event):
        self.IndexTree.LoadTank()
    def SaveTank(self,event):
        self.TankTree.SaveTank()
    def Save(self,event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.Output.AppendText("\nSave Initiated")
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=startdir, 
            defaultFile="", style=wx.SAVE
            )
        dlg.SetFilterIndex(2)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        self.select=path
        dlg.Destroy()
        if len(self.select)>0:
            file=open(self.select,"wb+",9999999)
            self.Output.AppendText('\n'+self.select)
            file.write(TankIndex[self.Current].Code) 
        else:
            self.Output.AppendText('\nSave Cancelled\n')
    def SaveArena(self,event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.Output.AppendText("\nSave Arena Initiated")
        dlg = wx.FileDialog(
            self, message="Save arena as ...", defaultDir=startdir, 
            defaultFile="", style=wx.SAVE
            )
        dlg.SetFilterIndex(2)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        self.select=path
        dlg.Destroy()
        if len(self.select)>0:
            out=open(self.select,"wb+",9999999)
            self.Output.AppendText('\n'+self.select)
            #step through all tanks in the list and save them in the arena file.
    
            for tank in TankIndex:
                out.write("999!+++++=====+++++\r\n")
                out.write("0!"+tank.title+"\r\n")
                out.write("1!"+tank.PlayerName+"\r\n")
                out.write("2!"+str(tank.Money)+"\r\n")
                z=0
                while z < len(tank.armor.alist):
                    out.write("3!"+tank.armor.alist[z].name+"\r\n")
                    z=z+1
                z=0
                while z < len(tank.ammo.amlist):
                    out.write("4!"+tank.ammo.amlist[z].name+"\r\n")
                    z=z+1
                out.write("5!"+tank.chassis.chaslist[0].name+"\r\n")
                z=0
                while z < len(tank.decoy.dlist):
                    out.write("6!"+tank.decoy.dlist[z].name+"\r\n")
                    z=z+1
                out.write("7!"+tank.engine.elist[0].name+"\r\n")
                out.write("8!"+tank.fuel.flist[0].name+"\r\n")
                out.write("9!"+tank.scanner.slist[0].name+"\r\n")
                out.write("10!"+tank.gunnery.glist[0].name+"\r\n")
                z=0
                while z < len(tank.mine.mmlist):
                    out.write("11!"+tank.mine.mmlist[z].name+"\r\n")
                    z=z+1
                for line in tank.Code.splitlines(): 
                    out.write("99!"+line+"\n")
        else:
            self.Output.AppendText('\nSave Arena Cancelled\n')
    def LoadArena(self,event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        #SOMETHING IS UP WITH INDICES!!!!!
        self.Output.AppendText("\nLoad Arena Initiated")
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=startdir, 
            defaultFile="",
            style=wx.OPEN #| wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        
#        self.select=dlg.GetFilename()
        self.select=paths[0]
        dlg.Destroy()
        text=open(self.select,"r+",99999999)
        text1=text.readlines()
        z=0
        self.sepline=[]
        #grab old values incase of a load failure
        self.oldtankindex=TankIndex
        self.oldcurrent=app.frame.Current
        self.oldtankcount=TankCount
        TankIndex=[]
        app.frame.Current=-1
        TankCount=-1
        while z < len(text1):
            click=text1[z].rstrip().lstrip().partition("!")
            self.sepline.append(click)
            z=z+1
        first_tank=True
        editon=False

        for line in self.sepline:
            if line[0]=="999":
                #new tank found
                if not first_tank:
                    if get_money(NewTank)!=maxmoney:
                        TankIndex=self.oldtankindex
                        app.frame.Current=self.oldcurrent
                        TankCount=self.oldtankcount
                        app.frame.Output.AppendText('\nError: Arena contains an invlaid tank profile.')
                        app.frame.IndexTree.Refresh()
                        app.frame.IndexTree.Update()
                        app.frame.TankTree.Update()
                        return
                    else:
                        app.frame.CodeArea.Clear()
                        editon=True
                        app.frame.CodeArea.AppendText(NewTank.Code)
                        editon=False

                        NewTank.Loading=False

                        app.frame.cashpan.Destroy()
                        app.frame.cashpan=CashPanel(app.frame)
                        app.frame.weightpan.Destroy()
                        app.frame.weightpan=WeightPanel(app.frame)
                        app.frame.namepan.Destroy()
                        app.frame.namepan=NamePanel(app.frame)

                        app.frame.Refresh()

                        app.frame.IndexTree.Update()
                        app.frame.IndexTree.Refresh()

                        app.frame.TankTree.Update()
                        app.frame.TankTree.Refresh()


            
                TankIndex.append(Tank())
                app.frame.Current=len(TankIndex)-1
                NewTank=TankIndex[app.frame.Current]
                NewTank.Loading=True
                NewTank.Code=''
                TankCount=TankCount+1
                NewTank.PlayerIdent=TankCount
                NewTank.Money=0
                first_tank=False

            if line[0]=='1':
                NewTank.PlayerName=line[2]
            if line[0]=='2':
                NewTank.Money=int(line[2])
            if line[0]=='3':
                NewTank.armor.AddArmor(line[2])
            if line[0]=='4':
                NewTank.ammo.AddAmmo(line[2])
            if line[0]=='5':
                NewTank.chassis.ChangeChassis(line[2])
            if line[0]=='6':
                NewTank.decoy.AddDecoy(line[2])
            if line[0]=='7':
                NewTank.engine.ChangeEngine(line[2])
            if line[0]=='8':
                NewTank.fuel.ChangeFuel(line[2])
            if line[0]=='9':
                NewTank.scanner.ChangeScanner(line[2])
            if line[0]=='10':
                NewTank.gunnery.ChangeGunnery(line[2])
            if line[0]=='11':
                NewTank.mine.AddMine(line[2])
            if line[0]=='99':
                NewTank.Code=NewTank.Code+line[2]+"\r\n"



        app.frame.CodeArea.Clear()
        app.frame.CodeArea.AppendText(NewTank.Code)

        editon=True
        NewTank.Code=self.CodeArea.GetValue()
        app.frame.cashpan.Destroy()
        app.frame.cashpan=CashPanel(app.frame)
        app.frame.weightpan.Destroy()
        app.frame.weightpan=WeightPanel(app.frame)
        app.frame.namepan.Destroy()
        app.frame.namepan=NamePanel(app.frame)
        NewTank.Loading=False


        self.Current=0
        app.frame.cashpan.Destroy()
        app.frame.cashpan=CashPanel(app.frame)
        app.frame.weightpan.Destroy()
        app.frame.weightpan=WeightPanel(app.frame)
        app.frame.namepan.Destroy()
        app.frame.namepan=NamePanel(app.frame)

        app.frame.Refresh()

        app.frame.IndexTree.Update()
        app.frame.IndexTree.ResetTanks()
        app.frame.IndexTree.Refresh()

        app.frame.TankTree.Update()
        app.frame.TankTree.Refresh()



    def LoadReplay(self,event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        #SOMETHING IS UP WITH INDICES!!!!!
        self.Output.AppendText("\nLoad Replay Initiated")
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=startdir+"/replays/", 
            defaultFile="",
            style=wx.OPEN #| wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        
#        self.select=dlg.GetFilename()
        self.select=paths[0]
        dlg.Destroy()
        text=open(self.select,"r+",99999999)
        text1=text.readlines()
        z=0
        self.sepline=[]
        #grab old values incase of a load failure
        self.oldtankindex=TankIndex
        self.oldcurrent=app.frame.Current
        self.oldtankcount=TankCount
        TankIndex=[]
        app.frame.Current=-1
        TankCount=-1
        while z < len(text1):
            click=text1[z].rstrip().lstrip().partition("!")
            self.sepline.append(click)
            z=z+1
        first_tank=True
        editon=False

        for line in self.sepline:
            if line[0]=="800":
                self.randstart=int(line[2])
                self.newrun=False
            if line[0]=="999":
                #new tank found
                if not first_tank:
                    if get_money(NewTank)!=maxmoney:
                        TankIndex=self.oldtankindex
                        app.frame.Current=self.oldcurrent
                        TankCount=self.oldtankcount
                        app.frame.Output.AppendText('\nError: Arena contains an invlaid tank profile.')
                        app.frame.IndexTree.Refresh()
                        app.frame.IndexTree.Update()
                        app.frame.TankTree.Update()
                        return
                    else:
                        app.frame.CodeArea.Clear()
                        editon=True
                        app.frame.CodeArea.AppendText(NewTank.Code)
                        editon=False

                        NewTank.Loading=False

                        app.frame.cashpan.Destroy()
                        app.frame.cashpan=CashPanel(app.frame)
                        app.frame.weightpan.Destroy()
                        app.frame.weightpan=WeightPanel(app.frame)
                        app.frame.namepan.Destroy()
                        app.frame.namepan=NamePanel(app.frame)

                        app.frame.Refresh()

                        app.frame.IndexTree.Update()
                        app.frame.IndexTree.Refresh()

                        app.frame.TankTree.Update()
                        app.frame.TankTree.Refresh()


            
                TankIndex.append(Tank())
                app.frame.Current=len(TankIndex)-1
                NewTank=TankIndex[app.frame.Current]
                NewTank.Loading=True
                NewTank.Code=''
                TankCount=TankCount+1
                NewTank.PlayerIdent=TankCount
                NewTank.Money=0
                first_tank=False

            if line[0]=='1':
                NewTank.PlayerName=line[2]
            if line[0]=='2':
                NewTank.Money=int(line[2])
            if line[0]=='3':
                NewTank.armor.AddArmor(line[2])
            if line[0]=='4':
                NewTank.ammo.AddAmmo(line[2])
            if line[0]=='5':
                NewTank.chassis.ChangeChassis(line[2])
            if line[0]=='6':
                NewTank.decoy.AddDecoy(line[2])
            if line[0]=='7':
                NewTank.engine.ChangeEngine(line[2])
            if line[0]=='8':
                NewTank.fuel.ChangeFuel(line[2])
            if line[0]=='9':
                NewTank.scanner.ChangeScanner(line[2])
            if line[0]=='10':
                NewTank.gunnery.ChangeGunnery(line[2])
            if line[0]=='11':
                NewTank.mine.AddMine(line[2])
            if line[0]=='99':
                NewTank.Code=NewTank.Code+line[2]+"\r\n"



        app.frame.CodeArea.Clear()
        app.frame.CodeArea.AppendText(NewTank.Code)

        editon=True
        NewTank.Code=self.CodeArea.GetValue()
        app.frame.cashpan.Destroy()
        app.frame.cashpan=CashPanel(app.frame)
        app.frame.weightpan.Destroy()
        app.frame.weightpan=WeightPanel(app.frame)
        app.frame.namepan.Destroy()
        app.frame.namepan=NamePanel(app.frame)
        NewTank.Loading=False


        self.Current=0
        app.frame.cashpan.Destroy()
        app.frame.cashpan=CashPanel(app.frame)
        app.frame.weightpan.Destroy()
        app.frame.weightpan=WeightPanel(app.frame)
        app.frame.namepan.Destroy()
        app.frame.namepan=NamePanel(app.frame)

        app.frame.Refresh()

        app.frame.IndexTree.Update()
        app.frame.IndexTree.ResetTanks()
        app.frame.IndexTree.Refresh()

        app.frame.TankTree.Update()
        app.frame.TankTree.Refresh()


    def Load(self,event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.Output.AppendText("\nLoad Initiated")
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=startdir, 
            defaultFile="",
            style=wx.OPEN #| wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        
#        self.select=dlg.GetFilename()
        self.select=paths[0]
        dlg.Destroy()
        if len(self.select)>0:
            text=open(self.select,"r+",99999999)
            text1=text.readlines()
            for x in text1:
                self.CodeArea.AppendText(x)
            self.Output.AppendText('\nLoad Successful')
            self.CodeArea.AppendText('\n')
        else:
            self.Output.AppendText('\nLoad Cancelled')
            self.CodeArea.AppendText('\n')
    def NewProgram(self,event):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.Output.AppendText("\nClearing code area...")
        self.CodeArea.Clear()
        self.CodeArea.AppendText("\n#Enter your Program Here\n")
        TankIndex[self.Current].Code=self.CodeArea.GetValue()
    def NewTank(self,event):
        self.IndexTree.NewTank()
    def returntomain(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.SetFocus()
        eng.stop()
        screen = pygame.display.set_mode((1,1))
        pork3.blit(pork4,(0,0)) #clear screen
        #remove all Missiles
        for x in range(0,len(MissileIndex)):
            del MissileIndex[0]
        #remove all Mines
        for x in range(0,len(MineIndex)):
            del MineIndex[0]
        #remove all Tanks
        GameRun=False
        for z in TankIndex:
            if z.Dead:
                z.score=z.score-3000 # deduct 3000 for each dead tank
            for y in z.armor.alist:
                y.damage=100
            z.chassis.chaslist[0].damage=100
            z.Dead=False
        self.Current=0
        app.frame.cashpan.Destroy()
        app.frame.cashpan=CashPanel(app.frame)
        app.frame.weightpan.Destroy()
        app.frame.weightpan=WeightPanel(app.frame)
        app.frame.namepan.Destroy()
        app.frame.namepan=NamePanel(app.frame)

        app.frame.Refresh()

        app.frame.IndexTree.Update()
        app.frame.IndexTree.ResetTanks()
        app.frame.IndexTree.Refresh()

        app.frame.TankTree.Update()
        app.frame.TankTree.Refresh()

        backmusic.fadeout(1500)

    def saverun(self,randstart):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        runfilename=startdir+"/replays/"+"run_"+str(self.randstart)+strftime("%d_%m_%Y_%H_%M_%S", gmtime())+".run"
        out=open(runfilename,"w")#note that you can enter a number here for the buffer, but I removed it from this statement because I didn't see why it was there
        #step through all tanks in the list and save them in the arena file.
        for tank in TankIndex:
            out.write("800!"+str(self.randstart)+"\r\n")#compass2
            out.write("999!+++++=====+++++\r\n")
            out.write("0!"+tank.title+"\r\n")
            out.write("1!"+tank.PlayerName+"\r\n")
            out.write("2!"+str(tank.Money)+"\r\n")
            z=0
            while z < len(tank.armor.alist):
                out.write("3!"+tank.armor.alist[z].name+"\r\n")
                z=z+1
            z=0
            while z < len(tank.ammo.amlist):
                out.write("4!"+tank.ammo.amlist[z].name+"\r\n")
                z=z+1
            out.write("5!"+tank.chassis.chaslist[0].name+"\r\n")
            z=0
            while z < len(tank.decoy.dlist):
                out.write("6!"+tank.decoy.dlist[z].name+"\r\n")
                z=z+1
            out.write("7!"+tank.engine.elist[0].name+"\r\n")
            out.write("8!"+tank.fuel.flist[0].name+"\r\n")
            out.write("9!"+tank.scanner.slist[0].name+"\r\n")
            out.write("10!"+tank.gunnery.glist[0].name+"\r\n")
            z=0
            while z < len(tank.mine.mmlist):
                out.write("11!"+tank.mine.mmlist[z].name+"\r\n")
                z=z+1
            for line in tank.Code.splitlines(): 
                out.write("99!"+line+"\n")

    def Start(self,event):#This function is what runs when "Enter Arena" is pressed in the game
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        GameRun=True
        tanks=0
        z=0
        self.time=300000
        screen=pygame.display.set_mode(flags=pygame.FULLSCREEN)

        backmusic.play(-1,self.time)
            
        random.seed()

        if self.newrun:
            self.randstart=random.randint(1,10000000)
            random.seed(self.randstart)
            self.saverun(self.randstart) #this line calls saverun, another import method in the myframe class
        else:  # using an already generated run ie a replay
            random.seed(self.randstart)

        self.newrun=True

        cnt=0
        tanksingame=0
        for z in TankIndex:
            z.score=z.score+3000 # add score of 100 for survival
            z.ai_prog=ai_prog(z,None,[])
            lines=z.Code
            lines=lines.split("\n")
            z.ai_prog.build(lines)
            z.ai_prog.execute([])
            z.Dead=False
            tanksingame=tanksingame+1
        displaymode="r"
        self.paused=False
        #set random positions
        
        row=int(math.sqrt(tanksingame)+1)
        cells=row*row
        cellwidth=int(maxwidth/row)-20
        if cellwidth<100:
            cellwidth=100
        cellheight=int(maxheight/row)-20
        if cellheight<100:
            cellheight=100
        halfwidth=int(cellwidth/2)
        halfheight=int(cellheight/2)
        rw=0
        tankstarts=[]
        while rw<row:
            cl=0
            while cl<row:
                tankstarts.append((cellwidth*rw+halfwidth+random.randint(int(-.5*halfwidth),int(.5*halfwidth)),cellheight*cl+halfheight+random.randint(int(-.5*halfheight),int(.5*halfheight))))
                cl=cl+1
            rw=rw+1
        for currtank in TankIndex:
            # go in a spiral inward toward the center of the field for intial starting positions
            startcell=random.randint(0,len(tankstarts)-1)
            stx=tankstarts[startcell][0]
            sty=tankstarts[startcell][1]
            del tankstarts[startcell]
            currtank.xpos=stx
            currtank.ypos=sty
            currtank.destx=currtank.xpos
            currtank.desty=currtank.ypos
            currtank.speed=currtank.chassis.chaslist[0].damage*40*currtank.engine.elist[0].horsepower/(currtank.Weight*50) 
            if len(currtank.ammo.amlist)>0:
                currtank.currentammo=currtank.ammo.amlist[0]
            else:
                currtank.currentammo=None
            if len(currtank.mine.mmlist)>0:
                currtank.currentmine=currtank.mine.mmlist[0]
            else:
                currtank.currentmine=None
                        
            currtank.guncircle=pygame.Surface((currtank.gunnery.glist[0].range*2,currtank.gunnery.glist[0].range*2)).convert_alpha()
            currtank.guncircle.fill((0,0,0,0))
            ratio1=int(255*(float(currtank.gunnery.glist[0].reloadtime)/float(currtank.gunnery.glist[0].rateoffire)))
            ratio2=int(255-255*(float(currtank.gunnery.glist[0].reloadtime)/float(currtank.gunnery.glist[0].rateoffire)))
            pygame.draw.circle(currtank.guncircle, (ratio2,ratio1,50,120), (currtank.gunnery.glist[0].range-2,currtank.gunnery.glist[0].range-2), currtank.gunnery.glist[0].range, 10)
            currtank.scancircle=pygame.Surface((currtank.scanner.slist[0].range*2,currtank.scanner.slist[0].range*2)).convert_alpha()
            currtank.scancircle.fill((0,0,0,0))
            pygame.draw.arc(currtank.scancircle, (30,30,220,30), pygame.Rect((0,0),(currtank.scanner.slist[0].range*2,currtank.scanner.slist[0].range*2)), 6.28*(currtank.scanner.slist[0].angle-currtank.scanner.slist[0].arc/2)/360, 6.28*(currtank.scanner.slist[0].angle+currtank.scanner.slist[0].arc/2)/360,currtank.scanner.slist[0].range)

            tanks=tanks+1 #set number of tanks currently in the game

        eng.play(-1)
        miltime=pygame.time.get_ticks()
        mil2time=pygame.time.get_ticks()
        while 1:
            mil3time=pygame.time.get_ticks()
            while (mil3time-mil2time<20):
                mil3time=pygame.time.get_ticks()
            mil2time=pygame.time.get_ticks()
            #manage and update gameprogress here

            #Clean up dead tanks and Missiles here
            cnt=0
            for x in MissileIndex:
                if not x.active:
                    del MissileIndex[cnt]
                    cnt=cnt-1
                else:
                    x.index=cnt
                cnt=cnt+1
            cnt=0
            for x in MineIndex:
                if not x.active:
                    del MineIndex[cnt]
                    cnt=cnt-1
                else:
                    x.index=cnt
                cnt=cnt+1
            cnt=0
            for x in TankIndex:
                if not x.Dead:
                    cnt=cnt+1
            if cnt!=tanks:
                pork3.blit(pork4,(0,0)) #clear screen
                tanks=cnt
                

            #Check end of game here
            pygame.display.set_caption(TankIndex[self.Current].PlayerName)
            pygame.event.pump()
            keys=pygame.event.get(pygame.KEYUP)
            pygame.event.get()
            if len(keys)>0:
                if keys[0].key==pygame.K_f:
                    self.SetWindowStyle(wx.MINIMIZE_BOX)
                    screen=pygame.display.set_mode((width,height),pygame.FULLSCREEN)
                    displaymode="f"
                if keys[0].key==pygame.K_r:
                    self.SetWindowStyle(wx.MAXIMIZE_BOX)
                    screen=pygame.display.set_mode((width,height))
                    displaymode="r"
                if keys[0].key==pygame.K_l:
                    dlg = wx.FileDialog(
                        self, message="Choose a file",
                        defaultDir=startdir, 
                        defaultFile="",
                        style=wx.OPEN #| wx.CHANGE_DIR
                        )

                    paths=[None]
                    if dlg.ShowModal() == wx.ID_OK:
                        paths = dlg.GetPaths()
                    
            #        self.select=dlg.GetFilename()
                    self.select=paths[0]
                    dlg.Destroy()


                if keys[0].key==pygame.K_p:
                    if self.paused:                    
                        self.paused=False
                    else:
                        self.paused=True
                if keys[0].key==pygame.K_RIGHT:
                    self.Current=self.Current+1
                    if self.Current>=len(TankIndex):
                        self.Current=0
                    while TankIndex[self.Current].Dead:
                        self.Current=self.Current+1
                        if self.Current>=len(TankIndex):
                            self.Current=0
                if keys[0].key==pygame.K_LEFT:
                    self.Current=self.Current-1
                    if self.Current<0:
                        self.Current=len(TankIndex)-1
                    while TankIndex[self.Current].Dead:
                        self.Current=self.Current-1
                        if self.Current<0:
                            self.Current=len(TankIndex)-1
                if keys[0].key==pygame.K_ESCAPE:
                    self.returntomain()
                    break                
            if not self.paused:
                for currtank in TankIndex:
                    if not currtank.Dead:
                        tempprog=currtank.ai_prog.next_step()            
                        if tempprog!=None:
                            currtank.ai_prog=tempprog
                for currtank in TankIndex:
                    if not currtank.Dead:
                        currtank.speed=currtank.chassis.chaslist[0].damage*40*currtank.engine.elist[0].horsepower/(currtank.Weight*50)
                        currtank.movetank()
                for currmiss in MissileIndex:
                    if currmiss.active:
                        currmiss.Move()
                for currmine in MineIndex:
                    if currmine.active:
                        currmine.Move()
                for currtank in TankIndex:
                    if not currtank.Dead:
                        currtank.drawtank()
                for currmiss in MissileIndex:
                    if currmiss.active and not currmiss.exploding:
                        currmiss.Draw()
                for currmine in MineIndex:
                    if currmine.active and not currmine.exploding:
                        currmine.Draw()
                miltime2=pygame.time.get_ticks()
                self.time=self.time-(miltime2-miltime)
                miltime=miltime2
                if self.time<=0:
                    tanks=0
#            if displaymode=="f":
#                screen.blit(pygame.transform.scale(pork3.subsurface(pygame.Rect(0,0,maxwidth,maxheight)),(width,height)),(0,0))
#            else:
            screen.blit(TankIndex[self.Current].viewtank(),(0,0))#returns a surface to display on screen
            # now blit special effects on screen after update has happened.
            # first weapon ranges
            ttnk=TankIndex[self.Current]
            left=ttnk.screenx
            top=ttnk.screeny
            right=left+width
            bottom=top+height
            weaprect=pygame.Rect((left,top),(width,height))
            scanrect=pygame.Rect((left,top),(width,height))
            weaplist=[]
            scanlist=[]
            for tnk in TankIndex:
                #do we show the weapon range for the current tank?
                weaplist.append(pygame.Rect((tnk.xpos-tnk.gunnery.glist[0].range,tnk.ypos-tnk.gunnery.glist[0].range),(2*tnk.gunnery.glist[0].range,2*tnk.gunnery.glist[0].range)))
                scanlist.append(pygame.Rect((tnk.xpos-tnk.scanner.slist[0].range,tnk.ypos-tnk.scanner.slist[0].range),(2*tnk.scanner.slist[0].range,2*tnk.scanner.slist[0].range)))


            for wp in weaprect.collidelistall(weaplist):
                #it is in the screen draw it at position offset 
                tnk=TankIndex[wp]
                xp=tnk.xpos-ttnk.screenx
                yp=tnk.ypos-ttnk.screeny
                if not tnk.Dead:
                    ratio1=(float(tnk.gunnery.glist[0].reloadtime)/float(tnk.gunnery.glist[0].rateoffire))
                    ratio2=1-(float(tnk.gunnery.glist[0].reloadtime)/float(tnk.gunnery.glist[0].rateoffire))
#                    ratio1=int(255*(float(tnk.gunnery.glist[0].reloadtime)/float(tnk.gunnery.glist[0].rateoffire)))
#                    ratio2=int(255-255*(float(tnk.gunnery.glist[0].reloadtime)/float(tnk.gunnery.glist[0].rateoffire)))
                    pygame.draw.circle(tnk.guncircle, (int(255*ratio2),int(255*ratio1),50,10+(240*ratio1)), (tnk.gunnery.glist[0].range-2,tnk.gunnery.glist[0].range-2), tnk.gunnery.glist[0].range, 3+int(12*ratio2))
                    screen.blit(tnk.guncircle,(xp-tnk.gunnery.glist[0].range,yp-tnk.gunnery.glist[0].range))
            
            for sc in scanrect.collidelistall(scanlist):
                tnk=TankIndex[sc]
                xp=tnk.xpos-ttnk.screenx
                yp=tnk.ypos-ttnk.screeny
                if not tnk.Dead:
                    screen.blit(tnk.scancircle,(xp-tnk.scanner.slist[0].range,yp-tnk.scanner.slist[0].range))


            
            scoreboard.updatescore()
            if tanks==1:
                #find winner
                for winner in TankIndex:
                    if not winner.Dead:
                        puttext(screen,(250,50),winner.PlayerName+" WINS!",None,30,(220,220,220,180),"None")
                self.paused=True
            elif tanks<1:
                self.time=0
                puttext(screen,(250,50),"DRAW!",None,30,(220,220,220,180),"None")
                self.paused=True
            pygame.display.flip()
            
    def RebootCall(self,keyword):
        self.dialog = wx.TextEntryDialog(self, "Please enter the password for this selection", "Verification")

        if self.dialog.ShowModal() == wx.ID_OK:
            if self.dialog.GetValue()==keyword:
                self.dialog.Destroy()
                return True
            else:
                self.dialog.Destroy()
                return False
    def WindowAdjust(self,event):
        x=1
    def InTreeAdd(self,data,script):
        self.dialog = TestDialog(self, -1, data,script, 
                         style=wx.DEFAULT_DIALOG_STYLE
                         )
        # this does not return until the dialog is closed.
        val = self.dialog.ShowModal()
#        print val
#end of myframe class
class score():
    def __init__(self):
        self.board=pygame.surface.Surface((250,175))
        self.board=self.board.convert_alpha()
        self.boardtime=pygame.surface.Surface((150,30))
        self.boardtime=self.boardtime.convert_alpha()
    def ptext(self,x,y,text,surf,color):
        puttext(surf,(x,y),text,None,20,color,"None")
    def updatescore(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,app,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.tank=TankIndex[app.frame.Current]
        strength=0
        for x in self.tank.armor.alist:
            strength=strength+x.damage*x.strength/100
        strength2=self.tank.chassis.chaslist[0].damage*self.tank.chassis.chaslist[0].strength/100   
        self.board.fill((30,50,150,80))
        self.ptext(5,5,"Player:             "+self.tank.PlayerName,self.board,(220,220,100,150))
        if self.tank.currentammo!=None:
            self.ptext(5,20,"Current Ammo:      "+self.tank.currentammo.name,self.board,(220,220,100,150))
        if self.tank.currentmine!=None:
            self.ptext(5,35,"Current Mine:      "+self.tank.currentmine.name,self.board,(220,220,100,150))
        self.ptext(5,50,"Armor Strength:    "+str(int(strength)),self.board,(220,220,100,150))
        self.ptext(5,65,"Chassis Strength:  "+str(int(strength2)),self.board,(220,220,100,150))
        self.ptext(5,80,"Current Position:  ("+str(int(self.tank.xpos))+", "+str(int(self.tank.ypos))+")",self.board,(220,220,100,150))
        self.ptext(5,95,"Destination:       ("+str(int(self.tank.destx))+", "+str(int(self.tank.desty))+")",self.board,(220,220,100,150))
        self.ptext(5,110,"Speed:             "+str(int(self.tank.speed)),self.board,(220,220,100,150))
        self.ptext(5,125,"Tank ID:           "+str(self.tank.PlayerIdent),self.board,(220,220,100,150))
        self.ptext(5,140,"SCORE:           "+str(int(self.tank.score)),self.board,(220,220,100,150))
#        ratio1=int(10*(float(self.tank.gunnery.glist[0].reloadtime)/float(self.tank.gunnery.glist[0].rateoffire)))
#        ratio2=int(10-10*(float(self.tank.gunnery.glist[0].reloadtime)/float(self.tank.gunnery.glist[0].rateoffire)))
#        self.ptext(5,155,"Gun Charge:      ",self.board,(220,220,100,150))


        
#        self.ptext(5,155,"Gun Charge:      "+chr(219)*ratio1+chr(177)*ratio2,self.board,(220,220,100,150))
        screen.blit(self.board,(0,0))

        self.boardtime.fill((30,150,50,80))
        hrs=int(app.frame.time/3600000)
        mins=int((app.frame.time-hrs*3600000)/60000)
        secs=int((app.frame.time-hrs*3600000-mins*60000)/1000)
        huns=app.frame.time-hrs*3600000-mins*60000-secs*1000
        
        self.ptext(5,5,"Time:  "+str(hrs).rjust(2,"0")+":"+str(mins).rjust(2,"0")+":"+str(secs).rjust(2,"0")+"."+str(huns).rjust(2,"0")[0:2],self.boardtime,(220,220,100,150))
        screen.blit(self.boardtime,(width-150,height-30))#compass3

class nameplate():
    def __init__(self,parent):
        self.board=pygame.surface.Surface((80,20))
        self.board=self.board.convert_alpha()
        self.parent=parent
    def ptext(self,x,y,text,surf,color):
        puttext(surf,(x,y),text,None,16,color,"left")
    def update(self):
        global mineexp,mineimg,missexp,missimg,pork5,editon,maxmoney,startdir,app,width,height,size,screen,maxwidth,maxheight,pork3,road,notroad,notroadrock,road_notroad,recroad_rectnotroad,input,roadmap,counta,countb,countc,tanks,pork4,OriginalTanks,TankCount,TankIndex,MissileIndex,GameRun,mastererror,ammodata,minedata,armordata,gunnerydata,chassisdata,enginedata,decoydata,fueldata,scannerdata,keyword_list,arg_list,function_list,variable_list,statement_list,operator_list,sep_list,operator_list2,operators,comp_list1,comp_list2,keywords_list,canned_list,app
        self.tank=self.parent
        bars=[self.tank.chassis.chaslist[0].damage]
        for barsitem in self.tank.armor.alist:
            bars.insert(1,barsitem.damage)
        self.board.fill((30,50,150,0))
        self.ptext(2,20,self.tank.PlayerName,self.board,(220,220,150,200))
        x=0
        for bar in bars:
            self.board.blit(self.statusbar(bar,4,15,(20,250,20,190)),(x*6+50,0))
            x=x+1

        return self.board
    def statusbar(self,percent,x,y,color):
        surf=pygame.surface.Surface((x,y))
        greenrect=surf.get_rect()
        grayrect=surf.get_rect()
        green=int(y*percent/100)
        gray=int(y*(100-percent)/100)
        greenrect.height=green
        grayrect.height=gray
        greenrect.top=gray
        pygame.draw.rect(surf,(250,20,20,0),grayrect)
        pygame.draw.rect(surf,color,greenrect)
        return surf






class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None)
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        return True


if __name__ == '__main__':
    scoreboard=score()
    app = MyApp(0)
    app.MainLoop()
    
