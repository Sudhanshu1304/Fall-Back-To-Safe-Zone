import pygame
import sys
import math
import  pickle
import numpy as np
import random

from pygame import draw


pygame.init()

Number = 100
TIME = 40


class Cars:

    def __init__(self,win,speed,x,y):
        self.speed = speed
        self.win = win
        self.x = x
        self.y = y
        self.last = 1
        self.lis=[1,2,3,4]
        self.car_col = (219, 3, 252)
        self.car_moved_index=0
        # self.rect = pygame.rect.Rect(self.x,self.y,125,125)
        # pygame.draw.rect(self.win,(0,255,0),self.rect,0)
        height = int(pygame.display.get_surface().get_height())
        width = height
        self.block_sizew = int((width)/Number)
        self.vel = 1#self.block_sizew
        
    def moveUp(self):
        #print("Moving up")
        self.y = self.y - self.vel 
    
    def moveDown(self):
        #print("Moving  down")
        self.y = self.y + self.vel 

    def moveRight(self):
        #print("Moving right")
        self.x = self.x + self.vel 

    def moveLeft(self):
        #print("Moving left")
        self.x = self.x - self.vel 

    def mov_opt(self,val):
        if(val==1):
            return (self.x + self.vel,self.y)
        elif(val==2):
            return (self.x,self.y + self.vel )
        elif(val==3):
            return (self.x - self.vel,self.y )
        else:
            return (self.x,self.y - self.vel)

    def move_on_path(self,path):
        
        
        self.x= path[self.car_moved_index][0]
        self.y= path[self.car_moved_index][1]
        x = self.x*self.block_sizew
        y = self.y*self.block_sizew
        self.rect = pygame.rect.Rect(x,y,self.block_sizew,self.block_sizew)
        pygame.draw.rect(self.win,self.car_col,self.rect,0)
        
        
        if(self.car_moved_index==len(path)-1):
           # print("FINISH LINE !!")
            pass
        else:
            self.car_moved_index=self.car_moved_index+1
        
        
    def move(self,path,path_given=False):
        
        
        
        x=self.x
        y=self.y

        #print("Present loc : ",self.x,self.y)
        #print("New List is : ",self.lis,"\n",self.x,self.y)
        
        for i in range(1,5):
            check = self.lis[i-1]
            #print(self.mov_opt(check))
            if(self.mov_opt(check) in path):
                if(check==1):
                    self.moveRight()
                    self.last=1
                    break
                elif(check==2):
                    self.moveDown()
                    self.last=2
                    break
                elif(check==3):
                    self.moveLeft()
                    self.last=3
                    break
                else:
                    self.moveUp()
                    self.last=4
                    break
                    
        if(self.last==1):
            self.lis.remove(3)
            self.lis.append(3)
        elif(self.last==3):
            self.lis.remove(1)
            self.lis.append(1)
        elif(self.last==2):
            self.lis.remove(4)
            self.lis.append(4)
        else:
            self.lis.remove(2)
            self.lis.append(2)
        self.lis.insert(0,self.lis.pop(self.lis.index(self.last)))
        
        
        #print("Cords : ",self.x,self.y) 
        if(path_given==False):
            #print("Trueee")
            if((x,y) in path):
                x = self.x*self.block_sizew
                y = self.y*self.block_sizew
                
                self.rect = pygame.rect.Rect(x,y,self.block_sizew,self.block_sizew)
                pygame.draw.rect(self.win,self.car_col,self.rect,0)
  
        return (self.x,self.y)


###########  GUI


Background = (33, 173, 103)
factor = 1

class Grid:

    global block ,blockColor ,Normal, STATE, path_col, dest_co, Block, Adj_list,density,factor,start_node,ANS,activate

    blockColor = (0,0,250)
    Normal = (255,255,255)#Background
    path_col = (223, 235, 0)
    dest_co = (0, 145, 235)
    density=True
    activate=False

    #block=[]
    Block = {}
    STATE = {}
    
    Adj_list = {}


    def __init__(self,win,):
        global Block 
        self.win= win
        self.font = pygame.font.SysFont('Arial', 25)
        
        self.path = []
        self.dest = []
        self.dest_capacity={}
        self.visited = set()
        self.visited2=[]
        self.path_des_val = {}
        self.found_path = []
        self.First=True
        self.Path_obj=[]
        self.help_region=[]
        
        file = open("state.pkl",'rb')
        Block = pickle.load(file)
        self.Path()
        self.ANS2={}
        self.ANS2_KEY=[]
        self.ANS2_VAEUE=[]
        
        n = 200
        #print("Len is : ",len(self.path))
        #print("Paths : ",self.path)
        self.obj=[]
        factor = 1
        for _ in range(1*n):
            rand_num = random.randint(0,len(self.path)-1)
            loc  = self.path[rand_num]
            
            
            
            if loc in self.path_des_val:
                self.path_des_val[loc] = self.path_des_val[loc] + factor
            else:
                self.path_des_val[loc] = factor
            
            # if(loc in self.help_region):
            #     self.Path_obj.append(Cars(self.win,5,loc[0],loc[1]))
            # else:
            self.obj.append(Cars(self.win,5,loc[0],loc[1]))


        for i  in range(1):
            for region in self.help_region:
                self.Path_obj.append(Cars(self.win,5,region[0],region[1]))
        
        
    def Create_Adj_list(self,node):

        for nigh in [(node[0],node[1]+1),(node[0]+1,node[1]),(node[0]-1,node[1]),(node[0],node[1]-1)]:
            if(nigh in self.path):

                if(nigh in self.visited2):
                    #Adj_list[node].append(nigh)
                    try:
                        if nigh not in Adj_list[node]:
                            Adj_list[node].append(nigh)
                    except:
                        Adj_list[node] = [nigh]
                    return
                else:
                    try:
                        if nigh not in Adj_list[node]:
                            Adj_list[node].append(nigh)
                    except:
                        Adj_list[node] = [nigh]
                    
                    self.visited2.append(node)
                  
                    self.Create_Adj_list(nigh)
    

    
    def Path(self):
        global Block
        #print("Block : ",Block)
        for key in Block:
            if(Block[key] ==2 or Block[key] ==3 or Block[key]==7 ):

                if( Block[key]==3):
                    self.dest.append(key)
                    self.dest_capacity[key]=random.randint(1,5)
                self.path.append(key)
                if(Block[key]==7):
                    self.help_region.append(key)
        #print("Path is : ",self.path)
            
    def VAL(self):
        self.path=[]
        self.dest = []
        self.Path()

        #print("\n\nBloc 2 ",self.path)
    
    def Path_col_patter(self,x,y,blocksizew,blocksizeh):

        x = x*blocksizew
        y=  y*blocksizew
      #  print("Adress ; ",x,y)
        rec = pygame.Rect(x,y,blocksizew,blocksizeh)
        pygame.draw.rect(self.win,(66, 245, 96),rec,0)
        pygame.display.update()

    def DFS(self,node,blocksizew,blocksizeh):
        #print("out node : ",node)
        
        if node not in self.visited:
            #print("Node is ",node)
            self.Path_col_patter(node[0],node[1],blocksizew,blocksizeh)
                #return
            #pygame.time.wait(10)
            if(node in self.dest):
                print("fonud !!!!!!!!!!!! : ",node)
                
            self.visited.add(node)

            for nigh in [(node[0],node[1]+1),(node[0]+1,node[1]),(node[0]-1,node[1]),(node[0],node[1]-1)]:
                #print("nigh are : ",nigh)
               
                if(nigh in self.path):
                    #print("In path")
                    self.DFS(nigh,blocksizew,blocksizeh)

    
    
    
    
    
    def dj_algo(self,blocksizew,blocksizeh):
        va=40
        global start_node,ANS
        start_node = self.path[va]
        final_start =self.path[va]
        #prev_node =0
        path_cost = 1
        start_sum = 0 
        visited = {"[{}]".format(start_node):0}
        single_visited = [start_node]
        prev_node=[start_node]
        Min = (-100,-100)
        
        no_of_compititors = False
        compititors=[]
        compi_score=[]
        total_cars = len(self.Path_obj)
        
        to_check = {}
        
        print(self.path_des_val)
        print("START NODE : ",start_node)
        
        flag=0
        destinations_covered=0
        destinations_covered_cord = []
        compent = total_cars
        while(True):
            
            # temp_check = [ [(start_node[0],start_node[1]+1)],[(start_node[0]+1,start_node[1])],[(start_node[0]-1,start_node[1])],[(start_node[0],start_node[1]-1)]]
            
            x = start_node[0]
            y = start_node[1]
            
            temp_check = [
                
                [(x+1,y)],
                #[(x+1,y+1)],
                [(x,y+1)],
                #[(x-1,y+1)],
                [(x-1,y)],
                #[(x-1,y-1)],
                [(x,y-1)],
                #[(x+1,y-1)]
            ]
            
            try:
                
                temp_check.remove(str([prev_node[-1]]))
                
            except Exception as e:
                
                pass
            
            
            te = temp_check
            
            prev_nn = prev_node.copy()
            #print("\nThe prev node was : ",prev_nn)
            #prev_node_copy = prev_node.copy()
            for val in te:
                #print("Checking if Node is Path : ",val)
                prev_node_copy = prev_node.copy()
                
                if(val[-1] in self.path):
                    
                    if(val[-1] not in single_visited):
                        single_visited.append(val[-1])
                        #print("Yes it is in path!")
                        #pygame.time.wait(2000)
                        if val[-1] in self.dest:
                           # print("IT IS IN DESTINATION **** 111111111111  **********")
                            flag=1
                        try:
                            
                            prev_node_copy.append(val[-1]) 
                            
                            test = str(prev_node_copy.copy())

                            
                            
                            try:
                                den = self.path_des_val[val[-1]] 
                            except:
                                #print("Tried False")
                                den=0

                            if(val[-1] in self.path_des_val):
                               # print("TRUEE")
                                #print("DEN : ",den)
                                pass

                            rev = str((prev_node_copy.copy())[::-1])
                            #print("Org and rev : ",rev)
                            
                            
                            
                            
                            if(test not in to_check and rev not in to_check):
                              
                                to_check[test] = den+ path_cost + visited[str(prev_nn)]
                                compscore = den+ path_cost + visited[str(prev_nn)]
                               
                            else:
                                compscore = to_check[test]
                               
                            
                            if val[-1] in self.dest:
                               
                                if(val[-1] not in destinations_covered_cord):
                                    
                                    flag=1
                                    ANS = prev_node_copy.copy()
                                    print("ANS : ",total_cars,destinations_covered,compent,self.dest_capacity[ANS[-1]])
                                    #print("des cov-== : ",destinations_covered)
                                    compititors.append(ANS)
                                   # print("   ---  0 - -- -  ",self.dest_capacity)
                                    compi_score.append(compscore)
                                    #print("   ---  1 - -- -  : ",total_cars,ANS[-1])
                                    
                                   
                                        
                                    compent = compent-self.dest_capacity[ANS[-1]]
                                    #print("   ---  1.1 - -- -  ",compent)
                                    if(compent>0):
                                      #  print("   ---  1.2 - -- -  ")
                                        self.ANS2_KEY.append(ANS)
                                        self.ANS2_VAEUE.append(self.dest_capacity[ANS[-1]])
                                    
                                    elif(compent<=0):
                                      #  print("   ---  1.3 - -- -  ")
                                       
                                        self.ANS2_KEY.append(ANS)
                                        self.ANS2_VAEUE.append(abs(compent))
                                       # print("   ---  1.3.1 - -- -  ")
                                        no_of_compititors = True
                                        
                                    print("   ---  2 - -- -  ", destinations_covered)
                                    if(destinations_covered>=5):
                                        self.ANS2_KEY.append(ANS)
                                        self.ANS2_VAEUE.append(abs(compent))
                                        no_of_compititors=True
                                   # print("   ---  3 - -- -  ")
                                    destinations_covered = destinations_covered+1
                                   # print("Ececuted : ",destinations_covered)
                                   
                                
                                else:
                                    
                                    destinations_covered_cord[val[-1]]
                                
                                #break
                            #gf = input("Next ?? : ")
                            
                        except :
                            #print("Ecp !!!!!!!!!!!! ")
                            ind = val
                        
                            try:
                                
                                den = self.path_des_val[ind[0]]
                            except:
                                
                                den=0
                    
                        
                            to_check[str(ind)] = den + path_cost 
                            
                    else:
                        pass
                        #print("Alresdy in single visited : ",val[-1])
            prev_node = prev_node_copy
          
            
            Min = min(to_check, key=to_check.get)
            checking_val = [eval(Min.strip('][').split('()')[0])]
            try:
                if(len(checking_val[0][0])>1):
                    checking_val = list(eval(checking_val.strip('][').split('()')[0]))
            except:
                pass
            checking_val=checking_val[-1]
            #print("CHHHHHH : ",Min,str([checking_val]))
            
            while(str([checking_val]) in visited or Min in visited):
                #print("\n!!!!!!!!!!!!!!!!!! Min in viited : ",Min)
                
                try:
                    del to_check[Min]
                except:
                    pass
                Min = min(to_check, key=to_check.get)
                
                checking_val = [eval(Min.strip('][').split('()')[0])]
                #print("New trying ::: ",checking_val,checking_val[0][0])
                try:
                    if(len(checking_val[0][0])>1):
                       # print("YESSSSS.........",eval(Min.strip('][').split('()')[0]))
                        checking_val = list(eval(Min.strip('][').split('()')[0]))
                except:
                    pass
               
                checking_val=checking_val[-1]
    
            try:
         
                den22 = self.path_des_val[checking_val] + 1
            except:
            
                den22=1

            single_visited.append(checking_val[-1])
          
            visited[str([checking_val])] = den22
        
            Min2 =  [eval(Min.strip('][').split('()')[0])]
            
            try:
                if(len(Min2[0][0])>1):
                    Min2 = list(eval(Min.strip('][').split('()')[0]))
            except:
                pass
            
            
        
            
            
            Min3 = Min2.copy()
            Min2 = Min2[-1]
            try:
                #print("It is Min 2 : ",Min2)
                self.Path_col_patter(Min2[0],Min2[1],blocksizew,blocksizeh)
            except Exception as ee:
                Min2 = Min2[0]
                #print("Eception is : ",ee)
                #print("Trying   :  ",Min2[0],Min2[1])
                self.Path_col_patter(Min2[0],Min2[1],blocksizew,blocksizeh)
                
                #print("EEEEEE : ",Min2[0][0],Min2[0][1],Min2)
                
                
            ##pygame.time.wait(TIME)
            
            
            #print("Min , Min2 : ",Min,Min2,type(Min))
            visited[Min] = to_check[Min]
            #print("Visited : ",visited)
            if(no_of_compititors==True):
              
                    
          
                # ind = compi_score.index(min(compi_score))
                # ANS = compititors[ind]
                
                
                for ANS in compititors:    
                                
                    for points in ANS:
                        self.found_path.append(points)
                    self.ANS.append(ANS)
                
                
                # #print("Ans : ",key,Min22)
                
                print("Compo : \n",compititors)
                print("scores : \n",compi_score)
                
                #print("\n\n",visited)
                break
    
            del to_check[Min]
   
            prev_node = Min3
            start_node = Min2
        
        
        
        
        
        
        
    
    
    def drawGrid(self,height,width,blocksizew,blocksizeh,val=None,dclick=False,but_val=1):
        
        height = int(pygame.display.get_surface().get_height())
        width = height#int( pygame.display.get_surface().get_width())

        #pygame.display.set_mode((height,height),pygame.RESIZABLE)
        
        
        block_sizew = int((width)/Number)
        block_sizeh = int((height/Number))
        
        global Block,density,factor,activate
        
        
        if val is not None:
           # print("Num : ",Number,val,"\n",Block)
            if(val[0]<Number):
                # Determines if Val is on the right meanu column or on the left og column
                
                if  val not in Block:
                    #print("Added in block : ",block)
                    #block.append(val)
                    Block[val]=but_val
                else :
                    if val in Block:
                        if Block[(val)] != but_val:
                            Block[(val)] = but_val

                if(dclick==True):
                    #print("Inside ",val)
                    try:
                        del Block[val]    
                        #print("Not deleted")
                    except:
                        pass
            else:
                if(but_val==4):
                    #print("Svaig...")
                    file = open("state.pkl","wb")
                    pickle.dump(Block,file)
                    file.close()
                if(but_val==5):
                    file = open("state.pkl",'rb')
                    Block = pickle.load(file)
                    self.path = []
                    self.dest = []
                    self.ANS=[]
                    self.help_region=[]
                    self.Path()
                    self.path_des_val = {}
                    self.found_path = []
                    
                    activate=True
                        
                    #print("Des ",self.path)
                    #self.dj_algo(block_sizew,block_sizeh)
                    density=True

        for x in range(0,width-20,blocksizew):
            for y in range(0,height,blocksizeh):
                rect = pygame.Rect(x,y,blocksizew,blocksizeh)

                wid = math.ceil(x/blocksizew)
                hig = math.ceil(y/blocksizew)
                
                
                if((wid,hig) in self.found_path):
                    #self.Path_col_patter(wid,hig,block_sizew,block_sizeh)
                    pygame.draw.rect(self.win,(0,0,0),rect,0)
                elif((wid,hig) in Block):
                    #print("Into block")
                    if(Block[(wid,hig)]==1):
                        pygame.draw.rect(self.win,blockColor,rect,0)
                    elif(Block[(wid,hig)]==2):
                        pygame.draw.rect(self.win,path_col,rect,0)
                    elif(Block[(wid,hig)]==7):
                        pygame.draw.rect(self.win,(255,0,0),rect,1)
                    else:
                        pygame.draw.rect(self.win,dest_co,rect,0)
                
                else:
                    pygame.draw.rect(self.win,Normal,rect,1)
        #print(Block)
        rect2 = pygame.Rect(width,0,width,height)
        pygame.draw.rect(self.win,(73, 74, 67),rect2,0) 

        wid = 200
        hig = 50

        building_but = pygame.Rect(width,0,wid,hig)
        self.win.blit(self.font.render('Buildings', True, (255,255,255)), ((width+10,0+10)))
        path_but = pygame.Rect(width,hig,wid,hig)
        self.win.blit(self.font.render('Path', True, (255,255,255)), ((width+10,hig+10)))
        destination = pygame.Rect(width,2*hig,wid,hig)
        self.win.blit(self.font.render('Destination', True, (255,255,255)), ((width+10,(2*hig)+10)))
        start = pygame.Rect(width,3*hig,wid,hig)
        self.win.blit(self.font.render('Save', True, (255,255,255)), ((width+10,(3*hig)+10)))
        load = pygame.Rect(width,4*hig,wid,hig)
        self.win.blit(self.font.render('Load', True, (255,255,255)), ((width+10,(4*hig)+10)))
        dfs = pygame.Rect(width,5*hig,wid,hig)
        self.win.blit(self.font.render('DFS', True, (255,255,255)), ((width+10,(5*hig)+10)))
        HELP = pygame.Rect(width,6*hig,wid,hig)
        self.win.blit(self.font.render('HELP', True, (255,255,255)), ((width+10,(6*hig)+10)))

        

        pygame.draw.rect(self.win,blockColor,building_but,1)
        
        pygame.draw.rect(self.win,path_col,path_but,1)
        pygame.draw.rect(self.win,dest_co,destination,1)
        pygame.draw.rect(self.win,(204, 235, 0),start,1)
        pygame.draw.rect(self.win,(204, 235, 0),load,1)
        pygame.draw.rect(self.win,(204, 235, 0),dfs,1)
        pygame.draw.rect(self.win,(204, 235, 0),HELP,1)
        
        
        if(activate==True):
            if(density== True):
                
                self.path_des_val = {}
                for obj  in self.obj:
                    LOC = obj.move(self.path)
                
                    if LOC in self.path_des_val:
                        self.path_des_val[LOC] = self.path_des_val[LOC] + factor
                    else:
                        self.path_des_val[LOC] = factor
                #print("New Position : ",self.path_des_val)
                density = False
                self.dj_algo(block_sizew,block_sizeh)
                #print("\n\nDencity : ",self.path_des_val)
                print("\nIN GRID DRAW : ",self.ANS2_VAEUE)
                
                
            else:
                cou=0
                
                ind_val=0
                ans_val=0
                for obj in self.Path_obj:
                    
                   
                    print("COUNT : ",cou,len(self.ANS2_KEY),ans_val)
                    ANS = self.ANS2_KEY[cou%len(self.ANS2_KEY)]
                    # ind_ans= self.ANS2_KEY.index(ANS)
                    obj.move_on_path(ANS)
                    # ans_val = self.ANS2_VAEUE[ind_ans]
                    # if(ind_val!=ans_val):
                    #     ind_val= ind_val+1
                    # elif(ind_val>=ans_val and cou<len(self.ANS2_KEY)):
                    #     cou=cou+1
                    cou=cou+1
                    
                
                    
                
                
                for obj  in self.obj:
                    
                    if(obj in self.Path_obj):
                        continue
                
                    obj.move(self.path)
                    #x,y=obj.move(self.path)
                    #print("FINAL : \n",self.help_region,(x,y))
                    # if (x,y) in self.help_region:
                    # # print("FINISH!!!!!!!!")
                    #     self.Path_obj.append(obj)
                    # if(x,y)==(68, 89):
                    #     self.Path_obj.append(obj)
                        
                    
                        
                    #self.dj_algo()
        
            # for obj  in self.obj:
            #     obj.move(self.path)
               

                



def Main( win_height=500,win_width=700,Number=10):

    #(18, 140, 184)
    global Background

    win = pygame.display.set_mode((win_width,win_height),pygame.RESIZABLE)
    pygame.display.set_caption("Navigate")
    win.fill(Background)
    obj = Grid(win)
    
    val = None
    drag = False
    
    click=0
    dbclock = pygame.time.Clock()
    dclick=False
    but_val=1

    #car = Cars(win,5,200,200)

    while True:
        win.fill(Background)
        
        height = int(pygame.display.get_surface().get_height())
        width = height#int( pygame.display.get_surface().get_width())

        #pygame.display.set_mode((height,height),pygame.RESIZABLE)
        
        
        block_sizew = int((width)/Number)
        block_sizeh = int((height/Number))

    
        
        if(dclick==True):
            obj.drawGrid(height,width,block_sizew,block_sizeh,val,dclick=True,but_val=but_val)
            dclick=False
        else:
            obj.drawGrid(height,width,block_sizew,block_sizeh,val,but_val=but_val)
        
        # car.move()
        # car.moveDown()
        # car.moveRight()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            # Mouse events
            #x_coord,y_coord= event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:

                col = (200,200,200)
                drag = True
                x_coord,y_coord= event.pos
                #print(x_coord,y_coord)
                wid = math.ceil(x_coord/block_sizew)
                hig = math.ceil(y_coord/block_sizew)
                #print("Down detected : ",x_coord,y_coord)
                val = (wid-1,hig-1)
                
                hi_but=50
                if(wid>=Number+1  and y_coord>0 and y_coord<hi_but):
                    #print("buil")
                    but_val=1
                elif(wid>=Number+1 and y_coord>hi_but and y_coord<2*hi_but):
                    #print("path")
                    but_val=2
                elif(wid >= Number+1 and y_coord>2*hi_but and y_coord<3*hi_but):
                   # print("destination")
                    but_val=3
                elif(wid >= Number+1 and  y_coord>3*hi_but and y_coord<4*hi_but):
                    #print("Save")
                    but_val=4
                elif(wid >= Number+1 and  y_coord>4*hi_but and y_coord<5*hi_but):
                    #print("Load")
                    but_val=5

                elif(wid >= Number+1 and  y_coord>5*hi_but and y_coord<6*hi_but):
                    #print("Load")
                    but_val=6
                elif(wid >= Number+1 and  y_coord>6*hi_but and y_coord<7*hi_but):
                    #print("HELP BOX")
                    but_val=7
                if dbclock.tick() < 500:
                   # print("Double")
                    drag=False
                    dclick=True


            elif event.type == pygame.MOUSEBUTTONUP:
                
                val = None
                drag = False
            else:
                val = None

        if(but_val==6):
            # obj2.VAL()
            # obj2.DFS((0,0),block_sizew,block_sizeh)
            # obj2.drawGrid(height,width,block_sizew,block_sizeh,val,but_val=but_val)
            obj.VAL()
            obj.DFS((0,1),block_sizew,block_sizeh)
            # obj.drawGrid(height,width,block_sizew,block_sizeh,val,but_val=but_val)
            # obj3.VAL()
            # obj3.DFS((5,16),block_sizew,block_sizeh)
            # obj3.drawGrid(height,width,block_sizew,block_sizeh,val,but_val=but_val)
            # obj4.VAL()
            # obj4.DFS((9,11),block_sizew,block_sizeh)
            
            #but_val=1

        #print("Running")
        if(drag==True ):
            x_coord,y_coord= event.pos
            #print(x_coord,y_coord)
            wid = math.ceil(x_coord/block_sizew)
            hig = math.ceil(y_coord/block_sizew)
            val = (wid-1,hig-1)
            
        #print("drag is : ",drag)
        #pygame.time.wait(100)
        pygame.display.update()
        

Main(Number=Number)
