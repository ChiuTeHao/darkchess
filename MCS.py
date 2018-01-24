import random
from tkinter import *
from tkinter import messagebox
'''
0  紅兵
1  紅炮
2  紅馬
3  紅車
4  紅象
5  紅仕
6  紅帥
7  黑兵
8  黑炮
9  黑馬
10 黑車
11 黑象
12 黑士
13 黑將
14 暗子
15 空格
16 紅子
17 黑子
'''
class Node:
  def __init__(self):
    self.bestchildindex=-1
    self.bestpos=-1
    self.bestact=-1
  def update(self,pos,act,bestchildid):
    self.bestpos=pos
    self.bestact=act
    self.bestchildindex=bestchildid
pmove=[[0x00000102,0x00000205,0x0000040a,0x00000814,0x00001028,0x00002050,0x000040a0,0x00008040],
       [0x00010201,0x00020502,0x00040a04,0x00081408,0x00102810,0x00205020,0x0040a040,0x00804080],
       [0x01020100,0x02050200,0x040a0400,0x08140800,0x10281000,0x20502000,0x40a04000,0x80408000],
       [0x02010000,0x05020000,0x0a040000,0x14080000,0x28100000,0x50200000,0xa0400000,0x40800000]]
def printBoard(state):
  board=[[-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1]]
  chessname=['紅兵','紅炮','紅馬','紅車','紅象','紅仕','紅帥','黑兵','黑炮','黑馬','黑車','黑象','黑士','黑將','暗子','空格']
  for i in range(0,16):
    tmp=state[i]
    while tmp>0:
      pos=getpos(LSB(tmp))
      board[pos//8][pos%8]=i
      tmp^=(1<<pos)
  for i in range(0,4):
    for j in range(0,8):
      print('%s '%chessname[getType(state,i*8+j)],end=' ')
    print('\n')
  print('===========================================\n')
def getpos(x):
  table=[31,0,1,5,2,16,27,6,3,14,17,19,28,11,7,21,30,
         4,15,26,13,18,10,20,29,25,12,9,24,8,23,22]
  x&=0xFFFFFFFF
  x*=0x08ED2BE6
  x&=0xFFFFFFFF
  x=x>>27
  return table[x]
def LSB(x):
  if x==0:
    return -1
  else:
    return x&(-x)
def MSB(x):
  if x==0:
    return -1
  x|=x>>32
  x|=x>>16
  x|=x>>8
  x|=x>>4
  x|=x>>2
  x|=x>>1
  return (x>>1)+1
def getType(state,pos):
  if pos<0 or pos>31:
    return -1
  mask=1<<pos
  for i in range(0,18):
    if (state[i]&mask)!=0:
      return i
def Move(state,boardstring,chesstype,pos,newpos): #state是每個兵種bitboard的list，chesstype是指哪個兵種
  mask1=1<<pos                        #pos是舊位置，newpos是新位置
  mask2=1<<newpos
  state[chesstype]^=mask1
  state[chesstype]|=mask2
  state[15]|=mask1
  state[15]^=mask2
  boardstring[pos]=str(15)
  boardstring[newpos]=str(newpos)
def canMove(state,chesstype,pos,newpos):
  if pos>31 or pos<0 or newpos>31 or newpos<0:
    return False
  mask1=1<<pos
  mask2=1<<newpos
  if abs(pos-newpos)!=1 and abs(pos-newpos)!=8:       #亂移
    return False
  if pos%8==0 and pos-newpos==1:      #不能左移
    return False
  if pos%8==7 and newpos-pos==1:    #不能右移
    return False
  if pos<8 and newpos<0:            #不能上移
    return False
  if pos>23 and newpos>31:          #不能下移
    return False
  if (state[15]&mask2)!=0:          #判斷新位置是否為空
    return True
  else:
    return False
def canEat(state,takechesstype,takenchesstype,pos,newpos):
  if not(takechesstype>=0 and takechesstype<=13) or not(takenchesstype>=0 and takenchesstype<=13):
    return False
  if takechesstype//7==takenchesstype//7:   #顏色相同不能互吃
    return False
  if abs(pos-newpos)!=8 and abs(pos-newpos)!=1:  #不在攻擊的4方位  
    return False
  if pos%8==0 and pos-newpos==1:
    return False
  if pos//8==0 and pos-newpos==8:
    return False
  if pos%8==7 and newpos-pos==1:
    return False
  if pos//8==3 and newpos-pos==8:
    return False
  if (takechesstype==13 and takenchesstype==0) or (takechesstype==6 and takenchesstype==7):
    return False
  if (takechesstype==0 and takenchesstype==13) or (takechesstype==7 and takenchesstype==6):
    return True
  if (takechesstype==1 and takenchesstype//7==1) or (takenchesstype==8 and takenchesstype//7==0):
    return True        
  if (takechesstype%7)>=(takenchesstype%7):
    return True
  else:
    return False
def eat(state,boardstring,takechesstype,takenchesstype,pos,newpos):
  mask1=1<<pos
  mask2=1<<newpos
  state[takechesstype]^=mask1
  state[takechesstype]|=mask2
  state[takenchesstype]^=mask2
  state[15]|=mask1
  boardstring[pos]=str(15)
  boardstring[newpos]=str(takechesstype)
def uneat(state,boardstring,takechesstype,takenchesstype,pos,newpos):
  mask1=1<<pos
  mask2=1<<newpos
  state[takechesstype]|=mask1
  state[takechesstype]^=mask2
  state[takenchesstype]|=mask2
  state[15]^=mask1
  boardstring[pos]=str(takechesstype)
  boardstring[newpos]=str(takenchesstype)
def flip(state,boardstring,pos,newchesstype):
  mask=1<<pos
  state[14]^=mask
  state[newchesstype]|=mask
  boardstring[pos]=str(newchesstype)
def unflip(state,boardstring,pos):
  mask=1<<pos
  chesstype=getType(state,pos)
  state[chesstype]^=mask
  state[14]|=mask
  boardstring[pos]=str(14)
def findCannonTarget(state,pos,chesstype,direction):
  enemy=1-(chesstype//7)  #算敵方棋子顏色
  cnt=start=stop=occupied=0
  targetpos=-1
  jump=[-1,-8,1,8]
  start=pos+jump[direction]
  if direction==0:
    stop=(pos//8)*8+jump[direction]
  elif direction==1:
    stop=pos%8+jump[direction]
  elif direction==2:
    stop=(pos//8+1)*8
  else:
    stop=32+pos%8
  for i in range(start,stop,jump[direction]):
    tmp=getType(state,i)
    if tmp!=15:
      cnt+=1
    if cnt==2 and tmp//7==enemy:   #有砲架且第2顆棋子是敵方棋子
      targetpos=i
    if cnt>=3:
      break
  return targetpos
def getScore(own,state):
  red=[1,2,3,4,5,6,7]
  black=[1,2,3,4,5,6,7]
  score=0
  if own==0:
    for i in range(0,7):
      for j in range(0,32):
        if (state[i]&(1<<j))>0:
          score+=red[i]
        if (state[i+7]&(1<<j))>0:
          score-=black[i]
  else:
    for i in range(0,7):
      for j in range(0,32):
        if (state[i]&(1<<j))>0:
          score-=red[i]
        if (state[i+7]&(1<<j))>0:
          score+=black[i]
  return score
def distance(pos1,pos2):
  return abs(pos1//8-pos2//8)+abs(pos1%8-pos2%8)
def enCodeBoardState(boardstring,turn):
  string=''
  for i in boardstring:
    string+=i
  string+=turn
  return string
def printlist(id):
  global nodelist
  actlist=[]
  poslist=[]
  while (id!=-1):
    poslist.append(nodelist[id].bestpos)
    actlist.append(nodelist[id].bestact)
    id=nodelist[id].bestchildindex
  print('poslist ',poslist)
  print('actlist ',actlist)
  print('=========================================')
def Min(AIcolor,state,darkchess,boarddic,boardstring,depth,Maxdepth,center,addscore):
  if depth>Maxdepth:
    return getScore(AIcolor,state)+addscore
  global nodelist
  eatscore=[10000,40000,80000,160000,320000,640000,1280000,10000,40000,80000,160000,320000,640000,1280000]
  bestscore=bestpos=bestact=-1
  direction=[-1,-8,1,8]
  inverdirection=[1,8,-1,-8]
  selfindex=len(nodelist)-1
  '''if depth==2:
    print('Min function in depth ',depth)
    print('before search')
    printBoard(state)
    for i in range(0,32):
      tmp=getType(state,i)
      if tmp>=14 or tmp//7==AIcolor or (depth>1 and distance(i,center)>10 and tmp!=1 and tmp!=8):
        continue
      if tmp==1 or tmp==8:
        for j in range(0,4):
          if canMove(state,tmp,i,i+direction[j]):
            print('chesstype ',tmp,' in pos ',i,' can move to pos ',i+direction[j])
          targetpos=findCannonTarget(state,i,tmp,j)
          if targetpos!=-1:
            print('chesstype ',tmp,' in pos ',i,'can eat chess in pos ',targetpos)
      else:
        for j in range(0,4):
          if canMove(state,tmp,i,i+direction[j]):
            print('chesstype ',tmp,' in pos ',i,' can move to pos ',i+direction[j])
          if i+direction[j]>31 or i+direction[j]<0:
            continue
          if canEat(state,tmp,getType(state,i+direction[j]),i,i+direction[j]):
            print('chesstype ',tmp,' in pos ',i,' can eat chess in pos ',i+direction[j])'''
  for i in range(0,32):
    chesstype=getType(state,i)
    if chesstype>=14 or chesstype//7==AIcolor or (depth>1 and distance(i,center)>10 and chesstype!=1 and chesstype!=8):
      continue
    if chesstype==1 or chesstype==8:
      for j in range(0,4):
        if canMove(state,chesstype,i,i+direction[j]):
          Move(state,boardstring,chesstype,i,i+direction[j])
          string=enCodeBoardState(boardstring,'Min')
          if string not in boarddic or boarddic[string]>depth:
            boarddic[string]=depth
            childindex=len(nodelist)
            nodelist.append(Node())
            score=Max(AIcolor,state,darkchess,boarddic,boardstring,depth+1,Maxdepth,i,addscore)
            if score<bestscore or bestpos==-1:
              bestscore=score
              bestpos=i
              bestact=j
              nodelist[selfindex].update(bestpos,bestact,childindex)
          Move(state,boardstring,chesstype,i+direction[j],i)
        targetpos=findCannonTarget(state,i,chesstype,j)
        if targetpos!=-1:
          takenchesstype=getType(state,targetpos)
          eat(state,boardstring,chesstype,takenchesstype,i,targetpos)
          string=enCodeBoardState(boardstring,'Min')
          if string not in boarddic or boarddic[string]>depth:
            boarddic[string]=depth
            childindex=len(nodelist)
            nodelist.append(Node())
            score=Max(AIcolor,state,darkchess,boarddic,boardstring,depth+1,Maxdepth,i,addscore-eatscore[takenchesstype]*(Maxdepth-depth))
            if score<bestscore or bestpos==-1:
              bestscore=score
              bestpos=i
              bestact=j+4
              nodelist[selfindex].update(bestpos,bestact,childindex)
          uneat(state,boardstring,chesstype,takenchesstype,i,targetpos)
    else:
      for j in range(0,4):
        if canMove(state,chesstype,i,i+direction[j]):
          Move(state,boardstring,chesstype,i,i+direction[j])
          string=enCodeBoardState(boardstring,'Min')
          if string not in boarddic or boarddic[string]>depth:
            boarddic[string]=depth
            childindex=len(nodelist)
            nodelist.append(Node())
            score=Max(AIcolor,state,darkchess,boarddic,boardstring,depth+1,Maxdepth,i,addscore)
            if score<bestscore or bestpos==-1:
              bestscore=score
              bestpos=i
              bestact=j
              nodelist[selfindex].update(bestpos,bestact,childindex)
          Move(state,boardstring,chesstype,i+direction[j],i)
        if i+direction[j]>31 or i+direction[j]<0:
          continue
        if canEat(state,chesstype,getType(state,i+direction[j]),i,i+direction[j]):
          takenchesstype=getType(state,i+direction[j])
          eat(state,boardstring,chesstype,takenchesstype,i,i+direction[j])
          string=enCodeBoardState(boardstring,'Min')
          if string not in boarddic or boarddic[string]>depth:
            boarddic[string]=depth
            childindex=len(nodelist)
            nodelist.append(Node())
            score=Max(AIcolor,state,darkchess,boarddic,boardstring,depth+1,Maxdepth,i,addscore-eatscore[takenchesstype]*(Maxdepth-depth))
            if score<bestscore or bestpos==-1:
              bestscore=score
              bestpos=i
              bestact=j+4
              nodelist[selfindex].update(bestpos,bestact,childindex)
          uneat(state,boardstring,chesstype,takenchesstype,i,i+direction[j])
  if len(darkchess)>0:
    cnt=random.randint(1,len(darkchess))
    for i in range(0,32):
      if getType(state,i)==14:
        cnt-=1
      if cnt==0:
        num=random.randint(0,len(darkchess)-1)
        chesstype=darkchess[num]
        flip(state,boardstring,i,chesstype)
        darkchess.pop(num)
        string=enCodeBoardState(boardstring,'Min')
        if string not in boarddic or boarddic[string]>depth:
          boarddic[string]=depth
          childindex=len(nodelist)
          nodelist.append(Node())
          score=Max(AIcolor,state,darkchess,boarddic,boardstring,depth+1,Maxdepth,i,addscore)
          if score<bestscore or bestpos==-1:
            bestscore=score
            bestpos=i
            bestact=8
            nodelist[selfindex].update(bestpos,bestact,childindex)
        unflip(state,boardstring,i)
        darkchess.insert(num,chesstype)
        break
  return bestscore
def Max(AIcolor,state,darkchess,boarddic,boardstring,depth,Maxdepth,center,addscore):
  global finalpos,finalact,finalscore
  global nodelist
  if depth==1:
    nodelist=[]
    finalact=finalpos=finalscore=-1
    boarddic={}
    node=Node()
    nodelist.append(node)
  if depth>Maxdepth:
    return getScore(AIcolor,state)+addscore
  eatscore=[10000,40000,80000,160000,320000,640000,1280000,10000,40000,80000,160000,320000,640000,1280000]
  bestscore=bestpos=bestact=-1
  direction=[-1,-8,1,8]
  inverdirection=[1,8,-1,-8]
  selfindex=len(nodelist)-1
  for i in range(0,32):
    chesstype=getType(state,i)
    if chesstype>=14 or chesstype//7==1-AIcolor or (depth>1 and distance(i,center)>10 and chesstype!=1 and chesstype!=8):
      continue
    if chesstype==1 or chesstype==8:
      for j in range(0,4):
        if canMove(state,chesstype,i,i+direction[j]):  #炮移子
          Move(state,boardstring,chesstype,i,i+direction[j])
          string=enCodeBoardState(boardstring,'Max')
          if string not in boarddic or boarddic[string]>depth:
            boarddic[string]=depth
            childindex=len(nodelist)
            nodelist.append(Node())
            score=Min(AIcolor,state,darkchess,boarddic,boardstring,depth+1,Maxdepth,i,addscore)
            if depth==1:
              print('In max at cannon move ')
              printlist(0)
            if score>bestscore or bestpos==-1:
              bestscore=score
              bestpos=i
              bestact=j
              nodelist[selfindex].update(bestpos,bestact,childindex)
          Move(state,boardstring,chesstype,i+direction[j],i)
        targetpos=findCannonTarget(state,i,chesstype,j)
        if targetpos!=-1:
          takenchesstype=getType(state,targetpos)
          eat(state,boardstring,chesstype,takenchesstype,i,targetpos)
          string=enCodeBoardState(boardstring,'Max')
          if string not in boarddic or boarddic[string]>depth:
            boarddic[string]=1
            childindex=len(nodelist)
            nodelist.append(Node())
            score=Min(AIcolor,state,darkchess,boarddic,boardstring,depth+1,Maxdepth,i,addscore+eatscore[takenchesstype]*(Maxdepth-depth))
            if depth==1:
              print('In max at cannon eat ')
              printlist(0)
            if score>bestscore or bestpos==-1:
              bestscore=score
              bestpos=i
              bestact=j+4
              nodelist[selfindex].update(bestpos,bestact,childindex)
          uneat(state,boardstring,chesstype,takenchesstype,i,targetpos)
    else:
      for j in range(0,4):
        if canMove(state,chesstype,i,i+direction[j]):
          Move(state,boardstring,chesstype,i,i+direction[j])
          string=enCodeBoardState(boardstring,'Max')
          if string not in boarddic or boarddic[string]>depth:
            boarddic[string]=depth
            childindex=len(nodelist)
            nodelist.append(Node())
            score=Min(AIcolor,state,darkchess,boarddic,boardstring,depth+1,Maxdepth,i,addscore)
            if depth==1:
              print('In max at general chess move')
              printlist(0)
            if score>bestscore or bestpos==-1:
              bestscore=score
              bestpos=i
              bestact=j
              nodelist[selfindex].update(bestpos,bestact,childindex)
          Move(state,boardstring,chesstype,i+direction[j],i)
        if i+direction[j]>31 or i+direction[j]<0:
          continue
        if canEat(state,chesstype,getType(state,i+direction[j]),i,i+direction[j]):
          takenchesstype=getType(state,i+direction[j])
          eat(state,boardstring,chesstype,takenchesstype,i,i+direction[j])
          string=enCodeBoardState(boardstring,'Max')
          if string not in boarddic or boarddic[string]>depth:
            boarddic[string]=depth
            childindex=len(nodelist)
            nodelist.append(Node())
            score=Min(AIcolor,state,darkchess,boarddic,boardstring,depth+1,Maxdepth,i,addscore+eatscore[takenchesstype]*(Maxdepth-depth))
            if depth==1:
              print('In max at general chess eat')
              printlist(0)            
            if score>bestscore or bestpos==-1:
              bestscore=score
              bestpos=i
              bestact=j+4
              nodelist[selfindex].update(bestpos,bestact,childindex)
          uneat(state,boardstring,chesstype,takenchesstype,i,i+direction[j])
  if len(darkchess)>0:
    cnt=random.randint(1,len(darkchess))
    for i in range(0,32):
      if getType(state,i)==14:
        cnt-=1
      if cnt==0:
        num=random.randint(0,len(darkchess)-1)
        chesstype=darkchess[num]
        flip(state,boardstring,i,chesstype)
        darkchess.pop(num)
        string=enCodeBoardState(boardstring,'Max')
        if string not in boarddic or boarddic[string]>depth:
          boarddic[string]=depth
          childindex=len(nodelist)
          nodelist.append(Node())
          score=Min(AIcolor,state,darkchess,boarddic,boardstring,depth+1,Maxdepth,i,addscore)
          if depth==1:
              print('In max at chess flip')
              printlist(0)
          if score>bestscore or bestpos==-1:
            bestscore=score
            bestpos=i
            bestact=8
            nodelist[selfindex].update(bestpos,bestact,childindex)
        unflip(state,boardstring,i)
        darkchess.insert(num,chesstype)
        break
  if depth==1:
    finalpos=bestpos
    finalact=bestact
    finalscore=bestscore
    index=0
    actlist=[]
    poslist=[]
    while(index!=-1):
      poslist.append(nodelist[index].bestpos)
      actlist.append(nodelist[index].bestact)
      index=nodelist[index].bestchildindex
    print(poslist)
    print(actlist)
  return bestscore
chesspos=[0,0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,7,7,7,7,7,8,8,9,9,10,10,11,11,12,12,13]   #暗子翻開的棋種
darkchess=[0,0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,7,7,7,7,7,8,8,9,9,10,10,11,11,12,12,13]  #紀錄哪些案子尚未翻開
state=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,4294967295,0,0,0]
boardstring=['14','14','14','14','14','14','14','14',
             '14','14','14','14','14','14','14','14',
             '14','14','14','14','14','14','14','14',
             '14','14','14','14','14','14','14','14']
boarddic={}
finalscore=finalpos=finalact=-1
nodelist=[]